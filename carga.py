from pathlib import Path
from neo4j import GraphDatabase

# ==============================================================================
# GUIA RÁPIDO DE EXECUÇÃO E VISUALIZAÇÃO (MEMGRAPH + LAB)
# ==============================================================================
# 1. Pré-requisito: Abra o Docker Desktop e aguarde ele iniciar completamente.
#
# 2. Subir o banco Memgraph e o Memgraph Lab:
#    docker compose up -d
#
# 3. Criar e ativar o ambiente virtual Python + instalar dependências:
#    python -m venv .venv
#    .\.venv\Scripts\Activate.ps1   (Windows PowerShell)
#    pip install -r requirements.txt
#
# 4. Popular o grafo com a base de serpentes (27 nós e 61 relacionamentos):
#    python carga.py
#
# 5. Abrir o Memgraph Lab (interface visual):
#    - Acesse http://localhost:3000 no navegador.
#    - Clique em "Connect now" (ou Manual Connection: Host localhost, Port 7687, sem usuário/senha).
#    - Vá em "Query Execution" e teste, por exemplo:
#      MATCH p = (s:Peconhenta)-[:HABITA_BIOMA]->(b) RETURN p;
#
# 6. Ao encerrar os trabalhos, desligue os containers SEM apagar o volume (-v):
#    docker compose down
# ==============================================================================

URI = "bolt://localhost:7687"
AUTH = ("", "")

# Localiza cypher/01_seed.cypher independente de carga.py estar na raiz ou em src/
BASE_DIR = Path(__file__).resolve().parent
SEED_FILE = (
    BASE_DIR / "cypher" / "seed.cypher"
    if (BASE_DIR / "cypher" / "seed.cypher").exists()
    else BASE_DIR.parent / "cypher" / "seed.cypher"
)


def executar_carga():
    conteudo = SEED_FILE.read_text(encoding="utf-8")

    # Remove comentários de linha e separa cada comando Cypher pelo ponto e vírgula
    linhas_validas = [
        linha for linha in conteudo.splitlines()
        if not linha.strip().startswith("//")
    ]
    comandos = [
        cmd.strip() for cmd in "\n".join(linhas_validas).split(";")
        if cmd.strip()
    ]

    with GraphDatabase.driver(URI, auth=AUTH) as client:
        client.verify_connectivity()

        for cmd in comandos:
            client.execute_query(cmd, database_="memgraph")

        # Conferência de integridade da carga
        nos, _, _ = client.execute_query(
            "MATCH (n) RETURN count(n) AS total", database_="memgraph"
        )
        rels, _, _ = client.execute_query(
            "MATCH ()-[r]->() RETURN count(r) AS total", database_="memgraph"
        )
        serpentes, _, _ = client.execute_query(
            "MATCH (s:Serpente) RETURN count(s) AS total", database_="memgraph"
        )

        print("Carga concluída com sucesso!")
        print(f"- Total de nós: {nos[0]['total']} (esperado: 27)")
        print(f"- Total de serpentes: {serpentes[0]['total']} (esperado: 18)")
        print(f"- Total de relacionamentos: {rels[0]['total']} (esperado: 61)")


if __name__ == "__main__":
    executar_carga()