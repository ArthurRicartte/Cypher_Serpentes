// ==============================================================================
// LIMPEZA INICIAL (Garante recarga limpa do zero)
// ==============================================================================
MATCH (n) DETACH DELETE n;

// ==============================================================================
// BIOMAS (5 instâncias - Raiz 2)
// ==============================================================================
CREATE (:Bioma:BiomaCampestre {id: 'Caatinga', name: 'Caatinga'}),
       (:Bioma:BiomaCampestre {id: 'Cerrado', name: 'Cerrado'}),
       (:Bioma:BiomaFlorestal {id: 'MataAtlantica', name: 'Mata Atlântica'}),
       (:Bioma:BiomaFlorestal {id: 'Amazonia', name: 'Amazônia'}),
       (:Bioma:BiomaCampestre {id: 'Pantanal', name: 'Pantanal'});

// ==============================================================================
// TIPOS DE DENTIÇÃO (4 instâncias - Raiz 3)
// ==============================================================================
CREATE (:TipoDenticao {id: 'Solenoglifa', name: 'Solenóglifa'}),
       (:TipoDenticao {id: 'Proteroglifa', name: 'Proteróglifa'}),
       (:TipoDenticao {id: 'Opistoglifa', name: 'Opistóglifa'}),
       (:TipoDenticao {id: 'Aglifa', name: 'Áglifa'});

// ==============================================================================
// SERPENTES (18 instâncias - Raiz 1 com Multi-Labeling)
// ==============================================================================

// --- Família Viperidae (4 Espécies - Peçonhentas) ---
CREATE (:Serpente:Peconhenta:Viperidae {
    id: 'JararacaDaCaatinga',
    name: 'Jararaca-da-Caatinga',
    nomeCientifico: 'Bothrops erythromelas',
    comprimentoMedioMetros: 0.6,
    eNoturna: true,
    nivelRiscoAcidente: 5,
    alimentacao: 'Pequenos roedores e lagartos'
}),
(:Serpente:Peconhenta:Viperidae {
    id: 'JararacaComum',
    name: 'Jararaca',
    nomeCientifico: 'Bothrops jararaca',
    comprimentoMedioMetros: 1.2,
    eNoturna: true,
    nivelRiscoAcidente: 5,
    alimentacao: 'Roedores e sapos'
}),
(:Serpente:Peconhenta:Viperidae {
    id: 'Cascavel',
    name: 'Cascavel',
    nomeCientifico: 'Crotalus durissus',
    comprimentoMedioMetros: 1.5,
    eNoturna: true,
    nivelRiscoAcidente: 5,
    alimentacao: 'Roedores e pequenos mamíferos'
}),
(:Serpente:Peconhenta:Viperidae {
    id: 'Surucucu',
    name: 'Surucucu-pico-de-jaca',
    nomeCientifico: 'Lachesis muta',
    comprimentoMedioMetros: 2.5,
    eNoturna: true,
    nivelRiscoAcidente: 5,
    alimentacao: 'Pequenos e médios mamíferos'
}),

// --- Família Elapidae (2 Espécies - Peçonhentas) ---
(:Serpente:Peconhenta:Elapidae {
    id: 'CoralVerdadeira',
    name: 'Coral-verdadeira',
    nomeCientifico: 'Micrurus ibiboboca',
    comprimentoMedioMetros: 0.8,
    eNoturna: true,
    nivelRiscoAcidente: 4,
    alimentacao: 'Outras serpentes e lagartos'
}),
(:Serpente:Peconhenta:Elapidae {
    id: 'CoralAmazonica',
    name: 'Coral-amazônica',
    nomeCientifico: 'Micrurus lemniscatus',
    comprimentoMedioMetros: 0.9,
    eNoturna: true,
    nivelRiscoAcidente: 4,
    alimentacao: 'Peixes e anfíbios'
}),

// --- Família Boidae (3 Espécies - Não Peçonhentas) ---
(:Serpente:NaoPeconhenta:Boidae {
    id: 'Jiboia',
    name: 'Jiboia',
    nomeCientifico: 'Boa constrictor',
    comprimentoMedioMetros: 2.0,
    eNoturna: true,
    nivelRiscoAcidente: 1,
    alimentacao: 'Aves e mamíferos'
}),
(:Serpente:NaoPeconhenta:Boidae {
    id: 'SucuriVerde',
    name: 'Sucuri-verde',
    nomeCientifico: 'Eunectes murinus',
    comprimentoMedioMetros: 4.5,
    eNoturna: false,
    nivelRiscoAcidente: 2,
    alimentacao: 'Peixes, aves e mamíferos'
}),
(:Serpente:NaoPeconhenta:Boidae {
    id: 'SucuriAmarela',
    name: 'Sucuri-amarela',
    nomeCientifico: 'Eunectes notaeus',
    comprimentoMedioMetros: 3.0,
    eNoturna: false,
    nivelRiscoAcidente: 2,
    alimentacao: 'Peixes e jacarés pequenos'
}),

// --- Família Colubridae (8 Espécies - Não Peçonhentas) ---
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'FalsaCoral',
    name: 'Falsa-coral',
    nomeCientifico: 'Oxyrhopus trigeminus',
    comprimentoMedioMetros: 0.7,
    eNoturna: true,
    nivelRiscoAcidente: 1,
    alimentacao: 'Pequenos roedores e lagartos'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'CobraCipoVerde',
    name: 'Cobra-cipó-verde',
    nomeCientifico: 'Philodryas olfersii',
    comprimentoMedioMetros: 1.0,
    eNoturna: false,
    nivelRiscoAcidente: 2,
    alimentacao: 'Anfíbios, aves e pequenos roedores'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'CorreCampo',
    name: 'Corre-campo',
    nomeCientifico: 'Philodryas nattereri',
    comprimentoMedioMetros: 1.1,
    eNoturna: false,
    nivelRiscoAcidente: 2,
    alimentacao: 'Lagartos, ovos e pequenos mamíferos'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'Caninana',
    name: 'Caninana',
    nomeCientifico: 'Spilotes pullatus',
    comprimentoMedioMetros: 2.0,
    eNoturna: false,
    nivelRiscoAcidente: 1,
    alimentacao: 'Pequenos roedores e aves'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'CobraCipo',
    name: 'Cobra-cipó',
    nomeCientifico: 'Chironius carinatus',
    comprimentoMedioMetros: 1.2,
    eNoturna: false,
    nivelRiscoAcidente: 1,
    alimentacao: 'Anfíbios e lagartos'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'Mussurana',
    name: 'Mussurana',
    nomeCientifico: 'Pseudoboa nigra',
    comprimentoMedioMetros: 1.4,
    eNoturna: true,
    nivelRiscoAcidente: 1,
    alimentacao: 'Outras serpentes'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'CobraVerde',
    name: 'Cobra-verde',
    nomeCientifico: 'Erythrolamprus reginae',
    comprimentoMedioMetros: 0.6,
    eNoturna: false,
    nivelRiscoAcidente: 1,
    alimentacao: 'Sapos e girinos'
}),
(:Serpente:NaoPeconhenta:Colubridae {
    id: 'FalsaJararaca',
    name: 'Falsa-Jararaca',
    nomeCientifico: 'Xenodon merremii',
    comprimentoMedioMetros: 1.0,
    eNoturna: false,
    nivelRiscoAcidente: 1,
    alimentacao: 'Sapos e rãs'
}),

// --- Família Aniliidae (1 Espécie - Não Peçonhenta) ---
(:Serpente:NaoPeconhenta:Aniliidae {
    id: 'CobraCega',
    name: 'Cobra-cega',
    nomeCientifico: 'Anilius scytale',
    comprimentoMedioMetros: 0.7,
    eNoturna: true,
    nivelRiscoAcidente: 1,
    alimentacao: 'Anfíbios subterrâneos e peixes-cobra'
});

// ==============================================================================
// RELACIONAMENTOS: HABITA_BIOMA (33 arestas)
// ==============================================================================
UNWIND [
    ['JararacaDaCaatinga', ['Caatinga']],
    ['JararacaComum', ['MataAtlantica']],
    ['Cascavel', ['Caatinga', 'Cerrado']],
    ['Surucucu', ['Amazonia', 'MataAtlantica']],
    ['CoralVerdadeira', ['Caatinga', 'MataAtlantica']],
    ['CoralAmazonica', ['Amazonia']],
    ['Jiboia', ['Caatinga', 'Cerrado', 'Amazonia']],
    ['SucuriVerde', ['Amazonia', 'Pantanal']],
    ['SucuriAmarela', ['Pantanal']],
    ['FalsaCoral', ['Caatinga', 'Cerrado']],
    ['CobraCipoVerde', ['Caatinga', 'Cerrado', 'MataAtlantica']],
    ['CorreCampo', ['Caatinga', 'Cerrado']],
    ['Caninana', ['MataAtlantica', 'Cerrado']],
    ['CobraCipo', ['MataAtlantica', 'Amazonia']],
    ['Mussurana', ['Cerrado', 'Caatinga']],
    ['CobraVerde', ['Amazonia', 'MataAtlantica']],
    ['FalsaJararaca', ['Cerrado', 'Caatinga', 'MataAtlantica']],
    ['CobraCega', ['Amazonia']]
] AS item
MATCH (s:Serpente {id: item[0]})
UNWIND item[1] AS bioma_id
MATCH (b:Bioma {id: bioma_id})
CREATE (s)-[:HABITA_BIOMA]->(b);

// ==============================================================================
// RELACIONAMENTOS: POSSUI_DENTICAO (18 arestas)
// ==============================================================================
UNWIND [
    ['JararacaDaCaatinga', 'Solenoglifa'],
    ['JararacaComum', 'Solenoglifa'],
    ['Cascavel', 'Solenoglifa'],
    ['Surucucu', 'Solenoglifa'],
    ['CoralVerdadeira', 'Proteroglifa'],
    ['CoralAmazonica', 'Proteroglifa'],
    ['Jiboia', 'Aglifa'],
    ['SucuriVerde', 'Aglifa'],
    ['SucuriAmarela', 'Aglifa'],
    ['FalsaCoral', 'Opistoglifa'],
    ['CobraCipoVerde', 'Opistoglifa'],
    ['CorreCampo', 'Opistoglifa'],
    ['Caninana', 'Aglifa'],
    ['CobraCipo', 'Aglifa'],
    ['Mussurana', 'Opistoglifa'],
    ['CobraVerde', 'Opistoglifa'],
    ['FalsaJararaca', 'Opistoglifa'],
    ['CobraCega', 'Aglifa']
] AS item
MATCH (s:Serpente {id: item[0]}), (d:TipoDenticao {id: item[1]})
CREATE (s)-[:POSSUI_DENTICAO]->(d);

// ==============================================================================
// RELACIONAMENTOS SIMÉTRICOS MATERIALIZADOS (10 arestas bidirecionais)
// ==============================================================================
UNWIND [
    ['JararacaDaCaatinga', 'Cascavel'],
    ['FalsaCoral', 'CoralVerdadeira']
] AS par
MATCH (s1:Serpente {id: par[0]}), (s2:Serpente {id: par[1]})
CREATE (s1)-[:E_SIMPATRICA_COM]->(s2),
       (s2)-[:E_SIMPATRICA_COM]->(s1);

UNWIND [
    ['JararacaDaCaatinga', 'JararacaComum'],
    ['SucuriAmarela', 'SucuriVerde'],
    ['CobraCipoVerde', 'CorreCampo']
] AS par
MATCH (s1:Serpente {id: par[0]}), (s2:Serpente {id: par[1]})
CREATE (s1)-[:TEM_PARENTE_PROXIMO]->(s2),
       (s2)-[:TEM_PARENTE_PROXIMO]->(s1);