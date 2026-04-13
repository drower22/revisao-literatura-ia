#!/usr/bin/env python3
"""
Script 04-validacao_amostra_krippendorff.py
Valida concordância entre Claude e Gemini usando Krippendorff's Alpha
Mede qualidade dos fichamentos com métrica robusta
"""

import json
import csv
from pathlib import Path
from typing import List, Dict
import sys

# Adicionar utils ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.krippendorff_calculator import KrippendorffAlpha, AnalisadorConcordancia


class ValidadorKrippendorff:
    """Valida fichamentos com Krippendorff's Alpha"""
    
    def __init__(self, diretorio_fichamentos: str = "analysis/fichamentos"):
        self.dir_fichamentos = Path(diretorio_fichamentos)
        self.analisador = AnalisadorConcordancia()
    
    def carregar_comparacoes(self, arquivo_csv: str) -> List[Dict]:
        """
        Carrega arquivo CSV com comparações Claude vs Gemini
        
        Formato esperado:
        artigo_id,titulo,claude_decisao,gemini_decisao,claude_score,gemini_score,observacoes
        001,Artigo1,1,1,8.5,8.3,
        002,Artigo2,1,0,8.2,6.5,"Discordância em método"
        """
        comparacoes = []
        
        with open(arquivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                comparacao = {
                    'artigo_id': row['artigo_id'],
                    'titulo': row.get('titulo', ''),
                    'claude_decisao': int(row['claude_decisao']),
                    'gemini_decisao': int(row['gemini_decisao']),
                    'claude_score': float(row.get('claude_score', 0)),
                    'gemini_score': float(row.get('gemini_score', 0)),
                    'observacoes': row.get('observacoes', '')
                }
                comparacoes.append(comparacao)
        
        return comparacoes
    
    def validar_decisoes(self, comparacoes: List[Dict]) -> Dict:
        """Valida decisões de incluir/excluir"""
        return self.analisador.analisar_inclusao_exclusao(comparacoes)
    
    def validar_scores(self, comparacoes: List[Dict]) -> Dict:
        """Valida scores de qualidade"""
        fichamentos = [
            {
                'artigo_id': c['artigo_id'],
                'claude_score': c['claude_score'],
                'gemini_score': c['gemini_score']
            }
            for c in comparacoes
        ]
        return self.analisador.analisar_fichamentos(fichamentos)
    
    def gerar_relatorio_completo(self, comparacoes: List[Dict], 
                                 arquivo_saida: str = "validacao_krippendorff.json") -> Dict:
        """Gera relatório completo de validação"""
        
        print(f"📊 Processando {len(comparacoes)} comparações...")
        
        # Validar decisões
        validacao_decisoes = self.validar_decisoes(comparacoes)
        
        # Validar scores
        validacao_scores = self.validar_scores(comparacoes)
        
        # Identificar discordâncias
        discordancias = [
            c for c in comparacoes
            if c['claude_decisao'] != c['gemini_decisao']
        ]
        
        # Compilar relatório
        relatorio = {
            "data_validacao": "2026-04-10",
            "total_comparacoes": len(comparacoes),
            "validacao_decisoes": {
                "alpha": validacao_decisoes['alpha'],
                "concordancia_simples_pct": validacao_decisoes['concordancia_simples_pct'],
                "incluir_ambos": validacao_decisoes['incluir_ambos'],
                "excluir_ambos": validacao_decisoes['excluir_ambos'],
                "discordancia": validacao_decisoes['discordancia'],
                "interpretacao": validacao_decisoes['interpretacao'],
                "recomendacao": validacao_decisoes['recomendacao']
            },
            "validacao_scores": {
                "alpha": validacao_scores['alpha_scores'],
                "score_claude_media": validacao_scores['score_claude_media'],
                "score_gemini_media": validacao_scores['score_gemini_media'],
                "diferenca_media": validacao_scores['diferenca_media'],
                "diferenca_maxima": validacao_scores['diferenca_maxima'],
                "interpretacao": validacao_scores['interpretacao'],
                "recomendacao": validacao_scores['recomendacao']
            },
            "discordancias": [
                {
                    "artigo_id": d['artigo_id'],
                    "titulo": d['titulo'],
                    "claude_decisao": d['claude_decisao'],
                    "gemini_decisao": d['gemini_decisao'],
                    "score_diff": abs(d['claude_score'] - d['gemini_score']),
                    "observacoes": d['observacoes']
                }
                for d in discordancias[:10]  # Top 10 discordâncias
            ],
            "resumo_executivo": {
                "metodologia": "Krippendorff's Alpha (PRISMA 2024-IA)",
                "versao_alpha": "2.0",
                "referencia": "Krippendorff, K. (2004). Content Analysis: An Introduction to Its Methodology"
            }
        }
        
        # Salvar relatório
        Path(arquivo_saida).parent.mkdir(parents=True, exist_ok=True)
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Relatório salvo em: {arquivo_saida}")
        
        return relatorio
    
    def imprimir_resumo(self, relatorio: Dict):
        """Imprime resumo executivo"""
        
        print("\n" + "="*70)
        print("VALIDAÇÃO COM KRIPPENDORFF'S ALPHA")
        print("="*70)
        
        print("\n📊 DECISÕES (Incluir/Excluir)")
        print("─"*70)
        validacao_dec = relatorio['validacao_decisoes']
        print(f"α = {validacao_dec['alpha']:.4f} ({validacao_dec['interpretacao']['nivel']})")
        print(f"Concordância Simples: {validacao_dec['concordancia_simples_pct']:.1f}%")
        print(f"  • Incluir (ambos): {validacao_dec['incluir_ambos']}")
        print(f"  • Excluir (ambos): {validacao_dec['excluir_ambos']}")
        print(f"  • Discordância: {validacao_dec['discordancia']}")
        print(f"✅ {validacao_dec['recomendacao']}")
        
        print("\n📈 SCORES (Qualidade dos Fichamentos)")
        print("─"*70)
        validacao_sc = relatorio['validacao_scores']
        print(f"α = {validacao_sc['alpha']:.4f} ({validacao_sc['interpretacao']['nivel']})")
        print(f"Claude (média): {validacao_sc['score_claude_media']}/10")
        print(f"Gemini (média): {validacao_sc['score_gemini_media']}/10")
        print(f"Diferença média: {validacao_sc['diferenca_media']}")
        print(f"✅ {validacao_sc['recomendacao']}")
        
        print("\n🚨 TOP DISCORDÂNCIAS")
        print("─"*70)
        for i, disc in enumerate(relatorio['discordancias'][:3], 1):
            print(f"\n{i}. Artigo {disc['artigo_id']}")
            print(f"   Título: {disc['titulo'][:50]}...")
            print(f"   Claude: {'Incluir' if disc['claude_decisao'] else 'Excluir'}")
            print(f"   Gemini: {'Incluir' if disc['gemini_decisao'] else 'Excluir'}")
            print(f"   Score Diff: {disc['score_diff']:.1f}")
        
        print("\n" + "="*70)
        print("Metodologia: Krippendorff's Alpha (PRISMA 2024-IA)")
        print("="*70 + "\n")


def main():
    """Executa validação completa"""
    
    # Caminhos
    arquivo_comparacoes = "data/processed/comparacao_claude_gemini.csv"
    arquivo_saida = "data/processed/validacao_krippendorff.json"
    
    # Validar arquivo de entrada
    if not Path(arquivo_comparacoes).exists():
        print(f"❌ Erro: {arquivo_comparacoes} não encontrado!")
        print("   Certifique-se de ter executado o script 03-fichamento_ia.py")
        sys.exit(1)
    
    # Carregar e validar
    validador = ValidadorKrippendorff()
    comparacoes = validador.carregar_comparacoes(arquivo_comparacoes)
    relatorio = validador.gerar_relatorio_completo(comparacoes, arquivo_saida)
    validador.imprimir_resumo(relatorio)
    
    print(f"✅ Validação concluída!")
    print(f"📊 Relatório detalhado: {arquivo_saida}")


if __name__ == "__main__":
    main()
