# 🔄 PIPELINES - Fluxo de Processamento de Dados

## Revisão Sistemática de Literatura - Arquitetura de Dados

**Versão:** 1.0  
**Data:** 10 de abril de 2026  
**Status:** Documentado para Replicabilidade

---

## 📊 Visão Geral do Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                   REVISÃO SISTEMÁTICA OPEN SCIENCE                   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
            ┌──────────────────┐        ┌──────────────────┐
            │ FASE 1: BUSCA    │        │ ENTRADA: Dados   │
            │ python 01-...    │        │ (config.py)      │
            └──────────────────┘        └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ data/raw/        │  ← ~587 artigos (CSV)
            │ *.csv            │     scopus, WoS, etc.
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────────────────────────┐
            │ FASE 1.5: RANKING PRÉ-FICHAMENTO ⭐  │
            │ python 06-ranking_relevancia.py      │
            │                                      │
            │ 1. Remove duplicatas (DOI, título)   │
            │ 2. Análise léxica (palavras-chave)  │
            │ 3. Score relevância (0-100)          │
            │ 4. Rankeia artigos                   │
            │ 5. Recomenda TOP para download       │
            └──────────────────────────────────────┘
                    │
        [Output: artigos_ranqueados.csv]
        [Você revisa TOP 30-50% apenas]
                    │
                    ↓
            ┌──────────────────┐
            │[MANUAL] Download │  ← ~150 TOP artigos
            │PDFs selecionados │     (baseado no ranking)
            │articles/pdf/     │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ FASE 2: PDF→MD   │
            │ python 02-...    │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ articles/md/     │  ← ~150 artigos (Markdown)
            │ *.md             │     texto estruturado
            └──────────────────┘
                    │
                    ↓
        ┌──────────────────────────────────────┐
        │ FASE 0: CALIBRAGEM ⭐ NOVO!          │
        │ python 00-calibragem_prompts.py      │
        │ (Com 15-20 artigos seminais)         │
        │ Resultado: Prompts 90%+ confiáveis   │
        └──────────────────────────────────────┘
                    │
            ┌───────┴─────────┐
            ↓                 ↓
        [Concordância     [Concordância
         ≥90%?]           <90%?]
         ↓                 ↓
        ✅ OK          Refinar prompts
        ↓               e reexecutar
        ↓
            ┌──────────────────────────────────────┐
            │ FASE 3: FICHAMENTO A/B TESTING       │
            │ python 03-fichamento_ia_...py        │
            │ (Usa prompts CALIBRADOS!)            │
            │                                      │
            │ ✨ INOVAÇÃO: Dual-IA Validation     │
            │ • Claude (precisão teórica)         │
            │ • Gemini (síntese criativa)         │
            └──────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ↓                       ↓
    ┌────────┐             ┌────────┐
    │ CLAUDE │             │ GEMINI │
    │ File 1 │             │ File 2 │
    └────────┘             └────────┘
        │                       │
        └───────────┬───────────┘
                    ↓
        ┌──────────────────────────────┐
        │ COMPARAÇÃO A/B                │
        │ • Krippendorff's Alpha        │
        │ • Matriz Concordância         │
        │ • Detecção ambiguidades       │
        │ • Score de relevância         │
        └──────────────────────────────┘
                    │
        ┌───────────┴──────────────────────┐
        │                                  │
        ↓                                  ↓
    [Concordância > 85%]          [Concordância 70-85%]
    USAR MÉDIA PONDERADA          REVISAR DISCREPÂNCIAS
        │                                  │
        ↓                                  ↓
    ┌──────────────────┐          ┌──────────────────┐
    │ analysis/        │          │ MARCADO PARA     │
    │ fichamentos/     │          │ REVISÃO HUMANA   │
    │ fichamento_final │          │ PRIORITÁRIA      │
    │ *.md + metadata  │          └──────────────────┘
    └──────────────────┘
                    │
                    ├─→ VALIDAÇÃO HUMANA (10-20%)
                    │   analysis/validacao/
                    │   + Concordância inter-avaliador
                    │
                    ↓
    ┌──────────────────┐
    │ FASE 4: SÍNTESE  │
    │ python 05-...    │
    │ (Usar fichamentos│
    │ + ranking)       │
    └──────────────────┘
            │
            ├─→ VALIDAÇÃO HUMANA (10-20%)
            │   analysis/validacao/
            │   + Concordância inter-avaliador
            │
            ↓
    ┌──────────────────┐
    │ FASE 4: SÍNTESE  │
    │ python 05-...    │
    │ (Usar fichamentos│
    │  validados A/B)  │
    └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ analysis/        │  ← Matriz temática
            │ synthesis/       │  ← Lacunas identificadas
            │ *.md, *.csv      │  ← Proposições
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ FASE 5: ARTIGO   │
            │ Redação ✍️        │
            └──────────────────┘
                    │
                    ↓
            ┌──────────────────┐
            │ Publicação 📚     │
            │ Periódico        │
            └──────────────────┘
```

---

## 🔄 Pipeline 1: BUSCA E COLETA

### Entrada
```
config.py:
  - BASES_DADOS: [scopus, wos, google_scholar, doaj, researchgate]
  - QUERY: termos de busca
  - ANO_INICIO: 2010
  - ANO_FIM: 2026
  - IDIOMAS: [português, inglês]
  - CREDENCIAIS: API keys
```

### Processamento
```
scripts/01-busca_artigos.py

1. Para cada base de dados:
   - Conectar (API ou web scraping)
   - Executar query
   - Recuperar metadados:
     * Título
     * Autores
     * Ano
     * Abstract
     * DOI
     * URL
     * Tipo (journal/conference)
   - Salvar em CSV

2. Consolidação:
   - Mesclar todas as bases
   - Remover duplicatas (por DOI/título)
   - Gerar estatísticas
```

### Saída
```
data/raw/
├── scopus_results.csv (245)
├── wos_results.csv (189)
├── google_scholar_results.csv (412)
├── doaj_results.csv (67)
├── consolidated_searches.csv (434) ← PRINCIPAL
└── busca_relatorio.txt
    ├── Total: 913 iniciais
    ├── Deduplicadas: 434
    └── Estatísticas por base, período, etc.
```

### Formato CSV
```
doi,título,autores,ano,periódico,abstract,url,tipo,fonte
10.1234/ex,Knowledge Transfer...,Smith J; Jones A,2022,JoSBM,"This study...",https://...,journal,scopus
...
```

---

## 📄 Pipeline 2: PDF PARA MARKDOWN

### Entrada
```
articles/pdf/
├── 2022_smith_et_al_knowledge_transfer.pdf
├── 2021_jones_absorptive_capacity.pdf
└── ... (180 arquivos)
```

### Processamento
```
scripts/02-pdf_to_markdown.py

1. Para cada PDF:
   - Detectar se é texto ou escaneado
   - Se texto:
     * Extrair com pdfplumber
     * Estruturar em seções
   - Se escaneado:
     * Usar OCR (Tesseract)
     * Converter para texto
   - Estruturar em Markdown:
     * Metadados (Título, Autores, etc)
     * Seções (Intro, Método, Resultados, Conclusão)
     * Referências

2. Validação:
   - Verificar se MD está bem formado
   - Contar palavras (mínimo 2000)
   - Validar encoding (UTF-8)

3. Consolidação:
   - Criar INDEX.md com lista de artigos
```

### Saída
```
articles/md/
├── 2022_smith_et_al_knowledge_transfer.md
│   # Metadados
│   - Título: Knowledge Transfer in SMEs
│   - Autores: Smith, J.; Jones, A.
│   - DOI: 10.1234/example
│   - Acesso: open/closed
│   
│   # Abstract
│   This study examines...
│   
│   # 1. Introdução
│   ...
│   
│   # 2. Metodologia
│   ...
│   
│   # 3. Resultados
│   ...
│   
│   # 4. Conclusão
│   ...
│   
│   # Referências
│   [1] Cohen, W. M., & Levinthal, D. A...
│
├── 2021_jones_absorptive_capacity.md
├── INDEX.md (lista com links)
└── conversion_report.txt (estatísticas)
```

---

## 🤖 Pipeline 3: FICHAMENTO COM IA

### Entrada
```
articles/md/
├── 2022_smith_et_al_knowledge_transfer.md
└── ... (180 arquivos)

config.py:
  - API_PROVIDER: "openai" ou "anthropic"
  - MODEL: "gpt-4" ou "claude-3-opus"
  - API_KEY: sua chave
```

---

## 🔬 Pipeline 3A: A/B TESTING COM 2 IAs (NOVO ✨)

### Objetivo
Validar robustez dos fichamentos usando **duas IAs independentes**:
- **Claude (Anthropic)**: Precisão em argumentação rigorosa, coerência teórica
- **Gemini (Google)**: Síntese criativa, detecção de padrões emergentes

Comparar resultados para detectar vieses, ambiguidades e aumentar confiança nos dados.

### Processamento Detalhado

```
Para CADA artigo em articles/md/:

┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 1: PREPARAÇÃO                                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Ler arquivo Markdown                                         │
│  2. Validar conteúdo:                                            │
│     - Comprimento mínimo: 500 caracteres                         │
│     - Encoding UTF-8                                             │
│     - Estrutura básica (título, abstract, seções)                │
│  3. Preparar payload para ambas as IAs                           │
│  4. Adicionar prompt system (AB_TESTING_SYSTEM_PROMPT)           │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        ↓                                 ↓
    ┌─────────────────┐             ┌─────────────────┐
    │  CHAMADA CLAUDE │             │  CHAMADA GEMINI │
    │  (Anthropic)    │             │  (Google)       │
    └─────────────────┘             └─────────────────┘
        │                               │
        │ Aguardar 45s max              │ Aguardar 45s max
        │ (com retry 3x)                │ (com retry 3x)
        │                               │
        ↓                               ↓
    ┌─────────────────────────────┐ ┌──────────────────────────────┐
    │  FICHAMENTO_CLAUDE.MD       │ │  FICHAMENTO_GEMINI.MD        │
    │  ✅ Rigoroso                │ │  ✅ Criativo                 │
    │  ✅ Teórico                 │ │  ✅ Sintético                │
    │                             │ │                              │
    │  ## Metadados               │ │  ## Metadados                │
    │  Autores: Smith, J.; ...    │ │  Autores: Smith, J.; ...     │
    │  Ano: 2022                  │ │  Ano: 2022                   │
    │  ...                        │ │  ...                         │
    │                             │ │                              │
    │  ## 1. Objetivo             │ │  ## 1. Objetivo              │
    │  Como AC afeta...           │ │  Como AC afeta...            │
    │  ...                        │ │  ...                         │
    └─────────────────────────────┘ └──────────────────────────────┘
        │                               │
        └───────────────┬───────────────┘
                        ↓
        ┌───────────────────────────────────────────────┐
        │  ETAPA 2: COMPARAÇÃO A/B                      │
        │  (validation_ab.py)                           │
        ├───────────────────────────────────────────────┤
        │                                               │
        │  1. Extrair seções estruturadas:              │
        │     - Metadados (10 campos)                   │
        │     - Objetivo (semântica)                    │
        │     - Metodologia (estrutura)                 │
        │     - Achados (lista de proposições)          │
        │     - ... (8 seções mais)                     │
        │                                               │
        │  2. Para CADA seção estruturada:              │
        │     - Calcular similaridade (token-level)     │
        │     - Verificar campos críticos (100%)        │
        │     - Classificar em: ✅/🟡/❌                │
        │                                               │
        │  3. Gerar matriz concordância:                │
        │     ┌────────────────────────────────────┐   │
        │     │ Seção          │ % Concordância   │   │
        │     ├────────────────────────────────────┤   │
        │     │ Metadados      │ 100% ✅          │   │
        │     │ Objetivo       │ 95%  ✅          │   │
        │     │ Metodologia    │ 88%  ✅          │   │
        │     │ Achados        │ 82%  ✅          │   │
        │     │ Proposições    │ 75%  🟡          │   │
        │     │ Pontos Fortes  │ 65%  ❌          │   │
        │     └────────────────────────────────────┘   │
        │                                               │
        │  4. Calcular Krippendorff's Alpha:            │
        │     Alpha = 0.78 (Strong agreement)          │
        │                                               │
        │  5. Decisão automática:                       │
        │     IF média_concordancia > 85%:              │
        │        → USAR (válido)                        │
        │     ELIF 70% < média < 85%:                   │
        │        → REVISAR (sinalizar)                  │
        │     ELSE:                                     │
        │        → REJEITAR (reprocessar)               │
        │                                               │
        └───────────────────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ↓ [Concordância > 85%]          ↓ [Concordância 70-85%]
                                            (ou < 70%)
    ┌─────────────────────────┐    ┌──────────────────────────┐
    │  ETAPA 3A: CONSENSO     │    │  ETAPA 3B: REVISÃO       │
    ├─────────────────────────┤    ├──────────────────────────┤
    │                         │    │                          │
    │  Criar FICHAMENTO_FINAL │    │  Marcar discrepâncias:   │
    │                         │    │  📌 REQUERE REVISÃO      │
    │  Estratégia:            │    │                          │
    │  • Seções 100% = usar   │    │  1. Listar seções:       │
    │  • Seções 80-99% =      │    │     - Proposições (75%)  │
    │    média ponderada      │    │     - Pontos Fortes      │
    │  • Seções <80% =        │    │                          │
    │    usar Claude (mais    │    │  2. Gerar relatório:     │
    │    rigoroso)            │    │     report_ab_*.md       │
    │                         │    │                          │
    │  Output:                │    │  3. Sinalizar para:      │
    │  fichamento_final.md    │    │     - Revisor humano     │
    │  +metadata_quality.json │    │     - Re-processamento   │
    │                         │    │                          │
    │  metadata_quality.json: │    │  Ação: FILA DE REVISÃO   │
    │  {                      │    │                          │
    │    "fonte": "ab_test",  │    │  Output:                 │
    │    "concordancia": 0.87,│    │  discrepancia_report.md  │
    │    "alpha": 0.78,      │    │  + fichamento_draft.md   │
    │    "estrategia": "media │    │                          │
    │     ponderada",         │    │                          │
    │    "confianca": "alta"  │    │                          │
    │  }                      │    │                          │
    │                         │    │                          │
    └─────────────────────────┘    └──────────────────────────┘
                 │                         │
                 └──────────────┬──────────┘
                                ↓
                    ┌─────────────────────────┐
                    │  PASTA DE SAÍDA:        │
                    │  analysis/fichamentos/  │
                    │  {artigo_id}/           │
                    │  ├── fichamento_claude  │
                    │  ├── fichamento_gemini  │
                    │  ├── comparison_*.json  │
                    │  ├── fichamento_final ✅│
                    │  └── metadata_quality   │
                    └─────────────────────────┘
```

### Exemplo Real de Comparação

**Artigo**: "Knowledge Transfer in Small Firms" (Smith et al., 2022)

**COMPARAÇÃO A/B**:

```json
{
  "artigo_id": "smith_2022_knowledge_transfer",
  "data_analise": "2026-04-10T14:30:00Z",
  "claude_alpha": 0.82,
  "gemini_alpha": 0.79,
  "secoes": {
    "metadados": {
      "claude": "Smith, J.; Jones, A.; Wang, B.",
      "gemini": "Smith, J.; Jones, A.; Wang, B.",
      "concordancia": 1.0,
      "status": "✅ PERFEITO"
    },
    "objetivo": {
      "claude": "Exami the mechanisms of knowledge transfer in small firms...",
      "gemini": "Examine how knowledge is transferred within small firms...",
      "concordancia": 0.92,
      "status": "✅ FORTE"
    },
    "metodologia": {
      "claude": "Qualitativo, 12 casos, entrevistas semi-estruturadas",
      "gemini": "Qualitativo, 12 estudo de casos, 48 entrevistas",
      "concordancia": 0.85,
      "status": "✅ OK",
      "nota": "Claude omitiu número de entrevistas"
    },
    "achados": {
      "claude": [
        "AC limitada em contexto brasileiro",
        "Redes informais críticas para transferência",
        "Liderança tem papel central"
      ],
      "gemini": [
        "Capacidade absortiva é fator limitante",
        "Redes de conhecimento viabilizam inovação",
        "Envolvimento gerencial determina sucesso",
        "Contexto político afeta transferência"
      ],
      "concordancia": 0.78,
      "status": "🟡 REVISAR",
      "diferenca": "Gemini identificou 1 achado extra (contexto político)"
    },
    "proposicoes": {
      "p1": {
        "claude": "✅ AC limitada em MPEs",
        "gemini": "✅ AC limitada em MPEs",
        "concordancia": 1.0,
        "status": "✅"
      },
      "p4": {
        "claude": "🟡 Contexto institucional modera",
        "gemini": "✅ Contexto institucional modera",
        "concordancia": 0.8,
        "status": "🟡",
        "nota": "Gemini mais assertivo que Claude"
      }
    }
  },
  "resumo_geral": {
    "concordancia_media": 0.88,
    "alpha_geral": 0.80,
    "status": "✅ APROVADO",
    "recomendacao": "Usar fichamento final (média ponderada)",
    "secoes_revisar": ["achados", "p4"]
  }
}
```

### Saída de Pastas

```
analysis/fichamentos/
├── 2022_smith_et_al_knowledge_transfer/
│   ├── artigo_original.md
│   ├── fichamento_claude.md
│   │   (Versão gerada por Claude)
│   ├── fichamento_gemini.md
│   │   (Versão gerada por Gemini)
│   ├── comparison_report.json
│   │   {
│   │     "concordancia": 0.88,
│   │     "alpha": 0.80,
│   │     "status": "aprovado",
│   │     "matriz_secoes": {...}
│   │   }
│   ├── fichamento_final.md ← ✅ USAR ESTE
│   │   (Gerado por consenso de ambas)
│   └── metadata_quality.json
│       {
│         "fonte": "ab_testing",
│         "data_processamento": "2026-04-10T14:30:00Z",
│         "modelo_principal": "claude",
│         "modelo_validacao": "gemini",
│         "confianca": "alta",
│         "requer_revisao": false
│       }
│
├── 2021_jones_absorptive_capacity/
│   └── [mesma estrutura]
│
└── ab_testing_summary.csv
    (Resumo concordância para TODOS os artigos)
    id,titulo,autores,ano,concordancia,alpha,status,requer_revisao
    1,Knowledge Transfer...,Smith et al,2022,0.88,0.80,OK,false
    2,Absorptive Capacity...,Jones et al,2021,0.76,0.68,OK,true
    ...
```

---

## 🤖 Pipeline 3B: FICHAMENTO COM IA (Processamento Original)

### Processamento (após A/B Testing)
```
scripts/03-fichamento_ia.py

1. Para cada arquivo MD:
   - Ler conteúdo (extrair até 8000 tokens)
   - Preparar prompt (templates.py)
   - Enviar para IA com contexto:
     * Research question: "Como AC afeta competitividade?"
     * Framework: Conceitos principais
     * Template: Estrutura esperada

2. Prompt de IA:
   SISTEMA: Você é um pesquisador especialista em...
   
   USUÁRIO: Faça um fichamento de:
   {conteúdo_artigo}
   
   Siga este template:
   # Fichamento: [TÍTULO]
   ## 1. Referência Completa
   ## 2. Questão de Pesquisa
   ...

3. Processamento da resposta:
   - Validar formato Markdown
   - Verificar 10 seções presentes
   - Validar comprimento mínimo
   - Se falhar: retentar com modelo menor
   - Se sucesso: salvar

4. Consolidação:
   - Criar FICHAMENTOS_INDEX.csv
   - Gerar RESUMO_FICHAMENTOS.md
```

### Saída
```
analysis/fichamentos/
├── 2022_smith_et_al_knowledge_transfer.md (fichamento)
│   # Fichamento: Knowledge Transfer in SMEs
│   ## 1. Referência Completa
│   Smith, J., & Jones, A. (2022). Knowledge Transfer...
│   DOI: 10.1234/example
│   
│   ## 2. Questão de Pesquisa
│   Como a transferência de conhecimento afeta...
│   
│   ## 3. Método
│   Revisão sistemática de 150 artigos...
│   
│   ... (seções 4-10)
│   
│   ## Validação
│   ✅ Formato correto
│   ✅ 10 seções presentes
│   ✅ 1200 palavras
│
├── 2021_jones_absorptive_capacity.md
├── FICHAMENTOS_INDEX.csv
│   id,título,autores,ano,palavras,status,validação_humana
│   1,Knowledge Transfer...,Smith et al.,2022,1200,OK,pendente
│
├── RESUMO_FICHAMENTOS.md
│   # Resumo de Fichamentos
│   - Total: 180 fichamentos
│   - Taxa sucesso: 97%
│   - Palavras média: 1150
│   - Tempo processamento: 4.5 horas
│
└── fichamento_relatorio.txt
    Estatísticas detalhadas
```

---

## 👤 Pipeline 4: VALIDAÇÃO HUMANA

### Entrada
```
analysis/fichamentos/
├── 2022_smith_et_al_knowledge_transfer.md
├── 2021_jones_absorptive_capacity.md
├── ... (180 arquivos)

articles/md/
└── ... (artigos originais para comparação)
```

### Processamento
```
scripts/04-validacao_amostra.py

1. Seleção de Amostra:
   - Total de fichamentos: 180
   - Amostra: 10-20% = 18-36 artigos
   - Método: Seleção aleatória estratificada
     * 33% sobre Capacidade Absortiva
     * 33% sobre Transferência de Conhecimento
     * 33% sobre MPEs/Competitividade

2. Gerar lista de validação:
   - AMOSTRA-VALIDACAO.md (30 artigos)
   
3. Para cada artigo da amostra (VALIDAÇÃO HUMANA):
   - Leia artigo original (MD ou PDF)
   - Leia fichamento gerado (MD)
   - Preencha CHECKLIST-VALIDACAO.md
     * 10 dimensões verificadas
     * Cada uma com 3-5 sub-itens
     * Resultado: Aprovado / Ajustes / Rejeitar
   
4. Feedback Agregado:
   - Calcular taxa de aprovação
   - Identificar padrões de erro
   - Sugerir melhorias no prompt
```

### Saída
```
analysis/validacao/
├── AMOSTRA-VALIDACAO.md
│   # Amostra de Validação (n=30)
│   - [ ] 2022_smith_et_al.md (Tema: AC)
│   - [ ] 2021_jones_ac.md (Tema: AC)
│   ...
│
├── CHECKLIST-VALIDACAO.md (template)
│   Preenchido 30 vezes (um por artigo)
│
├── VALIDACOES-COMPLETAS.md
│   ## Resultados
│   | Artigo | Status | Ajustes | Notas |
│   | 2022_smith | ✅ | Nenhum | Excelente |
│   
│   ## Feedback Agregado
│   - Taxa aprovação: 90%
│   - Ajustes menores: 25%
│   - Refazer: 10%
│
└── validacao_relatorio.txt
    Estatísticas
```

---

## 📊 Pipeline 5: SÍNTESE QUALITATIVA

### Entrada
```
analysis/fichamentos/
├── 180 fichamentos validados (ou com 90%+ aprovação)

analysis/validacao/
└── VALIDACOES-COMPLETAS.md (feedback)
```

### Processamento
```
scripts/05-sintese_qualitativa.py

1. Extração de Dados:
   - De cada fichamento, extrair:
     * Conceitos-chave
     * Achados principais
     * Métodos usados
     * Contextos geográficos
     * Períodos estudados
     * Lacunas identificadas

2. Codificação Temática (Thematic Analysis):
   - Agrupar por tema:
     * Transferência de Conhecimento (mecanismos)
     * Capacidade Absortiva (dimensões)
     * Competitividade (fatores)
     * MPEs Brasileiras (contexto)
   
3. Matriz Temática:
   - Cruzar temas com:
     * Autores
     * Anos
     * Contextos
     * Achados
   
4. Análise de Lacunas:
   - Geográficas (ex: Brasil vs. mundo)
   - Teóricas (ex: modelos faltando)
   - Metodológicas (ex: qualitativo vs quantitativo)
   - Setoriais (ex: manufatura vs serviços)

5. Proposições de Pesquisa:
   - Formular 5-10 proposições
   - Baseadas nas lacunas
   - Testáveis e relevantes
```

### Saída
```
analysis/synthesis/
├── MATRIZ-TEMATICA.md
│   # Matriz Temática
│   
│   ## Tema 1: Transferência de Conhecimento
│   | Mecanismo | Autores | N Estudos | Contexto |
│   | Colaboração Univ | Smith et al | 45 | Global |
│   
│   ## Tema 2: Capacidade Absortiva
│   | Dimensão | Definição | Autores | Importância |
│   | Realização | Identificar | Cohen & L | Alta |
│
├── LACUNAS-PESQUISA.md
│   # Lacunas Identificadas
│   
│   ## Lacuna 1: Geográfica
│   - Problema: Poucos estudos em Brasil
│   - Encontrado: 12 estudos (3%)
│   - Oportunidade: CRÍTICA
│   
│   ## Lacuna 2: Teórica
│   ...
│
├── PROPOSICOES-FINAIS.md
│   # Proposições de Pesquisa
│   
│   ## P1: Modelo Integrativo
│   - Descrição: Conhecimento → AC → Competitividade
│   - Contexto: MPEs Brasileiras
│   - Tipo: Quantitativa (SEM)
│   - Relevância: CRÍTICA
│
├── TENDENCIAS.md
│   # Tendências Temporais e Temáticas
│   - Evolução dos tópicos (2010-2026)
│   - Foco geográfico
│   - Método preferido
│   - Periódicos principais
│
└── GRAFICOS.csv (dados para visualização)
    tema,ano,freq,autores,contexto
    AC,2022,45,Smith et al.,Global
```

---

## 📝 Pipeline 6: REDAÇÃO DO ARTIGO

### Entrada
```
analysis/synthesis/
├── MATRIZ-TEMATICA.md
├── LACUNAS-PESQUISA.md
└── PROPOSICOES-FINAIS.md

docs/
├── PROTOCOLO-PRISMA-COMPLETO.md
└── framework/FRAMEWORK-CONCEITUAL.md

analysis/fichamentos/
└── 180 fichamentos (para citações)
```

### Processamento
```
Redação Manual (você + orientador)

Estrutura:
1. Título + Abstract
2. Introdução
3. Framework Conceitual
4. Metodologia (PRISMA)
5. Resultados
   - Síntese Quantitativa
   - Síntese Qualitativa
   - Matriz Temática
6. Discussão
7. Lacunas de Pesquisa e Agenda
8. Conclusões
9. Referências (180+)

Para cada seção:
- Use dados de synthesis/
- Cite artigos analisados
- Inclua figuras/tabelas
- Integre com conhecimento próprio
```

### Saída
```
artigo_final.docx ou artigo_final.tex

Versão 1: Rascunho
Versão 2: Com feedback orientador
Versão 3: Final pronto submissão
```

---

## 📁 Estrutura de Arquivos (Mapa de Dados)

```
revisao-literatura-mestrado/
│
├── 📂 data/raw/ (DADOS BRUTOS)
│   ├── scopus_results.csv (245)
│   ├── wos_results.csv (189)
│   ├── google_scholar_results.csv (412)
│   ├── doaj_results.csv (67)
│   ├── consolidated_searches.csv (434) ⭐ PRINCIPAL
│   └── busca_relatorio.txt
│
├── 📂 data/processed/ (DADOS PROCESSADOS)
│   ├── triagem_inicial_resultados.csv (180 selecionados)
│   ├── articles_metadata.csv (178 com DOI recuperado)
│   └── deduplication_log.txt
│
├── 📂 articles/pdf/ (ARTIGOS EM PDF)
│   ├── 2022_smith_et_al_knowledge_transfer.pdf
│   ├── 2021_jones_absorptive_capacity.pdf
│   └── ... (180 arquivos)
│
├── 📂 articles/md/ (ARTIGOS EM MARKDOWN)
│   ├── 2022_smith_et_al_knowledge_transfer.md
│   ├── 2021_jones_absorptive_capacity.md
│   ├── INDEX.md ⭐ ÍNDICE
│   └── conversion_report.txt
│
├── 📂 analysis/fichamentos/ (FICHAMENTOS IA)
│   ├── 2022_smith_et_al_knowledge_transfer.md
│   ├── 2021_jones_absorptive_capacity.md
│   ├── FICHAMENTOS_INDEX.csv
│   ├── RESUMO_FICHAMENTOS.md
│   └── fichamento_relatorio.txt
│
├── 📂 analysis/validacao/ (VALIDAÇÃO HUMANA)
│   ├── AMOSTRA-VALIDACAO.md (30 artigos)
│   ├── CHECKLIST-VALIDACAO.md (template)
│   ├── VALIDACOES-COMPLETAS.md (resultados)
│   └── validacao_relatorio.txt
│
├── 📂 analysis/synthesis/ (SÍNTESE FINAL)
│   ├── MATRIZ-TEMATICA.md ⭐ RESULTADO CHAVE
│   ├── LACUNAS-PESQUISA.md ⭐ RESULTADO CHAVE
│   ├── PROPOSICOES-FINAIS.md ⭐ RESULTADO CHAVE
│   ├── TENDENCIAS.md
│   ├── GRAFICOS.csv (dados)
│   └── synthesis_relatorio.txt
│
└── 📂 docs/ (DOCUMENTAÇÃO)
    ├── 00-ROTEIRO-COMPLETO.md ⭐ LEIA
    ├── PROTOCOLO-PRISMA-COMPLETO.md (PRISMA 2020 + 2024-IA)
    ├── 02-CRITERIOS-INCLUSAO.md
    ├── 03-PALAVRAS-CHAVE.md
    └── framework/
        ├── FRAMEWORK-CONCEITUAL.md
        └── PROPOSICOES-PESQUISA.md
```

---

## 🔐 Garantias de Replicabilidade

### Open Data
- ✅ Todos os artigos em `data/raw/` (metadados)
- ✅ Artigos convertidos em `articles/md/` (legível)
- ✅ Fichamentos em `analysis/fichamentos/` (estruturado)
- ✅ Validações em `analysis/validacao/` (transparente)

### Open Code
- ✅ Scripts Python versados e documentados
- ✅ Configurações em `config.py` editável
- ✅ Prompts em `prompts.py` editável
- ✅ Todos em Git

### Open Methodology
- ✅ Protocolo PRISMA documentado
- ✅ Critérios explícitos
- ✅ Decisões rastreáveis
- ✅ Changelog mantido

---

## 🚀 Como Usar Este Documento

1. **Para Entender o Fluxo:** Leia "Visão Geral do Pipeline"
2. **Para Executar:** Siga cada pipeline sequencialmente
3. **Para Debugar:** Verifique entradas/saídas esperadas
4. **Para Replicar:** Copie estrutura exatamente

---

**Próximo Passo:** Leia [docs/00-ROTEIRO-COMPLETO.md](docs/00-ROTEIRO-COMPLETO.md)

*Open Science é assim que fazemos pesquisa! 🚀*
