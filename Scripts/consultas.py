from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("", "")


def executar_query(client, query, params=None):
    records, _, _ = client.execute_query(query, parameters_=params or {}, database_="memgraph")
    return records


def main():
    with GraphDatabase.driver(URI, auth=AUTH) as client:
        client.verify_connectivity()

        # ======================================================================
        # Parte 1: equivalentes a consultas diretas (g.triples -> MATCH)
        # ======================================================================
        print("=" * 70)
        print("Parte 1: consultas diretas (equivalentes ao g.triples)")
        print("=" * 70)

        # 1.1 Sujeito Fixo: Propriedades e relacionamentos da Jararaca-da-Caatinga
        q1_1 = """
        MATCH (s:Serpente {id: 'JararacaDaCaatinga'})-[r]->(destino)
        RETURN properties(s) AS props,
               type(r) AS relacao,
               destino.name AS destino
        """
        resultados = executar_query(client, q1_1)

        # 1. Imprime os atributos do nó UMA única vez (pegando do 1º registro)
        print(f"\n# [1.1] Detalhes da {resultados[0]['props']['name']}:")
        for k, v in resultados[0]["props"].items():
            print(f"  • {k}: {v}")

        # 2. Percorre a lista apenas para imprimir os relacionamentos
        for r in resultados:
            print(f"  • {r['relacao']} -> {r['destino']}")

        # 1.2 Rótulo Específico: Membros da Família Elapidae
        print("\n# [1.2] Serpentes da família Elapidae:")
        q1_2 = "MATCH (s:Elapidae) RETURN s.name AS nome ORDER BY nome"
        for r in executar_query(client, q1_2):
            print(f"  • {r['nome']}")

        # 1.3 Relacionamento + Nó Alvo: Habitantes da Caatinga
        print("\n# [1.3] Serpentes que habitam a Caatinga:")
        q1_3 = """
        MATCH (s:Serpente)-[:HABITA_BIOMA]->(b:Bioma {id: 'Caatinga'})
        RETURN s.name AS nome ORDER BY nome
        """
        for r in executar_query(client, q1_3):
            print(f"  • {r['nome']}")

        # 1.4 Filtro Booleano: Serpentes Noturnas
        print("\n# [1.4] Serpentes com hábito noturno:")
        q1_4 = "MATCH (s:Serpente {eNoturna: true}) RETURN s.name AS nome ORDER BY nome"
        for r in executar_query(client, q1_4):
            print(f"  • {r['nome']}")

        # 1.5 Dentição Opistóglifa
        print("\n# [1.5] Serpentes com dentição Opistóglifa:")
        q1_5 = """
        MATCH (s:Serpente)-[:POSSUI_DENTICAO]->(d:TipoDenticao {id: 'Opistoglifa'})
        RETURN s.name AS nome ORDER BY nome
        """
        for r in executar_query(client, q1_5):
            print(f"  • {r['nome']}")

        # ======================================================================
        # PARTE 2: Migrando as consultas SPARQL para CYPHER
        # ======================================================================
        print("\n" + "=" * 70)
        print("Parte 2: migração: (SPARQL -> CYPHER)")
        print("=" * 70)

        # C1: Nome popular (name) e nome científico de cobras noturnas
        print("\n# [C1] Serpentes com hábito noturno (ordenado):")
        c1 = """
        MATCH (s:Serpente)
        WHERE s.eNoturna = true
        RETURN s.name AS nome, s.nomeCientifico AS cientifico
        ORDER BY nome
        """
        for r in executar_query(client, c1):
            print(f"  • {r['nome']} -> ({r['cientifico']})")

        # C2: Ranking de tamanho médio >= 1.5 metros
        print("\n# [C2] Ranking de tamanho médio >= 1.5 metros:")
        c2 = """
        MATCH (s:Serpente)
        WHERE s.comprimentoMedioMetros >= 1.5
        RETURN s.name AS nome,
               s.nomeCientifico AS cientifico,
               s.comprimentoMedioMetros AS tamanho
        ORDER BY tamanho DESC
        """
        for r in executar_query(client, c2):
            print(f"  • {r['nome']} -> ({r['cientifico']}) -> {r['tamanho']:.1f} metros")

        # C3: Top 5 cobras com maior Nível de Risco de Acidente
        print("\n# [C3] Top 5 cobras com maior Nível de Risco de Acidente:")
        c3 = """
        MATCH (s:Serpente)
        RETURN s.name AS nome,
               s.nomeCientifico AS cientifico,
               s.nivelRiscoAcidente AS risco
        ORDER BY risco DESC, nome ASC
        LIMIT 5
        """
        for r in executar_query(client, c3):
            print(f"  • {r['nome']} ({r['cientifico']}) -> Nível de Risco: {r['risco']}/5")

        # C4: Top 3 cobras com maior diversidade de biomas
        print("\n# [C4] Top 3 Serpentes com maior diversidade de Biomas:")
        c4 = """
        MATCH (s:Serpente)-[:HABITA_BIOMA]->(b:Bioma)
        RETURN s.name AS nome, count(b) AS qtdBiomas, collect(b.name) AS biomas
        ORDER BY qtdBiomas DESC, nome ASC
        LIMIT 3
        """
        for r in executar_query(client, c4):
            print(f"  • {r['nome']} -> Habita {r['qtdBiomas']} biomas -> {r['biomas']}")

        # C5: Existe alguma serpente peçonhenta na Amazônia? (Equivalente ao ASK)
        c5 = """
        MATCH (s:Peconhenta)-[:HABITA_BIOMA]->(b:Bioma {id: 'Amazonia'})
        RETURN count(s) > 0 AS existe
        """
        existe_amazonia = executar_query(client, c5)[0]["existe"]
        print(f"\n# [C5 - ASK] Existe alguma serpente peçonhenta na Amazônia? {existe_amazonia}")

        # C6: Quais são as serpentes peçonhentas na Amazônia e sua família?
        print("\n# [C6] Serpentes peçonhentas que habitam a Amazônia:")
        c6 = """
        MATCH (s:Peconhenta)-[:HABITA_BIOMA]->(b:Bioma {id: 'Amazonia'})
        RETURN s.name AS nome, s.nomeCientifico AS cientifico, labels(s)[-1] AS familia
        ORDER BY nome
        """
        for r in executar_query(client, c6):
            print(f"  • {r['nome']} ({r['cientifico']}) -> Família: {r['familia']}")

        # C7: Projeção de alerta para todas as cobras peçonhentas (Equivalente ao CONSTRUCT)
        print("\n# [C7 - Projeção] Alerta gerado para espécies peçonhentas:")
        c7 = """
        MATCH (s:Peconhenta)
        RETURN s.name AS nome, 'Atenção: Espécie Peçonhenta!' AS alerta
        ORDER BY nome
        """
        for r in executar_query(client, c7):
            print(f"  • {r['nome']} -> {r['alerta']}")

        # C8: INSERT DATA -> SET propriedade observacao na Cascavel
        c8 = """
        MATCH (s:Serpente {id: 'Cascavel'})
        SET s.observacao = 'Possui chocalho na cauda.'
        RETURN s.name AS nome, s.observacao AS obs
        """
        res_c8 = executar_query(client, c8)[0]
        print(f"\n# [C8 - SET] Observação adicionada à {res_c8['nome']}: \"{res_c8['obs']}\"")

        # C9: DELETE DATA -> REMOVE propriedade observacao da Cascavel
        c9 = """
        MATCH (s:Serpente {id: 'Cascavel'})
        REMOVE s.observacao
        RETURN s.observacao AS obs
        """
        res_c9 = executar_query(client, c9)[0]
        print(f"# [C9 - REMOVE] Observação após remoção: {res_c9['obs']} (removida com sucesso!)")

        # C10: UPDATE -> Atualiza comprimento médio da Coral-verdadeira e restaura em seguida
        antes_c10 = executar_query(client, "MATCH (s:Serpente {id: 'CoralVerdadeira'}) RETURN s.comprimentoMedioMetros AS tam")[0]['tam']

        c10_update = """
        MATCH (s:Serpente {id: 'CoralVerdadeira'})
        SET s.comprimentoMedioMetros = 0.85
        RETURN s.name AS nome, s.comprimentoMedioMetros AS novoTamanho
        """
        res_c10 = executar_query(client, c10_update)[0]
        print(f"# [C10 - UPDATE] Comprimento médio da {res_c10['nome']}: {antes_c10:.2f}m -> {res_c10['novoTamanho']}m")

        # Restaura silenciosamente o valor original (0.8m) no banco
        executar_query(client, "MATCH (s:Serpente {id: 'CoralVerdadeira'}) SET s.comprimentoMedioMetros = 0.8")

        # ======================================================================
        # Parte 3: Travessias: 
        # ======================================================================
        print("\n" + "=" * 70)
        print("Parte 3: Travessias encadeadas no grafo: ")
        print("=" * 70)

        # T1 (Direcionada - 2 saltos): Serpente -> Simpátrica -> Dentição
        
        '''
        Consulta para o Memgraph lab:
        MATCH p = (s1:Serpente)-[:E_SIMPATRICA_COM]->(s2:Serpente)-[:POSSUI_DENTICAO]->(d:TipoDenticao)
        RETURN p;
        '''
        
        print("\n# [T1 - Direcionada] Dentição das espécies simpátricas:")
        t1 = """
        MATCH (s1:Serpente)-[:E_SIMPATRICA_COM]->(s2:Serpente)-[:POSSUI_DENTICAO]->(d:TipoDenticao)
        RETURN s1.name AS especie,
               s2.name AS simpatrica,
               d.name AS denticaoSimpatrica
        ORDER BY especie
        """
        for r in executar_query(client, t1):
            print(f"  • {r['especie']} -> {r['simpatrica']} -> Dentição: {r['denticaoSimpatrica']}")


         # T2 (Direcionada - 2 saltos): Peçonhenta -> Simpátrica -> Bioma
        '''
        MATCH p = (pec:Peconhenta)-[:E_SIMPATRICA_COM]->(simp:Serpente)-[:HABITA_BIOMA]->(b:Bioma)
        RETURN p;
        '''
        print("\n# [T2 - Direcionada] Biomas das espécies simpátricas às peçonhentas:")
        t2 = """
        MATCH (pec:Peconhenta)-[:E_SIMPATRICA_COM]->(simp:Serpente)-[:HABITA_BIOMA]->(b:Bioma)
        RETURN pec.name AS peconhenta,
                simp.name AS simpatrica,
                collect(b.name) AS biomas
        ORDER BY peconhenta
        """
        for r in executar_query(client, t2):
            print(f"  • {r['peconhenta']} -> {r['simpatrica']} -> (habita: {', '.join(r['biomas'])})")
       
        # T3 (Bidirecional BFS - 3 saltos): Caminho mais curto de Cobra-cipó até Corre-campo
        
        '''
        Consulta para o Memgraph lab:
        MATCH p = (origem:Serpente {id: 'CobraCipo'})-[*BFS ..6]-(destino:Serpente {id: 'CorreCampo'})
        RETURN p, length(p) AS saltos;
        '''

        t3 = """
        MATCH p = (origem:Serpente {id: 'CobraCipo'})-[*BFS ..6]-(destino:Serpente {id: 'CorreCampo'})
        RETURN origem.name AS origem,
               destino.name AS destino,
               length(p) AS saltos,
               [n IN nodes(p) | n.name] AS nosCaminho,
               [rel IN relationships(p) | type(rel)] AS relacoesCaminho
        """
        res_t3 = executar_query(client, t3)[0]

        print(f"\n# [T3 - BFS] Caminho de {res_t3['origem']} até {res_t3['destino']} ({res_t3['saltos']} saltos):")
        for i, rel in enumerate(res_t3['relacoesCaminho']):
            print(f"  {i + 1}. ({res_t3['nosCaminho'][i]}) --[{rel}]--> ({res_t3['nosCaminho'][i + 1]})")

        # T4 (Bidirecional BFS - 4 saltos): Caminho mais curto de Solenóglifa até Opistóglifa
        
        '''
        Consulta para o Memgraph lab:
        MATCH p = (origem:TipoDenticao {id: 'Solenoglifa'})-[*BFS ..6]-(destino:TipoDenticao {id: 'Opistoglifa'})
        RETURN p, length(p) AS saltos;
        '''
        
        t4 = """
        MATCH p = (origem:TipoDenticao {id: 'Solenoglifa'})-[*BFS ..6]-(destino:TipoDenticao {id: 'Opistoglifa'})
        RETURN origem.name AS origem,
               destino.name AS destino,
               length(p) AS saltos,
               [n IN nodes(p) | n.name] AS nosCaminho,
               [rel IN relationships(p) | type(rel)] AS relacoesCaminho
        """
        res_t4 = executar_query(client, t4)[0]

        print(f"\n# [T4 - BFS] Caminho de {res_t4['origem']} até {res_t4['destino']} ({res_t4['saltos']} saltos):")
        for i, rel in enumerate(res_t4['relacoesCaminho']):
            print(f"  {i + 1}. ({res_t4['nosCaminho'][i]}) --[{rel}]--> ({res_t4['nosCaminho'][i + 1]})")

       

if __name__ == "__main__":
    main()