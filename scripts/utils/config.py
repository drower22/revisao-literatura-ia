"""
Configuration Settings
======================

Configurações centralizadas para todos os scripts
"""

import os
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTRACTS_DIR = DATA_DIR / "extracts"
ARTICLES_DIR = BASE_DIR / "articles"
ARTICLES_PDF_DIR = ARTICLES_DIR / "pdf"
ARTICLES_MD_DIR = ARTICLES_DIR / "md"
ANALYSIS_DIR = BASE_DIR / "analysis"
FICHAMENTOS_DIR = ANALYSIS_DIR / "fichamentos"
VALIDACAO_DIR = ANALYSIS_DIR / "validacao"
SYNTHESIS_DIR = ANALYSIS_DIR / "synthesis"
DOCS_DIR = BASE_DIR / "docs"

# Criar diretórios se não existirem
for d in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTRACTS_DIR, 
          ARTICLES_PDF_DIR, ARTICLES_MD_DIR, FICHAMENTOS_DIR, 
          VALIDACAO_DIR, SYNTHESIS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Configurações LLM - A/B Testing
# ================================
# IMPORTANTE: Este projeto usa A/B Testing com 2 IAs para validação robusta
# - Claude (Anthropic): Precisão em argumentação rigorosa, coesão teórica
# - Gemini (Google): Síntese criativa, detecção padrões emergentes
# 
# METODOLOGIA: Ambas geram fichamentos do MESMO artigo em paralelo
# Discrepâncias sinalizadas para revisão prioritária
# Consenso forte aumenta confiança nos dados

# Modelos a usar em A/B Testing
LLM_MODELS = {
    "claude": "claude-3-opus-20240229",      # Anthropic - Precisão teórica
    "gemini": "gemini-1.5-pro",              # Google - Síntese criativa
}

# Configuração global (para compatibilidade com scripts existentes)
LLM_PRIMARY_PROVIDER = "anthropic"  # Provider padrão
LLM_PROVIDER = "anthropic"  # "anthropic" ou "google"
LLM_MODEL = "claude-3-opus-20240229"
LLM_TEMPERATURE = 0.2  # Baixo para consistência em ambos
LLM_MAX_TOKENS = 3000
LLM_RETRIES = 3
LLM_TIMEOUT = 60

# A/B Testing Configuration
AB_TESTING_ENABLED = True  # Ativar A/B testing para fichamentos
AB_TESTING_PRIORITY = ["claude", "gemini"]  # Ordem de execução
AB_TESTING_TIMEOUT_BETWEEN = 2  # Segundos entre chamadas (rate limiting)
AB_TESTING_CONSENSUS_THRESHOLD = 0.85  # 85% de concordância = consenso

# API Keys (usar variáveis de ambiente)
# IMPORTANTE PRIVACIDADE: As APIs NÃO salvam conteúdo dos artigos
# para treinamento futuro. Dados retidos por 24-90 dias apenas.
# Veja: docs/02-METODOLOGIA-IA-AB-TESTING.md para detalhes
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Para Gemini

# Configurações de Processamento
PDF_EXTRACTION_METHOD = "pypdf"  # "pypdf", "pdfplumber", ou "ocr"
MIN_TEXT_LENGTH = 500  # Mínimo de caracteres para considerar válido
ENCODING = "utf-8"

# Configurações de Validação
AMOSTRA_VALIDATION_SIZE = 0.30  # 30% dos fichamentos
CONCORDANCIA_MINIMA = 0.80  # 80% de concordância aceitável
COHEN_KAPPA_MINIMA = 0.70  # Mínimo kappa aceitável

# A/B Testing - Métricas de Concordância
AB_TESTING_METRICS = {
    "cohen_kappa_minimo": 0.70,  # Validação entre dois LLMs
    "porcentagem_discrepancia_aceitavel": 20,  # Máx 20% de discordância
    "secoes_criticas": [  # Seções que exigem 100% concordância
        "Metadados",
        "Objetivo/Pergunta Pesquisa",
        "Metodologia"
    ]
}

# Configurações de Busca
SEARCH_KEYWORDS_PT = [
    '"transferência de conhecimento"',
    '"capacidade absortiva"',
    '"absorção de conhecimento"',
    'MPE OR PME',
    '"pequenas empresas"'
]

SEARCH_KEYWORDS_EN = [
    '"knowledge transfer"',
    '"absorptive capacity"',
    '"knowledge absorption"',
    'SME OR PME',
    '"small and medium enterprises"'
]

# Critérios de Inclusão
INCLUSION_CRITERIA = {
    "min_year": 2015,
    "max_year": 2026,
    "languages": ["pt", "en", "es"],
    "document_types": ["journal_article", "conference_paper"],
    "peer_reviewed": True,
    "min_sample_size": 5,  # Mínimo N para estudos empíricos
}

# Teorias para mapeamento
TEORIAS = {
    "KBV": "Knowledge-Based View",
    "RBV": "Resource-Based View",
    "AC": "Absorptive Capacity",
    "DC": "Dynamic Capabilities",
    "OL": "Organizational Learning",
    "IS": "Innovation Systems",
    "IT": "Institutional Theory"
}

# Proposições de Pesquisa
PROPOSICOES = {
    "P1": "AC limitada em MPEs",
    "P2": "AC Realizada → Competitividade",
    "P3": "DC media AC → Competitividade",
    "P4": "Contexto institucional modera",
    "P5": "Redes facilitam em AC baixa",
    "P6": "OL cria vantagem sustentável"
}

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = BASE_DIR / "logs" / "revisao.log"
LOG_FILE.parent.mkdir(exist_ok=True)

# Defaults
DEFAULT_ENCODING = "utf-8"
SEPARATOR_FIELDS = ";"
QUOTE_CHAR = '"'
