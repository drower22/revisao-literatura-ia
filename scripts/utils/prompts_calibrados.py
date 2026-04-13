"""
Prompts Calibrados - Versão 2.0
==============================

Define prompts otimizados após calibragem com artigos seminais.
Use SEMPRE a versão calibrada para fichamentos em massa.

HISTÓRICO:
- v1.0: Prompts iniciais genéricos
- v2.0: Calibrados com 15-20 artigos seminais
         Ajustes baseados em matriz de concordância

INSTRUÇÕES DE USO:
1. Execute: python scripts/00-calibragem_prompts.py
2. Revise: analysis/calibragem/relatorio_calibragem.md
3. Se concordância <90%, refine este arquivo
4. Reexecute calibragem para validar
5. Quando pronto (90%+), use para fichamento em massa
"""

# Prompt para Fichamento - Versão Calibrada
PROMPT_FICHAMENTO_CALIBRADO = """Você é um pesquisador especialista em análise de literatura científica.

CONTEXTO: Análise rigorosa de artigo acadêmico para revisão sistemática.

⚠️ INSTRUÇÕES CRÍTICAS (NÃO VIOLE):
1. MÁXIMA PRECISÃO E FIDELIDADE ao texto original
2. NÃO interprete além do explícito - se ambíguo, marque 🟡
3. Cite EXATAMENTE como aparece no artigo (com página se possível)
4. Se houver contradição interna, MENCIONE explicitamente
5. Forneça sínteses concisos mas informativos
6. Para proposições: use ✅ (suporta), ❌ (contradiz), 🟡 (ambíguo)

CONTEÚDO DO ARTIGO:
{article_content}

GERE FICHAMENTO ESTRUTURADO NO FORMATO EXATO ABAIXO:

## Metadados
- Autores: [extrair]
- Ano: [extrair]
- DOI/URL: [extrair]
- Periódico/Conferência: [extrair]
- País estudo: [extrair]
- N participantes/amostra: [extrair]
- Tipo estudo: [Qualitativo/Quantitativo/Misto]

## Resumo Executivo (100-150 palavras)
[O que o artigo discute, sem opiniões]

## 1. Objetivo/Pergunta Pesquisa
[Qual era a pergunta central?]

## 2. Quadro Teórico
Teorias mencionadas:
- [ ] Absorptive Capacity (AC)
- [ ] Dynamic Capabilities (DC)
- [ ] Organizational Learning (OL)
- [ ] Resource-Based View (RBV)
- [ ] Knowledge-Based View (KBV)
- [ ] Institutional Theory
- [ ] Outra: [especificar]

Conceitos principais (máximo 3 definições):
1. [Conceito e definição conforme artigo]
2. [Conceito e definição conforme artigo]

## 3. Metodologia
[Delineamento, método, amostra, contexto, período, análise]

## 4. Achados Principais
Máximo 5 achados com evidências específicas:
1. [Achado com citação/evidência]
2. [Achado com citação/evidência]

## 5. Análise de Proposições
P1: AC limitada em MPEs → ✅/❌/🟡 porque: [evidência]
P2: AC→Competitividade → ✅/❌/🟡 porque: [evidência]
P3: DC media relação → ✅/❌/🟡 porque: [evidência]
P4: Contexto modifica → ✅/❌/🟡 porque: [evidência]
P5: Redes facilitam → ✅/❌/🟡 porque: [evidência]

## 6. Pontos Fortes (máximo 3)
[Força metodológica, contribuições, relevância]

## 7. Limitações (máximo 3)
[Escopo, metodologia, generalização]

## 8. Lacunas Identificadas (máximo 3)
[O que artigo reconhece como não estudado]

## 9. Contexto Brasil
- Menciona Brasil? [SIM/NÃO]
- Se SIM: [breve descrição]
- MPEs brasileiras? [SIM/NÃO]

## 10. Categorias Temáticas
Marque todas aplicáveis:
- [ ] Fonte conhecimento externo
- [ ] Mecanismos transferência
- [ ] Capacidade absortiva
- [ ] Dinâmicas aprendizagem
- [ ] Inovação/desempenho
- [ ] Redes/parcerias
- [ ] Contexto institucional
- [ ] Setor específico
- [ ] Tamanho empresa
- [ ] Localização geográfica

## 11. Relevância para Projeto
[ ] Muito Alta (problema emergente)
[ ] Alta (suporte teórico importante)
[ ] Moderada (contexto útil)
[ ] Baixa (marginal)

Justificativa: [1-2 linhas]

---
INSTRUÇÕES FINAIS:
- Se informação não está disponível, marque como "Não especificado"
- Máximo 3 páginas
- Diferencie ARTIGO disse vs SUAS interpretações
- Use símbolos para clareza (✅/❌/🟡)

Responda APENAS no formato acima.
"""

# Prompt para análise de proposições específicas
PROMPT_ANALISE_PROPOSICOES_CALIBRADO = """Como especialista em absorptive capacity e dinâmicas organizacionais:

ARTIGO: {titulo}

ANALISE RIGOROSAMENTE o suporte do artigo para cada proposição:

**P1: Absorptive Capacity limitada em MPEs**
- Encontra discussão sobre AC em empresas pequenas? [SIM/NÃO/PARCIAL]
- Se SIM, qual a limitação identificada?
- Evidência TEXTUAL: [citar exatamente]
- Status: ✅/❌/🟡

**P2: AC correlacionada com competitividade/desempenho**
- Conecta AC com performance/competitividade? [SIM/NÃO]
- Como define competitividade?
- Relação é causal, correlacional ou especulativa?
- Evidência: [citar]
- Status: ✅/❌/🟡

**P3: Dynamic Capabilities medeiam relação AC→Performance**
- Menciona DC especificamente? [SIM/NÃO]
- Se SIM, como conecta com AC?
- Evidência: [citar]
- Status: ✅/❌/🟡

**P4: Contexto institucional modifica relações**
- Discute contexto institucional? [SIM/NÃO]
- Identifica como afeta AC/DC/learning?
- Que contextos? [país, setor, tipo empresa]
- Status: ✅/❌/🟡

**P5: Redes/parcerias facilitam AC em contexto de baixa capacidade**
- Menciona redes, parcerias, colaboração? [SIM/NÃO]
- Como facilitam transferência conhecimento?
- Evidência: [citar]
- Status: ✅/❌/🟡

Responda em formato estruturado acima.
"""

# Prompt para síntese de conhecimentos
PROMPT_SINTESE_CONHECIMENTO_CALIBRADO = """Com base no fichamento estruturado:

TÍTULO: {titulo}

GERE SÍNTESE ESTRUTURADA:

### Conhecimento Transferência Identificado
[Que conhecimento externo o artigo identifica ser transferido?]

### Mecanismos de Absorção
[Que mecanismos o artigo identifica para absorção?]

### Barreiras Identificadas
[Que limitações ou barreiras encontra?]

### Aplicabilidade MPE Brasil
[Como achados do artigo se aplicam a MPEs brasileiras?]

### Recomendações para Pesquisa Futura
[Baseado em lacunas identificadas, o que seria próximo passo?]

Responda concisamente (máximo 1 página).
"""

# Variáveis para tracking de versão
VERSAO = "2.0"
DATA_CALIBRAGEM = "2026-04-13"
STATUS_CALIBRAGEM = "PENDENTE"  # Mude para "CONCLUÍDO" após calibragem
CONCORDANCIA_MEDIA = 0.0  # Será preenchido após calibragem
ARTIGOS_TESTADOS = 0

# Notas de mudanças na v2.0
NOTAS_VERSAO_2_0 = """
MUDANÇAS DA V1.0 PARA V2.0:

1. Prompts mais específicos para PRECISÃO (menos "criatividade")
2. Instruções críticas separadas com ⚠️ warning
3. Símbolo 🟡 introduzido para ambiguidade
4. Proposições específicas do projeto integradas
5. Contexto Brasil como seção obrigatória
6. Categoria de relevância (P1-P5) agora explícita

CALIBRAGEM ESPERADA:
- Concordância baseline: 75-80%
- Alvo pós-calibragem: 90%+
- Métrica: Similitude textual entre baseline e output IA

USO:
import prompts_calibrados as prompts_cal

prompt = prompts_cal.PROMPT_FICHAMENTO_CALIBRADO.format(
    article_content="..."
)
"""

def obter_status_calibragem():
    """Retorna status atual de calibragem"""
    return {
        'versao': VERSAO,
        'data_calibragem': DATA_CALIBRAGEM,
        'status': STATUS_CALIBRAGEM,
        'concordancia_media': CONCORDANCIA_MEDIA,
        'artigos_testados': ARTIGOS_TESTADOS,
    }

def atualizar_apos_calibragem(concordancia: float, n_artigos: int):
    """Atualiza variáveis após calibragem bem-sucedida"""
    global STATUS_CALIBRAGEM, CONCORDANCIA_MEDIA, ARTIGOS_TESTADOS
    STATUS_CALIBRAGEM = "CONCLUÍDO"
    CONCORDANCIA_MEDIA = concordancia
    ARTIGOS_TESTADOS = n_artigos
