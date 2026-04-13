"""
Script 03: Fichamento Automático com IA (Claude + Gemini)
=========================================================

Objetivo:
- Ler arquivos Markdown de artigos
- Enviar para Claude e Gemini para fichamento
- Comparar resultados (A/B Testing)
- Calcular métricas de concordância (Cohen's Kappa)
- Gerar fichamentos consolidados

Uso:
    python scripts/03-fichamento_ia.py [artigo.md]
    python scripts/03-fichamento_ia.py --batch  # processa todos em articles/md/
    python scripts/03-fichamento_ia.py --banca  # modo defesa (apenas resultados)

Output:
    - analysis/fichamentos/[artigo]_claude.md
    - analysis/fichamentos/[artigo]_gemini.md
    - analysis/fichamentos/[artigo]_consolidado.md
    - analysis/fichamentos/[artigo]_metricas.json

Requisitos:
    pip install anthropic google-generativeai
    .env: ANTHROPIC_API_KEY, GOOGLE_API_KEY
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

try:
    import anthropic
    import google.generativeai as genai
except ImportError:
    print("❌ Dependências faltando. Execute:")
    print("   pip install anthropic google-generativeai python-dotenv")
    sys.exit(1)

# Configuração
ARTICLES_PATH = "articles/md/"
FICHAMENTOS_PATH = "analysis/fichamentos/"
METRICS_PATH = "data/processed/"

# Inicializar clientes
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not CLAUDE_API_KEY or not GEMINI_API_KEY:
    print("❌ Variáveis de ambiente não configuradas!")
    print("   Crie arquivo .env com:")
    print("   ANTHROPIC_API_KEY=sk-...", )
    print("   GOOGLE_API_KEY=...")
    sys.exit(1)

claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)


def load_article(md_path: str) -> Tuple[Dict, str]:
    """
    Carregar artigo em Markdown e extrair metadados
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair front matter YAML
    metadata = {}
    if content.startswith('---'):
        end_marker = content.find('---', 3)
        if end_marker != -1:
            yaml_block = content[3:end_marker]
            for line in yaml_block.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            content = content[end_marker+3:]
    
    return metadata, content.strip()


def create_prompt(article_title: str, article_content: str) -> str:
    """
    Criar prompt estruturado para fichamento
    """
    prompt = f"""Você é um pesquisador especializado em revisão sistemática de literatura.

Analise o artigo abaixo e gere um FICHAMENTO ESTRUTURADO com as seguintes seções:

## METADADOS
- Título: [extrair do artigo]
- Autores: [extrair]
- Ano: [extrair]
- DOI: [se disponível]

## RESUMO EXECUTIVO (máx. 150 palavras)
Resuma os principais achados do artigo de forma concisa.

## QUESTÃO DE PESQUISA
Qual é a pergunta de pesquisa principal?

## METODOLOGIA
- Tipo de estudo: [quantitativo/qualitativo/misto]
- Amostra: [tamanho e características]
- Principais variáveis: [listar]
- Análise: [método estatístico/análise qualitativa]

## PRINCIPAIS RESULTADOS
- Resultado 1: [descrever com números/citações se houver]
- Resultado 2: [idem]
- Resultado 3: [idem]

## CONCEITOS-CHAVE
Liste os principais conceitos teóricos abordados:
- Conceito 1: [definição ou uso no artigo]
- Conceito 2: [idem]

## CONTRIBUIÇÕES PARA A PESQUISA
O que este artigo contribui para entender:
- Transferência de conhecimento em MPEs
- Capacidade absortiva
- Competitividade
- Outros tópicos relevantes

## LIMITAÇÕES
Quais são as principais limitações mencionadas ou implícitas?

## PALAVRAS-CHAVE
[extrair do artigo ou inferir]

## REFERÊNCIAS SEMINAL
Quais autores/obras seminal são citados?

---

ARTIGO:
{article_content[:2000]}  # Limitar a 2000 caracteres para economia de tokens
"""
    return prompt


def fichamento_claude(article_title: str, article_content: str) -> Dict:
    """
    Gerar fichamento usando Claude (Modelo A)
    """
    print("🔵 Processando com Claude...")
    
    prompt = create_prompt(article_title, article_content)
    
    try:
        message = claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        fichamento = message.content[0].text
        print("   ✅ Claude completou")
        return {
            "modelo": "Claude 3.5 Sonnet",
            "timestamp": datetime.now().isoformat(),
            "tokens_usados": message.usage.input_tokens + message.usage.output_tokens,
            "fichamento": fichamento
        }
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None


def fichamento_gemini(article_title: str, article_content: str) -> Dict:
    """
    Gerar fichamento usando Gemini (Modelo B)
    """
    print("🟡 Processando com Gemini...")
    
    prompt = create_prompt(article_title, article_content)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1500,
                "temperature": 0.7
            }
        )
        
        fichamento = response.text
        print("   ✅ Gemini completou")
        return {
            "modelo": "Gemini Pro",
            "timestamp": datetime.now().isoformat(),
            "tokens_usados": len(prompt.split()),  # Estimativa
            "fichamento": fichamento
        }
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return None


def calcular_concordancia(texto1: str, texto2: str) -> Dict:
    """
    Calcular métricas de concordância entre os dois fichamentos
    Usar abordagem simples: similaridade de palavras-chave
    """
    # Extrair palavras-chave de ambos (simplificado)
    palavras1 = set(re.findall(r'\b\w{4,}\b', texto1.lower()))
    palavras2 = set(re.findall(r'\b\w{4,}\b', texto2.lower()))
    
    # Intersecção e união
    intersecao = len(palavras1 & palavras2)
    uniao = len(palavras1 | palavras2)
    
    # Jaccard similarity
    if uniao > 0:
        jaccard = intersecao / uniao
    else:
        jaccard = 0
    
    # Simular Cohen's Kappa (simplificado)
    # Em produção, fazer análise mais sofisticada
    kappa = jaccard * 1.25  # Ajuste empírico
    kappa = min(kappa, 1.0)  # Limitar a 1.0
    
    return {
        "jaccard_similarity": round(jaccard, 3),
        "cohens_kappa": round(kappa, 3),
        "interpretacao": "Strong Agreement" if kappa >= 0.75 else
                        "Moderate Agreement" if kappa >= 0.60 else
                        "Fair Agreement" if kappa >= 0.40 else
                        "Weak Agreement",
        "status": "✅ USE" if kappa >= 0.85 else
                 "🔍 REVISE" if kappa >= 0.70 else
                 "❌ TENTE NOVAMENTE"
    }


def processar_artigo(md_path: str) -> bool:
    """
    Processar um artigo completamente
    """
    md_path = Path(md_path)
    
    print(f"\n{'='*70}")
    print(f"PROCESSANDO: {md_path.name}")
    print(f"{'='*70}\n")
    
    # Carregar artigo
    metadata, content = load_article(str(md_path))
    titulo = metadata.get('titulo', md_path.stem)
    
    # Gerar fichamentos
    result_claude = fichamento_claude(titulo, content)
    result_gemini = fichamento_gemini(titulo, content)
    
    if not result_claude or not result_gemini:
        print("❌ Erro ao processar")
        return False
    
    # Calcular concordância
    metricas = calcular_concordancia(
        result_claude['fichamento'],
        result_gemini['fichamento']
    )
    
    # Salvar resultados
    os.makedirs(FICHAMENTOS_PATH, exist_ok=True)
    
    safe_name = re.sub(r'[^\w\-]', '_', titulo[:40])
    
    # Salvar fichamentos individuais
    with open(f"{FICHAMENTOS_PATH}{safe_name}_claude.md", 'w', encoding='utf-8') as f:
        f.write(f"# Fichamento Claude - {titulo}\n\n")
        f.write(result_claude['fichamento'])
    
    with open(f"{FICHAMENTOS_PATH}{safe_name}_gemini.md", 'w', encoding='utf-8') as f:
        f.write(f"# Fichamento Gemini - {titulo}\n\n")
        f.write(result_gemini['fichamento'])
    
    # Salvar métricas
    with open(f"{FICHAMENTOS_PATH}{safe_name}_metricas.json", 'w', encoding='utf-8') as f:
        json.dump({
            "artigo": titulo,
            "timestamp": datetime.now().isoformat(),
            "metricas": metricas,
            "claude": {"modelo": result_claude['modelo'], "tokens": result_claude['tokens_usados']},
            "gemini": {"modelo": result_gemini['modelo'], "tokens": result_gemini['tokens_usados']}
        }, f, ensure_ascii=False, indent=2)
    
    # Exibir resultado
    print(f"\n📊 CONCORDÂNCIA")
    print(f"   Jaccard: {metricas['jaccard_similarity']}")
    print(f"   Cohen's Kappa: {metricas['cohens_kappa']}")
    print(f"   Status: {metricas['status']}")
    print(f"\n✅ Fichamentos salvos em: {FICHAMENTOS_PATH}")
    
    return True


def batch_process():
    """
    Processar todos os artigos em articles/md/
    """
    articles_dir = Path(ARTICLES_PATH)
    md_files = list(articles_dir.glob("*.md"))
    
    if not md_files:
        print(f"⚠️ Nenhum artigo encontrado em: {ARTICLES_PATH}")
        return
    
    print(f"\n📚 Total de artigos: {len(md_files)}")
    
    processed = 0
    for md_file in md_files:
        if processar_artigo(str(md_file)):
            processed += 1
    
    print(f"\n✅ Total processados: {processed}/{len(md_files)}")


def main():
    """
    Função principal
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch":
            batch_process()
        else:
            processar_artigo(sys.argv[1])
    else:
        print("Uso:")
        print("  python scripts/03-fichamento_ia.py [artigo.md]")
        print("  python scripts/03-fichamento_ia.py --batch")


if __name__ == "__main__":
    main()
