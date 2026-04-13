"""
Script 01: Busca e Consolidação de Artigos
==========================================

Objetivo: 
- Ler CSVs de múltiplas bases de dados (Scopus, WoS, SciELO, Scholar)
- Consolidar em arquivo único
- Remover duplicatas
- Gerar relatório de estatísticas

Uso:
    python scripts/01-busca_artigos.py
    
Output:
    - data/processed/artigos_consolidados.csv
    - data/processed/relatorio_busca.txt
"""

import pandas as pd
import os
from datetime import datetime
import re

# Configuration
RAW_DATA_PATH = "data/raw/"
PROCESSED_DATA_PATH = "data/processed/"
DATABASES = ["scopus", "wos", "scielo", "scholar"]

def load_raw_data():
    """
    Load CSVs from all databases
    """
    print("=" * 60)
    print("FASE 1: CARREGANDO DADOS BRUTOS DE BASES")
    print("=" * 60)
    
    all_articles = []
    
    for db in DATABASES:
        filepath = os.path.join(RAW_DATA_PATH, f"{db}_resultados.csv")
        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                print(f"✓ {db.upper()}: {len(df)} artigos carregados")
                all_articles.append(df)
            except Exception as e:
                print(f"✗ Erro ao carregar {db}: {e}")
        else:
            print(f"⚠ Arquivo não encontrado: {filepath}")
    
    if all_articles:
        consolidated = pd.concat(all_articles, ignore_index=True)
        return consolidated
    else:
        print("\n❌ Nenhum arquivo encontrado em data/raw/")
        return None

def normalize_metadata(df):
    """
    Normalize column names and data formats across databases
    """
    print("\n" + "=" * 60)
    print("FASE 2: NORMALIZANDO METADADOS")
    print("=" * 60)
    
    # Map common column names
    column_mapping = {
        'Title': 'titulo',
        'title': 'titulo',
        'Authors': 'autores',
        'authors': 'autores',
        'Author': 'autores',
        'Year': 'ano',
        'year': 'ano',
        'Published in': 'publicacao',
        'Publication': 'publicacao',
        'publication': 'publicacao',
        'Journal': 'publicacao',
        'journal': 'publicacao',
        'DOI': 'doi',
        'doi': 'doi',
        'Abstract': 'resumo',
        'abstract': 'resumo',
        'Abstract / Summary': 'resumo',
    }
    
    df.rename(columns=column_mapping, inplace=True)
    
    # Ensure key columns exist
    required_cols = ['titulo', 'autores', 'ano', 'doi']
    for col in required_cols:
        if col not in df.columns:
            df[col] = ''
    
    # Clean up data
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['titulo'] = df['titulo'].str.strip()
    df['autores'] = df['autores'].str.strip()
    df['doi'] = df['doi'].str.strip().str.lower()
    
    print(f"✓ {len(df)} registros normalizados")
    print(f"✓ Colunas principais: {', '.join(required_cols)}")
    
    return df

def remove_duplicates(df):
    """
    Remove duplicate articles based on DOI and title
    """
    print("\n" + "=" * 60)
    print("FASE 3: REMOVENDO DUPLICATAS")
    print("=" * 60)
    
    initial_count = len(df)
    
    # Remove by DOI (if available)
    df_with_doi = df[df['doi'] != ''].copy()
    df_no_doi = df[df['doi'] == ''].copy()
    
    if len(df_with_doi) > 0:
        df_with_doi = df_with_doi.drop_duplicates(subset=['doi'], keep='first')
        print(f"✓ Removidas duplicatas por DOI: {len(df) - len(df_with_doi) - len(df_no_doi)} artigos")
    
    df = pd.concat([df_with_doi, df_no_doi], ignore_index=True)
    
    # Remove by title similarity (case-insensitive)
    df['titulo_normalizado'] = df['titulo'].str.lower().str.strip()
    df = df.drop_duplicates(subset=['titulo_normalizado'], keep='first')
    
    # Drop temporary column
    df = df.drop('titulo_normalizado', axis=1)
    
    final_count = len(df)
    removed = initial_count - final_count
    
    print(f"✓ Removidas {removed} duplicatas (total: {initial_count} → {final_count})")
    
    return df

def add_metadata(df):
    """
    Add processing metadata
    """
    df['data_processamento'] = datetime.now().strftime('%Y-%m-%d')
    df['processado_por'] = 'Script 01 - Busca Consolidação'
    
    return df

def generate_report(df):
    """
    Generate statistics report
    """
    print("\n" + "=" * 60)
    print("FASE 4: GERANDO RELATÓRIO DE ESTATÍSTICAS")
    print("=" * 60)
    
    report = f"""
RELATÓRIO DE BUSCA SISTEMÁTICA
Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}

RESUMO EXECUTIVO
================
Total de artigos únicos: {len(df)}

DISTRIBUIÇÃO POR ANO
====================
"""
    
    year_dist = df['ano'].value_counts().sort_index()
    for year, count in year_dist.items():
        report += f"\n{int(year)}: {count} artigos"
    
    report += f"""

DISTRIBUIÇÃO POR PUBLICAÇÃO (TOP 10)
====================================
"""
    
    pub_dist = df['publicacao'].value_counts().head(10)
    for i, (pub, count) in enumerate(pub_dist.items(), 1):
        report += f"\n{i}. {pub}: {count} artigos"
    
    report += f"""

QUALIDADE DOS DADOS
===================
- Artigos com DOI: {len(df[df['doi'] != ''])} ({len(df[df['doi'] != ''])/len(df)*100:.1f}%)
- Artigos com resumo: {len(df[df['resumo'].notna()]) if 'resumo' in df.columns else 'N/A'}
- Artigos com autores: {len(df[df['autores'] != ''])} ({len(df[df['autores'] != ''])/len(df)*100:.1f}%)

PRÓXIMOS PASSOS
===============
1. Abrir data/processed/artigos_consolidados.csv em planilha
2. Aplicar filtros automáticos (ano, idioma)
3. Executar Triagem Nível 1 (título + resumo)
4. Registrar em: data/processed/triagem_nivel1_resultados.csv

---
Gerado por: Script 01 - Busca Consolidação
"""
    
    return report

def main():
    """
    Main execution
    """
    print("\n🔍 SCRIPT 01: BUSCA E CONSOLIDAÇÃO DE ARTIGOS\n")
    
    # Create output directory if not exists
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    
    # Load data
    df = load_raw_data()
    if df is None:
        return
    
    # Process data
    df = normalize_metadata(df)
    df = remove_duplicates(df)
    df = add_metadata(df)
    
    # Generate report
    report = generate_report(df)
    
    # Save outputs
    output_csv = os.path.join(PROCESSED_DATA_PATH, "artigos_consolidados.csv")
    output_txt = os.path.join(PROCESSED_DATA_PATH, "relatorio_busca.txt")
    
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"\n✓ Arquivo salvo: {output_csv}")
    
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Relatório salvo: {output_txt}")
    
    print("\n" + "=" * 60)
    print("✅ SCRIPT 01 CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    print(report)

if __name__ == "__main__":
    main()
