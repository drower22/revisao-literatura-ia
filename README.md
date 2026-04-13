# Revisão Si## 🚀 Destaques Metodológicos

### ✨ Inovação: A/B Testing com 2 IAs (Claude + Gemini)

Este projeto implementa **validação robusta de fichamentos** usando duas IAs independentes para eliminar viés de modelo único.

**O que é?**  
Cada artigo é processado 2 vezes (Claude + Gemini) e comparado usando Krippendorff's Alpha.

**Por quê?**  
Detecta vieses invisíveis e aumenta confiança nos dados.

**Como começar?**  
� **ABRA ISTO PRIMEIRO**: `INICIO.md`

Ele irá guiá-lo através de:
- `GUIA-AB-TESTING.md` - Implementação passo-a-passo (PRINCIPAL)
- `BANCA.md` - Argumentação para defesa
- `docs/02-METODOLOGIA-IA-AB-TESTING.md` - Referência técnica

---

## 📋 Estrutura do Projetoteratura - Open Science

## 📚 Projeto: Transferência de Conhecimento, Absorptive Capacity e Competitividade em MPEs Brasileiras

**Objetivo**: Realizar uma revisão sistemática robusta, replicável e transparente sobre transferência de conhecimento externo, capacidade absortiva e competitividade em Micro e Pequenas Empresas (MPEs) brasileiras.

**Conformidade**: PRISMA 2020, Open Science, Práticas de Ciência Aberta

**Status**: 🟢 Em construção

---

## � Destaques Metodológicos

### ✨ Inovações deste Projeto

| Inovação | Benefício | Documentação |
|----------|----------|----------------|
| **A/B Testing com 2 IAs** | Elimina viés de modelo único (Claude + Gemini) | `docs/02-METODOLOGIA-IA-AB-TESTING.md` |
| **Validação Inter-IA** | Krippendorff's Alpha para confiabilidade | Seção Métricas |
| **Conformidade LGPD** | APIs não salvam dados para treino futuro | `docs/02-METODOLOGIA-IA-AB-TESTING.md#privacidade` |
| **Rastreabilidade Completa** | Todos prompts documentados e versionados | `scripts/utils/prompts.py` |
| **Open Science** | Código, dados, métodos 100% replicáveis | GitHub (em breve) |

---

## �📋 Estrutura do Projeto

```
revisao-literatura-mestrado/
├── README.md                          # Este arquivo
├── docs/                              # Documentação
│   ├── 00-ROTEIRO-EXECUTIVO.md       # Guia passo a passo
│   ├── PROTOCOLO-PRISMA-COMPLETO.md  # Protocolo PRISMA 2020 + 2024-IA (ÚNICO)
│   ├── 02-CRITERIOS-INCLUSAO.md      # Critérios detalhados
│   ├── 03-PALAVRAS-CHAVE.md          # Estratégia de busca
│   └── framework/
│       ├── FRAMEWORK-CONCEITUAL.md   # Modelo teórico integrado
│       └── PROPOSICOES-PESQUISA.md   # Proposições testáveis
├── scripts/                           # Automação Python
│   ├── 01-busca_artigos.py           # Busca em bases de dados
│   ├── 02-pdf_to_markdown.py         # Conversão PDF → MD
│   ├── 03-fichamento_ia.py           # Fichamento com IA
│   ├── 04-validacao_amostra.py       # Validação por humano
│   ├── 05-sintese_qualitativa.py     # Análise qualitativa
│   └── utils/
│       ├── prompts.py                # Prompts para IA
│       ├── validators.py             # Validações
│       └── config.py                 # Configurações
├── data/
│   ├── raw/                          # Dados brutos
│   │   └── busca_resultados.csv      # Resultados das buscas
│   ├── processed/                    # Dados processados
│   │   ├── artigos_filtrados.csv     # Após critérios
│   │   └── metadados.json            # Metadados estruturados
│   └── extracts/                     # Extratos de artigos
├── articles/
│   ├── pdf/                          # PDFs originais
│   └── md/                           # Conversão Markdown
├── analysis/
│   ├── fichamentos/                  # Fichamentos em MD
│   │   ├── fichamento_001.md
│   │   └── ...
│   ├── validacao/                    # Validação humana
│   │   ├── amostra_validacao.csv     # Amostra para validação
│   │   ├── feedback_revisor.md       # Feedback do revisor
│   │   └── matriz_validacao.csv      # Matriz de validação
│   └── synthesis/                    # Síntese qualitativa
│       ├── mapa_conceitual.md        # Mapeamento de conceitos
│       ├── lacunas_identificadas.md # Gaps na literatura
│       ├── problemas_pesquisa.md    # Problemas emergentes
│       └── relatorio_final.md        # Relatório de achados
└── .gitignore                        # Git ignore
```

---

## 🎯 Fases do Projeto

### **FASE 1: Planejamento e Protocolo (Semana 1)**
- [x] Definir framework conceitual
- [ ] Documentar protocolo PRISMA
- [ ] Definir critérios de inclusão/exclusão
- [ ] Estabelecer estratégia de busca

📄 Saídas: `docs/PROTOCOLO-PRISMA-COMPLETO.md`, `docs/02-CRITERIOS-INCLUSAO.md`

### **FASE 2: Busca Sistemática (Semana 2-3)**
- [ ] Executar buscas em bases de dados
- [ ] Registrar resultados (EndNote, Mendeley ou CSV)
- [ ] Aplicar filtros automáticos
- [ ] Exportar metadados

📄 Saídas: `data/raw/busca_resultados.csv`, `data/processed/artigos_filtrados.csv`

### **FASE 3: Conversão de Artigos (Semana 4)**
- [ ] Baixar PDFs dos artigos selecionados
- [ ] Converter PDF → Markdown com IA
- [ ] Validar qualidade da conversão
- [ ] Organizar em pasta estruturada

📄 Saídas: `articles/md/*.md` (arquivos convertidos)

### **FASE 4: Fichamento com IA A/B Testing (Semana 5-6)**
- [ ] Aplicar template de fichamento com A/B Testing
- [ ] Executar Claude + Gemini em paralelo (validação robusta)
- [ ] Comparar fichamentos (Krippendorff's Alpha, concordância)
- [ ] Codificar por teorias/proposições
- [ ] Gerar fichamentos finais com metadados de qualidade

**Inovação**: Uso de **A/B Testing com 2 IAs** (Claude + Gemini)
- Elimina vieses sistemáticos de modelo único
- Detecta ambiguidades no texto original
- Aumenta confiabilidade dos dados extraídos
- Alinhado com PRISMA 2020 (transparência metodológica)

📄 Saídas: `analysis/fichamentos/*.md` (validados), `docs/02-METODOLOGIA-IA-AB-TESTING.md`

### **FASE 5: Validação de Amostra (Semana 7)**
- [ ] Sortear amostra aleatória (30-40% dos fichamentos)
- [ ] Revisor humano valida fichamentos
- [ ] Registrar discrepâncias e feedback
- [ ] Calcular taxa de concordância (Krippendorff's Alpha)
- [ ] Refinar critérios se necessário

📄 Saídas: `analysis/validacao/amostra_validacao.csv`, `analysis/validacao/feedback_revisor.md`

### **FASE 6: Síntese Qualitativa (Semana 8-9)**
- [ ] Analisar padrões entre fichamentos
- [ ] Mapear conceitos e relações
- [ ] Identificar lacunas na literatura
- [ ] Formular problemas de pesquisa
- [ ] Gerar matriz de achados

📄 Saídas: `analysis/synthesis/mapa_conceitual.md`, `analysis/synthesis/problemas_pesquisa.md`

### **FASE 7: Redação do Artigo (Semana 10-12)**
- [ ] Elaborar introdução
- [ ] Descrever metodologia (PRISMA)
- [ ] Apresentar resultados
- [ ] Discussão crítica
- [ ] Conclusões e lacunas

📄 Saídas: `artigo_final.md`, `artigo_final.docx`

---

## 🔑 Princípios de Open Science

Este projeto segue os princípios FAIR:

- **F**indable: Tudo documentado e versionado no Git
- **A**ccessible: Todos os arquivos e scripts públicos
- **I**nteroperable: Formatos abertos (MD, CSV, JSON)
- **R**eusable: Replicável por outros pesquisadores

### Transparência
- ✅ Protocolo completo registrado antes da busca
- ✅ Critérios de inclusão/exclusão explícitos
- ✅ Scripts automatizados e comentados
- ✅ Validação independente por humano
- ✅ Dados brutos e processados disponíveis

---

## 🛠️ Ferramentas Utilizadas

| Ferramenta | Função | Status |
|-----------|--------|--------|
| **Python 3.11+** | Automação de busca e processamento | ✅ |
| **PyPDF/pdfplumber** | Extração de texto de PDFs | ✅ |
| **LLM (OpenAI/Claude)** | Fichamento e síntese | ✅ |
| **Pandas** | Manipulação de dados | ✅ |
| **Git/GitHub** | Versionamento | ✅ |
| **Markdown** | Documentação | ✅ |
| **CSV/JSON** | Armazenamento estruturado | ✅ |

---

## 📖 Como Usar Este Repositório

### Início Rápido

1. **Clonar o repositório**
   ```bash
   git clone [url]
   cd revisao-literatura-mestrado
   ```

2. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ler o protocolo**
   ```bash
   cat docs/00-ROTEIRO-EXECUTIVO.md
   ```

4. **Executar scripts na ordem**
   ```bash
   python scripts/01-busca_artigos.py
   python scripts/02-pdf_to_markdown.py
   python scripts/03-fichamento_ia.py
   python scripts/04-validacao_amostra.py
   python scripts/05-sintese_qualitativa.py
   ```

### Replicação

Para replicar este estudo:

1. Seguir o `PROTOCOLO-PRISMA.md`
2. Usar os mesmos `CRITERIOS-INCLUSAO.md`
3. Executar `scripts/` na ordem
4. Validar amostra conforme `validacao/`

---

## 📝 Documentação Detalhada

| Arquivo | Conteúdo |
|---------|----------|
| `00-ROTEIRO-EXECUTIVO.md` | Guia passo a passo com instruções |
| `PROTOCOLO-PRISMA-COMPLETO.md` | Protocolo PRISMA 2020 + 2024-IA |
| `02-CRITERIOS-INCLUSAO.md` | Critérios explícitos de inclusão/exclusão |
| `03-PALAVRAS-CHAVE.md` | Estratégia de busca por base de dados |
| `framework/FRAMEWORK-CONCEITUAL.md` | Modelo teórico integrado |
| `framework/PROPOSICOES-PESQUISA.md` | Proposições testáveis |

---

## 📊 Fluxo de Dados

```
Bases de Dados
    ↓ (Script 01)
CSV: busca_resultados.csv
    ↓ (Filtros automáticos)
CSV: artigos_filtrados.csv
    ↓ (Downloads + Script 02)
PDFs → Markdown (articles/md/)
    ↓ (Script 03 + IA)
Fichamentos MD (analysis/fichamentos/)
    ↓ (Script 04)
Amostra Validação (30-40%)
    ↓ (Revisor Humano)
Feedback + Taxa Concordância
    ↓ (Script 05)
Síntese Qualitativa
    ↓
Artigo Final
```

---

## 👥 Contribuintes

- **Pesquisador**: [Seu Nome]
- **Revisor Validação**: [A definir]
- **Supervisor**: [A definir]

---

## 📅 Timeline

| Fase | Semanas | Status |
|------|---------|--------|
| Planejamento | 1 | 🟡 Em andamento |
| Busca Sistemática | 2-3 | ⬜ A fazer |
| Conversão Artigos | 4 | ⬜ A fazer |
| Fichamento IA | 5-6 | ⬜ A fazer |
| Validação | 7 | ⬜ A fazer |
| Síntese | 8-9 | ⬜ A fazer |
| Redação | 10-12 | ⬜ A fazer |

---

## 📞 Dúvidas e Suporte

Consulte a documentação detalhada em `docs/`.

Para questões metodológicas, veja `docs/PROTOCOLO-PRISMA-COMPLETO.md`.

---

## 📜 Licença

Este projeto segue os princípios de Open Science. Todos os materiais estão disponíveis sob licença Creative Commons (CC-BY 4.0).

---

**Última atualização**: 10 de abril de 2026
