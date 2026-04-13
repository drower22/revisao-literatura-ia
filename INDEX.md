# 📑 Índice Completo da Documentação

> **Navegação**: Este documento organiza TODA a documentação do projeto de forma lógica e sequencial

---

## 🎯 Como Usar Este Índice

**Se você é novo no projeto**: Siga a ordem dos níveis (1 → 2 → 3 → 4)  
**Se você já conhece o projeto**: Use como referência rápida

---

## 📚 Nível 1: Primeiros Passos (30 minutos)

### Documentos Essenciais

| # | Documento | Descrição | Tempo |
|---|-----------|-----------|-------|
| 1 | [README.md](README.md) | **COMECE AQUI** - Visão geral completa do projeto | 10 min |
| 2 | [GUIA-RAPIDO.md](GUIA-RAPIDO.md) | Setup e execução em 5 passos | 10 min |
| 3 | [PIPELINES.md](PIPELINES.md) | Fluxo de execução dos scripts | 10 min |

**Objetivo**: Entender o que é o projeto e como começar

---

## 🔬 Nível 2: Metodologia Científica (2-3 horas)

### Protocolo PRISMA e Fundamentos

| # | Documento | Descrição | Tempo |
|---|-----------|-----------|-------|
| 4 | [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md) | Protocolo PRISMA 2020 + 2024-IA completo | 1h |
| 5 | [docs/02-CRITERIOS-INCLUSAO.md](docs/02-CRITERIOS-INCLUSAO.md) | Critérios de inclusão e exclusão | 30 min |
| 6 | [docs/03-PALAVRAS-CHAVE.md](docs/03-PALAVRAS-CHAVE.md) | Estratégia de busca e palavras-chave | 30 min |
| 7 | [docs/02-METODOLOGIA-IA-AB-TESTING.md](docs/02-METODOLOGIA-IA-AB-TESTING.md) | Como funciona o A/B Testing com IAs | 30 min |

### Framework Teórico

| # | Documento | Descrição | Tempo |
|---|-----------|-----------|-------|
| 8 | [docs/framework/FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md) | 7 teorias principais do projeto | 1h |

**Objetivo**: Compreender a base científica e metodológica

---

## 💻 Nível 3: Implementação Técnica (2-3 horas)

### Scripts e Automação

| # | Documento | Descrição | Tempo |
|---|-----------|-----------|-------|
| 9 | [scripts/README.md](scripts/README.md) | **Documentação completa de todos os scripts** | 1h |
| 10 | [IMPLEMENTACAO-CALIBRAGEM-RANKING.md](IMPLEMENTACAO-CALIBRAGEM-RANKING.md) | Detalhes da calibragem e ranking | 30 min |
| 11 | [VERIFICACAO_SCRIPT_06.md](VERIFICACAO_SCRIPT_06.md) | Validação técnica do script de ranking | 20 min |

### Consolidação e Deploy

| # | Documento | Descrição | Tempo |
|---|-----------|-----------|-------|
| 12 | [CONSOLIDACAO_FINAL.md](CONSOLIDACAO_FINAL.md) | Consolidação de melhorias | 20 min |
| 13 | [DEPLOY_GITHUB.md](DEPLOY_GITHUB.md) | Instruções para deploy no GitHub | 15 min |

**Objetivo**: Entender como os scripts funcionam tecnicamente

---

## 🚀 Nível 4: Execução Prática

### Ordem de Leitura para Execução

1. **Antes de executar**: Leia [GUIA-RAPIDO.md](GUIA-RAPIDO.md)
2. **Durante execução**: Consulte [PIPELINES.md](PIPELINES.md)
3. **Para cada script**: Veja [scripts/README.md](scripts/README.md)
4. **Em caso de dúvidas**: Consulte [README.md](README.md) seção FAQ

---

## 📂 Estrutura de Pastas e Arquivos

### Raiz do Projeto

```
revisao-literatura-mestrado/
├── README.md                           ← Documento principal (LEIA PRIMEIRO)
├── INDEX.md                            ← Este arquivo (índice completo)
├── GUIA-RAPIDO.md                      ← Setup rápido em 5 passos
├── PIPELINES.md                        ← Fluxo de execução
│
├── IMPLEMENTACAO-CALIBRAGEM-RANKING.md ← Detalhes técnicos
├── VERIFICACAO_SCRIPT_06.md            ← Validação do ranking
├── CONSOLIDACAO_FINAL.md               ← Consolidação
├── DEPLOY_GITHUB.md                    ← Deploy
│
├── requirements.txt                    ← Dependências Python
├── .gitignore                          ← Arquivos ignorados
└── .env.example                        ← Template de configuração
```

### Pasta `docs/` - Documentação Científica

```
docs/
├── PROTOCOLO-PRISMA-COMPLETO.md       ← Protocolo completo PRISMA 2020 + 2024-IA
├── 02-CRITERIOS-INCLUSAO.md           ← Critérios de screening
├── 03-PALAVRAS-CHAVE.md               ← Estratégia de busca
├── 02-METODOLOGIA-IA-AB-TESTING.md    ← A/B Testing explicado
├── 00-ROTEIRO-COMPLETO.md             ← Roteiro detalhado (legacy)
├── 00-ROTEIRO-EXECUTIVO.md            ← Roteiro executivo (legacy)
└── framework/
    └── FRAMEWORK-CONCEITUAL.md        ← 7 teorias principais
```

### Pasta `scripts/` - Código Python

```
scripts/
├── README.md                          ← Documentação completa dos scripts
│
├── 00-calibragem_prompts.py           ← Calibra prompts com seminais
├── 01-busca_artigos.py                ← Consolida buscas
├── 06-ranking_relevancia.py           ← Ranking de relevância
├── 02-pdf_to_markdown.py              ← Converte PDFs
├── 03-fichamento_ia_krippendorff.py   ← Fichamento A/B Testing
├── 04-validacao_krippendorff.py       ← Validação estatística
├── 05-sintese_qualitativa.py          ← Síntese temática
│
└── utils/                             ← Utilitários
    ├── config.py                      ← Configurações
    ├── prompts.py                     ← Prompts originais
    ├── prompts_calibrados.py          ← Prompts v2.0
    ├── analise_lexical.py             ← Dicionários
    └── krippendorff_calculator.py     ← Cálculo Alpha
```

### Pasta `data/` - Dados do Projeto

```
data/
├── raw/                               ← CSVs brutos de buscas
│   ├── scopus_resultados.csv
│   ├── wos_resultados.csv
│   └── scielo_resultados.csv
│
├── processed/                         ← Dados processados
│   ├── artigos_consolidados.csv       ← Consolidado
│   ├── artigos_ranqueados.csv         ← Com ranking
│   └── duplicatas_removidas.csv       ← Rastreamento PRISMA
│
└── calibragem/                        ← Artigos seminais
    ├── artigos_seminais.txt
    └── leituras_baseline/
```

### Pasta `analysis/` - Resultados

```
analysis/
├── fichamentos/                       ← Fichamentos gerados
│   ├── [artigo]_claude.md
│   └── [artigo]_gemini.md
│
├── calibragem/                        ← Resultados calibragem
│   ├── matriz_calibragem.csv
│   └── relatorio_calibragem.md
│
├── relevancia/                        ← Análise de ranking
│   └── relatorio_ranking.md
│
├── validacao/                         ← Validação estatística
│   └── krippendorff_alpha_resultado.txt
│
└── sintese/                           ← Síntese final
    ├── relatorio_final.md
    └── matriz_conceitos.csv
```

### Pasta `articles/` - Artigos Coletados

```
articles/
├── pdf/                               ← PDFs originais
│   └── [AUTOR_ANO].pdf
│
└── md/                                ← Markdown convertido
    └── [AUTOR_ANO].md
```

---

## 🗺️ Roadmap de Leitura por Objetivo

### Objetivo: "Quero entender o projeto rapidamente"
1. [README.md](README.md) - 10 min
2. [GUIA-RAPIDO.md](GUIA-RAPIDO.md) - 10 min
3. **Total**: 20 minutos

### Objetivo: "Quero executar os scripts"
1. [GUIA-RAPIDO.md](GUIA-RAPIDO.md) - 10 min
2. [PIPELINES.md](PIPELINES.md) - 10 min
3. [scripts/README.md](scripts/README.md) - 30 min
4. **Total**: 50 minutos

### Objetivo: "Quero entender a metodologia científica"
1. [README.md](README.md) - 10 min
2. [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md) - 1h
3. [docs/02-METODOLOGIA-IA-AB-TESTING.md](docs/02-METODOLOGIA-IA-AB-TESTING.md) - 30 min
4. [docs/framework/FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md) - 1h
5. **Total**: 2h 40min

### Objetivo: "Quero adaptar para meu tema"
1. [README.md](README.md) - 10 min
2. [scripts/README.md](scripts/README.md) - 30 min
3. [docs/02-CRITERIOS-INCLUSAO.md](docs/02-CRITERIOS-INCLUSAO.md) - 30 min
4. [docs/03-PALAVRAS-CHAVE.md](docs/03-PALAVRAS-CHAVE.md) - 30 min
5. Editar: `scripts/utils/analise_lexical.py` e `scripts/utils/prompts.py`
6. **Total**: 1h 40min + edição

### Objetivo: "Quero publicar minha revisão"
1. Todos os documentos de Nível 2 (Metodologia)
2. [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md) - Seção "Disseminação"
3. [README.md](README.md) - Seção "Como Citar"
4. **Total**: 3h

---

## 🔍 Busca Rápida por Tópico

### Configuração e Setup
- [GUIA-RAPIDO.md](GUIA-RAPIDO.md) - Passos 1-3
- [README.md](README.md) - Seção "Pré-requisitos"

### Execução de Scripts
- [PIPELINES.md](PIPELINES.md) - Fluxo completo
- [scripts/README.md](scripts/README.md) - Documentação detalhada

### Metodologia PRISMA
- [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)
- [docs/02-CRITERIOS-INCLUSAO.md](docs/02-CRITERIOS-INCLUSAO.md)

### A/B Testing e IA
- [docs/02-METODOLOGIA-IA-AB-TESTING.md](docs/02-METODOLOGIA-IA-AB-TESTING.md)
- [README.md](README.md) - Seção "Inovações Metodológicas"

### Calibragem de Prompts
- [IMPLEMENTACAO-CALIBRAGEM-RANKING.md](IMPLEMENTACAO-CALIBRAGEM-RANKING.md)
- [scripts/README.md](scripts/README.md) - Script 00

### Ranking de Relevância
- [VERIFICACAO_SCRIPT_06.md](VERIFICACAO_SCRIPT_06.md)
- [scripts/README.md](scripts/README.md) - Script 06

### Validação Estatística
- [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md) - Seção 5.4
- [scripts/README.md](scripts/README.md) - Script 04

### Framework Teórico
- [docs/framework/FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md)

### Troubleshooting
- [GUIA-RAPIDO.md](GUIA-RAPIDO.md) - Seção "Troubleshooting"
- [README.md](README.md) - Seção "FAQ"

---

## 📊 Documentos por Categoria

### 📘 Documentação Geral
- [README.md](README.md) - Documento principal
- [INDEX.md](INDEX.md) - Este arquivo
- [GUIA-RAPIDO.md](GUIA-RAPIDO.md) - Setup rápido

### 🔬 Documentação Científica
- [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)
- [docs/02-CRITERIOS-INCLUSAO.md](docs/02-CRITERIOS-INCLUSAO.md)
- [docs/03-PALAVRAS-CHAVE.md](docs/03-PALAVRAS-CHAVE.md)
- [docs/02-METODOLOGIA-IA-AB-TESTING.md](docs/02-METODOLOGIA-IA-AB-TESTING.md)
- [docs/framework/FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md)

### 💻 Documentação Técnica
- [scripts/README.md](scripts/README.md)
- [PIPELINES.md](PIPELINES.md)
- [IMPLEMENTACAO-CALIBRAGEM-RANKING.md](IMPLEMENTACAO-CALIBRAGEM-RANKING.md)
- [VERIFICACAO_SCRIPT_06.md](VERIFICACAO_SCRIPT_06.md)

### 📦 Documentação de Deploy
- [DEPLOY_GITHUB.md](DEPLOY_GITHUB.md)
- [CONSOLIDACAO_FINAL.md](CONSOLIDACAO_FINAL.md)

---

## ✅ Checklist de Leitura

Use este checklist para acompanhar seu progresso:

### Essenciais (Todos devem ler)
- [ ] [README.md](README.md)
- [ ] [GUIA-RAPIDO.md](GUIA-RAPIDO.md)
- [ ] [PIPELINES.md](PIPELINES.md)

### Para Pesquisadores (Metodologia)
- [ ] [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)
- [ ] [docs/02-CRITERIOS-INCLUSAO.md](docs/02-CRITERIOS-INCLUSAO.md)
- [ ] [docs/framework/FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md)

### Para Desenvolvedores (Técnico)
- [ ] [scripts/README.md](scripts/README.md)
- [ ] [IMPLEMENTACAO-CALIBRAGEM-RANKING.md](IMPLEMENTACAO-CALIBRAGEM-RANKING.md)
- [ ] [VERIFICACAO_SCRIPT_06.md](VERIFICACAO_SCRIPT_06.md)

---

## 🔄 Documentos Deprecados (Legacy)

Estes documentos foram consolidados em versões mais recentes:

- ~~COMECE-AQUI.md~~ → Substituído por [GUIA-RAPIDO.md](GUIA-RAPIDO.md)
- ~~INDICE.md~~ → Substituído por [INDEX.md](INDEX.md) (este arquivo)
- `docs/00-ROTEIRO-COMPLETO.md` → Mantido para referência histórica
- `docs/00-ROTEIRO-EXECUTIVO.md` → Mantido para referência histórica

---

## 📞 Precisa de Ajuda?

- 📖 **Documentação**: Comece pelo [README.md](README.md)
- 🐙 **GitHub Issues**: https://github.com/drower22/revisao-literatura-ia/issues
- 💬 **Discussões**: GitHub Discussions

---

**Última atualização**: 13 de Abril de 2026  
**Versão**: 2.0  
**Total de documentos**: 20+
