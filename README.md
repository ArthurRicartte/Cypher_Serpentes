# Cypher Serpentes 🐍
# Grafo de Conhecimento de Serpentes Brasileiras (Memgraph + Cypher)

Base de conhecimento sobre serpentes brasileiras remodelada como um **Grafo de Propriedades (LPG)** no **Memgraph**, utilizando **Cypher** e **Python** para carga, consultas analíticas, operações de escrita e travessias.

---

## 1. Modelo do Grafo de Propriedades

O grafo possui **27 nós** e **62 relacionamentos**:

### Entidades

| Rótulo | Propriedades |
| :--- | :--- |
| `:Serpente` | `id`, `name`, `nomeCientifico`, `comprimentoMedioMetros`, `eNoturna`, `nivelRiscoAcidente`, `alimentacao` |
| `:Peconhenta` *(rótulo secundário de `:Serpente`)* | *(herda as propriedades de `:Serpente`)* |
| `:NaoPeconhenta` *(rótulo secundário de `:Serpente`)* | *(herda as propriedades de `:Serpente`)* |
| `:Viperidae`, `:Elapidae`, `:Boidae`, `:Colubridae`, `:Aniliidae` *(famílias de `:Serpente`)* | *(herdam as propriedades de `:Serpente`)* |
| `:Bioma` | `id`, `name` |
| `:BiomaCampestre`, `:BiomaFlorestal` *(rótulos secundários de `:Bioma`)* | *(herdam as propriedades de `:Bioma`)* |
| `:TipoDenticao` | `id`, `name` |

> **Uso de Rótulos Aninhados:** Os nós utilizam múltiplos rótulos combinados para representar a hierarquia taxonômica da base sem precisar criar nós extras de categoria:
> * **Exemplo em Serpentes:** `(:Serpente:Peconhenta:Viperidae {id: 'Cascavel', name: 'Cascavel', ...})` — identifica simultaneamente que o nó é uma serpente, possui peçonha e pertence à família *Viperidae*.
> * **Exemplo em Biomas:** `(:Bioma:BiomaFlorestal {id: 'Amazonia', name: 'Amazônia'})` — classifica o nó como um bioma e especifica sua característica predominante (*florestal*).

### Relacionamentos

| Rótulo | Propriedades |
| :--- | :--- |
| `:HABITA_BIOMA` (`:Serpente -> :Bioma`) | *(sem propriedades)* |
| `:POSSUI_DENTICAO` (`:Serpente -> :TipoDenticao`) | *(sem propriedades)* |
| `:E_SIMPATRICA_COM` (`:Serpente -> :Serpente`) | *(sem propriedades)* |
| `:TEM_PARENTE_PROXIMO` (`:Serpente -> :Serpente`) | *(sem propriedades)* |
---

## 2. Catálogo de Consultas (`Scripts/consultas.py`)

O script executa e exibe no terminal três conjuntos de consultas:

### Consultas Diretas (Equivalentes ao `g.triples`)
- **1.1:** Propriedades e relacionamentos da `Jararaca-da-Caatinga`.
- **1.2:** Serpentes pertencentes à família `Elapidae`.
- **1.3:** Serpentes que habitam o bioma `Caatinga`.
- **1.4:** Serpentes com hábito noturno (`eNoturna: true`).
- **1.5:** Serpentes com dentição `Opistóglifa`.

### Migração SPARQL -> Cypher
- **C1:** Nome popular e científico de serpentes noturnas ordenados alfabeticamente.
- **C2:** Ranking de serpentes com comprimento médio $\ge 1.5\text{m}$.
- **C3:** Top 5 serpentes com maior `nivelRiscoAcidente`.
- **C4:** Top 3 serpentes com maior diversidade de biomas habitados (`count` + `collect`).
- **C5 (`ASK`):** Verificação booleana se existe alguma serpente peçonhenta na `Amazônia`.
- **C6:** Listagem das serpentes peçonhentas na `Amazônia` com suas respectivas famílias.
- **C7 (`CONSTRUCT` / Projeção):** Geração dinâmica de alerta de risco para espécies peçonhentas.
- **C8 (`SET`):** Inserção da propriedade `observacao` na `Cascavel`.
- **C9 (`REMOVE`):** Remoção da propriedade `observacao` da `Cascavel`.
- **C10 (`UPDATE`):** Atualização temporária do comprimento médio da `Coral-verdadeira` (`0.80m -> 0.85m`) com restauração automática do estado original.

### Travessias Encadeadas no Grafo (Multi-Hop)
- **T1 (Direcionada — 2 saltos):** `(:Serpente)-[:E_SIMPATRICA_COM]->(:Serpente)-[:POSSUI_DENTICAO]->(:TipoDenticao)` — Descobre a dentição das espécies simpátricas.
- **T2 (Direcionada — 2 saltos):** `(:Peconhenta)-[:E_SIMPATRICA_COM]->(:Serpente)-[:HABITA_BIOMA]->(:Bioma)` — Identifica os biomas das espécies simpátricas às peçonhentas.
- **T3 (Bidirecional — 3 saltos):** Caminho mínimo entre `Cobra-cipó` e `Corre-campo` exibindo nós e arestas intermediárias.
- **T4 (Bidirecional — 4 saltos):** Caminho mínimo entre os tipos de dentição `Solenóglifa` e `Opistóglifa`.

---

## 3. Passo a Passo de Execução

### Pré-requisitos
- **Docker** (Docker Desktop ou Docker Engine + Compose) instalado e em execução.
- **Python 3.10+** instalado.

### 1. Criar e ativar o ambiente virtual (`venv`)
Na raiz do repositório, crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

* **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Baixar e instalar as dependências (`requirements.txt`)
Com o ambiente virtual ativo, instale o driver oficial do banco:

```bash
pip install -r requirements.txt
```

### 3. Rodar o Docker (Memgraph + Memgraph Lab)
Suba os containers em segundo plano:

```bash
docker compose up -d
```

### 4. Rodar o script de carga (`carga.py`)
Popule o banco de dados com os 27 nós e 61 relacionamentos:

```bash
python Scripts/carga.py
```

### 5. Rodar o script de consultas (`consultas.py`)
Execute todas as consultas diretas, analíticas, operações de escrita e travessias no terminal:

```bash
python Scripts/consultas.py
```

### 6. Visualizar no Memgraph Lab (Opcional)
Se quiser visualizar o grafo e testar as consultas interativamente no navegador:
1. Acesse **[http://localhost:3000](http://localhost:3000)**.
2. Conecte-se ao banco.
3. Na aba **Query Execution**, rode qualquer consulta Cypher (por exemplo, para exibir o grafo completo):
   ```cypher
   MATCH (n)
   OPTIONAL MATCH (n)-[r]->(m)
   RETURN n, r, m;
   ```

### 7. Encerrar o ambiente
Para desligar os containers mantendo os dados salvos no volume `mg_lib`:

```bash
docker compose down
```
