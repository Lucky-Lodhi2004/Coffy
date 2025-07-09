from ast import stmt
from lark import Lark, Transformer, v_args

cypher_grammar = r"""
    start: statement+

    statement: create_statement
             | match_statement
             | return_statement
             | delete_statement

    create_statement: "CREATE" pattern
    match_statement: "MATCH" pattern ("WHERE" where_clause)?
    return_statement: "RETURN" distinct? var_list
    distinct: "DISTINCT"
    delete_statement: "DELETE" var_list

    pattern: pattern_element ("," pattern_element)*
    pattern_element: node_pattern (relationship_pattern node_pattern)*

    node_pattern: "(" variable? (":" label)? ("{" properties "}")? ")"
    relationship_pattern: "-[" variable? (":" type)? ("{" properties "}")? "]->"

    var_list: variable ("," variable)*

    where_clause: condition
    condition: variable "." key "=" value

    properties: property ("," property)*
    property: key ":" value

    variable: CNAME
    label: CNAME
    type: CNAME
    key: CNAME
    value: STRING | SIGNED_NUMBER

    %import common.CNAME
    %import common.SIGNED_NUMBER
    %import common.WS
    %import common.ESCAPED_STRING -> STRING

    %ignore WS
"""

parser = Lark(cypher_grammar, start='start')

@v_args(inline=True)
class CypherTransformer(Transformer):
    def start(self, *statements):
        return list(statements)
    
    def statement(self, stmt):
        return stmt

    def create_statement(self, pattern):
        return {'type': 'CREATE', 'pattern': pattern}

    def match_statement(self, pattern, where=None):
        return {'type': 'MATCH', 'pattern': pattern, 'where': where}

    def return_statement(self, *args):
        if args[0] == "DISTINCT":
            return {'type': 'RETURN', 'distinct': True, 'variables': args[1]}
        else:
            return {'type': 'RETURN', 'distinct': False, 'variables': args[0]}

    def distinct(self, token=None):
        return "DISTINCT"

    def delete_statement(self, vars):
        return {'type': 'DELETE', 'variables': vars}

    def pattern(self, *elements):
        return list(elements)

    def pattern_element(self, node, *rest):
        # rest alternates: relationship, node, relationship, node...
        result = [node]
        result.extend(rest)
        return result

    def node_pattern(self, variable=None, label=None, properties=None):
        return {'type': 'NODE', 'variable': variable, 'label': label, 'properties': properties or {}}

    def relationship_pattern(self, variable=None, rel_type=None, properties=None):
        return {'type': 'REL', 'variable': variable, 'rel_type': rel_type, 'properties': properties or {}}

    def var_list(self, *vars):
        return list(vars)

    def where_clause(self, cond):
        return cond

    def condition(self, variable, key, value):
        return {'variable': variable, 'key': key, 'value': value}

    def properties(self, *props):
        return dict(props)

    def property(self, key, value):
        return (key, value)

    def variable(self, token):
        return str(token)

    def label(self, token):
        return str(token)

    def type(self, token):
        return str(token)

    def key(self, token):
        return str(token)

    def value(self, token):
        if token.type == "STRING":
            return str(token)[1:-1]  # remove quotes
        return float(token) if "." in str(token) else int(token)

def parse_query(query: str):
    tree = parser.parse(query)
    parsed = CypherTransformer().transform(tree)
    return parsed

if __name__ == "__main__":
    queries = [
        'CREATE (a:Person {name: "Alice", age: 30})-[:FRIENDS_WITH]->(b:Person {name: "Bob"})',
        'MATCH (a:Person)-[:FRIENDS_WITH]->(b:Person) WHERE a.name="Alice" RETURN b',
        'DELETE a, b'
    ]
    for q in queries:
        print(f"Query: {q}")
        result = parse_query(q)
        print("Parsed:", result)
        print("-" * 60)
