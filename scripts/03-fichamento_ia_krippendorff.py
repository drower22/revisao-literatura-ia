#!/usr/bin/env python3
"""
Script 03-fichamento_ia_krippendorff.py
Fichamentos paralelos (Claude vs Gemini) com saída para Krippendorff's Alpha
Gera CSV compatível com validação robusta de concordância
"""

import os
import json
import csv
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
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
ARTICLES_PATH = Path("articles/md/")
FICHAMENTOS_PATH = Path("analysis/fichamentos/")
METRICS_PATH = Path("data/processed/")

# Inicializar clientes
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not CLAUDE_API_KEY or not GEMINI_API_KEY:
    print("❌ Variáveis de ambiente não configuradas!")
    sys.exit(1)

claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)


class ProcessadorFichamentoKrippendorff:
    """Processa fichamentos para análise com Krippendorff's Alpha"""
    
    def __init__(self):
        self.comparacoes = []
    
    @staticmethod
    def criar_prompt_fichamento(titulo: str, conteudo: str) -> str:
        """Cria prompt estruturado para fichamento"""
        return f"""Você é um pesquisador especializado em revisão sistemática.

ARTIGO: {titulo}

TAREFA: Gere um FICHAMENTO ESTRUTURADO com scores numéricos.

INSTRUÇÕES:
1. Analize APENAS o conteúdo fornecido
2. Atribua scores de 1-10 para cada critério
3. Seja ESPECÍFICO e CONCISO
4. Se não conseguir avaliar, marque como "Não identificado"

FORMATO OBRIGATÓRIO (máquina):
```
DECISAO: [1=INCLUIR | 0=EXCLUIR]
RELEVANCIA_SCORE: [1-10]
QUALIDADE_METODO_SCORE: [1-10]
DISPONIBILIDADE_SCORE: [1-10]
```

CONTEÚDO DO ARTIGO:
{conteudo[:2000]}...

Responda APENAS no formato acima. Primeiro a seção estruturada, depois comentários opcionais.
"""
    
    @staticmethod
    def extrair_scores_do_fichamento(texto: str) -> Dict:
        """Extrai scores estruturados da resposta da IA"""
        scores = {
            'decisao': 0,  # 1=incluir, 0=excluir
            'relevancia': 0,
            'qualidade_metodo': 0,
            'disponibilidade': 0,
            'score_media': 0
        }
        
        # Extrair DECISAO
        match_decisao = re.search(r'DECISAO:\s*([01])', texto)
        if match_decisao:
            scores['decisao'] = int(match_decisao.group(1))
        
        # Extrair RELEVANCIA_SCORE
        match_rel = re.search(r'RELEVANCIA_SCORE:\s*(\d+)', texto)
        if match_rel:
            scores['relevancia'] = int(match_rel.group(1))
        
        # Extrair QUALIDADE_METODO_SCORE
        match_qual = re.search(r'QUALIDADE_METODO_SCORE:\s*(\d+)', texto)
        if match_qual:
            scores['qualidade_metodo'] = int(match_qual.group(1))
        
        # Extrair DISPONIBILIDADE_SCORE
        match_disp = re.search(r'DISPONIBILIDADE_SCORE:\s*(\d+)', texto)
        if match_disp:
            scores['disponibilidade'] = int(match_disp.group(1))
        
        # Calcular média dos scores (normalizados para 0-10)
        scores_numericos = [
            scores['relevancia'],
            scores['qualidade_metodo'],
            scores['disponibilidade']
        ]
        if all(s > 0 for s in scores_numericos):
            scores['score_media'] = round(sum(scores_numericos) / len(scores_numericos), 1)
        
        return scores
    
    def processar_artigo(self, caminho_md: Path, artigo_id: str) -> Dict:
        """Processa um artigo com Claude e Gemini em paralelo"""
        
        print(f"\n📄 Processando: {caminho_md.name}")
        
        # Carregar artigo
        with open(caminho_md, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Extrair título
        match_titulo = re.search(r'^#\s+(.+)$', conteudo, re.MULTILINE)
        titulo = match_titulo.group(1) if match_titulo else caminho_md.stem
        
        prompt = self.criar_prompt_fichamento(titulo, conteudo)
        
        # Processar com Claude
        print("  → Claude processando...")
        try:
            response_claude = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            fichamento_claude = response_claude.content[0].text
            scores_claude = self.extrair_scores_do_fichamento(fichamento_claude)
        except Exception as e:
            print(f"  ❌ Erro Claude: {e}")
            scores_claude = {'decisao': 0, 'score_media': 0}
            fichamento_claude = f"Erro: {str(e)}"
        
        # Processar com Gemini
        print("  → Gemini processando...")
        try:
            model_gemini = genai.GenerativeModel('gemini-2.0-flash')
            response_gemini = model_gemini.generate_content(prompt)
            fichamento_gemini = response_gemini.text
            scores_gemini = self.extrair_scores_do_fichamento(fichamento_gemini)
        except Exception as e:
            print(f"  ❌ Erro Gemini: {e}")
            scores_gemini = {'decisao': 0, 'score_media': 0}
            fichamento_gemini = f"Erro: {str(e)}"
        
        # Salvar fichamentos individuais
        FICHAMENTOS_PATH.mkdir(parents=True, exist_ok=True)
        
        with open(FICHAMENTOS_PATH / f"{artigo_id}_claude.md", 'w', encoding='utf-8') as f:
            f.write(f"# Fichamento Claude\n\n{fichamento_claude}")
        
        with open(FICHAMENTOS_PATH / f"{artigo_id}_gemini.md", 'w', encoding='utf-8') as f:
            f.write(f"# Fichamento Gemini\n\n{fichamento_gemini}")
        
        # Compilar comparação para Krippendorff's Alpha
        comparacao = {
            'artigo_id': artigo_id,
            'titulo': titulo[:60],
            'claude_decisao': scores_claude['decisao'],
            'gemini_decisao': scores_gemini['decisao'],
            'claude_score': scores_claude.get('score_media', 0),
            'gemini_score': scores_gemini.get('score_media', 0),
            'observacoes': ''
        }
        
        # Adicionar observações se houver discordância
        if scores_claude['decisao'] != scores_gemini['decisao']:
            comparacao['observacoes'] = "Discordância na decisão de inclusão"
        
        self.comparacoes.append(comparacao)
        
        print(f"  ✅ Salvo: {artigo_id}")
        print(f"     Claude: {'Incluir' if scores_claude['decisao'] else 'Excluir'} (score: {scores_claude.get('score_media', 0)})")
        print(f"     Gemini: {'Incluir' if scores_gemini['decisao'] else 'Excluir'} (score: {scores_gemini.get('score_media', 0)})")
        
        return comparacao
    
    def salvar_comparacoes_csv(self, caminho_csv: str = "data/processed/comparacao_claude_gemini.csv"):
        """Salva comparações em formato CSV para Krippendorff's Alpha"""
        
        Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)
        
        if not self.comparacoes:
            print("⚠️ Nenhuma comparação para salvar!")
            return
        
        # Headers
        headers = [
            'artigo_id',
            'titulo',
            'claude_decisao',
            'gemini_decisao',
            'claude_score',
            'gemini_score',
            'observacoes'
        ]
        
        with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.comparacoes)
        
        print(f"\n✅ Comparações salvas em: {caminho_csv}")
        print(f"   Total de artigos: {len(self.comparacoes)}")
    
    def gerar_relatorio_processamento(self, caminho_json: str = "data/processed/relatorio_fichamento_krippendorff.json"):
        """Gera relatório de processamento"""
        
        concordancia_decisoes = sum(
            1 for c in self.comparacoes
            if c['claude_decisao'] == c['gemini_decisao']
        )
        
        relatorio = {
            "data": datetime.now().isoformat(),
            "total_processados": len(self.comparacoes),
            "concordancia_simples": {
                "total": concordancia_decisoes,
                "percentual": round(concordancia_decisoes / len(self.comparacoes) * 100, 1)
            },
            "decisoes": {
                "incluir_ambos": sum(
                    1 for c in self.comparacoes
                    if c['claude_decisao'] == 1 and c['gemini_decisao'] == 1
                ),
                "excluir_ambos": sum(
                    1 for c in self.comparacoes
                    if c['claude_decisao'] == 0 and c['gemini_decisao'] == 0
                ),
                "discordancia": len(self.comparacoes) - concordancia_decisoes
            },
            "scores": {
                "claude_media": round(
                    sum(c['claude_score'] for c in self.comparacoes) / len(self.comparacoes), 2
                ),
                "gemini_media": round(
                    sum(c['gemini_score'] for c in self.comparacoes) / len(self.comparacoes), 2
                )
            },
            "proximo_passo": "Executar: python scripts/04-validacao_krippendorff.py"
        }
        
        Path(caminho_json).parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_json, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Relatório salvo em: {caminho_json}")


def main():
    """Executa processamento de todos os artigos"""
    
    if not ARTICLES_PATH.exists():
        print(f"❌ Diretório não encontrado: {ARTICLES_PATH}")
        sys.exit(1)
    
    # Listar artigos
    artigos = sorted(ARTICLES_PATH.glob("*.md"))
    if not artigos:
        print(f"⚠️ Nenhum artigo encontrado em {ARTICLES_PATH}")
        sys.exit(1)
    
    print(f"\n{'='*70}")
    print(f"FICHAMENTO COM KRIPPENDORFF'S ALPHA")
    print(f"{'='*70}")
    print(f"Total de artigos: {len(artigos)}")
    print(f"Processador iniciado...\n")
    
    # Processar
    processador = ProcessadorFichamentoKrippendorff()
    
    for idx, artigo_path in enumerate(artigos, 1):
        artigo_id = f"{idx:03d}"
        try:
            processador.processar_artigo(artigo_path, artigo_id)
        except Exception as e:
            print(f"  ❌ Erro ao processar {artigo_path.name}: {e}")
    
    # Salvar resultados
    processador.salvar_comparacoes_csv()
    processador.gerar_relatorio_processamento()
    
    print(f"\n{'='*70}")
    print(f"✅ Processamento concluído!")
    print(f"{'='*70}\n")
    
    print("Próximo passo:")
    print("  python scripts/04-validacao_krippendorff.py")


if __name__ == "__main__":
    main()
