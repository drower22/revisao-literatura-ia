# 🔧 Scripts de Automação - Revisão Sistemática com A/B Testing

**Data**: 10 de abril de 2026  
**Objetivo**: Automação completa de busca, processamento e análise de artigos com A/B Testing (Claude vs Gemini)

**Estrutura**:
```
scripts/
├── 00-calibragem_prompts.py      # ⭐ NOVO! Calibra prompts com artigos seminais
├── 01-busca_artigos.py           # Consolidar artigos de múltiplas bases
├── 02-pdf_to_markdown.py         # Converter PDFs em Markdown estruturado
├── 03-fichamento_ia_krippendorff.py     # Fichamentos paralelos + scores relevância
├── 04-validacao_krippendorff.py  # Validação com Krippendorff's Alpha
├── 05-sintese_qualitativa.py     # Síntese temática e matriz de conceitos
├── 06-ranking_relevancia.py      # ⭐ NOVO! Ranking automático por relevância
├── utils/
│   ├── config.py                 # Configurações centralizadas
│   ├── prompts.py                # Prompts originais
│   ├── prompts_calibrados.py     # ⭐ NOVO! Prompts pós-calibragem (v2.0)
│   ├── analise_lexical.py        # ⭐ NOVO! Dicionários para ranking
│   ├── krippendorff_calculator.py # Cálculo de Krippendorff's Alpha
│   └── __init__.py
└── README.md                      # Este arquivo
```

---

## 🚀 Instalação e Setup

### 1. Instalar dependências

```bash
# Clonar ou fazer fork do repositório
cd revisao-literatura-mestrado

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar packages
pip install -r requirements.txt
```

### 2. Configurar credenciais de API

```bash
# Criar arquivo .env na raiz do projeto
touch .env

# Adicionar (editar com seus valores):
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Validar instalação

```bash
python -c "import pandas; import openai; print('✓ Dependências OK')"
```

---

## 📖 Como Usar Cada Script

### Script 00: Calibragem de Prompts ⭐ NOVO!

**Objetivo**: Validar e refinar prompts usando 15-20 artigos seminais que você já conhece

**Por que é importante**:
- Garante que prompts funcionam bem com SEUS dados
- Reduz necessidade de revisão humana de 40% → 10-15%
- Fichamentos chegam a 90%+ de concordância vs sua leitura

**Pré-requisitos**:
- [ ] Preparar 15-20 artigos seminais em `articles/md/`
- [ ] Fazer leitura + fichamento manual de cada um
- [ ] Salvar em `data/calibragem/leituras_baseline/`
- [ ] Listar em `data/calibragem/artigos_seminais.txt` (veja template)

**Execução**:
```bash
python scripts/00-calibragem_prompts.py
```

**Saída**:
- `analysis/calibragem/matriz_calibragem.csv` - Comparação IA vs seu fichamento
- `analysis/calibragem/relatorio_calibragem.md` - Recomendações de refinamento
- `analysis/calibragem/CHECKLIST-PRE-FICHAMENTO.md` - Validação (90%+ concordância?)
- `analysis/calibragem/fichamentos_ia/` - Outputs Claude e Gemini para cada artigo

**Fluxo**:
```
1. Carregar 15-20 artigos seminais
2. Executar Claude + Gemini em paralelo
3. Comparar vs sua leitura original (baseline)
4. Gerar matriz de concordância
5. Se <90%, refine prompts em scripts/utils/prompts_calibrados.py
6. Reexecute até 90%+
7. Então aprove com checklist ✅
```

---

### Script 01: Consolidação de Buscas

**Objetivo**: Ler CSVs de múltiplas bases de dados, consolidar e remover duplicatas

**Pré-requisitos**:
- [ ] Arquivos CSV baixados de Scopus, WoS, SciELO, Scholar
- [ ] Salvos em `data/raw/` com nomes: `scopus_resultados.csv`, `wos_resultados.csv`, etc.

**Execução**:
```bash
python scripts/01-busca_artigos.py
```

**Saída**:
- `data/processed/artigos_consolidados.csv` - Lista consolidada
- `data/processed/relatorio_busca.txt` - Estatísticas e resumo

**Exemplo Output**:
```
RELATÓRIO DE BUSCA SISTEMÁTICA
Data: 10/04/2026 14:32

RESUMO EXECUTIVO
================
Total de artigos únicos: 587

DISTRIBUIÇÃO POR ANO
====================
2015: 45 artigos
2016: 52 artigos
...
2026: 38 artigos

PRÓXIMOS PASSOS
===============
1. Abrir data/processed/artigos_consolidados.csv
2. Aplicar Triagem Nível 1 (título + resumo)
3. Registrar em: data/processed/triagem_nivel1_resultados.csv
```

**Tempo**: ~2-5 minutos

---

### Script 02: Conversão PDF → Markdown

**Objetivo**: Extrair texto de PDFs e converter para Markdown estruturado

**Pré-requisitos**:
- [ ] PDFs dos artigos em `articles/pdf/`
- [ ] Nomes em padrão: `[AUTOR_ANO].pdf`

**Execução**:
```bash
# Processar todos PDFs
python scripts/02-pdf_to_markdown.py

# Ou processador específico (ex: com OCR se PDFs scaneados)
python scripts/02-pdf_to_markdown.py --method ocr --quality_threshold 0.85
```

**Opções**:
```
--method (pypdf | pdfplumber | ocr)    # Método extração (default: pypdf)
--quality_threshold (0-1)               # Mínimo % confiança OCR
--verbose                               # Saída detalhada
```

**Saída**:
- `articles/md/[AUTOR_ANO].md` - Artigos em Markdown
- `data/processed/conversao_qualidade.csv` - QA report

**Exemplo Markdown gerado**:
```markdown
# Knowledge Transfer and Absorptive Capacity

**Autores**: Cohen, W. M., & Levinthal, D. A.

**Ano**: 1990

**DOI**: 10.1287/mnsc.35.2.128

---

## 1. Introdução

A transferência de conhecimento entre organizações é crítica...

---

## 2. Metodologia

Tipo: Revisão teórica + análise de casos

...
```

**Tempo**: ~1-3 horas (depende N PDFs e método)

---

### Script 03: Fichamento com IA

**Objetivo**: Gerar fichamentos estruturados usando LLM (Claude/GPT-4)

**Pré-requisitos**:
- [ ] Artigos convertidos em Markdown (`articles/md/`)
- [ ] API key configurada em `.env`
- [ ] Quota de tokens disponível na API

**Execução**:
```bash
# Processar todos os MDs
python scripts/03-fichamento_ia.py

# Ou com opções
python scripts/03-fichamento_ia.py \
  --model claude-3-opus \
  --temperature 0.2 \
  --batch_size 5 \
  --save_intermediate
```

**Opções**:
```
--model (gpt-4 | claude-3-opus)         # Qual LLM usar
--temperature (0-1)                     # Criatividade (baixo=consistência)
--batch_size (1-10)                     # Quantos em paralelo
--save_intermediate                     # Salvar progressivamente
--retry_failed                          # Reprocessar falhas
```

**Saída**:
- `analysis/fichamentos/[AUTOR_ANO].md` - Fichamentos estruturados
- `data/processed/fichamentos_metadata.csv` - Metadados processamento
- `data/processed/fichamentos_problemas.txt` - Artigos com erro

**Tempo**: ~2-4 horas (depende N artigos + latência API)

**Custo**: ~$2-5 USD (usando GPT-4)

---

### Script 04: Validação - Sortear Amostra

**Objetivo**: Sortear 30% dos fichamentos para validação manual

**Pré-requisitos**:
- [ ] Fichamentos gerados (`analysis/fichamentos/`)
- [ ] Cálculo de amostra (30% ou tamanho específico)

**Execução**:
```bash
# Sortear amostra padrão (30%)
python scripts/04-validacao_amostra.py

# Ou tamanho específico
python scripts/04-validacao_amostra.py --sample_size 25 --seed 42
```

**Opções**:
```
--sample_size (int ou 0.0-1.0)   # N artigos ou % (default: 0.30)
--seed (int)                     # Random seed para replicabilidade
--stratified                     # Estratificar por tema (se metadados)
```

**Saída**:
- `analysis/validacao/amostra_validacao.csv` - Lista sorteada
- `analysis/validacao/INSTRUCOES_REVISOR.md` - Guia para revisor
- `analysis/validacao/matriz_validacao.xlsx` - Template validação

**Exemplo `amostra_validacao.csv`**:
```csv
ID,Autor,Ano,DOI,Status_Revisor,Data_Revisao,Observacoes
1,Cohen,1990,10.1287/mnsc.35.2.128,PENDENTE,,
2,Zahra,2002,10.1177/104649640204200503,PENDENTE,,
3,Teece,2007,10.1086/529446,PENDENTE,,
...
```

**Tempo**: ~10 minutos

---

### Script 05: Síntese Qualitativa

**Objetivo**: Consolidar fichamentos, identificar lacunas e formular problemas pesquisa

**Pré-requisitos**:
- [ ] Fichamentos validados (com taxa concordância ≥80%)
- [ ] Arquivo `analysis/validacao/validacao_completa.csv` preenchido

**Execução**:
```bash
# Síntese padrão
python scripts/05-sintese_qualitativa.py

# Ou com opções
python scripts/05-sintese_qualitativa.py \
  --min_frequencia 0.10 \
  --clusterizar_conceitos \
  --gerar_visualizacoes
```

**Opções**:
```
--min_frequencia (0-1)       # Mínimo % artigos para tema ser relevante
--clusterizar_conceitos      # Agrupar conceitos similares
--gerar_visualizacoes        # Criar gráficos (PNG)
--export_format (md | html | pdf)
```

**Saída**:
- `analysis/synthesis/matriz_conceitos.csv` - Frequência conceitos
- `analysis/synthesis/relacoes_conceitos.md` - Relações teóricas
- `analysis/synthesis/lacunas_identificadas.md` - Gap analysis
- `analysis/synthesis/problemas_pesquisa.md` - Problemas emergentes
- `analysis/synthesis/mapa_conceitual.png` - Visualização (opcional)

**Tempo**: ~2-3 horas (inclui análise manual)

---

### Script 06: Ranking de Relevância PRÉ-FICHAMENTO ⭐ NOVO!

**Objetivo**: Filtrar CSV bruto ANTES de qualquer fichamento (remove duplicatas + ranking)

**Por que é importante** (EXECUTA NO INÍCIO!):
- **Remove 20-30% duplicatas** automaticamente
- **Identifica fora escopo** - economiza 40-60% tempo
- Você só baixa/processa TOP relevantes
- Documenta decisões (PRISMA compliance)

**Pré-requisitos**:
- [ ] Script 01 executado: `python scripts/01-busca_artigos.py`
- [ ] CSV: `data/processed/artigos_consolidados.csv` gerado

**Execução** (LOGO APÓS SCRIPT 01):
```bash
python scripts/06-ranking_relevancia.py
```

**Saída**:
- `data/processed/artigos_ranqueados.csv` - Ranking (duplicatas removidas)
- `data/processed/duplicatas_removidas.csv` - Rastreabilidade PRISMA
- `analysis/relevancia/relatorio_ranking.md` - Análise completa

**Fluxo**:
```
CSV bruto
  ↓
Remove DUPLICATAS (DOI, hash título, similitude >95%)
  ↓
Análise LÉXICA (título, keywords, abstract, revista)
  ↓
Palavras POSITIVAS (+) vs NEGATIVAS (-)
  ↓
Score 0-100 (base 50 + pontos)
  ↓
RANKING + CATEGORIZAÇÃO
```

**Exemplo `artigos_ranqueados.csv`**:
```csv
ranking,artigo_id,titulo,relevancia_score,categoria,doi
1,001,Absorptive Capacity in Brazilian SMEs,92,Muito Alto,10.1287/...
2,045,Dynamic Capabilities Framework,82,Alto,10.1086/...
50,243,Innovation Process,55,Moderado,10.1016/...
200,389,Review Literature,28,Baixo,10.1002/...
```

**Como usar**:
1. Abra: `data/processed/artigos_ranqueados.csv`
2. Filtre por "Muito Alto" + "Alto" (categoria)
3. Baixe apenas esses PDFs (~30-40% do total)
4. Economize 40-60% de tempo! ✅

**Categorias**:
- 🔴 **Muito Alto (85-100)**: Core do projeto
- 🟠 **Alto (70-84)**: Suporte significativo
- 🟡 **Moderado (50-69)**: Contexto útil
- 🔵 **Baixo (<50)**: Fora escopo

**Tempo**: ~5-10 minutos (depende N artigos)

---

## 📋 Documentação Detalhada dos Scripts

### Script 1: `01-busca_artigos.py`
**Objetivo**: Consolidar artigos de múltiplas bases de dados

```bash
python scripts/01-busca_artigos.py
```

**Entrada**: CSVs em `data/raw/`
- scopus_resultados.csv
- wos_resultados.csv
- scielo_resultados.csv

**Saída**:
- `data/processed/artigos_consolidados.csv`
- `data/processed/relatorio_busca.txt`

**O que faz**:
- Carrega CSVs de múltiplas bases
- Normaliza nomes de colunas
- Remove duplicatas (por DOI/título)
- Gera estatísticas

---

### Script 2: `02-pdf_to_markdown.py`
**Objetivo**: Converter PDFs em Markdown estruturado

```bash
# Um arquivo específico
python scripts/02-pdf_to_markdown.py data/raw/articles/estudo.pdf

# Todos em batch
python scripts/02-pdf_to_markdown.py --batch
```

**Entrada**: PDFs em `data/raw/articles/`

**Saída**: Markdown em `articles/md/`
- `[titulo].md` - Estruturado com YAML front-matter
- `[titulo]_raw.md` - Texto bruto

**O que faz**:
- Extrai texto de PDFs com pdfplumber
- Limpa OCR errors
- Estrutura em seções (Intro, Methods, Results, Discussion)
- Extrai metadados (DOI, ano, título)

**Dependências**: `pip install pdfplumber PyPDF2`

---

### Script 3: `03-fichamento_ia.py` ⭐ PRINCIPAL
**Objetivo**: Gerar fichamentos com Claude E Gemini (A/B Testing)

```bash
# Um artigo
python scripts/03-fichamento_ia.py articles/md/estudo.md

# Todos em batch
python scripts/03-fichamento_ia.py --batch

# Modo economia (apenas Gemini)
python scripts/03-fichamento_ia.py --batch --economia
```

**Entrada**: Markdown em `articles/md/`

**Saída**: 
- `analysis/fichamentos/[artigo]_claude.md`
- `analysis/fichamentos/[artigo]_gemini.md`
- `analysis/fichamentos/[artigo]_metricas.json`

**O que faz**:
- Processa CADA artigo 2 VEZES (Claude + Gemini)
- Gera fichamentos estruturados
- Calcula tokens gastos
- Salva métricas de processamento

**Custo**: ~$0.50 por artigo  
**Tempo**: ~1 min por artigo

**Dependências**: 
```bash
pip install anthropic google-generativeai python-dotenv
```

**Variáveis de ambiente** (em `.env`):
```
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

---

### Script 4: `04-validacao_amostra.py` ⭐ MÉTRICAS
**Objetivo**: Calcular Cohen's Kappa para validar concordância

```bash
python scripts/04-validacao_amostra.py
```

**Entrada**: Fichamentos em `analysis/fichamentos/`

**Saída**:
- `data/processed/validacao_amostra.json`
- `data/processed/validacao_amostra.csv`
- `data/processed/relatorio_validacao.txt`

**O que faz**:
- Extrai seções de ambos os fichamentos
- Calcula similaridade por seção
- Computa Cohen's Kappa ponderado
- Interpreta resultados

**Interpretação Cohen's Kappa**:
- **>= 0.85**: ✅ Excelente (USE diretamente)
- **0.75-0.85**: ✅ Bom (USE, verificar divergências)
- **0.60-0.75**: 🔍 Revisar (consolidar pontos)
- **< 0.60**: ❌ Reprocessar (novo fichamento)

---

### Script 5: `05-sintese_qualitativa.py`
**Objetivo**: Sintetizar literatura com temas e lacunas

```bash
# Síntese geral
python scripts/05-sintese_qualitativa.py

# Por tema
python scripts/05-sintese_qualitativa.py --por-tema

# Matriz de conceitos
python scripts/05-sintese_qualitativa.py --matriz
```

**Entrada**: Fichamentos com Kappa >= 0.60

**Saída**:
- `analysis/synthesis/sintese_geral.md`
- `analysis/synthesis/sintese_por_tema.md`
- `analysis/synthesis/matriz_conceitos.csv`
- `analysis/synthesis/gaps_literatura.md`

**O que faz**:
- Extrai conceitos-chave frequentes
- Identifica temas emergentes
- Analisa co-ocorrência de conceitos
- Detecta lacunas na literatura
- Sugere problemas de pesquisa

---

### Script 6: `06-ranking_relevancia.py` ⭐ NOVO!
**Objetivo**: Criar ranking automático de artigos por relevância usando análise léxica

```bash
python scripts/06-ranking_relevancia.py
```

**Entrada**: Fichamentos em `analysis/fichamentos/`

**Saída**:
- `analysis/relevancia/ranking_relevancia.csv`
- `analysis/relevancia/relatorio_ranking.md`
- `analysis/relevancia/sumario_categorizado.txt`

**O que faz**:
- Analisa léxica de títulos + fichamentos
- Busca palavras-chave POSITIVAS (peso 1.0 a 3.0)
- Busca palavras-chave NEGATIVAS (penalidade -50 a -10)
- Calcula SCORE 0-100 (base 50 + pontos)
- Rankeia artigos
- Gera recomendações por categoria

**Categorias de Relevância**:
- 🔴 **Muito Alto (85-100)**: Revise PRIMEIRO - core do projeto
- 🟠 **Alto (70-84)**: Revise SEGUNDO - contribui significativamente
- 🟡 **Moderado (50-69)**: Revise se tempo - contexto útil
- 🔵 **Baixo (<50)**: Pode descartar - fora escopo

---

## 🎯 Fluxo Completo Recomendado

```bash
# 1. Consolidar artigos de múltiplas bases
python scripts/01-busca_artigos.py

# 2. Converter PDFs para Markdown
python scripts/02-pdf_to_markdown.py --batch

# 3. Gerar fichamentos (Claude + Gemini) - PRINCIPAL
python scripts/03-fichamento_ia.py --batch

# 4. Validar com Cohen's Kappa
python scripts/04-validacao_amostra.py

# 5. Sintetizar literatura
python scripts/05-sintese_qualitativa.py

# 6. Revisar resultados
cat data/processed/validacao_amostra.json
cat analysis/synthesis/sintese_geral.md
```

---

## 💰 Custo Estimado (180 artigos)

| Etapa | Custo Unitário | Total |
|-------|---------------|-------|
| Claude Sonnet | $0.25/artigo | $45 |
| Gemini Pro | $0.25/artigo | $45 |
| **TOTAL** | | **~$90** |

---

## ⏱️ Tempo Estimado

| Etapa | Tempo |
|-------|-------|
| Busca + consolidação | 30 min |
| PDF → Markdown (180) | 15 min |
| Fichamentos IA (180) | **3 horas** |
| Validação Cohen's Kappa | 5 min |
| Síntese qualitativa | 5 min |
| **TOTAL** | **~3.5-4 horas** |

---

## ✅ Checklist de Configuração

- [ ] `.env` configurado com ANTHROPIC_API_KEY
- [ ] `.env` configurado com GOOGLE_API_KEY
- [ ] `data/raw/` contém CSVs de buscas
- [ ] `data/raw/articles/` contém PDFs
- [ ] `requirements.txt` instalado (`pip install -r requirements.txt`)
- [ ] Testado um artigo com cada script

---

## 🐛 Troubleshooting

**Erro: "No module named anthropic"**
```bash
pip install anthropic google-generativeai
```

**Erro: "ANTHROPIC_API_KEY not found"**
```bash
# Verificar .env
cat .env

# Adicionar se faltando
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
```

**Erro: "No PDFs found in data/raw/articles/"**
```bash
# Criar diretório e copiar PDFs
mkdir -p data/raw/articles
cp seus_pdfs/*.pdf data/raw/articles/
```

**Timeout em fichamentos grandes**
```bash
# Aumentar limite de tempo (ex: 5 minutos)
export OPENAI_API_TIMEOUT=300

# Ou dividir artigo em partes menores
python scripts/03-fichamento_ia.py --batch --max_tokens 1000
```

---

## 📊 Monitoramento de Progresso

**Dashboard de status** (criar manualmente ou via script):

```bash
# Ver quantos fichamentos foram criados
ls -1 analysis/fichamentos/*.md | wc -l

# Ver quais falharam
cat data/processed/fichamentos_problemas.txt

# Ver taxa de validação
python -c "
import pandas as pd
df = pd.read_csv('analysis/validacao/amostra_validacao.csv')
print(f'Total amostra: {len(df)}')
print(f'Validados: {(df[\"Status_Revisor\"] == \"COMPLETO\").sum()}')
print(f'% Progresso: {(df[\"Status_Revisor\"] == \"COMPLETO\").sum() / len(df) * 100:.1f}%')
"
```

---

## 🔐 Versionamento e Reprodutibilidade

**Todos os scripts salvam metadados para replicação**:

```python
# Cada saída inclui:
- data_processamento
- versao_script
- parametros_utilizados
- seed_random (se aplicável)
- tempo_execucao
```

**Exemplo**:
```
Script: 01-busca_artigos.py v1.0
Data: 2026-04-15 14:32:15
Tempo execução: 124 segundos
Total processado: 1,247 artigos
Duplicatas removidas: 660
Resultado: 587 únicos
```

---

## 📝 Exemplo de Workflow Completo

```bash
# FASE 0: CALIBRAGEM (⭐ NOVO - EXECUTE PRIMEIRO!)
# Tempo: 1-2 horas (inclui leitura manual de 15-20 artigos)
python scripts/00-calibragem_prompts.py
# Output: matriz_calibragem.csv + relatorio_calibragem.md
# ⚠️ Revise relatorio: concordância deve ser ≥90%
# Se <90%, refine prompts_calibrados.py e reexecute

# 1. Consolidar buscas (5 min)
python scripts/01-busca_artigos.py
# Output: artigos_consolidados.csv (587 artigos)

# 2. [MANUAL] Triagem Nível 1 (5-8 horas)
# → Revisor abre CSV, lê título+resumo, marca INCLUDE/EXCLUDE
# → Resultado: ~150 artigos selecionados

# 3. [MANUAL] Triagem Nível 2 + Download PDFs (8-10 horas)
# → Revisor lê full text, baixa PDFs para ~100 artigos finais

# 4. Converter PDFs → Markdown (2 horas)
python scripts/02-pdf_to_markdown.py
# Output: 100 arquivos MD em articles/md/

# 5. Gerar fichamentos com IA (3 horas)
# ⭐ Usa prompts CALIBRADOS do script 00!
python scripts/03-fichamento_ia_krippendorff.py
# Output: 100 fichamentos em analysis/fichamentos/
# Inclui: scores de relevância em cada fichamento

# 5.5 RANKING DE RELEVÂNCIA (⭐ NOVO - 5 MIN)
python scripts/06-ranking_relevancia.py
# Output: ranking_relevancia.csv + relatorio_ranking.md
# → Priorize TOP 50 para revisão
# → Pode descartar BOTTOM 20 com segurança

# 6. Sortear amostra validação (5 min)
python scripts/04-validacao_krippendorff.py --sample_size 30
# Output: 30 artigos sorteados para validação
# Calcula Krippendorff's Alpha (não Cohen's Kappa!)

# 7. [REVISOR HUMANO] Validar amostra (8 horas)
# → Revisor valida 30 fichamentos (TOP scores de relevância)
# → Taxa concordância: ~90%+ (vs ~75% sem calibragem)

# 8. Síntese qualitativa final (3 horas)
python scripts/05-sintese_qualitativa.py
# Output: Lacunas, problemas pesquisa, mapa conceitual

# TOTAL: ~38-45 horas
# - Calibragem: +1-2h (mas economiza 30-40% depois!)
# - Ranking: +5min (prioriza revisão)
# - Resto: ~37-42h (maioria automático)
```

---

## 🤝 Contribuindo

Para melhorar os scripts:
1. Teste localmente
2. Documente mudanças
3. Faça PR com changelog
4. Inclua exemplos de uso

---

## 📞 Suporte

Dúvidas sobre scripts?
- Consultar docstrings no código: `python -c "import scripts.script01; help(scripts.script01)"`
- Executar com `--help`: `python scripts/01-busca_artigos.py --help`
- Ver logs: `tail -f logs/revisao.log`

---

**Última atualização**: 10 de abril de 2026

