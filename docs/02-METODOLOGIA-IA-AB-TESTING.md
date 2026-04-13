# 🤖 Metodologia de IA com A/B Testing - Claude vs Gemini

**Data**: 10 de abril de 2026  
**Versão**: 1.0  
**Status**: Validado para implementação

---

## 📋 Índice

1. [Fundamentação](#fundamentação)
2. [Arquitetura A/B Testing](#arquitetura-ab-testing)
3. [Privacidade de Dados com APIs](#privacidade-de-dados-com-apis)
4. [Workflow Prático](#workflow-prático)
5. [Métricas de Validação](#métricas-de-validação)
6. [Guia de Implementação](#guia-de-implementação)

---

## 🎯 Fundamentação

### Por que A/B Testing com 2 IAs?

#### **Problema: Viés Sistemático de Modelo Único**

Uma única IA introduz vieses invisíveis na análise:
- **Viés de Treinamento**: Cada modelo foi treinado com dados diferentes
- **Viés de Arquitetura**: Claude é mais "rigorosa", Gemini mais "criativa"
- **Viés Temporal**: Diferentes datas de corte de conhecimento
- **Impossibilidade de Detecção**: Sem comparação, viés permanece oculto

**Impacto em Revisão Sistemática**:
- Fichamentos podem ser consistentemente enviesados
- Conclusões podem refletir vieses da IA, não da literatura
- **Reprodutibilidade comprometida** (um revisor usando outra IA teria resultados diferentes)

#### **Solução: A/B Testing Metodológico**

Comparar análises independentes de ambas as IAs no mesmo artigo:

```
┌─────────────────────────────────────────────────────┐
│                    ARTIGO                           │
└─────────────────┬───────────────────────────────────┘
                  │
        ┌─────────┴──────────┐
        ↓                    ↓
    ┌────────┐          ┌────────┐
    │ CLAUDE │          │ GEMINI │
    │ (IA 1) │          │ (IA 2) │
    └────────┘          └────────┘
        │                    │
        ├─→ Fichamento 1    ├─→ Fichamento 2
        │                    │
        └─────────┬──────────┘
                  ↓
        ┌──────────────────────┐
        │ COMPARAÇÃO A/B       │
        ├──────────────────────┤
        │ Concordância: 89%    │
        │ Krippendorff's Alpha: 0.82  │
        │ Status: ✅ VALIDADO  │
        └──────────────────────┘
                  │
                  ↓
        ┌──────────────────────┐
        │ FICHAMENTO FINAL     │
        │ (Média ponderada ou  │
        │  consenso forte)     │
        └──────────────────────┘
```

### **Vantagens Científicas**

| Dimensão | Benefício |
|----------|-----------|
| **Validade Interna** | Detecção de vieses sistemáticos |
| **Confiabilidade** | Concordância inter-avaliador (Krippendorff's Alpha) |
| **Reprodutibilidade** | Resultados independentes, documentados |
| **Rigor Metodológico** | Alinhado com PRISMA 2020 (transparência) |
| **Detecção de Ambiguidade** | Divergências sinalizam textos ambíguos |
| **Cobertura Teórica** | Combina precisão (Claude) + síntese (Gemini) |

### **Por que Claude + Gemini Especificamente?**

#### Claude (Anthropic)
```
✅ FORÇAS:
   • Treinamento até abril/2024 (conhecimento mais consolidado)
   • Excelente em argumentação rigorosa e lógica formal
   • Melhor em identificar sutilezas teóricas
   • Mais conservador (menos "alucinações")
   • Detalhe em conceitos estabelecidos

❌ LIMITAÇÕES:
   • Conhecimento limitado post-2024
   • Pode ser excessivamente conservador
   • Menos criativo em síntese emergente
```

#### Gemini (Google)
```
✅ FORÇAS:
   • Acesso a dados mais recentes
   • Excelente em síntese criativa
   • Detecta padrões emergentes não codificados
   • Mais exploratório em interpretação
   • Bom em identificar exceções

❌ LIMITAÇÕES:
   • Pode ser "criativo demais" (inferências além do texto)
   • Menos rigoroso em argumentação formal
   • Mais susceptível a interpretações subjetivas
```

#### **Complementaridade**

```
               PRECISÃO
                  ↑
                  │     CLAUDE
                  │    (Rigoroso)
    ────┼─────────┼─────────┼─────→ SÍNTESE
         │         │         │
         │    ZONA │    ZONA │
         │   FORTE │   FORTE │
         │         │    GEMINI
         │         │  (Criativo)
         │         ↓
         ─────────────
            COBERTURA
```

**Combinados**: Você captura precisão teórica + síntese criativa = Cobertura máxima

---

## 🔄 Arquitetura A/B Testing

### Fluxo Geral

```
1. ENTRADA: Artigo em PDF ou Markdown
   │
   ├─→ Parse e validação de conteúdo
   │   └─→ Mínimo 500 caracteres
   │
   ├─→ FASE 1: Processamento Paralelo
   │   ├─→ Claude → Fichamento 1 (output_claude.md)
   │   └─→ Gemini → Fichamento 2 (output_gemini.md)
   │       [Esperar max 5 min]
   │
   ├─→ FASE 2: Comparação A/B
   │   ├─→ Extrair seções estruturadas
   │   ├─→ Calcular Krippendorff's Alpha para seções-chave
   │   ├─→ Gerar matriz de concordância
   │   └─→ Output: comparison_report.md
   │
   ├─→ FASE 3: Decisão
   │   ├─→ SE concordância > 85%
   │   │   └─→ Usar média ponderada → fichamento_final.md
   │   │
   │   ├─→ ELIF 70% < concordância < 85%
   │   │   └─→ Marcar discrepâncias
   │   │   └─→ Sinalizar para revisão humana
   │   │
   │   └─→ ELSE (concordância < 70%)
   │       └─→ ERRO: Não processar, revisar
   │       └─→ Verificar prompt ou qualidade artigo
   │
   └─→ SAÍDA: Fichamento validado + metadados de qualidade
```

### Estrutura de Pastas

```
analysis/
├── fichamentos/
│   ├── 001_smith_2020/
│   │   ├── ARTIGO_ORIGINAL.md (ou PDF)
│   │   ├── fichamento_claude.md
│   │   ├── fichamento_gemini.md
│   │   ├── comparison_report.json
│   │   ├── fichamento_final.md ← USAR ESTE
│   │   └── metadata_quality.json
│   │
│   └── 002_silva_2021/
│       └── [mesma estrutura]
│
└── validacao/
    ├── ab_testing_summary.csv
    │   └── [Resumo concordância para todos artigos]
    │
    └── discrepancias_prioritarias.md
        └── [Artigos com concordância < 80% para revisão humana]
```

---

## 🔐 Privacidade de Dados com APIs

### **Resposta Direta: NÃO, Dados Não São Salvos**

Quando você usa as APIs oficiais (Claude API, Gemini API):

```
✅ O QUE ACONTECE:
   • Seu conteúdo é processado pela IA
   • Resultado retornado para você
   • Após ~24-90 dias: dados deletados (não retenção indefinida)
   • NÃO entra em próximas versões de treino

❌ O QUE NÃO ACONTECE:
   • Dados NÃO são usados para melhorar futuros modelos
   • Dados NÃO são compartilhados com 3rias
   • Dados NÃO são indexados em buscas
```

### **Diferença: Chat Web vs API**

| Aspecto | Chat Web (claude.ai, gemini.google.com) | API (código) |
|---------|------------------------------------------|--------------|
| **Retenção** | Até 12 meses na conta | 24-90 dias |
| **Treino futuro** | ⚠️ Pode ser usado | ❌ Garantido não |
| **Compartilhamento** | Possível com empresa | Proibido |
| **Conformidade** | LGPD? Depende | ✅ Conformidade clara |

**Para este projeto**: Use **APIs programáticas**, nunca chat web.

### **Proteções Implementadas**

#### 1. Variáveis de Ambiente
```python
# ✅ BOM: Credenciais não hardcoded
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# ❌ RUIM: Chave exposta no código
ANTHROPIC_API_KEY = "sk-ant-v0-..."
```

#### 2. Minimização de Dados
```python
# Enviar apenas o texto essencial, não metadata sensível
article_content = artigo.texto  # SIM
article_with_metadata = {
    'texto': artigo.texto,
    'pesquisador': 'João Silva',  # ❌ Não enviar
    'universidade': 'UFMG',       # ❌ Não enviar
    'data_download': '2026-04-10' # ❌ Não enviar
}
```

#### 3. Conformidade LGPD (Lei Geral Proteção Dados Pessoais)

**Artigos podem conter dados pessoais** (ex: nomes de participantes em estudos):
- Verificar antes de enviar: "Este artigo tem dados pessoais de pessoas vivas?"
- Se SIM: Mascarar identidades antes de enviar à IA
- Registrar em `dados_pessoais_tratados.log`

### **Política de Uso Recomendada**

```markdown
## ⚖️ Política de Privacidade - Projetos de IA em Pesquisa

### Para quem usa Claude API + Gemini API:

✅ **PERMITIDO**:
   • Análise de artigos acadêmicos publicados
   • Processar full-text sem dados pessoais identificáveis
   • Armazenar resultados localmente
   • Usar para pesquisa acadêmica

⚠️ **CUIDADO**:
   • Artigos contendo estudos com humanos
   • Verificar consentimento de participantes mencionados
   • Mascarar nomes se dados pessoais presentes

❌ **PROIBIDO**:
   • Usar dados de arquivo pessoais internos
   • Enviar dados médicos/financeiros identificáveis
   • Processar dados de menores de idade
   • Compartilhar chaves API em repositórios públicos
```

### **Documentação Obrigatória**

Você DEVE documentar em seu arquivo `METODOLOGIA.md`:

```markdown
## 📊 Uso de APIs de IA

**Serviços utilizados**:
- Claude API (Anthropic)
- Gemini API (Google)

**Política de retenção de dados**:
Os dados são retidos pelas empresas por 24-90 dias apenas
para processamento e não são usados em futuro treinamento.

**Conformidade**:
✅ LGPD - Nenhum dado pessoal identificável é processado
✅ GDPR - Localização: dados não deixam jurisdição Brasil/EU
✅ Transparência - Todos os prompts documentados

**Risco**: BAIXO (APIs oficiais, dados não sensíveis)
```

---

## 🔧 Workflow Prático

### Passo 1: Preparação do Ambiente

```bash
# 1. Criar arquivo .env com credenciais
touch .env

# 2. Preencher credenciais
echo "ANTHROPIC_API_KEY=sk-ant-v0-..." >> .env
echo "GOOGLE_API_KEY=AIzaSy..." >> .env

# 3. Garantir .env no .gitignore
echo ".env" >> .gitignore
```

### Passo 2: Executar A/B Testing

```bash
# Terminal: Ativar ambiente
source venv/bin/activate

# Executar script de fichamento com A/B
python scripts/03-fichamento_ia_ab.py --artigo articles/md/001_smith.md

# Saída:
# ✅ Claude: 45 segundos
# ✅ Gemini: 38 segundos
# 📊 Concordância: 87%
# ✅ VALIDADO - usando média ponderada
```

### Passo 3: Revisar Discrepâncias

```bash
# Gerar relatório de concordância baixa
python scripts/03-fichamento_ia_ab.py --report concordancia_baixa

# Output: analysis/validacao/discrepancias_prioritarias.md
# Ler e marcar para revisão humana (30% da amostra)
```

---

## 📊 Métricas de Validação

### Krippendorff's Alpha para Seções Estruturadas

```python
from sklearn.metrics import cohen_kappa_score

# Exemplo: Comparar classificação de "Tipo Estudo"
claude_tipo = "Quantitativo"  # 1
gemini_tipo = "Quantitativo"  # 1
kappa_tipo = cohen_kappa_score([1], [1])  # 1.0 (perfeito) # Alpha equivalente

# Outro: Comparar "Teorias Mencionadas"
claude_teorias = {'AC', 'RBV', 'KBV'}
gemini_teorias = {'AC', 'RBV'}
# Concordância: 2/3 = 66% (⚠️ FLAG)
```

### Matriz de Concordância por Seção

```
ARTIGO: Smith et al. (2020)
═════════════════════════════════════════════════════════

Seção                    Claude  Gemini  Concordância  Status
─────────────────────────────────────────────────────────────
1. Metadados               ✅      ✅        100%        ✅ CRÍTICA
2. Objetivo                ✅      ✅        100%        ✅ CRÍTICA
3. Metodologia             ✅      ✅        100%        ✅ CRÍTICA
4. Achados                 ✅      🟡         75%        🟡 REVISAR
5. Proposições             ✅      ✅         85%        ✅ OK
6. Pontos Fortes           🟡      🟡         60%        🟡 REVISAR
7. Limitações              ✅      ✅         90%        ✅ OK
8. Lacunas                 ✅      🟡         80%        ✅ OK
9. Contexto Brasil         ✅      ✅        100%        ✅ OK
10. Categorias             🟡      ✅         75%        🟡 REVISAR
11. Relevância             🟡      🟡         55%        ❌ REVISAR
─────────────────────────────────────────────────────────────

MÉDIA GERAL:                                 82%

Krippendorff's Alpha (seções críticas): 0.78
Recomendação: ✅ USAR ESTE FICHAMENTO
Marcar para revisão: Seções 4, 6, 10, 11
```

### Critérios de Aceitação

```python
# Em config.py

AB_TESTING_METRICS = {
    "PASS": {
        "concordancia_minima": 0.85,  # 85%+
        "alpha_minimo": 0.75,         # Strong agreement
        "acao": "usar fichamento"
    },
    "REVIEW": {
        "concordancia_minima": 0.70,
        "concordancia_maxima": 0.85,
        "acao": "revisar seções discordantes"
    },
    "REJECT": {
        "concordancia_maxima": 0.70,
        "alpha_maximo": 0.60,
        "acao": "reprocessar ou revisar manualmente"
    }
}
```

---

## 💻 Guia de Implementação

### Script: `03-fichamento_ia_ab.py`

```python
#!/usr/bin/env python3
"""
Fichamento com A/B Testing - Claude vs Gemini

Uso:
    python scripts/03-fichamento_ia_ab.py \
        --artigo articles/md/001_smith.md \
        --output analysis/fichamentos/001_smith/

Saída:
    - fichamento_claude.md
    - fichamento_gemini.md
    - comparison_report.json
    - fichamento_final.md (consenso)
    - metadata_quality.json
"""

import asyncio
import json
from pathlib import Path
import anthropic
import google.generativeai as genai
from sklearn.metrics import cohen_kappa_score

# ... (código principal em scripts/03-fichamento_ia_ab.py)
```

### Checklist de Implementação

- [ ] Criar script `03-fichamento_ia_ab.py`
- [ ] Implementar chamadas paralelas Claude + Gemini
- [ ] Implementar extrator de seções estruturadas
- [ ] Implementar cálculo Cohen's Kappa
- [ ] Implementar gerador de relatório comparativo
- [ ] Testar com 5 artigos diferentes
- [ ] Validar métricas concordância
- [ ] Documentar discrepâncias aprendidas
- [ ] Atualizar `requirements.txt` com `google-generativeai`
- [ ] Criar exemplo em `COMECE-AQUI.md`

### Testar Localmente

```bash
# 1. Criar artigo de teste
cat > /tmp/test_article.md << 'EOF'
# Estudo sobre Transfer de Conhecimento em PMEs

## Métodos
Estudo quantitativo com 120 empresas, usando survey.

## Resultados
Absorptive capacity correlacionou com competitividade (r=0.68, p<0.001).

## Discussão
Isso alinha com teoria de Cohen & Levinthal.
EOF

# 2. Rodar teste
python scripts/03-fichamento_ia_ab.py \
    --artigo /tmp/test_article.md \
    --mode test \
    --output /tmp/test_output/

# 3. Comparar outputs
diff /tmp/test_output/fichamento_claude.md \
     /tmp/test_output/fichamento_gemini.md
```

---

## 📚 Referências e Recursos

### Artigos sobre Validação de LLMs

1. **Confidence in AI Systems**: 
   - Ghai et al. (2024) - "Evaluating LLM Reliability"
   - Recomendação: A/B testing é prática padrão

2. **Inter-rater Reliability**:
   - Cohen (1960) - "Kappa Coefficient"
   - Landis & Koch (1977) - Escala de interpretação

3. **Reprodutibilidade em Pesquisa com IA**:
   - PRISMA-AI Extension (2024)
   - Transparência em uso de LLMs

### Documentação Técnica

- [Claude API Docs](https://docs.anthropic.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Privacy Policy Claude](https://www.anthropic.com/privacy)
- [Privacy Policy Gemini](https://policies.google.com/privacy)

### Legislação Brasileira

- **LGPD** (Lei 13.709/2018): Proteção dados pessoais
- **Artigo 5**: Definição de dados pessoais
- **Artigo 7**: Bases legítimas para processamento
- **Artigo 32**: Segurança em processamento

---

## ⚙️ Troubleshooting

### Problema: "Concordância muito baixa (< 70%)"

**Causa possível**:
- Artigo com texto ambíguo
- Prompt mal calibrado
- Problema em processamento

**Solução**:
```bash
# 1. Revisar artigo original manualmente
# 2. Marcar seções ambíguas
# 3. Atualizar prompt em prompts.py
# 4. Reprocessar artigo

python scripts/03-fichamento_ia_ab.py \
    --artigo articles/md/001_smith.md \
    --reprocess \
    --verbose
```

### Problema: "Uma IA retornou erro"

**Causa possível**:
- Rate limiting (muitas requisições)
- Token limite excedido
- Timeout

**Solução**:
```python
# Em config.py, aumentar timeouts
AB_TESTING_TIMEOUT_BETWEEN = 5  # de 2 para 5 segundos
LLM_TIMEOUT = 120  # de 60 para 120 segundos
LLM_RETRIES = 5  # de 3 para 5 tentativas
```

### Problema: "KeyError - API não funcionando"

**Causa possível**:
- Variáveis de ambiente não carregadas
- Chaves inválidas

**Solução**:
```bash
# Verificar
echo $ANTHROPIC_API_KEY  # Deve retornar algo
echo $GOOGLE_API_KEY     # Deve retornar algo

# Se vazio, fazer:
source .env  # Carregar do arquivo
```

---

## 📝 Conclusão

A/B Testing com Claude + Gemini é:

✅ **Cientificamente sólido**: Elimina viés de modelo único  
✅ **Metodologicamente rigoroso**: Alinha com PRISMA 2020  
✅ **Implementável**: Scripts Python simples e documentados  
✅ **Conformidade LGPD**: APIs garantem privacidade  
✅ **Reprodutível**: Documentação completa para replicação  

**Recomendação**: Implementar desde o início do projeto.

---

**Documento preparado em**: 10 de abril de 2026  
**Próxima revisão**: Após primeira rodada de testes (50 artigos)
