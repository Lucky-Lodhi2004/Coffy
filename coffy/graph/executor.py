from .graphdb import GraphDB
from .cypher_parser import parse_query
import json

class CypherExecutor:
    def __init__(self, db: GraphDB):
        self.db = db
        self.last_match = []

    def execute(self, cypher_str: str):
        statements = parse_query(cypher_str)
        output = []
        for stmt in statements:
            typ = stmt['type']
            if typ == 'CREATE':
                self._handle_create(stmt['pattern'])
                output.append({'status': 'created'})
            elif typ == 'MATCH':
                self.last_match = self._handle_match(stmt['pattern'], stmt.get('where'))
                output.append({'matched': self.last_match})
            elif typ == 'RETURN':
                res = self._handle_return(stmt['variables'], stmt.get('distinct', False))
                output.append({'return': res})
            elif typ == 'DELETE':
                self._handle_delete(stmt['variables'])
                output.append({'status': 'deleted'})
            else:
                raise NotImplementedError(f"Unsupported statement: {typ}")
        return output

    def _handle_create(self, patterns):
        """
        Supports multiple, branching pattern elements.
        Each pattern element is [node, rel, node, ...].
        """
        variables = {}  # Map of variable name -> node_id
        for pattern_elem in patterns:
            prev_node_id = None
            for idx, item in enumerate(pattern_elem):
                if item['type'] == 'NODE':
                    var = item.get('variable')
                    if var and var in variables:
                        node_id = variables[var]
                    else:
                        node_id = self.db.add_node([item['label']], item['properties'])
                        if var:
                            variables[var] = node_id
                    prev_node_id = node_id
                elif item['type'] == 'REL':
                    next_node = pattern_elem[idx + 1]
                    next_var = next_node.get('variable')
                    if next_var and next_var in variables:
                        next_node_id = variables[next_var]
                    else:
                        next_node_id = self.db.add_node([next_node['label']], next_node['properties'])
                        if next_var:
                            variables[next_var] = next_node_id
                    self.db.add_relationship(item['rel_type'], prev_node_id, next_node_id, item['properties'])
                    prev_node_id = next_node_id
        self.db.save()

    def _handle_match(self, patterns, where=None):
        """
        Supports multiple, branching pattern elements.
        Each pattern element is [node, rel, node, ...].
        This finds all combinations of matches where all patterns are satisfied together (cross-product, joined on shared variables).
        """
        # For each pattern element, get all matches for that pattern element.
        pattern_matches = [self._match_pattern_element(elem, where) for elem in patterns]

        # Now join matches by variable names (dict-join on overlapping keys).
        matches = self._join_matches(pattern_matches)

        return matches

    def _match_pattern_element(self, pattern_elem, where=None):
        """
        Returns a list of dicts mapping variables to objects for a single pattern element.
        """
        if not pattern_elem:
            return []

        matches = []

        def match_recursive(idx, context):
            if idx >= len(pattern_elem):
                matches.append(context.copy())
                return

            item = pattern_elem[idx]

            if item['type'] == 'NODE':
                for node in self.db.all_nodes():
                    if item['label'] and item['label'] not in node.labels:
                        continue
                    if item['properties']:
                        if not all(node.properties.get(k) == v for k, v in item['properties'].items()):
                            continue
                    var = item.get('variable')
                    # Don't allow same variable to map to two different nodes in the same match
                    if var and var in context and context[var].id != node.id:
                        continue
                    # WHERE support (only in first node for now)
                    if where and var and where['variable'] == var:
                        if node.properties.get(where['key']) != where['value']:
                            continue
                    context_cp = context.copy()
                    if var:
                        context_cp[var] = node
                    match_recursive(idx + 1, context_cp)
            elif item['type'] == 'REL':
                prev_item = pattern_elem[idx - 1]
                prev_var = prev_item.get('variable')
                prev_node = context.get(prev_var) if prev_var else None
                if not prev_node:
                    return
                for rel in self.db.all_relationships():
                    if rel.type != item['rel_type']:
                        continue
                    if rel.start != prev_node.id:
                        continue
                    var = item.get('variable')
                    context_cp = context.copy()
                    if var:
                        context_cp[var] = rel
                    match_recursive(idx + 1, context_cp)

        match_recursive(0, {})
        return matches

    def _join_matches(self, pattern_matches):
        """
        pattern_matches: List[List[dict]]
        Joins them on shared variable names.
        Returns: List[dict]
        """
        if not pattern_matches:
            return []

        result = pattern_matches[0]
        for next_match in pattern_matches[1:]:
            joined = []
            for r in result:
                for n in next_match:
                    # Only keep if no conflicting assignments for shared variables
                    if all((k not in r or r[k] == n[k]) for k in n):
                        merged = r.copy()
                        merged.update(n)
                        joined.append(merged)
            result = joined
        return result
    
    def _handle_return(self, variables, distinct=False):
        result = []
        for m in self.last_match:
            entry = {}
            for var in variables:
                vobj = m.get(var)
                if vobj is None:
                    entry[var] = None
                elif hasattr(vobj, 'to_dict'):
                    entry[var] = vobj.to_dict()
                else:
                    entry[var] = vobj
            result.append(entry)
        if distinct:
            seen = set()
            deduped = []
            for row in result:
                key = json.dumps(row, sort_keys=True)
                if key not in seen:
                    deduped.append(row)
                    seen.add(key)
            return deduped
        return result

    def _handle_delete(self, variables):
        """
        Deletes all nodes/relationships by variable, from last match result.
        """
        for m in self.last_match:
            for var in variables:
                vobj = m.get(var)
                if vobj is None:
                    continue
                if hasattr(vobj, 'id') and hasattr(vobj, 'labels'):  # node
                    self.db.delete_node(vobj.id)
                elif hasattr(vobj, 'id') and hasattr(vobj, 'type'):  # relationship
                    self.db.delete_relationship(vobj.id)
        self.db.save()