from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("", "")


#Mini teste para saber se a conxeão com o memgraph (inicialmente vazio) deu certo:
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Conexão Bolt com Memgraph validada!")