# 🔄 Pipeline Completo - Fluxo de Execução

> **Objetivo**: Entender exatamente o que cada script faz, em que ordem executar, e o que esperar de output

**Leia este documento ANTES de executar qualquer script!**

---

## 📋 Índice

1. [Visão Geral](#-visão-geral)
2. [Execução Passo-a-Passo](#-execução-passo-a-passo)
3. [Tempos Estimados](#️-tempos-totais-estimados)
4. [Outputs Principais](#-outputs-principais)
5. [Próximos Passos](#próximo)

---

## 📊 Visão Geral

```
[CSV Bruto com Artigos]
         ↓
[06] RANKING DE RELEVÂNCIA ⭐
    └─ Remove duplicatas
    └─ Calcula score de relevância
    └─ Filtra artigos de baixa qualidade
         ↓
[00] CALIBRAGEM DE PROMPTS
    └─ Lê artigos seminais
    └─ Gera prompts calibrados
    └─ Salva versão 2.0 dos prompts
         ↓
[02] PDF → MARKDOWN
    └─ Baixa PDFs
    └─ Converte em Markdown
    └─ Extrai estrutura
         ↓
[03] FICHAMENTO AUTOMÁTICO 🤖🤖
    └─ Processa com Claude (thread 1)
    └─ Processa com Gemini (thread 2)
    └─ Ambas em paralelo!
         ↓
[04] VALIDAÇÃO COM KRIPPENDORFF
    └─ Compara fichamentos Claude vs Gemini
    └─ Calcula Alpha de concordância
    └─ Identifica discrepâncias
         ↓
[05] SÍNTESE QUALITATIVA
    └─ Agrupa por temas
    └─ Cria matriz conceitual
    └─ Mapeia gaps na literatura
         ↓
[Relatório Final + Dados Brutos]
```

---

## �� Execução Passo-a-Passo

### PASSO 1: Ranking de Relevância (NOVO!) ⭐

**Script**: `python scripts/06-ranking_relevancia.py`

**O que faz**: Remove duplicatas, análise léxica, calcula score 0-100 para cada artigo

**Tempo**: ~10 segundos para 100 artigos

**Benefício**: Economiza 40-60% do tempo processando apenas artigos relevantes

---

### PASSO 2: Calibragem de Prompts

**Script**: `python scripts/00-calibragem_prompts.py`

**O que faz**: Lê artigos seminais, gera prompts calibrados v2.0

**Tempo**: ~5 minutos

---

### PASSO 3: PDF → Markdown

**Script**: `python scripts/02-pdf_to_markdown.py`

**O que faz**: Converte PDFs em Markdown estruturado

**Tempo**: ~2-3 minutos por 100 artigos

---

### PASSO 4: Fichamento (A/B Testing) 🤖🤖

**Script**: `python scripts/03-fichamento_ia_krippendorff.py`

**O que faz**: Claude + Gemini processam em paralelo

**Tempo**: ~30-60 minutos para 100 artigos

---

### PASSO 5: Validação com Krippendorff

**Script**: `python scripts/04-validacao_krippendorff.py`

**O que faz**: Compara fichamentos, calcula Alpha de concordância

**Tempo**: ~5 minutos

---

### PASSO 6: Síntese Qualitativa

**Script**: `python scripts/05-sintese_qualitativa.py`

**O que faz**: Gera matriz conceitual, temas, gaps, relatório final

**Tempo**: ~10 minutos

---

## ⏱️ Tempos Totais Estimados

| Cenário | Tempo |
|---------|-------|
| 10 artigos | ~15 minutos |
| 100 artigos | ~1 hora 21 minutos |
| 100 artigos COM ranking (remove 40%) | ~50 minutos ⚡ |
| 1000 artigos | ~11 horas |

---

## 📊 Outputs Principais

- `analysis/fichamentos/*.md` - Fichamentos estruturados
- `analysis/validacao/krippendorff_alpha_resultado.txt` - Scores de concordância
- `analysis/sintese/relatorio_final.md` - Achados integrados
- `data/processed/duplicatas_removidas.csv` - Rastreamento PRISMA

---

**Próximo**: Leia [`README.md`](README.md) para visão geral
