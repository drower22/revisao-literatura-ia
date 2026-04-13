# Guia de Validação de Fichamentos

**Data**: 10 de abril de 2026  
**Objetivo**: Garantir qualidade de fichamentos gerados por IA através de validação humana independente

---

## 📋 Instruções Gerais

### Para o Revisor

1. **Antes de começar**:
   - Ler este guia completamente
   - Familiarizar-se com o framework conceitual (`docs/framework/FRAMEWORK-CONCEITUAL.md`)
   - Revisar 2-3 exemplos de fichamentos bons

2. **Durante validação**:
   - Trabalhar independente (dupla-cegada se possível)
   - Usar matriz abaixo para cada item
   - Anotar problemas específicos
   - NÃO corrigir, apenas avaliar

3. **Registro**:
   - Preencher `analysis/validacao/amostra_validacao.csv` para cada artigo
   - Adicionar notas em `analysis/validacao/matriz_validacao_detalhada.xlsx`
   - Documentar erros em `analysis/validacao/feedback_revisor.md`

---

## ✅ Matriz de Validação

Para **cada item** do fichamento, marque:

| Marca | Significado | Ação |
|-------|-----------|------|
| ✅ **CORRETO** | Informação está fiel ao original, completa, bem interpretada | Seguir |
| 🟡 **PARCIAL** | Informação existe mas está incompleta, ligeiramente distorcida ou ambígua | Revisar e refinar |
| ❌ **INCORRETO** | Informação não está no original, está errada ou interpretada inadequadamente | Corrigir em versão final |
| ⏭️ **N/A** | Item não aplicável (ex: Brasil mencionado quando artigo não trata) | Marcar e prosseguir |

---

## 🔍 Validação Item por Item

### 1. Metadados

**O que verificar:**
- Autores: Estão corretos no fichamento?
- Ano: Coincide com publicação?
- Periódico/Conferência: Nome completo e correto?
- DOI: Número correto (formato)?
- País estudo: Qual país(es) foi estudo realizado?
- Tipo estudo: Qualitativo/Quantitativo/Misto está correto?
- N Participantes: Número de respondentes/casos/entrevistas (se aplicável)?
- Setor/Contexto: Qual setor e contexto do estudo?

**Como fazer**:
- Comparar metadados do fichamento com primeira página do artigo
- Se houver discrepância, marcar ❌ e anotar diferença

**Exemplo Error**:
```
Fichamento diz: Ano: 2019
Original diz: 2020
Decisão: ❌ INCORRETO
Anotação: "Ano errado no fichamento"
```

---

### 2. Resumo Executivo

**O que verificar**:
- Síntese captura TEMA CENTRAL do artigo?
- Omitiu OBJETIVOS principais?
- Omitiu ACHADOS principais?
- Usa linguagem clara e precisa?
- Tamanho apropriado (~150 palavras)?

**Exemplos**:

✅ **BOM resumo**:
> "Cohen & Levinthal (1990) investigam como empresas manufatureiras reconhecem e absorvem conhecimento tecnológico externo. Através de survey com 50 empresas, demonstram que a base de conhecimento prévio (related knowledge) da empresa é crítica para absortive capacity. Achado principal: empresas com pesquisa interna (R&D) desenvolvem AC maior."

❌ **RUIM resumo**:
> "Este artigo fala sobre conhecimento em empresas."

🟡 **PARCIAL**:
> "Estudo sobre absorção de conhecimento em empresas. Encontraram que R&D é importante." [Incompleto, falta contexto e achado específico]

---

### 3. Objetivo/Pergunta de Pesquisa

**O que verificar**:
- Pergunta central está CLARA e ESPECÍFICA?
- É uma pergunta (?) não uma afirmação?
- Está explícita no artigo (introdução/abstract)?
- Objetivo geral está bem definido?

**Como fazer**:
- Ler a Introdução e Abstract do artigo
- Procurar por: "The purpose...", "Our research question is...", "This study aims..."
- Comparar com fichamento

**Erros Comuns**:
- ❌ Pergunta muito vaga ("Como transferência ocorre?")
- ❌ Múltiplas perguntas não diferenciadas
- ❌ Objetivo inferido, não explícito

---

### 4. Quadro Teórico

**O que verificar**:

1. **Teorias identificadas estão TODAS mencionadas no artigo?**
   - Para cada teoria marcada: procurar no texto
   - Se não encontrar: ❌ INCORRETO
   - Se menção superficial: 🟡 PARCIAL

2. **Conceitos principais estão bem definidos?**
   - Definição é fiel ao artigo?
   - Cita como autores definem?
   - Está clara?

**Exemplos**:

✅ **BOM**: 
- Marca: [X] Absorptive Capacity (Cohen & Levinthal)
- Artigo menciona: "Cohen & Levinthal (1990) define AC como..."
- Decisão: ✅ CORRETO

❌ **RUIM**:
- Marca: [X] Dynamic Capabilities
- Artigo NOT menciona DC
- Decisão: ❌ INCORRETO

---

### 5. Metodologia

**O que verificar**:

| Sub-item | Verificar |
|----------|-----------|
| **Delineamento** | Corresponde (exploratório/descritivo/explicativo)? |
| **Método** | Tipo correto (caso/survey/entrevista/etc)? |
| **Amostra N** | Número exato de participantes/empresas/casos? |
| **Contexto** | País, setor, período coletado - tudo correto? |
| **Procedimentos** | Como dados foram coletados descrito fielmente? |
| **Análise** | Método de análise (estatístico/qualitativo) correto? |

**Checklist**:
```
[ ] Delineamento: ✅ / 🟡 / ❌
[ ] Método: ✅ / 🟡 / ❌
[ ] Amostra: ✅ / 🟡 / ❌ [Se ❌, informar N correto: ___]
[ ] Contexto: ✅ / 🟡 / ❌
[ ] Procedimentos: ✅ / 🟡 / ❌
[ ] Análise: ✅ / 🟡 / ❌
```

---

### 6. Achados Principais

**O que verificar**:

1. **Quantos achados estão listados?** (máximo 5)
   - Se mais de 5: 🟡 talvez excesso

2. **Cada achado tem EVIDÊNCIA específica?**
   - Procurar números, citações, exemplos
   - ✅ Se tem
   - ❌ Se é genérico/inferido

3. **Achados são os PRINCIPAIS?**
   - Compare com resultados artigo
   - Os 5 listados são os mais importantes?

**Exemplo Validation**:

Fichamento diz:
> "Achado 1: AC é importante para inovação"

Original diz:
> "Regressão múltipla mostrou β=0.67 (p<0.001) entre AC realizada e número de produtos novos"

Decisão: 🟡 PARCIAL - achado correto mas IA omitiu evidência específica (β, p-value)
Anotação: "Adicionar dados estatísticos específicos"

---

### 7. Relacionamento com Proposições

**O que verificar**:

Para CADA proposição (P1-P6), o fichamento marcou:
- ✅ Se CONFIRMA
- ❌ Se CONTRARIA
- 🟡 Se IMPLÍCITO/AMBÍGUO

**Validação**:
1. Ler o que o fichamento diz que artigo evidencia para P1
2. Ler o artigo
3. Comparar: faz sentido o alinhamento?

**Exemplos**:

❌ **ERRO**:
- Fichamento: P2 (AC→Competitividade): ✅ CONFIRMA
- Artigo: Não menciona competitividade, apenas AC como conceito teórico
- Correto: 🟡 ou ❌

✅ **CORRETO**:
- Fichamento: P1 (AC limitada em MPEs): ✅ CONFIRMA
- Artigo: "Pequenas firmas têm menor R&D, limitando AC"
- Correto: ✅

---

### 8. Pontos Fortes

**O que verificar**:
- Força metodológica: Está bem descrita?
- Força teórica: Contribuição está clara?
- São realmente fortes (não fraquezas)?

**Exemplo**:

❌ Ponto Fraco mal identificado:
- Listado como "força": "Estudo com 1000 respondentes"
- Análise fichamento: Grande N é força? Sim, geralmente é
- Mas contexto importa: se viés de seleção alto, N grande NÃO é força

---

### 9. Limitações

**O que verificar**:
- Limitações são mencionadas EXPLICITAMENTE no artigo?
- IA inferiu limitações válidas?
- São realmente limitações (não achados)?

**Classificação de Severidade**:
- Crítica: Invalida conclusões
- Moderada: Reduz generalização
- Menor: Marginal, mas mencionável

---

### 10. Lacunas Identificadas

**O que verificar**:
- Lacunas listadas estão NO ARTIGO (explícitas ou claras inferências)?
- São relevantes para seu projeto?

**Diferenciação importante**:
- **Lacunas do artigo**: O que o artigo diz não foi estudado
- **Lacunas implied**: O que se depreende do estudo como não abordado

**Exemplo**:

Fichamento diz Lacuna 1: "Poucos estudos sobre AC em Brasil"
Artigo: "Estudos sobre AC realizados principalmente nos EUA e Europa..."
Validação: ✅ CORRETO, explícito no artigo

---

### 11. Contexto Brasil

**O que verificar**:
- [ ] Artigo menciona Brasil? [SIM/NÃO] - confira
- [ ] Se SIM: dados específicos estão corretos?
- [ ] MPEs brasileiras estudadas? Confirme
- [ ] Barreiras institucionais Brasil mencionadas? Confirme

**Atenção**: Muitos artigos podem ser sobre Brasil mas não mencionar contexto institucional. Marque ⏭️ N/A se aplicável.

---

### 12. Categorias Temáticas

**O que verificar**:
- Categorias marcadas fazem sentido?
- Faltam categorias importantes?
- Marque aquelas que artigo CLARAMENTE aborda

**Decisão**:
- Se ≥80% das categorias corretas: ✅ CORRETO
- Se 60-79%: 🟡 PARCIAL
- Se <60%: ❌ INCORRETO

---

### 13. Relevância para Projeto

**O que verificar**:
- Nível de relevância está justificado?
- Pode realmente sugerir problema de pesquisa?
- Fundamentação é adequada?

---

## 📊 Calculando Taxa de Concordância

Após validar todos os itens, calcule:

```
Taxa de Concordância = (Itens Corretos ✅) / (Total Itens) × 100%

Exemplo:
- Total itens validados: 13
- ✅ Corretos: 11
- 🟡 Parciais: 1
- ❌ Incorretos: 1
- ⏭️ N/A: 0

Taxa = (11 + 0.5×1) / 13 = 11.5 / 13 = 88.5%
```

**Interpretação**:
- **≥85%**: Excelente - Aprovar
- **80-84%**: Bom - Aprovado com pequenas revisões
- **70-79%**: Aceitável - Revisar pontos fracos
- **60-69%**: Revisão necessária - Refazer parcial
- **<60%**: Insuficiente - Refazer completo

---

## 📝 Preenchendo Formulários

### Arquivo 1: `amostra_validacao.csv`

```csv
ID,Autor,Ano,DOI,Status_Revisor,Data_Revisao,Taxa_Concordancia,Observacoes
1,Cohen,1990,10.1287/mnsc.35.2.128,COMPLETO,2026-06-20,88.5,"Correto, pequeno erro em P3"
2,Zahra,2002,10.1177/104649640204200503,COMPLETO,2026-06-20,92.3,"Excelente"
...
```

### Arquivo 2: `matriz_validacao_detalhada.xlsx`

Colunas:
- ID_artigo
- Item_fichamento
- Validacao (✅/🟡/❌/N/A)
- Evidencia_Original (citar página/seção)
- Notas_Revisor
- Acao_Recomendada

### Arquivo 3: `feedback_revisor.md`

```markdown
# Feedback Revisor - Validação Amostra

**Revisor**: [Nome]
**Data**: 2026-06-20
**N Artigos Validados**: 20
**Taxa Concordância Média**: 88.5%
**Cohen's Kappa**: 0.82

## Erros Sistemáticos Identificados

### Erro 1: Proposições mal interpretadas (Frequência: 25%)
Descrição: IA marca como ✅ (CONFIRMA) quando artigo apenas menciona conceito, sem estabelecer relação causal

Exemplo:
- Fichamento: P2 ✅ CONFIRMA
- Artigo: Menciona AC e competitividade seperately, não relação

Recomendação para prompt: 
"Apenas marque ✅ se artigo EXPLICITAMENTE estabelece relação CAUSAL/correlação. Caso contrário, marque 🟡"

### Erro 2: Síntese de achados muito resumida (Frequência: 20%)
Descrição: IA omite dados quantitativos específicos (β, p-value, r, N comparações)

Recomendação: "Para estudos quantitativos, INCLUA estatísticas: r=.45, p<.01, N=200, etc"

### Erro 3: Lacunas contextualizadas demais (Frequência: 15%)
Descrição: IA infere lacunas que não estão explícitas no artigo

Recomendação: "DIFERENCIE claramente: [Lacunas do artigo = explícitas] vs [Implícitas = sua interpretação]"

## Recomendações para Próximo Batch

1. Revisar prompts nos pontos 1-3 acima
2. Refazer fichamentos com taxa <75%
3. Revalidar amostra maior se muitos erros

## Conclusão

Taxa concordância aceitável (88.5%). Qualidade geral BOA.
Pequenos ajustes no prompt devem elevar para >92%.
```

---

## 🎯 Decisão Final de Qualidade

**Para cada fichamento, decidir**:

- ✅ **APROVADO**: Taxa ≥85% + erros não críticos → Usar em síntese
- 🟡 **REVISAR**: Taxa 70-84% → IA refaz com feedback, revalidar
- ❌ **REFAZER**: Taxa <70% → IA refaz completo do zero

---

## ⏱️ Tempo Esperado

- Validação por artigo: 15-20 minutos
- Amostra 20-25 artigos: 5-8 horas
- Cálculos + feedback: 1-2 horas

**TOTAL**: ~10 horas para validação completa

---

## 📞 Dúvidas

Se incerto sobre algum item:
1. Comparar com EXEMPLOS acima
2. Consultar Framework conceitual
3. Avisar ao pesquisador principal para esclarecimento

---

**Obrigado pela validação cuidadosa!** ✨

