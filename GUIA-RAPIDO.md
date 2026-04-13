# ⚡ Guia Rápido de Uso

> **Objetivo**: Começar a usar o framework em menos de 30 minutos

---

## 🎯 Para quem é este guia?

Este guia é para você que:
- ✅ Já leu o [README.md](README.md) e entendeu o projeto
- ✅ Tem seus dados (CSVs de buscas) prontos
- ✅ Quer executar os scripts rapidamente

---

## ⚡ Início em 5 Passos

### Passo 1: Clone e Configure (5 min)

```bash
# Clone o repositório
git clone git@github.com:drower22/revisao-literatura-ia.git
cd revisao-literatura-ia

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OU: venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt
```

### Passo 2: Configure APIs (3 min)

```bash
# Crie arquivo .env
touch .env

# Adicione suas chaves (edite com seu editor)
echo "ANTHROPIC_API_KEY=sua_chave_claude" >> .env
echo "GOOGLE_API_KEY=sua_chave_gemini" >> .env
```

**Obter chaves**:
- Claude: https://console.anthropic.com/
- Gemini: https://makersuite.google.com/app/apikey

### Passo 3: Prepare Seus Dados (5 min)

```bash
# Crie estrutura de pastas (se não existir)
mkdir -p data/raw
mkdir -p data/processed
mkdir -p articles/pdf
mkdir -p articles/md
mkdir -p analysis/fichamentos

# Copie seus CSVs para data/raw/
# Exemplo:
# cp ~/Downloads/scopus_results.csv data/raw/
# cp ~/Downloads/wos_results.csv data/raw/
```

**Formato esperado do CSV**:
- Colunas obrigatórias: `titulo`, `keywords`, `abstract`, `revista`, `doi`, `autores`, `ano`, `citacoes`

### Passo 4: Execute Pipeline Básico (10 min)

```bash
# 1. Consolidar buscas
python scripts/01-busca_artigos.py

# 2. Ranking de relevância (remove duplicatas)
python scripts/06-ranking_relevancia.py

# Veja os resultados
cat data/processed/artigos_ranqueados.csv | head -20
```

### Passo 5: Fichamento Completo (variável)

```bash
# Opcional: Calibrar prompts primeiro (recomendado)
python scripts/00-calibragem_prompts.py

# Converter PDFs para Markdown
python scripts/02-pdf_to_markdown.py

# Fichamento com IA (Claude + Gemini)
python scripts/03-fichamento_ia_krippendorff.py

# Validar concordância
python scripts/04-validacao_krippendorff.py

# Gerar síntese
python scripts/05-sintese_qualitativa.py
```

---

## 📊 Ordem de Execução Recomendada

```
┌─────────────────────────────────────────────────┐
│ FASE 0: CALIBRAGEM (Opcional mas recomendado)   │
│ python scripts/00-calibragem_prompts.py         │
│ Tempo: 1-2h | Benefício: +15% qualidade         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 1: CONSOLIDAÇÃO                            │
│ python scripts/01-busca_artigos.py              │
│ Tempo: 5 min                                    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 2: RANKING (Remove duplicatas + filtra)    │
│ python scripts/06-ranking_relevancia.py         │
│ Tempo: 10 min | Economiza: 40-60% depois        │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 3: CONVERSÃO                               │
│ python scripts/02-pdf_to_markdown.py            │
│ Tempo: 2-3 min/100 PDFs                         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 4: FICHAMENTO (A/B Testing)                │
│ python scripts/03-fichamento_ia_krippendorff.py │
│ Tempo: 30-60 min/100 artigos                    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 5: VALIDAÇÃO                               │
│ python scripts/04-validacao_krippendorff.py     │
│ Tempo: 5 min                                    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ FASE 6: SÍNTESE                                 │
│ python scripts/05-sintese_qualitativa.py        │
│ Tempo: 10 min                                   │
└─────────────────────────────────────────────────┘
```

---

## 🔍 Verificando Resultados

### Após Script 01 (Consolidação)
```bash
# Ver quantos artigos foram consolidados
wc -l data/processed/artigos_consolidados.csv

# Ver primeiras linhas
head -10 data/processed/artigos_consolidados.csv
```

### Após Script 06 (Ranking)
```bash
# Ver artigos ranqueados
cat data/processed/artigos_ranqueados.csv | head -20

# Ver relatório de ranking
cat analysis/relevancia/relatorio_ranking.md
```

### Após Script 04 (Validação)
```bash
# Ver Krippendorff's Alpha
cat analysis/validacao/krippendorff_alpha_resultado.txt

# Alpha >= 0.70 = ✅ Qualidade aprovada
# Alpha < 0.70 = ⚠️ Revisar prompts
```

---

## 💡 Dicas Importantes

### ✅ Faça
- Execute os scripts na ordem recomendada
- Leia os relatórios gerados em `analysis/`
- Faça backup de `data/` e `analysis/` regularmente
- Use a calibragem (Script 00) para melhor qualidade
- Revise o ranking antes de baixar todos os PDFs

### ❌ Evite
- Pular a etapa de ranking (economiza muito tempo)
- Executar scripts fora de ordem
- Modificar arquivos em `data/processed/` manualmente
- Usar apenas 1 IA (perde validação A/B)
- Ignorar Krippendorff's Alpha < 0.60

---

## 🆘 Troubleshooting Rápido

### Erro: "No module named 'anthropic'"
```bash
pip install anthropic google-generativeai python-dotenv
```

### Erro: "API key not found"
```bash
# Verifique se .env existe
cat .env

# Se não, crie:
echo "ANTHROPIC_API_KEY=sua_chave" > .env
echo "GOOGLE_API_KEY=sua_chave" >> .env
```

### Erro: "File not found"
```bash
# Verifique se está no diretório correto
pwd

# Deve mostrar: .../revisao-literatura-mestrado
```

### Script travou ou muito lento
```bash
# Ctrl+C para cancelar
# Verifique conexão internet
# Verifique se APIs estão funcionando
```

---

## 📚 Próximos Passos

Após executar o pipeline básico:

1. **Leia a documentação completa**: [PIPELINES.md](PIPELINES.md)
2. **Entenda a metodologia**: [docs/PROTOCOLO-PRISMA-COMPLETO.md](docs/PROTOCOLO-PRISMA-COMPLETO.md)
3. **Customize para seu tema**: Edite prompts e dicionários
4. **Contribua**: Abra issues ou PRs com melhorias

---

## 📞 Precisa de Ajuda?

- 📖 **Documentação completa**: [README.md](README.md)
- 🐙 **GitHub Issues**: https://github.com/drower22/revisao-literatura-ia/issues
- 💬 **Discussões**: GitHub Discussions

---

**Última atualização**: 13 de Abril de 2026  
**Tempo estimado total**: 30 minutos (setup) + 4-8 horas (processamento)
