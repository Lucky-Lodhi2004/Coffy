from antlr4 import InputStream, CommonTokenStream
from antlr4_cypher import CypherLexer, CypherParser

def parse_cypher_query(query):
    input_stream = InputStream(query)
    lexer = CypherLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = CypherParser(token_stream)
    tree = parser.script()
    return tree