#!/usr/bin/env python3
"""
Krippendorff's Alpha Calculator
Métrica robusta de concordância inter-avaliador para 2+ avaliadores
Referência: Krippendorff, K. (2004). Content Analysis: An Introduction to Its Methodology
"""

import numpy as np
from typing import List, Dict, Union, Tuple
import json
from pathlib import Path


class KrippendorffAlpha:
    """
    Implementação de Krippendorff's Alpha (α)
    
    Fórmula: α = 1 - (Do / De)
    Onde:
        Do = Discordância observada (erro real entre avaliadores)
        De = Discordância esperada (erro por acaso)
    
    Interpretação:
        α = 1.0   → Concordância PERFEITA
        α ≥ 0.80  → EXCELENTE
        α ≥ 0.70  → BOA
        α ≥ 0.60  → ACEITÁVEL
        α ≥ 0.50  → Acima do acaso
        α < 0.50  → Abaixo do acaso (PROBLEMA!)
    """
    
    def __init__(self):
        self.resultados = {}
    
    @staticmethod
    def calcular_alpha_nominal(dados: List[List[int]]) -> float:
        """
        Calcula Krippendorff's Alpha para dados NOMINAIS (categorias)
        
        Args:
            dados: Lista de listas onde:
                   - Linhas = unidades de análise (artigos)
                   - Colunas = avaliadores (Claude, Gemini, etc)
                   - Valores = categorias (0/1, 1/2/3, etc)
        
        Returns:
            float: Alpha (0 a 1)
        
        Exemplo:
            dados = [
                [1, 1],  # Artigo 1: Claude incluir (1), Gemini incluir (1)
                [1, 0],  # Artigo 2: Claude incluir (1), Gemini excluir (0)
                [0, 0],  # Artigo 3: ambos excluem
            ]
            alpha = KrippendorffAlpha.calcular_alpha_nominal(dados)
        """
        dados = np.array(dados, dtype=float)
        
        # Remover linhas com dados faltantes (NaN)
        dados_completos = dados[~np.isnan(dados).any(axis=1)]
        
        if len(dados_completos) == 0:
            return 0.0
        
        m = dados_completos.shape[1]  # número de avaliadores
        n = dados_completos.shape[0]  # número de unidades
        
        # Calcular frequências de cada categoria
        categorias = set()
        for linha in dados_completos:
            categorias.update(linha)
        categorias = sorted(list(categorias))
        
        # Construir matriz de coincidências (coincidence matrix)
        coincidencias = {}
        for c in categorias:
            coincidencias[c] = {}
            for c2 in categorias:
                coincidencias[c][c2] = 0
        
        # Preencher matriz de coincidências
        for linha in dados_completos:
            for i, v1 in enumerate(linha):
                for j, v2 in enumerate(linha):
                    if i != j:
                        c1, c2 = int(v1), int(v2)
                        if c1 in coincidencias and c2 in coincidencias[c1]:
                            coincidencias[c1][c2] += 1
        
        # Calcular discordância observada (Do)
        Do = 0
        total_pares = 0
        for c1 in categorias:
            for c2 in categorias:
                if c1 != c2:
                    Do += coincidencias[c1][c2]
                total_pares += coincidencias[c1][c2]
        
        if total_pares == 0:
            return 1.0  # Concordância perfeita (sem dados)
        
        Do = Do / total_pares
        
        # Calcular discordância esperada (De)
        # Frequências marginais
        freq_marginal = {}
        for c in categorias:
            count = 0
            for c1 in categorias:
                count += coincidencias[c1][c]
            freq_marginal[c] = count
        
        De = 0
        total = sum(freq_marginal.values())
        
        for c1 in categorias:
            for c2 in categorias:
                if c1 != c2:
                    p1 = freq_marginal[c1] / total if total > 0 else 0
                    p2 = freq_marginal[c2] / total if total > 0 else 0
                    De += p1 * p2
        
        # Calcular Alpha
        if De == 0:
            return 1.0 if Do == 0 else 0.0
        
        alpha = 1 - (Do / De)
        return max(0, alpha)  # Nunca negativo
    
    @staticmethod
    def calcular_alpha_intervalar(dados: List[List[float]]) -> float:
        """
        Calcula Krippendorff's Alpha para dados INTERVALARES (scores)
        
        Útil para scores de 0-100, 1-5, etc
        """
        dados = np.array(dados, dtype=float)
        
        # Remover linhas com dados faltantes
        dados_completos = dados[~np.isnan(dados).any(axis=1)]
        
        if len(dados_completos) < 2:
            return 0.0
        
        m = dados_completos.shape[1]  # avaliadores
        n = dados_completos.shape[0]  # unidades
        
        # Calcular variância dos dados
        media_geral = np.mean(dados_completos)
        
        # Do: Soma das diferenças quadradas dentro de cada unidade
        Do = 0
        for linha in dados_completos:
            for i in range(len(linha)):
                for j in range(i+1, len(linha)):
                    Do += (linha[i] - linha[j]) ** 2
        
        Do = Do / (n * m * (m - 1) / 2)  # Normalizar
        
        # De: Variância esperada por acaso
        De = 0
        for i in range(n):
            for j in range(n):
                if i != j:
                    for vi in dados_completos[i]:
                        for vj in dados_completos[j]:
                            De += (vi - vj) ** 2
        
        De = De / (n * (n - 1) * m * m)  # Normalizar
        
        if De == 0:
            return 1.0 if Do == 0 else 0.0
        
        alpha = 1 - (Do / De)
        return max(0, alpha)
    
    @staticmethod
    def interpretar_alpha(alpha: float) -> Dict[str, str]:
        """Retorna interpretação textual do valor de Alpha"""
        if alpha >= 0.80:
            return {
                "nivel": "EXCELENTE",
                "forca": "Strong agreement",
                "acao": "✅ Aprovação automática"
            }
        elif alpha >= 0.70:
            return {
                "nivel": "BOM",
                "forca": "Substantial agreement",
                "acao": "🔍 Revisar amostra (10%)"
            }
        elif alpha >= 0.60:
            return {
                "nivel": "ACEITÁVEL",
                "forca": "Moderate agreement",
                "acao": "⚠️ Revisar amostra (30%)"
            }
        elif alpha >= 0.50:
            return {
                "nivel": "FRACO",
                "forca": "Fair agreement (above chance)",
                "acao": "❌ Revisão manual (100%)"
            }
        else:
            return {
                "nivel": "CRÍTICO",
                "forca": "Below chance agreement",
                "acao": "❌ REJEITAR e refazer"
            }


class AnalisadorConcordancia:
    """Analisa concordância Claude vs Gemini usando Krippendorff's Alpha"""
    
    def __init__(self):
        self.krippendorff = KrippendorffAlpha()
    
    def analisar_inclusao_exclusao(self, comparacoes: List[Dict]) -> Dict:
        """
        Analisa concordância sobre inclusão/exclusão de artigos
        
        Args:
            comparacoes: Lista de dicts com:
                {
                    'artigo_id': '001',
                    'claude_decisao': 1,  # 1=incluir, 0=excluir
                    'gemini_decisao': 1,
                    'motivo_discordancia': 'opcional'
                }
        
        Returns:
            Dict com estatísticas de concordância
        """
        # Preparar dados para Krippendorff's Alpha (formato nominal)
        dados = []
        artigos = []
        
        for comp in comparacoes:
            dados.append([comp['claude_decisao'], comp['gemini_decisao']])
            artigos.append(comp['artigo_id'])
        
        # Calcular Alpha
        alpha = self.krippendorff.calcular_alpha_nominal(dados)
        
        # Calcular concordância simples (%)
        concordancia_simples = sum(
            1 for c, g in zip(
                [d[0] for d in dados],
                [d[1] for d in dados]
            ) if c == g
        ) / len(dados) * 100
        
        # Análise por categoria
        incluir_ambos = sum(
            1 for c, g in zip([d[0] for d in dados], [d[1] for d in dados])
            if c == 1 and g == 1
        )
        excluir_ambos = sum(
            1 for c, g in zip([d[0] for d in dados], [d[1] for d in dados])
            if c == 0 and g == 0
        )
        discordancia = len(dados) - incluir_ambos - excluir_ambos
        
        interpretacao = self.krippendorff.interpretar_alpha(alpha)
        
        resultado = {
            "alpha": round(alpha, 4),
            "concordancia_simples_pct": round(concordancia_simples, 1),
            "total_artigos": len(dados),
            "incluir_ambos": incluir_ambos,
            "excluir_ambos": excluir_ambos,
            "discordancia": discordancia,
            "interpretacao": interpretacao,
            "recomendacao": interpretacao["acao"],
            "artigos_concordancia": artigos
        }
        
        return resultado
    
    def analisar_fichamentos(self, fichamentos: List[Dict]) -> Dict:
        """
        Analisa concordância de scores de qualidade de fichamentos
        
        Args:
            fichamentos: Lista de dicts com:
                {
                    'artigo_id': '001',
                    'claude_score': 8.5,  # 0-10
                    'gemini_score': 8.2,
                    'secoes_correlacao': 0.92
                }
        """
        scores_claude = []
        scores_gemini = []
        
        for f in fichamentos:
            scores_claude.append(f['claude_score'])
            scores_gemini.append(f['gemini_score'])
        
        # Usar Alpha intervalar para scores
        dados_intervalar = []
        for sc, sg in zip(scores_claude, scores_gemini):
            dados_intervalar.append([sc, sg])
        
        alpha = self.krippendorff.calcular_alpha_intervalar(dados_intervalar)
        
        # Calcular diferença média
        diferencas = [abs(c - g) for c, g in zip(scores_claude, scores_gemini)]
        diff_media = np.mean(diferencas)
        diff_max = max(diferencas)
        
        interpretacao = self.krippendorff.interpretar_alpha(alpha)
        
        resultado = {
            "alpha_scores": round(alpha, 4),
            "score_claude_media": round(np.mean(scores_claude), 2),
            "score_gemini_media": round(np.mean(scores_gemini), 2),
            "diferenca_media": round(diff_media, 2),
            "diferenca_maxima": round(diff_max, 2),
            "total_fichamentos": len(fichamentos),
            "interpretacao": interpretacao,
            "recomendacao": interpretacao["acao"]
        }
        
        return resultado
    
    def gerar_relatorio(self, analise: Dict, nome_arquivo: str = None) -> str:
        """Gera relatório formatado de concordância"""
        
        relatorio = f"""
{'='*70}
RELATÓRIO DE CONCORDÂNCIA - KRIPPENDORFF'S ALPHA
{'='*70}

📊 MÉTRICA PRINCIPAL
{'─'*70}
Krippendorff's Alpha (α): {analise.get('alpha', analise.get('alpha_scores', 'N/A')):.4f}

Interpretação: {analise['interpretacao']['nivel']}
Força de Concordância: {analise['interpretacao']['forca']}
Recomendação: {analise['interpretacao']['acao']}

📈 ESTATÍSTICAS
{'─'*70}
"""
        
        if 'concordancia_simples_pct' in analise:
            relatorio += f"""
Total de Artigos: {analise['total_artigos']}
Concordância Simples: {analise['concordancia_simples_pct']:.1f}%

Decisões Concordantes:
  • Incluir (ambos): {analise['incluir_ambos']}
  • Excluir (ambos): {analise['excluir_ambos']}
  • Discordância: {analise['discordancia']}
"""
        
        if 'score_claude_media' in analise:
            relatorio += f"""
Score Claude (média): {analise['score_claude_media']}
Score Gemini (média): {analise['score_gemini_media']}
Diferença Média: {analise['diferenca_media']}
Diferença Máxima: {analise['diferenca_maxima']}
"""
        
        relatorio += f"""
{'='*70}

✅ INTERPRETAÇÃO SEGUNDO KRIPPENDORFF:
  0.00 - 0.50: Abaixo do acaso (CRÍTICO)
  0.50 - 0.60: Fraco
  0.60 - 0.70: Aceitável
  0.70 - 0.80: Bom
  0.80 - 1.00: Excelente

📚 REFERÊNCIA:
Krippendorff, K. (2004). Content Analysis: An Introduction to Its Methodology.
PRISMA 2024-IA: Recomendado para validação inter-avaliador com IA.

{'='*70}
"""
        
        if nome_arquivo:
            Path(nome_arquivo).parent.mkdir(parents=True, exist_ok=True)
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio)
        
        return relatorio


if __name__ == "__main__":
    # Exemplo de uso
    print("Krippendorff's Alpha Calculator - Módulo de Cálculo")
    print("Para usar em seus scripts: from utils.krippendorff_calculator import KrippendorffAlpha, AnalisadorConcordancia")
    
    # Teste simples
    dados_teste = [
        [1, 1],  # Concordância
        [1, 1],  # Concordância
        [0, 0],  # Concordância
        [1, 0],  # Discordância
        [1, 1],  # Concordância
    ]
    
    alpha = KrippendorffAlpha.calcular_alpha_nominal(dados_teste)
    print(f"\nTeste com 5 artigos (4 concordâncias, 1 discordância):")
    print(f"Krippendorff's Alpha = {alpha:.4f}")
    print(f"Interpretação: {KrippendorffAlpha.interpretar_alpha(alpha)['nivel']}")
