# ⭐ COMECE AQUI - Guia de Início Rápido

## 👋 Bem-vindo!

Você está em um projeto de **Revisão Sistemática de Literatura** seguindo os princípios de **Open Science**. 

### ⚡ IMPORTANTE: Começar por AQUI
👉 **Se você quer implementar A/B Testing com 2 IAs**: Abra **`INICIO.md`** (5 minutos, muito claro)

---

Este documento é sobre a estrutura geral do projeto original. Para o A/B Testing, use `INICIO.md`.

---

## 🎯 O Que Você Vai Fazer

1. ✅ **Configurar o ambiente** (Python, dependências)
2. ✅ **Entender a estrutura** do projeto
3. ✅ **Executar os scripts** em ordem
4. ✅ **Validar resultados** manualmente
5. ✅ **Gerar o artigo** final

---

## ⚡ 5 Minutos: Configuração Rápida

### Passo 1: Abra o Terminal

```bash
cd /home/ismar/Área\ de\ trabalho/revisao-literatura-mestrado
```

### Passo 2: Crie um Ambiente Python

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instale Dependências

```bash
pip install -r requirements.txt
```

✅ **Pronto!** Seu ambiente está configurado.

---

## 🤖 NOVO: A/B Testing com Múltiplas IAs

Este projeto valida fichamentos usando **2 IAs independentes** (Claude + Gemini) para detectar vieses e aumentar confiabilidade.

**Como funciona?** Cada artigo é processado 2 vezes e comparado usando Krippendorff's Alpha.

**Para aprender e implementar**:  
👉 **GUIA-AB-TESTING-DEFINITIVO.md** ← Leia isto (passo-a-passo completo)

---

## 📚 15 Minutos: Entenda a Estrutura

### Pasta `docs/` - Documentação Científica
```
📚 Aqui está toda a teoria e planejamento
├── 00-ROTEIRO-COMPLETO.md (passo a passo)
├── PROTOCOLO-PRISMA-COMPLETO.md (protocolo PRISMA 2020 + 2024-IA)
├── 02-CRITERIOS-INCLUSAO.md (filtros para artigos)
├── 03-PALAVRAS-CHAVE.md (termos de busca)
└── framework/ (teorias)
```

### Pasta `scripts/` - Automação
```
🔧 Aqui estão os scripts Python que fazem o trabalho
├── 00-calibragem_prompts.py ⭐ NOVO! (Calibra prompts com seminais)
├── 01-busca_artigos.py (busca artigos)
├── 02-pdf_to_markdown.py (converte PDFs)
├── 03-fichamento_ia_krippendorff.py (fichamento A/B com scores)
├── 04-validacao_krippendorff.py (valida com Krippendorff's Alpha)
├── 05-sintese_qualitativa.py (sintetiza)
├── 06-ranking_relevancia.py ⭐ NOVO! (Ranking automático)
└── utils/ (utilitários e configurações)
```

### Pasta `articles/` - Artigos
```
📄 Aqui vão os artigos que você coletar
├── pdf/ (artigos originais em PDF)
└── md/ (convertidos para Markdown)
```

### Pasta `analysis/` - Análise
```
📊 Resultado final da análise
├── fichamentos/ (fichamentos em MD)
├── validacao/ (validação humana)
└── synthesis/ (síntese dos resultados)
```

---

## 🚀 30 Minutos: Execute o Primeiro Script

### Script 01: Buscar Artigos

```bash
python scripts/01-busca_artigos.py
```

**O que ele faz:**
- Busca artigos em bases (Scopus, Web of Science, etc)
- Salva os resultados em `data/raw/`
- Gera arquivo `search_results.csv`

**Saída esperada:**
```
✅ Busca em Scopus: 245 artigos
✅ Busca em Web of Science: 189 artigos
✅ Total: 434 artigos (após deduplicação)
📁 Salvos em: data/raw/consolidated_searches.csv
```

---

## 📖 Conheça os Templates

### Template: Fichamento

Veja `/analysis/fichamentos/TEMPLATE-FICHAMENTO.md`

Exemplo de um fichamento completo:

```markdown
# Fichamento: O Impacto da Capacidade Absortiva

**Referência Completa:**
Zahra, S. A., & George, G. (2002). Absorptive capacity and its determinants...

**Questão de Pesquisa:**
Como a capacidade absortiva afeta a inovação?

**Achados Principais:**
- A capacidade absortiva tem dois componentes: realização e transformação
- Firmas com maior AC conseguem explorar mais inovações externas

**Críticas e Limitações:**
- Estudos são principalmente em contexto de países desenvolvidos
- Faltam estudos em MPEs brasileiras

**Aplicação para Minha Pesquisa:**
Este artigo é fundamental para definir AC como construto central
```

### Template: Validação

Veja `/analysis/validacao/GUIA-VALIDACAO.md`

Checklist de validação:

```markdown
- [ ] Metadados completos e corretos?
- [ ] Resumo captura ideias principais?
- [ ] Achados estão bem sintetizados?
- [ ] Citações estão precisas?
- [ ] Alinhamento com framework teórico?
```

---

## 🔄 O Fluxo Completo (passo a passo)

```
┌──────────────────────────────────────────────────────────────┐
│ 1. PLANEJAMENTO (JÁ FEITO)                                   │
│    - Protocolo PRISMA ✅                                     │
│    - Framework conceitual ✅                                 │
│    - Critérios de inclusão ✅                                │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. BUSCA E COLETA (COMEÇAR AGORA)                            │
│    python scripts/01-busca_artigos.py                        │
│    → Artigos salvos em: data/raw/                            │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. CONVERSÃO PDF → MARKDOWN                                  │
│    python scripts/02-pdf_to_markdown.py                      │
│    → Arquivos em: articles/md/                               │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. FICHAMENTO COM IA                                         │
│    python scripts/03-fichamento_ia.py                        │
│    → Fichamentos em: analysis/fichamentos/                   │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 5. VALIDAÇÃO HUMANA (10-20% da amostra)                      │
│    Leia: analysis/validacao/GUIA-VALIDACAO.md               │
│    Valide: analysis/validacao/AMOSTRA-VALIDACAO.md          │
│    → Documente em: analysis/validacao/VALIDACOES-COMPLETAS  │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 6. SÍNTESE QUALITATIVA                                       │
│    python scripts/05-sintese_qualitativa.py                  │
│    → Matriz de síntese em: analysis/synthesis/               │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│ 7. REDAÇÃO DO ARTIGO ✍️                                       │
│    - Estruturar seções                                       │
│    - Redigir com base na síntese                             │
│    - Submeter para publicação                                │
└──────────────────────────────────────────────────────────────┘
```

---

## ⭐ NOVO: Fluxo com Calibragem e Ranking (Recomendado!)

Se você quer **máxima qualidade e eficiência**, siga este fluxo:

```
FASE 0: CALIBRAGEM ⭐ NOVO!
───────────────────────────
1. Selecione 15-20 artigos seminais que você já leu
   - Artigos clássicos (Cohen 1990, Zahra 2002)
   - Publicações do orientador
   - Sua pesquisa anterior

2. Faça fichamento MANUAL de cada um (sua leitura)
   Salve em: data/calibragem/leituras_baseline/

3. Liste no arquivo: data/calibragem/artigos_seminais.txt

4. Execute calibragem:
   python scripts/00-calibragem_prompts.py

5. Revise: analysis/calibragem/relatorio_calibragem.md
   - Procure por concordância ≥90%
   - Se <90%, refine prompts e reexecute

6. Aprove com: analysis/calibragem/CHECKLIST-PRE-FICHAMENTO.md
   ✅ Quando tudo verde, continue

⏱️  TEMPO: 1-2 horas (inclui leitura manual)
💡 BENEFÍCIO: Fichamentos 90%+ confiáveis (vs 75% sem calibragem)

───────────────────────────────────────────────────────────────
DEPOIS: Scripts regulares 01-05 (igual antes)
───────────────────────────────────────────────────────────────

FASE 3.5: RANKING DE RELEVÂNCIA ⭐ NOVO!
────────────────────────────────────────
Após Script 03 (fichamento), execute:

python scripts/06-ranking_relevancia.py

Output:
- ranking_relevancia.csv (artigos ordenados por relevância)
- relatorio_ranking.md (análise completa)

USE ESTE RANKING PARA:
✅ Revisar TOP 50% primeiro (mais relevantes)
✅ Descartar BOTTOM 20% com confiança (fora escopo)
✅ Economize 30-40% do tempo de revisão

⏱️  TEMPO: 5 minutos (automático)
💡 BENEFÍCIO: Revisão priorizada + documentação PRISMA
```

---

## 📋 Checklist de Execução

### Primeira Semana
- [ ] Configurar ambiente Python
- [ ] Ler [PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)
- [ ] Executar `scripts/01-busca_artigos.py`
- [ ] Verificar artigos em `data/raw/`

### Segunda Semana
- [ ] Executar `scripts/02-pdf_to_markdown.py`
- [ ] Revisar conversão em `articles/md/`
- [ ] Executar `scripts/03-fichamento_ia.py`
- [ ] Verificar fichamentos em `analysis/fichamentos/`

### Terceira Semana
- [ ] Selecionar amostra de validação (10%)
- [ ] Validar manualmente conforme [GUIA-VALIDACAO.md](analysis/validacao/GUIA-VALIDACAO.md)
- [ ] Documentar validações
- [ ] Fazer ajustes baseado em feedback

### Quarta Semana
- [ ] Executar `scripts/05-sintese_qualitativa.py`
- [ ] Analisar resultados
- [ ] Começar rascunho do artigo

---

## ❓ Dúvidas Frequentes

### P: Por onde começo?
**R:** Leia este arquivo e depois execute `scripts/01-busca_artigos.py`

### P: Como obtenho um API key?
**R:** Veja [SETUP.md](SETUP.md) - tem tutorial completo

### P: Posso usar meus próprios artigos?
**R:** Sim! Coloque PDFs em `articles/pdf/` e execute os scripts

### P: E se um script falhar?
**R:** Veja [TROUBLESHOOTING.md](TROUBLESHOOTING.md) ou abra uma issue

### P: Quanto tempo leva?
**R:** Depende da quantidade de artigos:
- 50 artigos: ~3 horas
- 100 artigos: ~6 horas
- 200+ artigos: ~1-2 dias (processamento em lotes)

### P: Preciso ter conhecimento técnico?
**R:** Não! Basta saber usar terminal e Python básico

---

## 🎓 Aprenda Mais

### Documentos Essenciais
1. **[PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)** - Protocolo PRISMA 2020 + 2024-IA (consolidado e completo)
2. **[FRAMEWORK-CONCEITUAL.md](docs/framework/FRAMEWORK-CONCEITUAL.md)** - 7 teorias explicadas
3. **[scripts/README.md](scripts/README.md)** - Documentação técnica

### Recursos Externos
- 📘 [PRISMA 2020 Guidelines](https://www.prisma-statement.org/)
- 📘 [Open Science Framework](https://osf.io/)
- 📘 [Python for Research](https://www.coursera.org/learn/python-research)

---

## 🚨 Antes de Começar: Coisas Importantes

⚠️ **Segurança de API Keys:**
```
NUNCA faça commit de API keys!
Coloque em .env e adicione ao .gitignore
```

⚠️ **Backup Regular:**
```
Faça backup de:
- data/raw/ (artigos)
- analysis/ (fichamentos e validações)
- articles/md/ (markdown convertidos)
```

⚠️ **Documentação:**
```
Sempre documente decisões importantes
Deixe comentários nos scripts
Mantenha changelog atualizado
```

---

## 🌟 Recurso Especial: A/B Testing com 2 IAs

Este projeto usa uma abordagem inovadora de **A/B Testing** para validar fichamentos:

```
ARTIGO
  ├─→ Claude (Rigoroso)    ✅
  ├─→ Gemini (Criativo)    ✅
  └─→ Comparação           📊
      └─→ Concordância 85%+ → ✅ VALIDADO
```

**Por quê**? 
- Elimina vieses de uma única IA
- Detecta texto ambíguo automaticamente
- Aumenta confiança nos dados
- Alinhado com PRISMA 2020 (transparência)

**Aprenda mais**: `docs/02-METODOLOGIA-IA-AB-TESTING.md`

---

## ✅ Você Está Pronto!

Agora você pode:
1. ✅ Entender a estrutura
2. ✅ Configurar o ambiente
3. ✅ Executar scripts
4. ✅ Validar resultados
5. ✅ Gerar o artigo final

## 🚀 Próximo Passo

Abra o terminal e execute:

```bash
python scripts/01-busca_artigos.py
```

Boa sorte! 🎉

---

*Dúvidas? Leia [README.md](README.md) para mais informações.*
