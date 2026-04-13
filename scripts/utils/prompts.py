"""
Prompts para IA - Fichamento de Artigos
========================================

Define prompts otimizados para extrair informações de artigos
usando A/B Testing entre Claude (Anthropic) e Gemini (Google)

METODOLOGIA A/B TESTING:
- Ambas as IAs processam o MESMO artigo independentemente
- Gera 2 fichamentos para comparação
- Discrepâncias sinalizadas para revisão humana prioritária
- Consenso forte aumenta confiabilidade dos dados
"""

FICHAMENTO_SYSTEM_PROMPT = """Você é um pesquisador especialista em análise de literatura científica.
Sua tarefa é gerar fichamentos estruturados e precisos de artigos acadêmicos.

IMPORTANTE:
- Seja preciso e fiel ao conteúdo original
- Identifique corretamente quais teorias são mencionadas
- Diferencie entre achados EXPLÍCITOS (no artigo) vs INFERÊNCIAS
- Para proposições: marque ✅ se CLARA no artigo, ❌ se CONTRADIZ, 🟡 se IMPLÍCITO
- Forneça sínteses concisos mas informativos
- Cite evidências específicas quando possível
"""

# Template específico para A/B Testing
AB_TESTING_SYSTEM_PROMPT = """Você é um pesquisador especialista em análise de literatura científica.

CONTEXTO: Este fichamento faz parte de uma VALIDAÇÃO A/B com múltiplas IAs.
Sua resposta será comparada com análises de outro modelo para validação robusta.

INSTRUÇÕES CRÍTICAS:
- Máxima PRECISÃO e FIDELIDADE ao texto original
- NÃO interprete além do explícito - quando ambíguo, marque como 🟡 (implícito)
- Cite EXATAMENTE como aparece no artigo (com página/seção quando possível)
- Se houver contradição interna no artigo, MENCIONE explicitamente
- Forneça sínteses concisos mas informativos

CRITÉRIOS PARA ESTA ANÁLISE:
1. Metadados devem ser 100% precisos (sem inferências)
2. Teorias: identifique TODAS mencionadas, nunca suponha
3. Proposições: use ✅/❌/🟡 rigorosamente
4. Evite generalizações além do escopo do artigo
"""

FICHAMENTO_USER_PROMPT_TEMPLATE = """
Gere um fichamento completo do seguinte artigo em formato Markdown:

---INÍCIO DO ARTIGO---
{article_content}
---FIM DO ARTIGO---

Estruture o fichamento em EXATAMENTE as seguintes seções:

## Metadados
[Extrair: Autores, Ano, DOI, Periódico, País estudo, N participantes, Tipo estudo (Qualitativo/Quantitativo/Misto)]

## Resumo Executivo (100-150 palavras)
[Síntese do que o artigo discute, não opiniões]

## 1. Objetivo/Pergunta Pesquisa
[Qual era a pergunta central?]

## 2. Quadro Teórico
[Quais teorias usadas? Marque as que encontrar:]
- [ ] Knowledge-Based View (KBV)
- [ ] Resource-Based View (RBV)
- [ ] Absorptive Capacity (AC)
- [ ] Dynamic Capabilities (DC)
- [ ] Organizational Learning (OL)
- [ ] Innovation Systems (IS)
- [ ] Institutional Theory (IT)
- [ ] Outra: _______

[Conceitos principais definidos no artigo - máximo 3]

## 3. Metodologia
[Delineamento, método, amostra (N=?), contexto, período, análise]

## 4. Achados Principais
[Máximo 5 achados, com evidências específicas]

## 5. Relacionamento com Proposições
Para CADA proposição abaixo, marque:
- P1: AC limitada em MPEs → [✅/❌/🟡] porque: [breve evidência]
- P2: AC→Competitividade → [✅/❌/🟡] porque: [breve evidência]
- P3: DC media AC→Competitividade → [✅/❌/🟡] porque: [breve evidência]
- P4: Contexto institucional modera → [✅/❌/🟡] porque: [breve evidência]
- P5: Redes facilitam em AC baixa → [✅/❌/🟡] porque: [breve evidência]
- P6: OL cria vantagem sustentável → [✅/❌/🟡] porque: [breve evidência]

## 6. Pontos Fortes (máximo 3)
[Força metodológica, contribuições teóricas, relevância]

## 7. Limitações (máximo 3)
[Escopo, metodologia, generalização]

## 8. Lacunas Identificadas (máximo 3)
[O que o artigo RECONHECE como não estudado]

## 9. Contexto Brasil
- Menciona Brasil? [SIM/NÃO]
- Se SIM: [Breve descrição]
- MPEs brasileiras estudadas? [SIM/NÃO]

## 10. Categorias Temáticas
Marque todas aplicáveis:
- [ ] Fonte conhecimento externo
- [ ] Mecanismos transferência
- [ ] Capacidade absortiva
- [ ] Dinâmicas aprendizagem
- [ ] Inovação e desempenho
- [ ] Redes e parcerias
- [ ] Contexto institucional
- [ ] Setor específico
- [ ] Tamanho empresa
- [ ] Localização geográfica

## 11. Relevância para Projeto
[ ] Muito alta (problema pesquisa emergente)
[ ] Alta (suporte teórico importante)
[ ] Moderada (contexto útil)
[ ] Baixa (marginal)

Justificativa: [1-2 linhas]

---

INSTRUÇÕES ADICIONAIS:
- Se artigo não tem seção, marque como "Não especificado"
- Cite números/dados específicos quando disponível
- Diferencie claramente entre o que ARTIGO diz vs sua INTERPRETAÇÃO
- Se ambiguo, use 🟡 (parcialmente)
"""

# Template para análise de lacunas
LACUNAS_ANALYSIS_TEMPLATE = """
## Lacuna: {lacuna_titulo}

**Descrição**: {descricao}

**Frequência menção**: {frequencia}% dos artigos ({n_artigos}/{total_artigos})

**Exemplos de artigos mencionando**:
- {exemplo1}
- {exemplo2}

**Por que é lacuna**:
1. {razao1}
2. {razao2}
3. {razao3}

**Relevância para projeto**: ⭐⭐⭐ (escala 1-5)

**Problema pesquisa derivado**:
{problema_pesquisa}
"""

# Template para problema de pesquisa
PROBLEMA_PESQUISA_TEMPLATE = """
## Problema {id}: {titulo}

**Questão Central**:
"{questao}"

**Lacunas de origem**:
- {lacuna1}
- {lacuna2}

**Relevância teórica**:
- Testa: {proposicoes}
- Expande: {contexto}

**Relevância prática**:
- Contribuição 1: {contrib1}
- Contribuição 2: {contrib2}

**Hipóteses associadas**:
- H1: {hipotese1}
- H2: {hipotese2}

**Tipo de pesquisa recomendado**:
- Delineamento: {design}
- Amostra: {amostra}
- Método: {metodo}
- Período: {periodo}
"""

VALIDACAO_AB_TESTING_PROMPT = """Você é um pesquisador sênior validando CONSISTÊNCIA entre duas análises independentes.

TAREFA: Comparar fichamentos gerados por Claude e Gemini do MESMO artigo.

Para CADA seção, marque:
✅ CONCORDÂNCIA FORTE - ambas IAs chegaram a conclusões compatíveis
🟡 CONCORDÂNCIA PARCIAL - existe overlap mas com nuances diferentes
❌ DISCORDÂNCIA - análises conflitam significativamente
⚠️ AMBIGUIDADE NO ARTIGO - discordância justificada por texto ambíguo

SEÇÕES CRÍTICAS (devem ter ✅):
1. Metadados (autores, ano, periódico)
2. Tipo de estudo (qualitativo/quantitativo)
3. Tamanho amostra (N=?)
4. Objetivo principal

SEÇÕES COM MAIS VARIABILIDADE ESPERADA:
1. Síntese de achados (abordagens diferentes válidas)
2. Relevância para projeto (interpretação subjetiva)
3. Problemas de pesquisa derivados (criatividade)

RELATÓRIO FINAL:
1. Taxa concordância geral: X%
2. Cohen's Kappa (para seções estruturadas): X
3. Discrepâncias críticas: [lista]
4. Recomendação: [usar fichamento Claude / Gemini / média ponderada]
"""

COMPARACAO_AB_TESTING_TEMPLATE = """# Comparação A/B Testing - Artigo: {titulo}

**Data Análise**: {data}  
**Artigo**: {autores}, {ano}  
**DOI**: {doi}

## 📊 Resumo de Concordância

| Seção | Claude | Gemini | Concordância | Status |
|-------|--------|--------|--------------|--------|
| Metadados | {claude_meta} | {gemini_meta} | ✅ | Crítica |
| Metodologia | {claude_meth} | {gemini_meth} | {concordancia_meth} | OK |
| Achados | {claude_ach} | {gemini_ach} | {concordancia_ach} | OK |
| Proposições | {claude_prop} | {gemini_prop} | {concordancia_prop} | OK |
| **Total** | - | - | **{media_total}%** | {status_final} |

## 🔍 Análise Detalhada

### Concordância Forte (✅)
- {item1}
- {item2}
- {item3}

### Concordância Parcial (🟡)
- {item1} - Claude: {visao_claude} vs Gemini: {visao_gemini}
- {item2} - Diferença: {diferenca}

### Discordância (❌)
- {item1} - **CRÍTICO**: Claude vs Gemini divergem sobre {aspecto}
  * Verificação: {verificacao}
  * Recomendação: [usar um ou média]

### Ambiguidades no Artigo (⚠️)
- {item1} - Texto original é ambíguo sobre {topico}

## 📈 Estatísticas

- **Cohen's Kappa**: {kappa} (interpretação: {interpretacao})
- **Porcentagem Discrepância**: {pct_disc}%
- **Recomendação**: {recomendacao}

## ✅ Decisão Final

Fichamento final usar: **{claude_ou_gemini_ou_media}**  
Justificativa: {justificativa}

Marcar para revisão humana: [SIM/NÃO]  
Seções prioritárias: {secoes_prioritarias}
"""

VALIDACAO_SYSTEM_PROMPT = """Você é um pesquisador experiente fazendo validação de qualidade de análises.

Sua tarefa é COMPARAR um fichamento gerado por IA com o artigo original e avaliar precisão.

Para CADA item do fichamento:
- Verifique se informação está CORRETA no original
- Verifique se está COMPLETA (não omitida)
- Verifique se está INTERPRETADA adequadamente

Marque:
✅ CORRETO - informação fiel ao original
🟡 PARCIAL - informação existe mas está incompleta/ligeiramente distorcida
❌ INCORRETO - informação não está no original ou está errada
N/A - item não aplicável

Identifique ERROS SISTEMÁTICOS (padrões de erro para corrigir prompts)
"""

SINTESE_SYSTEM_PROMPT = """Você é um especialista em síntese de evidências de estudos múltiplos.

Tarefa: Integrar achados de MÚLTIPLOS fichamentos para identificar:
1. Padrões e consensos na literatura
2. Contradições e divergências
3. Lacunas e tópicos pouco explorados
4. Questões emergentes para pesquisa futura

Use pensamento crítico para ir além de simples agregação.

IMPORTANTE: Se disponível, use fichamentos validados por A/B Testing,
priorizando itens com CONCORDÂNCIA FORTE entre múltiplas IAs.
"""
