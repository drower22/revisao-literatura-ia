# 📋 ROTEIRO COMPLETO - Passo a Passo Detalhado

## Revisão Sistemática de Literatura sobre Transferência de Conhecimento Externo, Capacidade Absortiva e Competitividade em MPEs Brasileiras

**Data:** 10 de abril de 2026  
**Modelo:** Open Science + PRISMA  
**Status:** 🟢 Pronto para Execução

---

## 📖 Sumário

- [Fase 1: Planejamento](#fase-1-planejamento-) - ✅ COMPLETA
- [Fase 2: Busca e Coleta](#fase-2-busca-e-coleta-) - 🔄 A INICIAR
- [Fase 3: Conversão e Estruturação](#fase-3-conversão-e-estruturação-) - A INICIAR
- [Fase 4: Fichamento Automatizado](#fase-4-fichamento-automatizado-) - A INICIAR
- [Fase 5: Validação Humana](#fase-5-validação-humana-) - A INICIAR
- [Fase 6: Síntese Qualitativa](#fase-6-síntese-qualitativa-) - A INICIAR
- [Fase 7: Redação e Publicação](#fase-7-redação-e-publicação-) - A INICIAR

---

## 🎓 Fase 1: Planejamento ✅

**Status:** ✅ COMPLETA  
**Tempo Estimado:** (Já realizado)

### O que foi feito:

#### 1.1 Definição da Questão de Pesquisa

**Pergunta Principal:**
> Como a transferência de conhecimento externo, mediada pela capacidade absortiva, impacta a competitividade de MPEs brasileiras?

**Subquestões:**
1. Que mecanismos de transferência de conhecimento externo existem?
2. Como as MPEs desenvolvem capacidade absortiva?
3. Qual é o impacto na competitividade?
4. Quais são as lacunas de pesquisa?

#### 1.2 Protocolo PRISMA

✅ Criado: `docs/01-PROTOCOLO-PRISMA.md`

**Componentes:**
- Título e abstract estruturados
- Critérios de inclusão/exclusão definidos
- Estratégia de busca documentada
- Seleção de estudos padronizada
- Extração de dados padronizada

#### 1.3 Framework Conceitual

✅ Criado: `docs/framework/FRAMEWORK-CONCEITUAL.md`

**Teorias Integradas:**
1. Knowledge-Based View (KBV) - Nonaka & Takeuchi
2. Resource-Based View (RBV) - Wernerfelt
3. Absorptive Capacity (AC) - Cohen & Levinthal
4. Dynamic Capabilities (DC) - Teece et al.
5. Organizational Learning (OL) - Argyris & Schön
6. Innovation Systems (IS) - Freeman & Moen
7. International Trade (IT) - Porter & Krugman

#### 1.4 Critérios de Inclusão/Exclusão

✅ Criado: `docs/02-CRITERIOS-INCLUSAO.md`

**Inclusão:**
- ✅ Publicados entre 2010-2026
- ✅ Revisados por pares
- ✅ Inglês ou Português
- ✅ Focam em conhecimento, inovação ou competitividade
- ✅ Incluem MPE/PME/SME

**Exclusão:**
- ❌ Apenas teóricos sem evidências
- ❌ Foco exclusivo em grandes empresas
- ❌ Não revisados por pares
- ❌ Outros idiomas

#### 1.5 Palavras-chave de Busca

✅ Criado: `docs/03-PALAVRAS-CHAVE.md`

**Termos Principais:**
```
(knowledge transfer OR knowledge management OR knowledge sharing)
AND
(absorptive capacity OR ACAP)
AND
(SME OR SMEs OR "small and medium" OR MPE)
AND
(competitiveness OR competitive advantage OR performance)
```

**Variações para Português:**
```
(transferência conhecimento OR gestão conhecimento)
AND
(capacidade absortiva)
AND
(MPE OR "pequena e média")
AND
(competitividade OR vantagem competitiva)
```

---

## 🔍 Fase 2: Busca e Coleta 🔄

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 2-3 horas  
**Executor:** Python script `01-busca_artigos.py`

### Passo 2.1: Preparar Credenciais das Bases

**Bases de Dados a Usar:**

1. **Scopus** (maior coverage)
   - Credencial: API key ou acesso institucional
   - Coverage: Multidisciplinar
   - Período: 1960-presente

2. **Web of Science** (qualidade alta)
   - Credencial: Acesso institucional
   - Coverage: Pesquisa pura
   - Período: 1900-presente

3. **Google Scholar** (cobertura ampla)
   - Credencial: Nenhuma necessária
   - Coverage: Muito amplo (pode ter ruído)
   - Período: Sem limite

4. **DOAJ** (open access)
   - Credencial: Nenhuma
   - Coverage: Periódicos open access
   - Período: Variado

5. **ResearchGate / Academia.edu** (cinza)
   - Credencial: Nenhuma
   - Coverage: Incluir preprints
   - Período: Variado

### Passo 2.2: Executar Buscas

```bash
# Ative o ambiente
source venv/bin/activate

# Execute o script de busca
python scripts/01-busca_artigos.py
```

**O que o script faz:**

```python
1. Conecta em cada base de dados
2. Executa queries de busca (com variações)
3. Recupera metadados (título, autores, abstract, ano, DOI)
4. Salva resultados em CSV (data/raw/)
5. Faz deduplicação automática
6. Gera relatório (data/raw/busca_relatorio.txt)
```

**Saída esperada:**

```
data/raw/
├── scopus_results.csv (245 artigos)
├── wos_results.csv (189 artigos)
├── google_scholar_results.csv (412 artigos)
├── doaj_results.csv (67 artigos)
├── consolidated_searches.csv (434 artigos, após dedup)
└── busca_relatorio.txt (relatório detalhado)
```

### Passo 2.3: Revisar Relatório de Busca

```bash
cat data/raw/busca_relatorio.txt
```

**Conteúdo esperado:**
```
============ RELATÓRIO DE BUSCA ============
Data: 2026-04-10
Pesquisador: [Seu Nome]

1. SCOPUS
   Query: (knowledge transfer OR knowledge management)...
   Resultados: 245
   Período: 2010-2026

2. WEB OF SCIENCE
   Query: TS=(knowledge transfer OR knowledge management)...
   Resultados: 189
   Período: 2010-2026

3. GOOGLE SCHOLAR
   Query: "knowledge transfer" AND "absorptive capacity"...
   Resultados: 412
   Período: 2010-2026

4. DOAJ
   Query: knowledge transfer absorptive capacity SME
   Resultados: 67
   Período: 2010-2026

5. RESUMO
   Total antes deduplicação: 913
   Total após deduplicação: 434
   Duplicatas removidas: 479
   
   Por ano:
   2010-2014: 89 artigos
   2015-2019: 156 artigos
   2020-2026: 189 artigos
```

### Passo 2.4: Triagem Inicial (Título + Abstract)

**Arquivo:** `analysis/validacao/TRIAGEM-INICIAL.md`

Para cada artigo em `consolidated_searches.csv`, avalie:

```markdown
| Título | Autores | Ano | Incluir? | Motivo |
|--------|---------|-----|----------|--------|
| Knowledge Transfer... | Smith et al. | 2022 | SIM | Trata AC em SMEs |
| Big Data Analytics... | Jones, 2023 | 2023 | NÃO | Foco em grandes empresas |
```

**Critério de Inclusão Rápido:**

- ✅ Inclua se: Trata conhecimento/inovação/competitividade + contexto de MPE/PME
- ❌ Exclua se: Apenas para grandes empresas OU sem relação com MPE

**Resultado esperado:**
- De 434 artigos → ~150-200 inclusos na triagem (35-45%)
- Documente em: `data/processed/triagem_inicial_resultados.csv`

### Passo 2.5: Download de Artigos

**Para artigos inclusos:**

1. Se tem DOI → Acesse via institucional ou ResearchGate
2. Se open access → Download direto
3. Se indisponível → Solicitar via ResearchGate ou contatar autor

**Salve em:**
```
articles/pdf/
├── 2022_smith_et_al_knowledge_transfer.pdf
├── 2023_jones_innovation_smes.pdf
└── ...
```

**Dica:** Use uma ferramenta como Zotero ou Mendeley para gerenciar PDFs

---

## 📄 Fase 3: Conversão e Estruturação 🔄

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 2-4 horas (depende quantidade)  
**Executor:** Python script `02-pdf_to_markdown.py`

### Passo 3.1: Verificar PDFs

```bash
ls -la articles/pdf/ | wc -l
```

**Esperado:** ~150-200 artigos em PDF

### Passo 3.2: Converter PDFs para Markdown

```bash
python scripts/02-pdf_to_markdown.py
```

**O que o script faz:**

```python
1. Lê cada PDF em articles/pdf/
2. Extrai texto usando pdfplumber/PyPDF2
3. Estrutura em Markdown:
   - Título
   - Autores
   - Abstract
   - Introdução
   - Metodologia
   - Resultados
   - Conclusão
   - Referências
4. Salva em articles/md/
5. Cria índice: articles/md/INDEX.md
```

**Saída esperada:**

```
articles/md/
├── 2022_smith_et_al_knowledge_transfer.md
├── 2023_jones_innovation_smes.md
├── INDEX.md
└── conversion_report.txt
```

**Exemplo de arquivo convertido:**

```markdown
# Knowledge Transfer in SMEs: A Systematic Review

## Metadados
- **Autores:** Smith, J.; Johnson, A.
- **Ano:** 2022
- **DOI:** 10.1234/example
- **Periódico:** Journal of Small Business
- **Tipo:** Artigo Revisado por Pares
- **Acesso:** Open Access

## Abstract
Este artigo examina como a transferência de conhecimento afeta...

## 1. Introdução
A transferência de conhecimento é fundamental para...

## 2. Metodologia
Realizamos uma revisão sistemática de 150 artigos...

## 3. Resultados Principais
- Identificamos 5 mecanismos principais
- Capacidade absortiva é crítica
- Contexto institucional importa

## 4. Conclusões
Concluímos que...

## Referências
[1] Cohen, W. M., & Levinthal, D. A. (1990)...
```

### Passo 3.3: Revisar Conversão

```bash
# Verificar alguns arquivos
head -50 articles/md/2022_smith_et_al_knowledge_transfer.md

# Ver relatório
cat articles/md/conversion_report.txt
```

**Problemas Comuns e Soluções:**

| Problema | Causa | Solução |
|----------|-------|--------|
| Texto cortado | PDF com imagens | Extrair OCR |
| Formatação quebrada | PDF complexo | Ajuste manual |
| Caracteres estranhos | Encoding | Converter UTF-8 |
| Referências não aparecem | PDF escaneado | Usar OCR |

### Passo 3.4: Ajustes Manuais (se necessário)

Para PDFs problemáticos:

```bash
# Use ferramenta como Tesseract para OCR
tesseract input.pdf output -l por+eng

# Depois converta para Markdown manualmente
```

**Resultado esperado:**
- 150-200 arquivos Markdown bem estruturados em `articles/md/`
- Índice completo em `articles/md/INDEX.md`
- Relatório de conversão em `articles/md/conversion_report.txt`

---

## 🤖 Fase 4: Fichamento Automatizado 🔄

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 3-6 horas  
**Executor:** Python script `03-fichamento_ia.py`  
**Ferramenta:** OpenAI API (GPT-4) ou Claude

### Passo 4.1: Configurar API

**Arquivo:** `scripts/utils/config.py`

```python
# Escolha um:
API_PROVIDER = "openai"  # ou "anthropic"
API_KEY = "sk-..."  # Sua chave
MODEL = "gpt-4"  # ou "claude-3-opus"
```

**Como obter chaves:**

**OpenAI:**
1. Vá para https://platform.openai.com/
2. Sign up → Crie conta
3. API keys → Create new secret key
4. Salve em variável de ambiente: `export OPENAI_API_KEY="..."`

**Claude (Anthropic):**
1. Vá para https://console.anthropic.com/
2. Sign up → Crie conta
3. API keys → Generate new key
4. Salve: `export ANTHROPIC_API_KEY="..."`

### Passo 4.2: Preparar Prompts de Fichamento

**Arquivo:** `scripts/utils/prompts.py`

```python
FICHAMENTO_PROMPT = """
Faça um fichamento completo do seguinte artigo:

{article_content}

Siga este template em Markdown:

# Fichamento: [TÍTULO]

## 1. Referência Completa
[Autores], [Ano]. [Título]. [Periódico], [Vol(Issue)], [Pages]. DOI: [DOI]

## 2. Questão de Pesquisa / Objetivo
[Qual era a pergunta de pesquisa principal?]

## 3. Método de Pesquisa
[Que metodologia foi usada? Quantitativa/Qualitativa? Amostra?]

## 4. Conceitos-chave
[Principais teorias e construtos estudados]

## 5. Achados Principais
[Resultados e descobertas mais importantes]

## 6. Implicações Práticas
[Como os resultados podem ser aplicados?]

## 7. Limitações
[Quais foram as limitações do estudo?]

## 8. Lacunas Identificadas
[Que questões ficaram em aberto?]

## 9. Relevância para Minha Pesquisa
[Como este artigo contribui para minha dissertação?]

## 10. Referências-chave Citadas
[5 referências mais importantes citadas no artigo]

---
Fichamento realizado: [DATA E HORA]
"""
```

### Passo 4.3: Executar Fichamento

```bash
python scripts/03-fichamento_ia.py
```

**O que o script faz:**

```python
1. Lê todos os PDFs em articles/md/
2. Para cada arquivo:
   a. Extrai conteúdo
   b. Envia para IA com prompt
   c. Recebe fichamento estruturado
   d. Valida formato (é válido markdown?)
   e. Salva em analysis/fichamentos/
3. Gera resumo: analysis/fichamentos/RESUMO_FICHAMENTOS.md
4. Cria mapping: analysis/fichamentos/FICHAMENTOS_INDEX.csv
```

**Saída esperada:**

```
analysis/fichamentos/
├── 2022_smith_et_al_knowledge_transfer.md (fichamento)
├── 2023_jones_innovation_smes.md
├── FICHAMENTOS_INDEX.csv (índice com metadados)
├── RESUMO_FICHAMENTOS.md (resumo executivo)
└── fichamento_relatorio.txt
```

**Exemplo de fichamento IA:**

```markdown
# Fichamento: Knowledge Transfer in SMEs

## 1. Referência Completa
Smith, J., & Johnson, A. (2022). Knowledge Transfer in SMEs: 
A Systematic Review. Journal of Small Business, 45(3), 234-256. 
DOI: 10.1234/example

## 2. Questão de Pesquisa
Como a capacidade absortiva mediates o impacto da transferência 
de conhecimento externo na competitividade de PMEs?

## 3. Método de Pesquisa
Revisão sistemática de 150 artigos publicados entre 2010-2020,
com análise qualitativa de 45 estudos empíricos selecionados.
Abordagem: Mixed methods (síntese qualitativa + meta-análise).

## 4. Conceitos-chave
- Transferência de conhecimento externo
- Capacidade absortiva (realização, transformação, exploração)
- Competitividade e vantagem competitiva
- PMEs e contexto brasileiro

## 5. Achados Principais
- Identificados 5 mecanismos principais de transferência
- Capacidade absortiva modera relação com performance
- Contexto institucional (regulação, políticas) é crítico
- Falta pesquisa em contexto latino-americano

## 6. Implicações Práticas
- Políticas devem focar desenvolvimento de AC em PMEs
- Gerentes precisam investir em absorção ativa
- Colaborações universidade-indústria são efetivas

## 7. Limitações
- Maioria dos estudos em países desenvolvidos
- Foco em manufatura, pouca análise em serviços
- Causalidade nem sempre estabelecida

## 8. Lacunas Identificadas
- Pouca pesquisa em Brasil e América Latina
- Dinâmica temporal não bem compreendida
- Papel do digital/tecnologia ainda emergente

## 9. Relevância para Minha Pesquisa
Este é um artigo fundamental que:
- Define claramente AC e seus componentes
- Mostra importância em contexto de MPEs
- Identifica lacuna exatamente em pesquisa brasileira
→ Será referência-chave na minha dissertação

## 10. Referências-chave Citadas
1. Cohen & Levinthal (1990) - AC pioneer
2. Zahra & George (2002) - AC framework
3. Lane et al. (2006) - AC in context
4. Volberda et al. (2010) - DC perspective
5. Nonaka & Takeuchi (1995) - Knowledge creation

---
Fichamento realizado: 2026-04-10 14:32:15
```

### Passo 4.4: Validar Fichamentos

```bash
# Verificar alguns fichamentos
head -100 analysis/fichamentos/2022_smith_et_al_knowledge_transfer.md

# Ver relatório
cat analysis/fichamentos/fichamento_relatorio.txt
```

**Relatório esperado mostra:**
- ✅ Total de fichamentos criados
- ✅ Taxa de sucesso (%)
- ⚠️ Avisos (fichamentos muito curtos)
- ❌ Erros (artigos que falharam)

**Resultado esperado:**
- 150-200 fichamentos estruturados em Markdown
- Todos com 10 seções padronizadas
- Taxa de sucesso: 95%+
- Prontos para validação humana

---

## 👤 Fase 5: Validação Humana 🔄

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 8-12 horas (10-20% da amostra)  
**Executor:** Você (pesquisador/orientador)

### Passo 5.1: Selecionar Amostra de Validação

**Arquivo:** `scripts/04-validacao_amostra.py`

```bash
python scripts/04-validacao_amostra.py
```

**O que faz:**
- Seleciona aleatoriamente 10-20% dos fichamentos
- Agrupa por tema (diversidade)
- Cria lista de validação: `analysis/validacao/AMOSTRA-VALIDACAO.md`

**Saída:**

```
analysis/validacao/
├── AMOSTRA-VALIDACAO.md (lista de 30 artigos para validar)
├── CHECKLIST-VALIDACAO.md (formulário)
└── VALIDACOES-COMPLETAS.md (resultados)
```

**Exemplo de AMOSTRA-VALIDACAO.md:**

```markdown
# Amostra de Validação Humana (n=30)

**Total de fichamentos:** 180  
**Amostra:** 30 (16.7%)  
**Método:** Seleção aleatória estratificada por tema

## Artigos para Validar

### 1. Tema: Capacidade Absortiva (10 artigos)
- [ ] 2022_smith_et_al_knowledge_transfer.md
- [ ] 2021_jones_ac_performance.md
- [ ] 2020_silva_absorptive_capacity.md
- ...

### 2. Tema: Transferência de Conhecimento (10 artigos)
- [ ] 2023_santos_kt_mechanisms.md
- [ ] 2022_oliveira_external_knowledge.md
- ...

### 3. Tema: MPEs/PMEs Brasileiras (10 artigos)
- [ ] 2023_costa_mpes_innovation.md
- [ ] 2022_ferreira_competitividade_pme.md
- ...
```

### Passo 5.2: Ler Artigo Original + Fichamento IA

**Para cada artigo na amostra:**

1. Leia o artigo original (PDF ou Markdown em `articles/md/`)
2. Leia o fichamento gerado pela IA em `analysis/fichamentos/`
3. Compare os dois

### Passo 5.3: Validar Usando Checklist

**Arquivo:** `analysis/validacao/CHECKLIST-VALIDACAO.md`

```markdown
# Checklist de Validação de Fichamento

**Artigo:** [TÍTULO]  
**Validador:** [SEU NOME]  
**Data:** [DATA]

## Seção 1: Referência Completa
- [ ] Autores completos e corretos
- [ ] Ano correto
- [ ] Título exato
- [ ] Periódico/Conferência correto
- [ ] DOI presente (se aplicável)

**Observações:** [Se algum erro, descreva]

## Seção 2: Questão de Pesquisa
- [ ] Questão claramente identificada
- [ ] Compatível com o texto do artigo
- [ ] Objetivos bem descritos

**Observações:**

## Seção 3: Método
- [ ] Método descrito corretamente
- [ ] Amostra (n) reportada
- [ ] Abordagem (qual/quant/mixed) correta
- [ ] Período de análise correto

**Observações:**

## Seção 4: Conceitos-chave
- [ ] Principais teorias identificadas
- [ ] Construtos principais listados
- [ ] Alinhado com framework conceitual

**Observações:**

## Seção 5: Achados Principais
- [ ] Principais resultados inclusos
- [ ] Resultados refletem o artigo
- [ ] Sem omissões críticas

**Observações:**

## Seção 6: Implicações
- [ ] Implicações práticas corretas
- [ ] Implicações teóricas mencionadas

**Observações:**

## Seção 7: Limitações
- [ ] Limitações do estudo reportadas
- [ ] Realistas e bem descritas

**Observações:**

## Seção 8: Lacunas
- [ ] Lacunas de pesquisa identificadas
- [ ] Claras e bem justificadas

**Observações:**

## Seção 9: Relevância
- [ ] Conexão com pesquisa clara
- [ ] Bem justificada

**Observações:**

## Seção 10: Referências
- [ ] Pelo menos 5 referências
- [ ] Referências principais citadas
- [ ] Precisas

**Observações:**

## Avaliação Geral

**Qualidade do fichamento:**
- [ ] Excelente (sem alterações necessárias)
- [ ] Bom (ajustes menores)
- [ ] Aceitável (ajustes moderados)
- [ ] Fraco (precisa refazer)

**Comentários gerais:**
[Descreva qualidade geral, pontos fortes, fracos]

---

**Validador:** [ASSINATURA]  
**Data:** [DATA]
```

### Passo 5.4: Documentar Validações

Para cada fichamento validado, preencha:

**Arquivo:** `analysis/validacao/VALIDACOES-COMPLETAS.md`

```markdown
# Resultados de Validação

**Data:** 2026-04-15  
**Validador:** Pesquisador  
**Total validado:** 30 fichamentos  
**Taxa de aprovação:** 90%

## Resumo por Artigo

| Artigo | Status | Ajustes | Notas |
|--------|--------|---------|-------|
| 2022_smith_et_al.md | ✅ Aprovado | Nenhum | Excelente |
| 2021_jones_ac.md | ⚠️ Ajustes | Menor | Faltou 1 referência |
| 2020_silva_ac.md | ❌ Rejeitar | Maior | Refazer completamente |

## Feedback Agregado

### Pontos Positivos
- ✅ Referências bem estruturadas
- ✅ Questões de pesquisa claras
- ✅ Métodos bem descritos

### Pontos a Melhorar
- ⚠️ Lacunas nem sempre claras
- ⚠️ Relevância para pesquisa às vezes vaga
- ⚠️ Alguns fichamentos muito resumidos

## Ações

1. [ ] Refazer fichamentos com status "Rejeitar"
2. [ ] Ajustar prompts para melhorar
3. [ ] Validar novamente após ajustes
4. [ ] Aproveitar amostra aprovada
```

### Passo 5.5: Fazer Ajustes

**Se qualidade geral < 80%:**

1. Melhore o prompt em `scripts/utils/prompts.py`
2. Execute novamente: `python scripts/03-fichamento_ia.py`
3. Valide amostra novamente

**Se qualidade geral ≥ 80%:**

- ✅ Aprove e use todos os fichamentos para síntese

---

## 📊 Fase 6: Síntese Qualitativa 🔄

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 4-6 horas  
**Executor:** Python script `05-sintese_qualitativa.py`

### Passo 6.1: Preparar Análise

```bash
python scripts/05-sintese_qualitativa.py
```

**O que faz:**
1. Lê todos os 180 fichamentos
2. Extrai informações principais
3. Agrupa por tema
4. Cria matriz de síntese
5. Identifica tendências

### Passo 6.2: Revisar Matriz Temática

**Arquivo:** `analysis/synthesis/MATRIZ-TEMATICA.md`

```markdown
# Matriz Temática - Síntese Qualitativa

## 1. Transferência de Conhecimento Externo

### Mecanismos Identificados
| Mecanismo | Autor(es) | Ano | Contexto | N Estudos |
|-----------|-----------|-----|---------|-----------|
| Colaboração Universal | Smith et al. | 2022 | Global | 45 |
| Redes de Inovação | Jones | 2021 | Europa | 32 |
| Aquisições | Silva | 2020 | Ásia | 28 |
| Parcerias | Costa | 2019 | Brasil | 8 |

### Tendências Temporais
- 2010-2014: Foco em universidade-indústria
- 2015-2019: Diversificação de mecanismos
- 2020-2026: Ênfase em digital e redes

## 2. Capacidade Absortiva

### Dimensões
| Dimensão | Definição | Autores | Criticidade |
|----------|-----------|---------|------------|
| Realização | Capacidade de identificar | Cohen & Levinthal | Alta |
| Transformação | Assimilação e adaptação | Zahra & George | Alta |
| Exploração | Uso e aplicação | Teece | Alta |

### Preditores de AC
- [ ] R&D investment
- [ ] Educação dos funcionários
- [ ] Experiência prévia
- [ ] Estrutura organizacional

## 3. Competitividade em MPEs

### Fatores Críticos
1. Capacidade absortiva (80% dos estudos)
2. Inovação (76%)
3. Recursos humanos (65%)
4. Acesso a conhecimento (60%)

### Contexto Brasileiro
- Estudos encontrados: 12
- Foco principal: Manufatura
- Lacuna: Serviços, comércio digital
```

### Passo 6.3: Identificar Lacunas de Pesquisa

**Arquivo:** `analysis/synthesis/LACUNAS-PESQUISA.md`

```markdown
# Lacunas de Pesquisa Identificadas

## Lacunas Geográficas

### Crítica - Contexto Brasileiro/Latino-americano
- **Problema:** Maioria dos estudos em países desenvolvidos
- **Encontrado:** 12 estudos em Brasil
- **Encontrado:** 3 estudos em América Latina
- **Implicação:** Modelos podem não ser transferíveis
- **Oportunidade:** Pesquisa em contexto brasileiro é urgente

## Lacunas Teóricas

### Integradora - Cadeia Causal
- **Problema:** Relação entre conhecimento → AC → competitividade não bem testada
- **Encontrado:** Maioria testa relações isoladas
- **Faltando:** Estudos com 3+ variáveis integradas
- **Oportunidade:** Testar modelo integrativo em Brasil

### Dinâmica - Evolução Temporal
- **Problema:** Dinâmica de AC ao longo do tempo pouco explorada
- **Encontrado:** Maioria são estudos transversais
- **Faltando:** Estudos longitudinais
- **Oportunidade:** Acompanhar desenvolvido de AC em 3+ anos

## Lacunas Metodológicas

### Qualitativa em Contexto Específico
- **Problema:** Pesquisa qualitativa em MPEs brasileiras escassa
- **Encontrado:** 0 estudos de caso em profundidade em Brasil
- **Faltando:** Etnografias, estudos de caso detalhados
- **Oportunidade:** Entender mecanismos em contexto real brasileiro

### Exploração de Tecnologia Digital
- **Problema:** Impacto da transformação digital em AC para MPEs não estudado
- **Encontrado:** 3 estudos mencionam tecnologia
- **Faltando:** Estudos focused em digital
- **Oportunidade:** Pesquisa sobre digital + AC + competitividade

## Lacunas Setoriais

| Setor | Estudos | Gap | Oportunidade |
|-------|---------|-----|-------------|
| Manufatura | 120 | Bem coberto | Menos urgente |
| Serviços | 35 | Grande | 🔴 ALTA |
| Comércio | 15 | Muito grande | 🔴 CRÍTICA |
| Agro | 8 | Enorme | 🔴 CRÍTICA |
| Tecnologia | 22 | Médio | 🟡 MÉDIA |
```

### Passo 6.4: Gerar Proposições de Pesquisa

**Arquivo:** `analysis/synthesis/PROPOSICOES-FINAIS.md`

Com base nas lacunas, formule proposições testáveis:

```markdown
# Proposições de Pesquisa - Baseadas em Revisão

## P1: Modelo Integrativo
**Proposição:** Em MPEs brasileiras, transferência de conhecimento externo 
afeta competitividade MEDIADA por capacidade absortiva.

**Justificativa:** Modelo testado em países desenvolvidos, nunca em Brasil.
**Tipo de Pesquisa:** Quantitativa (SEM) ou Qualitativa (estudo de caso)
**Relevância:** CRÍTICA

## P2: Moderação de Contexto Institucional
**Proposição:** Políticas governamentais e regulação MODERATEM a relação entre 
AC e competitividade em MPEs.

**Justificativa:** Contexto institucional negligenciado em literatura
**Tipo de Pesquisa:** Qualitativa comparative (casos em diferentes contextos)
**Relevância:** ALTA

## P3: Dinâmica Temporal de AC
**Proposição:** Capacidade absortiva evolui ao longo do tempo, passando de 
realização → transformação → exploração (em 3-5 anos).

**Justificativa:** Dinâmica temporal não bem compreendida
**Tipo de Pesquisa:** Longitudinal (painel em 3-5 anos)
**Relevância:** MÉDIA-ALTA

## P4: Mediação de Tecnologia Digital
**Proposição:** Tecnologia digital amplifica os efeitos da capacidade 
absortiva em serviços digitais.

**Justificativa:** Era digital não contemplada adequadamente
**Tipo de Pesquisa:** Estudo de caso comparativo
**Relevância:** ALTA

## P5: Mecanismos em MPEs de Serviços
**Proposição:** Em MPEs de serviços, redes informais são os principais 
mecanismos de transferência de conhecimento externo.

**Justificativa:** Setor de serviços pouco estudado
**Tipo de Pesquisa:** Etnografia / Estudo qualitativo profundo
**Relevância:** ALTA
```

---

## ✍️ Fase 7: Redação e Publicação ✍️

**Status:** 🔄 A INICIAR  
**Tempo Estimado:** 4-8 semanas  
**Executor:** Você + Orientador

### Passo 7.1: Estrutura do Artigo

```markdown
# Título
Transferência de Conhecimento Externo e Capacidade Absortiva em MPEs 
Brasileiras: Uma Revisão Sistemática de Literatura

## Abstract (200-250 palavras)
[Contexto → Objetivo → Método → Resultados → Conclusões]

## 1. Introdução
- Contexto e relevância
- Lacuna identificada
- Objetivo e questão de pesquisa
- Contribuições esperadas

## 2. Framework Conceitual
- Teorias principais (KBV, RBV, AC, DC)
- Construtos chave
- Proposições integradas

## 3. Metodologia
- Protocolo PRISMA
- Critérios inclusão/exclusão
- Estratégia de busca
- Seleção e extração de dados
- Validação (qualidade)

## 4. Resultados
- Síntese quantitativa (número de estudos, tendências)
- Síntese qualitativa (temas, mecanismos)
- Matriz temática
- Análise por contexto

## 5. Discussão
- Análise das descobertas
- Comparação com literatura anterior
- Implicações práticas
- Implicações teóricas

## 6. Lacunas de Pesquisa e Agenda Futura
- Lacunas identificadas
- Proposições de pesquisa
- Prioridades

## 7. Conclusões
- Síntese dos achados
- Relevância para Brasil
- Chamado para ação

## Referências (100+)
[Baseadas nos 180 artigos analisados]
```

### Passo 7.2: Escrever cada Seção

**Fonte:** Resultados em `analysis/synthesis/`

**Para cada seção:**
1. Copie estrutura relevante
2. Cite artigos analisados
3. Use figuras/tabelas de síntese
4. Integre com seu conhecimento

### Passo 7.3: Validar com Orientador

- [ ] Leia com orientador
- [ ] Receba feedback
- [ ] Faça revisões
- [ ] Repita até aprovação

### Passo 7.4: Submeter para Publicação

**Periódicos Alvo:**

1. **Topo (Qualis A1-A2):**
   - Strategic Management Journal
   - Academy of Management Review
   - Journal of Management

2. **Médio (Qualis B1-B2):**
   - Journal of Small Business Management
   - R&D Management
   - Technovation

3. **Brasil (Qualis A-B):**
   - Revista de Administração Contemporânea
   - O&S - Organização & Sociedade
   - RAE - Revista de Administração de Empresas

**Passos:**
1. [ ] Escolha periódico
2. [ ] Leia instruções para autores
3. [ ] Prepare documento (template)
4. [ ] Escreva cover letter
5. [ ] Submeta via plataforma
6. [ ] Aguarde revisão (3-6 meses)

---

## 📈 Cronograma Sugerido

```
Semana 1-2: Fase 2 (Busca e Coleta)
Semana 3: Fase 3 (Conversão PDF→MD)
Semana 4: Fase 4 (Fichamento IA)
Semana 5: Fase 5 (Validação Humana)
Semana 6: Fase 6 (Síntese)
Semana 7-10: Fase 7 (Redação)
Semana 11-12: Submissão + Aguarde
```

---

## ✅ Checklist Final

- [ ] Fase 1: Planejamento ✅
- [ ] Fase 2: Busca (artigos em data/raw/)
- [ ] Fase 3: Conversão (markdown em articles/md/)
- [ ] Fase 4: Fichamento (fichamentos em analysis/fichamentos/)
- [ ] Fase 5: Validação (amostra 10-20% validada)
- [ ] Fase 6: Síntese (matriz e lacunas em analysis/synthesis/)
- [ ] Fase 7: Artigo (rascunho pronto para orientador)

---

## 🚀 Próximos Passos

1. Execute: `python scripts/01-busca_artigos.py`
2. Aguarde resultados em `data/raw/`
3. Proceda para Fase 3 quando tiver artigos

**Boa sorte!** 🎉

---

*Documento criado: 10 de abril de 2026*  
*Versão: 1.0*  
*Status: Pronto para Execução*
