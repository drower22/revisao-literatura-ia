# 🎯 ROTEIRO EXECUTIVO - Passo a Passo

**Versão**: 1.0  
**Data**: 10 de abril de 2026  
**Objetivo**: Guia prático para executar cada fase da revisão sistemática

---

## ✅ FASE 1: Planejamento e Protocolo (Semana 1)

### Tarefa 1.1: Registrar Protocolo PRISMA

**O que fazer:**
- [ ] Abrir arquivo `docs/01-PROTOCOLO-PRISMA.md`
- [ ] Preencher todos os campos obrigatórios do PRISMA 2020
- [ ] Documentar objetivos, critérios de inclusão/exclusão, método de análise
- [ ] **IMPORTANTE**: Não modificar protocolo após iniciar a busca (ou registrar mudanças)

**Saída esperada:**
- ✅ Arquivo `docs/01-PROTOCOLO-PRISMA.md` completo e assinado
- ✅ Data de registro do protocolo (importante para transparência)

**Tempo estimado**: 2-3 horas

---

### Tarefa 1.2: Definir Critérios de Inclusão/Exclusão

**O que fazer:**
- [ ] Abrir `docs/02-CRITERIOS-INCLUSAO.md`
- [ ] Documentar explicitamente cada critério
- [ ] Criar exemplos de artigos que INCLUEM e que EXCLUEM
- [ ] Definir: período (2015-2026), idiomas (PT/EN/ES), tipo de documento

**Critérios mínimos:**

```
INCLUSÃO:
✅ Peer-reviewed (artigos, proceedings de conferências indexadas)
✅ Anos: 2015-2026
✅ Idiomas: Português, Inglês, Espanhol
✅ Temática: Transferência conhecimento OU Absorptive Capacity OU Competitividade
✅ Contexto: PME/MPE/SME (qualquer país, mas com análise Brasil)
✅ Disponibilidade: Full text acesso aberto ou via CAPES

EXCLUSÃO:
❌ Estudos puramente teóricos sem dados empíricos
❌ Comentários, editoriais, resenhas
❌ Artigos não peer-reviewed
❌ Duplicatas
❌ Artigos em idiomas não especificados
❌ Estudos sobre grandes empresas (>500 funcionários)
```

**Saída esperada:**
- ✅ Arquivo `docs/02-CRITERIOS-INCLUSAO.md` detalhado

**Tempo estimado**: 1-2 horas

---

### Tarefa 1.3: Estratégia de Busca

**O que fazer:**
- [ ] Abrir `docs/03-PALAVRAS-CHAVE.md`
- [ ] Definir palavras-chave por base de dados
- [ ] Testar buscas piloto (10 artigos por base)
- [ ] Documentar operadores booleanos

**Palavras-chave principais:**

```
Português:
- "transferência de conhecimento" + PME/MPE
- "capacidade absortiva" + "pequenas empresas"
- "absorção de conhecimento" + competitividade
- "inovação" + "pequenas e médias empresas"

Inglês:
- "knowledge transfer" + SME/PME
- "absorptive capacity" + competitiveness
- "external knowledge" + innovation
- "small medium enterprises" + learning

Combinações booleanas:
("knowledge transfer" OR "knowledge absorption" OR "absorptive capacity")
AND
("SME" OR "PME" OR "small and medium" OR "small medium enterprise")
AND
("competitiveness" OR "competitive advantage" OR "innovation performance")
```

**Saída esperada:**
- ✅ Arquivo `docs/03-PALAVRAS-CHAVE.md` com strings de busca finais
- ✅ Resultado piloto mostrando viabilidade

**Tempo estimado**: 2-3 horas

---

### ✓ Checklist Fase 1

```
[ ] PROTOCOLO-PRISMA.md preenchido
[ ] CRITERIOS-INCLUSAO.md documentado
[ ] PALAVRAS-CHAVE.md finalizado
[ ] Revisor aprova protocolo (se aplicável)
[ ] Repositório Git criado e commits iniciais feitos
```

**Saída consolidada**: ✅ Protocolo pronto para busca

---

## ✅ FASE 2: Busca Sistemática (Semanas 2-3)

### Tarefa 2.1: Executar Buscas em Bases

**O que fazer:**

1. **Scopus**
   ```bash
   # Acesar: https://www.scopus.com
   # Usar string: ("knowledge transfer" OR "absorptive capacity") 
   #              AND ("SME" OR "small medium") 
   #              AND (2015-2026)
   # Exportar: CSV com metadados
   # Salvar em: data/raw/scopus_resultados.csv
   ```

2. **Web of Science**
   ```bash
   # Acessar: https://www.webofscience.com
   # Mesma estratégia de busca
   # Exportar completo (título, resumo, autores, ano)
   # Salvar em: data/raw/wos_resultados.csv
   ```

3. **SciELO**
   ```bash
   # Acessar: https://www.scielo.br
   # Busca por português: "capacidade absortiva"
   # Exportar: CSV
   # Salvar em: data/raw/scielo_resultados.csv
   ```

4. **Google Scholar**
   ```bash
   # Acessar: https://scholar.google.com
   # Busca: "knowledge transfer" SME Brazil
   # Coletar primeiros 100 resultados (relevância)
   # Salvar em: data/raw/scholar_resultados.csv
   ```

**Saída esperada:**
- ✅ `data/raw/scopus_resultados.csv` (ex: 350 artigos)
- ✅ `data/raw/wos_resultados.csv` (ex: 280 artigos)
- ✅ `data/raw/scielo_resultados.csv` (ex: 45 artigos)
- ✅ `data/raw/scholar_resultados.csv` (ex: 100 artigos)

**Tempo estimado**: 4-6 horas

---

### Tarefa 2.2: Consolidar e Remover Duplicatas

**O que fazer:**

```bash
# Executar script Python:
python scripts/01-busca_artigos.py

# Este script:
# 1. Lê todos os CSVs de data/raw/
# 2. Normaliza metadados
# 3. Identifica duplicatas (por DOI e título)
# 4. Gera data/processed/artigos_consolidados.csv
# 5. Relata estatísticas (ex: 450 únicos de 775 total)
```

**Saída esperada:**
- ✅ `data/processed/artigos_consolidados.csv`
- ✅ `data/processed/relatorio_busca.txt` (estatísticas)

**Tempo estimado**: 30 minutos (automático)

---

### Tarefa 2.3: Aplicar Critérios de Inclusão (Triagem)

**O que fazer:**

1. **Triagem por Título e Resumo (Nível 1)**
   - Ler título e resumo
   - Aplicar critérios de inclusão/exclusão
   - Marcar como: INCLUDE, EXCLUDE, MAYBE
   - Documentar motivo da exclusão

   **Ferramentas**:
   - Usar Covidence (pago) OU
   - Usar template `data/processed/triagem_nivel1.xlsx` OU
   - Usar script semi-automático em Python

   **Saída esperada:**
   - ✅ `data/processed/triagem_nivel1_resultados.csv`
   - Exemplo:
     ```csv
     DOI,Título,Decisão,Motivo
     10.1016/...,Knowledge Transfer in SMEs,INCLUDE,Alinhado
     10.1108/...,Large Corp Innovation,EXCLUDE,Foco em grandes empresas
     ```

2. **Análise de Full Text (Nível 2)**
   - Para artigos marcados como INCLUDE ou MAYBE
   - Baixar PDF do full text
   - Ler seções: Introdução, Metodologia, Resultados
   - Aplicar critérios novamente
   - Finalizar decisão: INCLUDE vs EXCLUDE

   **Saída esperada:**
   - ✅ PDFs salvos em `articles/pdf/`
   - ✅ `data/processed/triagem_nivel2_resultados.csv`

**Critério de decisão no Nível 2:**
```
INCLUDE se:
✓ Estuda transferência/absorção de conhecimento OU competitividade
✓ Tem dados empíricos (qualitativo ou quantitativo)
✓ Contexto relevante (PME/MPE/pequenas empresas)
✓ Metodologia clara e replicável

EXCLUDE se:
✗ Não tem dados empíricos
✗ Foco em grandes corporações
✗ Metodologia não clara
✗ Não relacionado aos temas
```

**Tempo estimado**: 15-20 horas (depende de n. artigos)

---

### ✓ Checklist Fase 2

```
[ ] Buscas executadas em todas as 4 bases
[ ] CSVs salvos em data/raw/
[ ] Script 01 executado (consolidação)
[ ] Triagem Nível 1 completa
[ ] PDFs baixados para Nível 2
[ ] Triagem Nível 2 completa
[ ] Amostra final aprovada
[ ] Registro PRISMA atualizado (n. triado vs incluído)
```

**Saída consolidada**: ✅ Lista final de artigos para análise (~50-80 artigos esperado)

---

## ✅ FASE 3: Conversão de Artigos (Semana 4)

### Tarefa 3.1: Converter PDFs para Markdown

**O que fazer:**

```bash
# Executar script:
python scripts/02-pdf_to_markdown.py

# Este script:
# 1. Lê todos os PDFs de articles/pdf/
# 2. Extrai texto usando PyPDF + OCR (se necessário)
# 3. Estrutura em seções (Intro, Método, Resultados, etc)
# 4. Converte para Markdown bem formatado
# 5. Salva em articles/md/ com nome: [AUTOR_ANO].md
# 6. Gera relatório de qualidade
```

**Exemplo de saída** (`articles/md/Cohen_1990.md`):

```markdown
# Knowledge Transfer and Absorptive Capacity

**Autores**: Cohen, W. M., & Levinthal, D. A.

**Ano**: 1990

**DOI**: 10.1287/mnsc.35.2.128

**Publicação**: Management Science, 35(2), 128-152

---

## Resumo

Este estudo seminal introduz o conceito de absorptive capacity...

---

## 1. Introdução

A transferência de conhecimento entre organizações...

---

## 2. Metodologia

**Tipo**: Revisão teórica + análise de casos

**Dados**: 50 empresas entrevistadas

---

## 3. Resultados Principais

### 3.1 Definição de Absorptive Capacity

AC é a capacidade da firma de:
1. Reconhecer conhecimento valioso
2. Assimilar conhecimento externo
3. Aplicar em contexto novo

### 3.2 Fatores que Influenciam AC

- Conhecimento prévio (base de conhecimento)
- Habilidades dos colaboradores
- Estrutura organizacional
- Mecanismos de transmissão interna

---

## 4. Discussão

Os achados sugerem que...

---

## 5. Conclusões

- AC é crítica para inovação
- Investimento em R&D constrói AC
- Conhecimento tácito é mais difícil de transferir

---

## Conceitos-Chave Identificados

- Absorptive Capacity
- Conhecimento Tácito/Explícito
- Inovação
- Base Conhecimento

---

## Referências Citadas

[Lista de referências em formato estruturado]

---

**Qualidade Conversão**: ✅ 98% (Texto legível)

**Data Processamento**: 2026-04-15

**Revisor**: [IA - Claude]
```

**Saída esperada:**
- ✅ ~60-80 arquivos Markdown em `articles/md/`
- ✅ `data/processed/conversao_qualidade.csv` (estatísticas)
- ✅ Relatório de artigos que precisam revisão manual

**Tempo estimado**: 2-3 horas (automático)

---

### Tarefa 3.2: Validar Qualidade de Conversão

**O que fazer:**

1. Abrir aleatoriamente 5-10 arquivos MD
2. Comparar com PDF original
3. Verificar:
   - [ ] Estrutura mantida
   - [ ] Tabelas convertidas corretamente
   - [ ] Figuras descritas
   - [ ] Nenhum texto perdido
4. Documentar problemas
5. Refazer conversão se < 90% qualidade

**Saída esperada:**
- ✅ Validação checklist preenchido
- ✅ Lista de artigos que precisam revisão manual

**Tempo estimado**: 1-2 horas

---

### ✓ Checklist Fase 3

```
[ ] Script 02 executado com sucesso
[ ] Todos os MDs gerados em articles/md/
[ ] Validação de qualidade feita
[ ] Problemas documentados e corrigidos
[ ] Relatório de conversão finalizado
```

**Saída consolidada**: ✅ Artigos prontos para fichamento

---

## ✅ FASE 4: Fichamento com IA (Semanas 5-6)

### Tarefa 4.1: Preparar Template de Fichamento

**O que fazer:**

- [ ] Abrir `scripts/utils/prompts.py`
- [ ] Revisar template de fichamento
- [ ] Ajustar para suas teorias (KBV, RBV, AC, DC, etc)
- [ ] Testar com 2-3 artigos manualmente

**Template de Fichamento**:

```markdown
# Fichamento - [TÍTULO ARTIGO]

## Metadados
- **Autores**: [Nomes]
- **Ano**: [YYYY]
- **Publicação**: [Periódico/Conferência]
- **DOI**: [DOI]
- **País Estudo**: [País]
- **Tipo Estudo**: [Qualitativo/Quantitativo/Misto]
- **N Participantes**: [N ou N/A]

---

## Resumo Executivo (150 palavras)

[Síntese automática do artigo]

---

## 1. Objetivo/Pergunta Pesquisa

**Questão Pesquisa**: [Qual era a pergunta central?]

**Objetivo**: [O que o estudo buscava responder?]

---

## 2. Quadro Teórico

**Teorias Utilizadas**:
- [ ] Knowledge-Based View (KBV)
- [ ] Resource-Based View (RBV)
- [ ] Absorptive Capacity (AC)
- [ ] Dynamic Capabilities (DC)
- [ ] Organizational Learning (OL)
- [ ] Innovation Systems (IS)
- [ ] Institutional Theory (IT)
- [ ] Outra: ________________

**Conceitos Principais**:
1. [Conceito 1 + definição]
2. [Conceito 2 + definição]
3. [Conceito 3 + definição]

---

## 3. Metodologia

**Delineamento**: [Descritivo/Explicativo/Exploratório]

**Método**: 
- [ ] Pesquisa Qualitativa (Entrevistas/Estudo Caso/etc)
- [ ] Pesquisa Quantitativa (Survey/Experimental/etc)
- [ ] Mista

**Amostra/Contexto**:
- Tamanho: [N = ?]
- Contexto: [Brasil/Outro país? Setor? Tamanho empresas?]
- Período: [Quando foi coletado?]

**Procedimentos Coleta**: [Como foi coletado?]

**Análise Dados**: [Métodos de análise]

---

## 4. Achados Principais

### 4.1 Achado 1
[Descrição do achado + evidência]

**Relevância para framework**: 
- Confirma/Contraria P1? [ ] [ ]
- Confirma/Contraria P2? [ ] [ ]
- Confirma/Contraria P3? [ ] [ ]
- Confirma/Contraria P4? [ ] [ ]
- Confirma/Contraria P5? [ ] [ ]
- Confirma/Contraria P6? [ ] [ ]

### 4.2 Achado 2
[Idem]

### 4.3 Achado 3
[Idem]

---

## 5. Relacionamento com Proposições de Pesquisa

| Proposição | Alinhamento | Evidência |
|-----------|-----------|-----------|
| P1: AC limitada em MPEs | ✅/❌/🟡 | [Breve evidência] |
| P2: AC → Competitividade | ✅/❌/🟡 | [Breve evidência] |
| P3: DC media AC → Competitividade | ✅/❌/🟡 | [Breve evidência] |
| P4: Contexto institucional modera | ✅/❌/🟡 | [Breve evidência] |
| P5: Redes facilitam transferência | ✅/❌/🟡 | [Breve evidência] |
| P6: OL cria vantagem sustentável | ✅/❌/🟡 | [Breve evidência] |

---

## 6. Pontos Fortes

- ✅ [Ponto forte 1]
- ✅ [Ponto forte 2]
- ✅ [Ponto forte 3]

---

## 7. Limitações Identificadas

- ⚠️ [Limitação 1]
- ⚠️ [Limitação 2]
- ⚠️ [Limitação 3]

---

## 8. Lacunas e Oportunidades Pesquisa

**Lacunas Identificadas pelo Artigo**:
1. [Lacuna 1]
2. [Lacuna 2]
3. [Lacuna 3]

**Oportunidades de Pesquisa Futura**:
- [Oportunidade 1]
- [Oportunidade 2]

**Relevância para seu projeto**:
[ ] Muito relevante - sugere novo problema pesquisa
[ ] Relevante - fornece suporte teórico
[ ] Moderadamente relevante - contexto útil
[ ] Pouco relevante - marginal

---

## 9. Contexto Brasil (se aplicável)

**O artigo menciona Brasil/contexto brasileiro?** [ ] Sim [ ] Não

Se sim:
- Dados específicos sobre Brasil: [Quais?]
- MPEs brasileiras estudadas? [ ] Sim [ ] Não
- Transferência conhecimento em contexto Brasil? [ ] Sim [ ] Não

---

## 10. Síntese para Matriz de Análise

**Dimensões para matriz temática**:
- Transferência Conhecimento: [ ] Focal [ ] Secundária [ ] Não aborda
- Absorptive Capacity: [ ] Focal [ ] Secundária [ ] Não aborda
- Competitividade: [ ] Focal [ ] Secundária [ ] Não aborda
- MPEs/PMEs: [ ] Focal [ ] Secundária [ ] Não aborda
- Brasil: [ ] Focal [ ] Secundária [ ] Não aborda

**Categorias temáticas** (marque todas as aplicáveis):
- [ ] Fonte de conhecimento externo
- [ ] Mecanismos de transferência
- [ ] Capacidade absortiva
- [ ] Dinâmicas de aprendizagem
- [ ] Inovação e desempenho
- [ ] Redes e parcerias
- [ ] Contexto institucional
- [ ] Setor industrial específico
- [ ] Tamanho empresa
- [ ] Localização geográfica

---

## 11. Anotações e Comentários Livres

[Espaço para comentários do analista]

---

## 12. Qualidade do Fichamento

- **Completude**: [ ] Completo [ ] Parcial [ ] Incompleto
- **Clareza**: [ ] Muito clara [ ] Clara [ ] Confusa
- **Consistência**: [ ] Consistente [ ] Parcial [ ] Inconsistente
- **Revisor**: [IA - Claude] + [Humano - A fazer]
- **Data**: [YYYY-MM-DD]

---
```

**Saída esperada:**
- ✅ Template validado e testado
- ✅ Exemplos de fichamentos bem feitos salvos

**Tempo estimado**: 3-4 horas

---

### Tarefa 4.2: Executar Fichamento Automático

**O que fazer:**

```bash
# Executar script:
python scripts/03-fichamento_ia.py

# Este script:
# 1. Lê cada arquivo MD de articles/md/
# 2. Envia para LLM (Claude/OpenAI) com prompt especializado
# 3. Recebe fichamento estruturado
# 4. Salva em analysis/fichamentos/[AUTOR_ANO].md
# 5. Gera data/processed/fichamentos_metadata.csv
# 6. Relata problemas (artigos que não processaram bem)
```

**Configuração** (em `scripts/config.py`):

```python
LLM_MODEL = "claude-3-opus"  # ou gpt-4
LLM_TEMPERATURE = 0.2  # Baixo para consistência
MAX_TOKENS = 3000
RETRIES = 3  # Se falhar, tenta 3x
```

**Saída esperada:**
- ✅ ~60-80 fichamentos em `analysis/fichamentos/`
- ✅ `data/processed/fichamentos_metadata.csv`
- ✅ Relatório de artigos com problemas

**Tempo estimado**: 2-3 horas (depende de n. artigos e API delays)

---

### Tarefa 4.3: Revisar Fichamentos Gerados

**O que fazer:**

1. Abrir aleatoriamente 5-10 fichamentos
2. Verificar:
   - [ ] Informações resumidas com precisão
   - [ ] Proposições foram corretamente identificadas
   - [ ] Conceitos-chave foram listados
   - [ ] Lacunas identificadas fazem sentido
3. Fazer anotações em `analysis/fichamentos/NOTAS_REVISAO.md`
4. Se qualidade < 80%, refazer com prompts ajustados

**Saída esperada:**
- ✅ Fichamentos validados
- ✅ Notas de revisão documentadas

**Tempo estimado**: 2-3 horas

---

### ✓ Checklist Fase 4

```
[ ] Template de fichamento definido
[ ] Script 03 testado com 2-3 artigos
[ ] Script 03 executado para todos os artigos
[ ] Fichamentos gerados e salvos
[ ] Revisão spot-check concluída
[ ] Problemas documentados e resolvidos
```

**Saída consolidada**: ✅ ~60-80 fichamentos prontos para validação

---

## ✅ FASE 5: Validação de Amostra (Semana 7)

### Tarefa 5.1: Sortear Amostra Aleatória

**O que fazer:**

```bash
# Executar script:
python scripts/04-validacao_amostra.py --tamanho_amostra 30

# Este script:
# 1. Lê lista de todos os fichamentos
# 2. Sorteia 30% deles (ou n. especificado)
# 3. Cria arquivo: analysis/validacao/amostra_validacao.csv
# 4. Gera lista checklist para revisor
```

**Exemplo de saída**:

```csv
ID,Autor,Ano,DOI,Status_Revisor,Data_Revisao,Observacoes
1,Cohen,1990,10.1287/mnsc.35.2.128,PENDENTE,,
2,Zahra,2002,10.1177/104649640204200503,PENDENTE,,
3,Teece,2007,10.1086/529446,PENDENTE,,
...
```

**Saída esperada:**
- ✅ `analysis/validacao/amostra_validacao.csv` (~20-25 artigos)
- ✅ `analysis/validacao/INSTRUCOES_REVISOR.md`

**Tempo estimado**: 30 minutos

---

### Tarefa 5.2: Revisor Humano Valida Amostra

**Instrução para Revisor (salvo em `INSTRUCOES_REVISOR.md`)**:

```markdown
# Instruções para Revisão de Fichamentos

## Objetivo

Validar qualidade de fichamentos gerados por IA e garantir:
1. Precisão na extração de informações
2. Correta identificação de proposições
3. Qualidade das sínteses

## Procedimento

### Para cada fichamento sorteado:

1. **Ler o fichamento** (analysis/fichamentos/[ARQUIVO].md)
2. **Comparar com original** (articles/md/[ARQUIVO].md)
3. **Preencher matriz de validação** (ver abaixo)
4. **Fazer anotações** em campo "Observacoes"

### Matriz de Validação

Para cada item, marque:
- ✅ Correto
- ❌ Incorreto
- 🟡 Parcialmente correto

| Item | Correto | Justificativa |
|------|---------|---------------|
| Metadados (Autores, Ano, DOI) | ✅/❌/🟡 | [Se ❌ ou 🟡, descrever erro] |
| Resumo Executivo (préciso e conciso) | ✅/❌/🟡 | |
| Objetivo/Pergunta (identificado corretamente) | ✅/❌/🟡 | |
| Quadro Teórico (teorias identificadas) | ✅/❌/🟡 | |
| Metodologia (resumida corretamente) | ✅/❌/🟡 | |
| Achados Principais (resumo fiel) | ✅/❌/🟡 | |
| Proposições (apontamentos corretos) | ✅/❌/🟡 | |
| Lacunas (identificadas apropriadamente) | ✅/❌/🟡 | |
| Contexto Brasil (se aplicável, correto) | ✅/❌/🟡 | |

### Scoring

- **Taxa de Concordância**: (Itens Corretos) / (Total Itens) × 100%
- **Aceitável**: ≥ 80%
- **Revisar**: 60-79%
- **Refazer**: < 60%

## Saída Esperada

1. Preencher `analysis/validacao/amostra_validacao.csv`
2. Preencher `analysis/validacao/matriz_validacao.xlsx`
3. Documentar erros sistemáticos em `analysis/validacao/feedback_revisor.md`

## Prazo

- Revisor A: [Data]
- Revisor B (se dupla cegada): [Data]
- Concordância entre revisores: Cohen's Kappa

---
```

**Saída esperada:**
- ✅ `analysis/validacao/amostra_validacao.csv` preenchido
- ✅ `analysis/validacao/matriz_validacao.xlsx` com notas
- ✅ `analysis/validacao/feedback_revisor.md` com observações

**Tempo estimado**: 4-6 horas (revisor humano)

---

### Tarefa 5.3: Calcular Taxa de Concordância

**O que fazer:**

```bash
# Executar análise:
python scripts/utils/validators.py --modo cohen_kappa

# Este script calcula:
# 1. Taxa de concordância geral (%)
# 2. Cohen's Kappa (concordância além do acaso)
# 3. Erros sistemáticos
# 4. Recomendações de melhoria
```

**Exemplo de saída**:

```
RELATÓRIO DE VALIDAÇÃO
======================

Amostra validada: 20 fichamentos
Taxa de concordância geral: 87.5%
Cohen's Kappa: 0.82 (Excelente)

Distribuição por item:
- Metadados: 100% correto
- Resumo: 90% correto
- Objetivo: 85% correto
- Teórico: 80% correto
- Metodologia: 95% correto
- Achados: 75% correto ⚠️
- Proposições: 80% correto
- Lacunas: 85% correto
- Brasil: 100% correto (N/A em 15 artigos)

Erros mais frequentes:
1. Síntese de achados muito resumida (frequência: 25%)
2. Proposições interpretadas por IA (frequência: 20%)
3. Lacunas contextualizadas demais (frequência: 15%)

Recomendações:
✓ Qualidade aceitável (>80%)
→ Ajustar prompt para "Achados" (mais detalhado)
→ Refazer 2 fichamentos com taxa < 70%
```

**Saída esperada:**
- ✅ `analysis/validacao/relatorio_concordancia.txt`
- ✅ Gráfico de distribuição erros (opcional)

**Tempo estimado**: 1 hora

---

### Tarefa 5.4: Refazer Fichamentos com Problemas

**O que fazer:**

Se taxa de concordância < 80%:

1. Revisar prompts em `scripts/utils/prompts.py`
2. Ajustar instrução para pontos problemáticos
3. Reprocessar fichamentos com taxa < 70%
4. Validar novamente

**Saída esperada:**
- ✅ Fichamentos corrigidos
- ✅ Taxa de concordância > 85%

**Tempo estimado**: 1-2 horas

---

### ✓ Checklist Fase 5

```
[ ] Amostra sorteada (30%)
[ ] Revisor recebeu instruções
[ ] Amostra validada
[ ] Taxa de concordância calculada
[ ] Erros sistemáticos documentados
[ ] Fichamentos refei dos se necessário
[ ] Aprovação para continuar com 100% da amostra
```

**Saída consolidada**: ✅ Validação de qualidade completa, taxa concordância > 80%

---

## ✅ FASE 6: Síntese Qualitativa (Semanas 8-9)

### Tarefa 6.1: Mapeamento Conceitual

**O que fazer:**

```bash
# Este é análise manual + Python
# 1. Abrir todos os fichamentos (analysis/fichamentos/)
# 2. Extrair conceitos principais de cada um
# 3. Usar Python para criar matriz de co-ocorrência
# 4. Gerar visualização (opcional)
```

**Processo**:

1. **Criar matriz conceitual** (`analysis/synthesis/matriz_conceitos.csv`):

```csv
Conceito,Frequência,Artigos,Proposições_Alinhadas,Observações
Transferência Conhecimento,58,45,P1-P3-P5,Tema central em 75% dos artigos
Absorptive Capacity,62,48,P1-P2-P3,Mais mencionado em artigos 2010+
Competitividade,41,32,P2-P6,Menos focal que nos anos 2000s
Dynamic Capabilities,28,22,P3-P4,Emergente nas últimas 5 anos
Conhecimento Tácito,36,28,P1-P4,Importante para contexto PME
...
```

2. **Identificar relações** (`analysis/synthesis/relacoes_conceitos.md`):

```markdown
## Relações Entre Conceitos

### Relação 1: Transferência → Absorptive Capacity
- Frequência conjunta: 42 artigos (70%)
- Tipo: Sequencial (primeiro ocorre, depois o segundo)
- Força: Forte (presente em maioria)
- Exemplos:
  * Cohen (1990): AC como resultado de transferência
  * Zahra (2002): Potencial AC recebe conhecimento externo

### Relação 2: AC → Competitividade
- Frequência conjunta: 28 artigos (47%)
- Tipo: Causal (AC causa competitividade)
- Força: Moderada
- Exemplos:
  * Teece (2007): DC (que requer AC) gera vantagem
  * ...

### Relação 3: Contexto Institucional MODERA transferência
- Frequência conjunta: 18 artigos (30%)
- Tipo: Moderadora
- Força: Fraca a moderada
- Exemplos:
  * Estudos Brasil mencionam barreiras institucionais
  * ...
```

**Saída esperada:**
- ✅ `analysis/synthesis/matriz_conceitos.csv`
- ✅ `analysis/synthesis/relacoes_conceitos.md`
- ✅ `analysis/synthesis/mapa_conceitual.png` (visualização, opcional)

**Tempo estimado**: 3-4 horas

---

### Tarefa 6.2: Identificar Lacunas

**O que fazer:**

1. **Compilar lacunas mencionadas** em fichamentos
2. **Agrupar por tema**
3. **Avaliar relevância para seu projeto**
4. **Documentar em matriz**

**Exemplo** (`analysis/synthesis/lacunas_identificadas.md`):

```markdown
# Lacunas Identificadas na Literatura

## Lacuna 1: Contexto Específico Brasil

**Descrição**: Poucos estudos sobre absorptive capacity em MPEs BRASILEIRAS especificamente

**Frequência de menção**: 12 artigos (20%)

**Exemplos**:
- Cohen & Levinthal (1990): Estudos USA
- Zahra & George (2002): Empresas europeias
- Teece (2007): Multinacionais

**Por que é lacuna**: 
- Brasil tem contexto institucional único
- MPEs brasileiras têm características distintivas
- Transferência conhecimento ocorre diferente em contexto local

**Relevância para seu projeto**: ⭐⭐⭐⭐⭐ MUITO ALTA

**Problema pesquisa derivado**:
"Como ocorre a absorção de conhecimento externo em MPEs brasileiras? Quais fatores institucionais facilitam/dificultam?"

---

## Lacuna 2: Dinâmica Temporal da AC

**Descrição**: Maioria são estudos transversais; faltam estudos longitudinais sobre evolução de AC

**Frequência de menção**: 8 artigos (13%)

**Por que é lacuna**:
- AC se desenvolve ao longo do tempo
- Estudos longitudinais raros (maioria < 2 anos)
- Dinâmica de aprendizado não bem compreendida

**Relevância para seu projeto**: ⭐⭐⭐ ALTA

**Problema pesquisa derivado**:
"Como evoluem e se consolidam as capacidades absortivas em MPEs ao longo do tempo?"

---

## Lacuna 3: Papel de Redes de Inovação em PMEs

**Descrição**: Foco em grandes empresas; pouco sobre PMEs em redes/ecossistemas

**Frequência de menção**: 6 artigos (10%)

**Por que é lacuna**:
- Innovation systems bem estudados em contexto macro
- Micro-perspectiva (como PMEs aproveitam redes) menos explorada
- Especialmente importante em contexto Brasil (APLs, SPLs)

**Relevância para seu projeto**: ⭐⭐⭐⭐ MUITO ALTA

**Problema pesquisa derivado**:
"Como redes de inovação (universidades, clientes, fornecedores) facilitam transferência e absorção de conhecimento em MPEs?"

---

[Continuar para outras lacunas identificadas]

---

## Síntese de Lacunas

| Lacuna | Frequência | Relevância | Problema Pesquisa Emergente |
|--------|-----------|-----------|---------------------------|
| Contexto Brasil | 20% | ⭐⭐⭐⭐⭐ | Como ocorre absorção em MPEs BR? |
| Dinâmica temporal | 13% | ⭐⭐⭐ | Como evolui AC ao tempo? |
| Redes inovação PME | 10% | ⭐⭐⭐⭐ | Como redes facilitam transfer? |
| AC em setores específicos | 8% | ⭐⭐⭐ | AC diferente por setor? |
| Conhecimento tácito transferência | 12% | ⭐⭐⭐ | Como transferir tácito? |
| Papel gestão conhecimento | 7% | ⭐⭐ | KM policies melhoram AC? |

---

## Matriz de Oportunidade Pesquisa

```
        Frequência menção
        Baixa    Alta
Alt
a  │  [Q1]    [Q2] ⭐
   │  Nicho   Promissor
R  │  [Q3]    [Q4]
e  │  Pouco   Bem conhecido
l  │  pesq.   
e  │
v  │
â  │
n  │  Baixa    Alta
   └─────────────────
       Relevância para projeto
```

**Posicionamento de lacunas**:
- **Q2 (Promissor)**: Contexto Brasil + Redes + Dinâmica temporal
- **Q4 (Bem conhecido)**: Definição e medida AC
- **Q1**: Menor relevância
```

**Saída esperada:**
- ✅ `analysis/synthesis/lacunas_identificadas.md`
- ✅ `analysis/synthesis/matriz_oportunidade_pesquisa.csv`

**Tempo estimado**: 3-4 horas

---

### Tarefa 6.3: Formular Problemas de Pesquisa

**O que fazer:**

Converter lacunas em **problemas de pesquisa específicos e testáveis**

(`analysis/synthesis/problemas_pesquisa.md`):

```markdown
# Problemas de Pesquisa Emergentes

## Problema 1: Absorção de Conhecimento Externo em MPEs Brasileiras

**Questão Central**:
"Como e em que medida as micro e pequenas empresas brasileiras absorvem conhecimento externo de fontes como universidades, fornecedores, clientes e redes de inovação?"

**Derivação das lacunas**:
- Lacuna: Contexto Brasil pouco estudado
- Lacuna: Redes de inovação não bem exploradas em PME
- Lacuna: Características específicas MPEs brasileiras desconhecidas

**Relevância teórica**:
- Testa proposição P1 (AC limitada em MPEs)
- Expande modelo de Innovation Systems para contexto local
- Contribui para entendimento de KBV em contexto emergente

**Relevância prática**:
- Identifica barreiras à absorção
- Sugere políticas para facilitar transfer
- Informa estratégias para MPEs

**Hipóteses associadas**:
- H1: Tamanho da firma limita capacidade absortiva
- H2: Acesso a redes aumenta absorção
- H3: Conhecimento prévio importante (efeito KPSS)
- H4: Contexto institucional modula absorção

---

## Problema 2: Dinâmica de Evolução de Capacidades Absortivas

**Questão Central**:
"Como evoluem e se consolidam as capacidades absortivas em MPEs ao longo do tempo? Quais práticas organizacionais facilitam essa evolução?"

**Derivação das lacunas**:
- Lacuna: Maioria estudos transversais
- Lacuna: Dinâmica temporal de AC pouco explorada
- Lacuna: Fatores que consolidam AC não mapeados

**Relevância teórica**:
- Aborda evolução de Dynamic Capabilities
- Testa proposição P3 (DC media AC → Competitividade)
- Contribui para Organizational Learning

**Tipo de estudo recomendado**:
- Longitudinal (3-5 anos)
- Métodos mistos (surveys + entrevistas)
- Estudos de caso múltiplos

---

[Continuar para outros problemas]

---

## Síntese de Problemas de Pesquisa

| ID | Problema | Lacuna Origem | Proposições | Tipo Estudo |
|----|---------|---|---|---|
| P-Pesq 1 | Absorção em MPEs BR | Contexto BR + Redes | P1, P4, P5 | Qualitativo multi-caso |
| P-Pesq 2 | Evolução AC temporal | Dinâmica temporal | P2, P3, P6 | Longitudinal |
| P-Pesq 3 | AC por setor | Especificidade setorial | P1 | Survey transversal |
| P-Pesq 4 | Gestão conhecimento | KM práticas | P6 | Quali + Quanti |

---
```

**Saída esperada:**
- ✅ `analysis/synthesis/problemas_pesquisa.md`
- ✅ 3-5 problemas bem formulados e fundamentados

**Tempo estimado**: 2-3 horas

---

### Tarefa 6.4: Análise Temática Estruturada

**O que fazer:**

Criar matriz temática que consolide ALL fichamentos por temas:

```python
# Script para criar matriz temática:
python scripts/utils/tema_matrix.py

# Saída: analysis/synthesis/matriz_tematica_completa.xlsx
```

**Exemplo de matriz** (`analysis/synthesis/matriz_tematica_completa.xlsx`):

```
| Artigo | Transf. Conhec | AC Pot | AC Real | DC | OL | Context Inst | Redes | Competit | Setor | País | Tipo N |
|--------|---|---|---|---|---|---|---|---|---|---|---|
| Cohen 90 | X | X | - | - | X | - | - | X | Múltiplos | USA | 50 |
| Zahra 02 | X | X | X | - | X | - | - | X | Múltiplos | Europa | 80 |
| Teece 07 | - | X | X | X | X | - | - | X | Múltiplos | Multi | Revisão |
| ... |
```

**Saída esperada:**
- ✅ `analysis/synthesis/matriz_tematica_completa.xlsx`
- ✅ Análise descritiva das células
- ✅ Padrões visualizados

**Tempo estimado**: 2 horas

---

### ✓ Checklist Fase 6

```
[ ] Matriz conceitual criada
[ ] Relações entre conceitos mapeadas
[ ] Lacunas identificadas e classificadas
[ ] Problemas de pesquisa formulados (3-5)
[ ] Matriz temática completa
[ ] Análise qualitativa documentada
[ ] Síntese pronta para redação
```

**Saída consolidada**: ✅ Síntese qualitativa completa com 3-5 problemas de pesquisa bem fundamentados

---

## ✅ FASE 7: Redação do Artigo (Semanas 10-12)

### Estrutura Recomendada

```markdown
# Transferência de Conhecimento, Absorptive Capacity e Competitividade em MPEs Brasileiras: Uma Revisão Sistemática

## 1. Introdução
- Contexto: Importância de MPEs no Brasil
- Relevância: Conhecimento como ativo estratégico
- Pergunta: O que sabemos sobre absorção de conhecimento em MPEs?

## 2. Fundamentação Teórica
- KBV + RBV + AC + DC + OL + Innovation Systems + Institutional Theory
- Integração das teorias (usar framework criado)
- Proposições de pesquisa

## 3. Metodologia
- Tipo: Revisão Sistemática (PRISMA 2020)
- Estratégia de busca (bases, palavras-chave)
- Critérios inclusão/exclusão
- Seleção artigos (triagem 1 e 2)
- Análise dados (fichamento + validação)
- Síntese qualitativa

## 4. Resultados
- Fluxo de triagem (diagrama PRISMA)
- Características artigos (tabela)
- Análise temática (mapa conceitual)
- Relações teóricas identificadas
- Lacunas na literatura

## 5. Discussão
- Síntese dos achados por proposição
- Contribuições teóricas
- Implicações práticas
- Limitações revisão

## 6. Lacunas e Problemas de Pesquisa Emergentes
- 3-5 problemas bem fundamentados
- Justificativa teórica
- Sugestões metodológicas

## 7. Conclusões

## 8. Referências

---

**Nº palavras**: ~8,000-10,000 (artigo padrão)
**Tabelas/Figuras**: 5-8
**Referências**: ~80-100
```

### Diretrizes de Redação

1. **Tom**: Acadêmico, objetivo, baseado em evidências
2. **Transparência**: Sempre remeter ao protocolo PRISMA
3. **Reprodutibilidade**: Seção de Metodologia muito detalhada
4. **Dados abertos**: Mencionar que dados estão em repositório GitHub
5. **Limitações**: Ser honesto sobre escopo

---

### ✓ Checklist Fase 7

```
[ ] Rascunho introdução
[ ] Rascunho metodologia (PRISMA)
[ ] Tabelas de resultados
[ ] Figuras (fluxo PRISMA, mapa conceitual)
[ ] Discussão alinhada com proposições
[ ] Problemas pesquisa emergentes bem descritos
[ ] Primeira versão completa
[ ] Revisão pares internos
[ ] Envio para revisor externo
[ ] Submissão para periódico
```

---

## 🎯 Cronograma Final

| Semana | Fase | Marco | Status |
|--------|------|-------|--------|
| 1 | Protocolo | ✅ Protocolo aprovado | 🟡 |
| 2-3 | Busca | ✅ Artigos selecionados | ⬜ |
| 4 | Conversão | ✅ PDFs → MD | ⬜ |
| 5-6 | Fichamento | ✅ Fichamentos IA | ⬜ |
| 7 | Validação | ✅ Taxa concordância > 80% | ⬜ |
| 8-9 | Síntese | ✅ Problemas pesquisa formulados | ⬜ |
| 10-12 | Redação | ✅ Artigo submetido | ⬜ |

---

## 📞 Suporte

Dúvidas sobre qualquer fase?
- Metodologia: Consultar `docs/01-PROTOCOLO-PRISMA.md`
- Scripts: Ver comments no código + `scripts/README.md`
- Conceitos teóricos: Consultar `docs/framework/FRAMEWORK-CONCEITUAL.md`

---

**Vamos começar!** 🚀

**Próximo passo**: Completar FASE 1 (Protocolo) esta semana.

