"""
Script 02: Conversão de PDFs para Markdown
==========================================

Objetivo:
- Extrair texto de arquivos PDF
- Converter para Markdown estruturado
- Limpar OCR errors
- Separar seções principais (intro, métodos, resultados, conclusão)
- Gerar arquivo de metadados (YAML front-matter)

Uso:
    python scripts/02-pdf_to_markdown.py [arquivo.pdf]
    python scripts/02-pdf_to_markdown.py --batch  # processa toda pasta data/raw/

Output:
    - articles/md/[titulo-do-artigo].md (estruturado com metadados)
    - articles/md/[titulo-do-artigo]_raw.md (texto bruto)

Requisitos:
    pip install pypdf pdfplumber
    pip install OCR (tesseract, para PDFs scaneados)
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple

try:
    import pdfplumber
    import PyPDF2
except ImportError:
    print("❌ Dependências faltando. Execute:")
    print("   pip install pdfplumber PyPDF2")
    sys.exit(1)

# Configuração
RAW_PDF_PATH = "data/raw/articles/"
OUTPUT_MD_PATH = "articles/md/"
OUTPUT_METADATA_PATH = "data/processed/metadados_pdfs.json"


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrair texto de PDF usando pdfplumber
    Tenta múltiplas estratégias para melhor resultado
    """
    print(f"📄 Processando: {Path(pdf_path).name}")
    
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"   - Total de páginas: {len(pdf.pages)}")
            
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n\n--- PÁGINA {page_num} ---\n{page_text}"
                    else:
                        print(f"   ⚠️ Página {page_num} vazia (pode ser imagem)")
                except Exception as e:
                    print(f"   ⚠️ Erro na página {page_num}: {e}")
        
        if not text:
            print("   ❌ Nenhum texto extraído com pdfplumber")
            return None
            
        return text
        
    except Exception as e:
        print(f"   ❌ Erro ao processar PDF: {e}")
        return None


def extract_metadata(text: str, filename: str) -> Dict:
    """
    Extrair metadados do texto (título, autores, ano, palavras-chave)
    """
    metadata = {
        "filename": filename,
        "data_processamento": datetime.now().isoformat(),
        "titulo": "Sem Título",
        "autores": [],
        "ano": None,
        "palavras_chave": [],
        "doi": None,
        "url": None,
        "resumo": None
    }
    
    lines = text.split('\n')
    
    # Tentar extrair título (geralmente primeiras linhas em CAPS)
    for line in lines[:5]:
        if line.strip() and len(line.strip()) > 10:
            if line.isupper() or (line[0].isupper() and len(line.split()) > 3):
                metadata["titulo"] = line.strip()
                break
    
    # Tentar extrair DOI
    doi_pattern = r'(?:doi[:\s/]*)?(?:https?://)?(?:dx\.)?doi\.org/([^\s\n\]"]*)'
    doi_match = re.search(doi_pattern, text, re.IGNORECASE)
    if doi_match:
        metadata["doi"] = doi_match.group(1)
    
    # Tentar extrair ano (padrão: 20XX)
    year_match = re.search(r'\b(20[0-2]\d)\b', text[:500])
    if year_match:
        metadata["ano"] = int(year_match.group(1))
    
    # Tentar extrair resumo (entre "Abstract" e "Introduction")
    abstract_match = re.search(
        r'(?:abstract|resumo)[:\s]*(.{50,500}?)(?:introduction|introdução|keywords|1\.|$)',
        text,
        re.IGNORECASE | re.DOTALL
    )
    if abstract_match:
        metadata["resumo"] = abstract_match.group(1).strip()[:300]
    
    return metadata


def clean_text(text: str) -> str:
    """
    Limpar texto extraído (remover caracteres especiais, corrigir espaços, etc.)
    """
    if not text:
        return ""
    
    # Remover caracteres OCR ruins
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬀ', 'ff')
    
    # Normalizar espaços
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Múltiplas linhas vazias
    text = re.sub(r' +', ' ', text)  # Múltiplos espaços
    
    # Remover números de página isolados
    text = re.sub(r'^-?\d+-?\s*$', '', text, flags=re.MULTILINE)
    
    return text.strip()


def structure_markdown(text: str, metadata: Dict) -> str:
    """
    Estruturar texto em Markdown com seções
    """
    sections = {
        "Introduction": ["Introduction", "Introdução", "Background", "Contexto"],
        "Methods": ["Methods", "Methodology", "Métodos", "Metodologia"],
        "Results": ["Results", "Resultados", "Findings"],
        "Discussion": ["Discussion", "Discussão", "Interpretation"],
        "Conclusion": ["Conclusion", "Conclusions", "Conclusão", "Conclusões"],
        "References": ["References", "Bibliography", "Referências", "Bibliografia"]
    }
    
    # Criar front matter YAML
    markdown = f"""---
titulo: {metadata['titulo']}
autores: {json.dumps(metadata['autores'])}
ano: {metadata['ano']}
doi: {metadata['doi']}
data_processamento: {metadata['data_processamento']}
resumo: {metadata['resumo']}
---

# {metadata['titulo']}

"""
    
    # Dividir por seções
    current_section = "Content"
    lines = text.split('\n')
    
    for line in lines:
        # Detectar mudança de seção
        found_section = False
        for section_name, keywords in sections.items():
            if any(keyword.lower() in line.lower() for keyword in keywords):
                if line.strip().endswith(':') or len(line.split()) < 5:
                    markdown += f"\n## {section_name}\n\n"
                    current_section = section_name
                    found_section = True
                    break
        
        if not found_section and line.strip():
            markdown += line + "\n"
    
    return markdown


def process_single_pdf(pdf_path: str) -> bool:
    """
    Processar um único arquivo PDF
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        return False
    
    # Extrair texto
    text = extract_text_from_pdf(str(pdf_path))
    if not text:
        return False
    
    # Limpar texto
    text = clean_text(text)
    
    # Extrair metadados
    metadata = extract_metadata(text, pdf_path.name)
    
    # Estruturar em Markdown
    markdown = structure_markdown(text, metadata)
    
    # Salvar arquivos
    os.makedirs(OUTPUT_MD_PATH, exist_ok=True)
    
    # Nome do arquivo de saída (baseado no título ou filename)
    safe_name = re.sub(r'[^\w\-]', '_', metadata['titulo'][:50])
    output_file = Path(OUTPUT_MD_PATH) / f"{safe_name}.md"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"   ✅ Salvo em: {output_file}")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao salvar: {e}")
        return False


def batch_process():
    """
    Processar todos os PDFs em data/raw/articles/
    """
    print("=" * 70)
    print("CONVERSÃO DE PDFs PARA MARKDOWN - MODO BATCH")
    print("=" * 70)
    
    pdf_dir = Path(RAW_PDF_PATH)
    if not pdf_dir.exists():
        print(f"❌ Diretório não encontrado: {pdf_dir}")
        print(f"   Crie a pasta e coloque PDFs em: {pdf_dir}")
        return
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"⚠️ Nenhum PDF encontrado em: {pdf_dir}")
        return
    
    print(f"\n📚 Total de PDFs encontrados: {len(pdf_files)}\n")
    
    processed = 0
    failed = 0
    
    for pdf_file in pdf_files:
        if process_single_pdf(pdf_file):
            processed += 1
        else:
            failed += 1
        print()
    
    # Relatório final
    print("=" * 70)
    print("RELATÓRIO FINAL")
    print("=" * 70)
    print(f"✅ Processados com sucesso: {processed}")
    print(f"❌ Falhas: {failed}")
    print(f"📂 Saída: {OUTPUT_MD_PATH}")


def main():
    """
    Função principal
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch":
            batch_process()
        else:
            # Processar arquivo específico
            process_single_pdf(sys.argv[1])
    else:
        print("Uso:")
        print("  python scripts/02-pdf_to_markdown.py [arquivo.pdf]")
        print("  python scripts/02-pdf_to_markdown.py --batch")
        print("\nExemplo:")
        print("  python scripts/02-pdf_to_markdown.py data/raw/articles/estudo.pdf")


if __name__ == "__main__":
    main()
