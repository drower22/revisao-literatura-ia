#!/usr/bin/env python3
"""
Script 06-ranking_relevancia.py (REVISADO)
Análise Léxica e Ranking de Relevância - PRÉ-FICHAMENTO
=======================================================

Processa CSV BRUTO para filtrar artigos ANTES de qualquer fichamento.

FLUXO:
  1. Carrega CSV bruto: data/processed/artigos_consolidados.csv
     Colunas esperadas: titulo, keywords, abstract, revista, citacoes, doi, autores, ano
  2. Remove DUPLICATAS (por DOI, título similitude >95%)
  3. Análise léxica contra dicionários de palavras-chave
  4. Calcula SCORE_RELEVANCIA (0-100) para cada artigo
  5. Rankeia artigos por relevância
  6. Gera outputs:
     - artigos_ranqueados.csv (filtrado + score + ranking)
     - relatorio_ranking.md (análise detalhada)
     - duplicatas_removidas.csv (rastreabilidade PRISMA)

BENEFÍCIO:
  - Remove duplicatas antes de investir tempo
  - Você só processa TOP relevantes (40-60% economy)
  - Documenta decisões (PRISMA compliance)
"""

import os
import csv
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import Counter
from datetime import datetime
from difflib import SequenceMatcher


# Configuração
PROCESSED_PATH = Path("data/processed/")
OUTPUT_PATH = Path("analysis/relevancia/")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


class DicionariosLexicais:
    """Palavras-chave para análise de relevância"""

    # PALAVRAS-CHAVE POSITIVAS (aumentam score)
    POSITIVAS = {
        'core_projeto': {
            'peso': 3.0,
            'palavras': [
                'absorptive capacity', 'capacidade absortiva', 'ac',
                'dynamic capabilities', 'capacidades dinâmicas', 'dc',
                'organizational learning', 'aprendizagem organizacional',
                'competitividade', 'competitiveness',
                'inovação', 'innovation', 'innovativeness',
                'knowledge management', 'gestão conhecimento',
            ]
        },
        'contexto_mpe': {
            'peso': 2.5,
            'palavras': [
                'pme', 'mpe', 'sme', 'small medium enterprise',
                'pequena empresa', 'pequena e média',
                'micro empresa', 'startup', 'startups',
                'medium enterprise', 'médium business',
                'smb', 'pmi', 'small business',
            ]
        },
        'mecanismos': {
            'peso': 2.0,
            'palavras': [
                'redes', 'networks', 'network', 'rede de negócios',
                'parcerias', 'partnerships', 'aliança', 'alianças',
                'colaboração', 'collaboration', 'collaborative',
                'cooperação', 'cooperation', 'clusters',
                'transferência conhecimento', 'knowledge transfer',
                'compartilhamento conhecimento', 'knowledge sharing',
                'spillover', 'knowledge spillover', 'open innovation',
                'aprendizagem', 'learning', 'conhecimento externo',
            ]
        },
        'contexto_geografico': {
            'peso': 1.5,
            'palavras': [
                'brasil', 'brazil', 'brazilian', 'brasileiras',
                'américa latina', 'latin america', 'latino-americanas',
                'mercado emergente', 'emerging market',
                'países emergentes', 'emerging economies',
                'países em desenvolvimento', 'developing countries',
            ]
        },
        'metodo_cientifico': {
            'peso': 1.0,
            'palavras': [
                'estudo empírico', 'empirical study', 'empirical research',
                'pesquisa quantitativa', 'quantitative research',
                'pesquisa qualitativa', 'qualitative research',
                'survey', 'entrevista', 'interviews', 'case study',
                'modelo estrutural', 'structural equation model',
            ]
        },
    }

    # PALAVRAS-CHAVE NEGATIVAS (diminuem score)
    NEGATIVAS = {
        'fora_escopo_fundamental': {
            'penalidade': -50,
            'palavras': [
                'apenas revisão', 'only review', 'literature review',
                'revisão literatura', 'revisão teórica', 'theoretical review',
                'opinion paper', 'editorial', 'news', 'commentary',
                'single case study', 'case study única',
            ]
        },
        'temporal_inadequado': {
            'penalidade': -30,
            'palavras': [
                'pré 2010', 'before 2010', 'anterior 2000', 'prior 2000',
            ]
        },
        'contexto_incompativel': {
            'penalidade': -15,
            'palavras': [
                'apenas grande empresa', 'only large firms',
                'fortune 500', 'multinacional apenas', 'multinational only',
                'large corporation', 'big company', 'grandes empresas',
            ]
        },
        'metodo_fraco': {
            'penalidade': -10,
            'palavras': [
                'apenas opinião', 'expert opinion only', 'purely theoretical',
                'teórico apenas', 'sem dados', 'especulativo',
            ]
        },
    }


class AnalisadorRelevanciaPreFichamento:
    """Analisa relevância de CSV BRUTO antes de fichamento"""

    def __init__(self):
        self.artigos_originais = []
        self.artigos_unicos = []
        self.artigos_ranqueados = []
        self.duplicatas = []
        self.estatisticas = {}

    @staticmethod
    def gerar_hash_duplicata(titulo: str, doi: str = "") -> str:
        """Gera hash para detectar duplicatas"""
        texto = f"{titulo.lower().strip()} {doi.lower().strip()}"
        texto = re.sub(r'[^a-z0-9\s]', '', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return hashlib.md5(texto.encode()).hexdigest()

    @staticmethod
    def calcular_similitude_titulo(titulo1: str, titulo2: str) -> float:
        """Calcula similitude entre títulos"""
        if not titulo1 or not titulo2:
            return 0.0

        t1 = re.sub(r'[^a-z0-9\s]', '', titulo1.lower().strip())
        t2 = re.sub(r'[^a-z0-9\s]', '', titulo2.lower().strip())
        t1 = re.sub(r'\s+', ' ', t1).strip()
        t2 = re.sub(r'\s+', ' ', t2).strip()

        if not t1 or not t2:
            return 0.0

        ratio = SequenceMatcher(None, t1, t2).ratio()
        return ratio * 100

    def remover_duplicatas(self, artigos: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Remove duplicatas por DOI, hash título ou similitude alta"""
        vistos_doi = set()
        vistos_hash = set()
        unicos = []
        duplicatas = []

        for artigo in artigos:
            doi = artigo.get('doi', '').lower().strip()
            titulo = artigo.get('titulo', '').strip()

            # Verificar por DOI
            if doi and doi not in ['nan', '', 'n/a', 'não disponível']:
                if doi in vistos_doi:
                    artigo['razao_exclusao'] = f"DOI duplicado: {doi}"
                    duplicatas.append(artigo)
                    continue
                vistos_doi.add(doi)

            # Verificar por hash título
            if titulo:
                hash_titulo = self.gerar_hash_duplicata(titulo, doi)
                if hash_titulo in vistos_hash:
                    artigo['razao_exclusao'] = "Título duplicado (hash)"
                    duplicatas.append(artigo)
                    continue
                vistos_hash.add(hash_titulo)

            # Verificar similitude título (>95%)
            duplicado = False
            for outro in unicos:
                sim = self.calcular_similitude_titulo(titulo, outro.get('titulo', ''))
                if sim > 95:
                    artigo['razao_exclusao'] = f"Duplicado (similitude {sim:.0f}%)"
                    duplicatas.append(artigo)
                    duplicado = True
                    break

            if not duplicado:
                unicos.append(artigo)

        return unicos, duplicatas

    @staticmethod
    def contar_ocorrencias(texto: str, palavras: List[str]) -> int:
        """Conta ocorrências de palavras em texto"""
        if not texto:
            return 0

        texto_lower = texto.lower()
        total = 0

        for palavra in palavras:
            pattern = r'\b' + re.escape(palavra) + r'\b'
            matches = len(re.findall(pattern, texto_lower))
            total += matches

        return total

    def calcular_score_relevancia(self, artigo: Dict) -> Tuple[float, Dict]:
        """
        Calcula score de relevância (0-100)

        Estrutura:
          - Base: 50 pontos
          - Palavras positivas: até +50
          - Palavras negativas: até -100
        """

        # Combinar texto disponível
        titulo = artigo.get('titulo', '')
        keywords = artigo.get('keywords', '')
        abstract = artigo.get('abstract', '')
        revista = artigo.get('revista', '')

        texto_completo = f"{titulo} {keywords} {abstract} {revista}".lower()

        score = 50.0  # Base
        detalhes = {
            'palavras_positivas': [],
            'palavras_negativas': [],
            'score_base': 50,
            'pontos_positivos': 0,
            'pontos_negativos': 0,
        }

        # Analisar POSITIVAS
        for categoria, dados in DicionariosLexicais.POSITIVAS.items():
            peso = dados['peso']
            palavras = dados['palavras']

            total_encontradas = self.contar_ocorrencias(texto_completo, palavras)

            if total_encontradas > 0:
                pontos = min(total_encontradas * 2, 50)
                score += pontos * (peso / 3.0)
                detalhes['palavras_positivas'].append(
                    f"{categoria}: +{pontos:.0f} (peso {peso})"
                )
                detalhes['pontos_positivos'] += pontos

        # Analisar NEGATIVAS
        for categoria, dados in DicionariosLexicais.NEGATIVAS.items():
            penalidade = dados['penalidade']
            palavras = dados['palavras']

            total_encontradas = self.contar_ocorrencias(texto_completo, palavras)

            if total_encontradas > 0:
                score += penalidade
                detalhes['palavras_negativas'].append(f"{categoria}: {penalidade}")
                detalhes['pontos_negativos'] += abs(penalidade)

        # Normalizar (0-100)
        score = max(0, min(100, score))

        return score, detalhes

    def processar_arquivo_csv(self, arquivo_csv: str) -> bool:
        """Processa arquivo CSV bruto"""

        if not Path(arquivo_csv).exists():
            print(f"❌ Arquivo não encontrado: {arquivo_csv}")
            return False

        print(f"📖 Lendo: {arquivo_csv}")

        try:
            with open(arquivo_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for idx, row in enumerate(reader, 1):
                    artigo = {
                        'artigo_id': row.get('artigo_id', f'art_{idx}'),
                        'titulo': row.get('titulo', ''),
                        'keywords': row.get('keywords', ''),
                        'abstract': row.get('abstract', ''),
                        'revista': row.get('revista', ''),
                        'doi': row.get('doi', ''),
                        'autores': row.get('autores', ''),
                        'ano': row.get('ano', ''),
                        'citacoes': row.get('citacoes', 0),
                    }
                    self.artigos_originais.append(artigo)

                    if idx % 100 == 0:
                        print(f"   ✅ {idx} artigos lidos...")

        except Exception as e:
            print(f"❌ Erro lendo CSV: {e}")
            return False

        return True

    def executar_pipeline(self, arquivo_csv: str):
        """Executa pipeline completo"""

        print("🔍 RANKING PRÉ-FICHAMENTO")
        print("=" * 70)

        # 1. Carregar CSV
        if not self.processar_arquivo_csv(arquivo_csv):
            return False

        print(f"✅ {len(self.artigos_originais)} artigos carregados")

        # 2. Remover duplicatas
        print("\n🔄 Removendo duplicatas...")
        self.artigos_unicos, self.duplicatas = self.remover_duplicatas(
            self.artigos_originais
        )

        print(f"✅ Duplicatas removidas: {len(self.duplicatas)}")
        print(f"✅ Artigos únicos: {len(self.artigos_unicos)}")

        # 3. Calcular scores
        print("\n📊 Calculando scores de relevância...")
        for artigo in self.artigos_unicos:
            score, detalhes = self.calcular_score_relevancia(artigo)
            artigo['relevancia_score'] = round(score, 1)
            artigo['pontos_positivos'] = detalhes['pontos_positivos']
            artigo['pontos_negativos'] = detalhes['pontos_negativos']
            artigo['palavras_positivas'] = '; '.join(detalhes['palavras_positivas'][:3])
            artigo['palavras_negativas'] = '; '.join(detalhes['palavras_negativas'])

        # 4. Rankear
        print("📈 Ranqueando artigos...")
        self.artigos_unicos.sort(key=lambda x: x['relevancia_score'], reverse=True)

        for idx, artigo in enumerate(self.artigos_unicos, 1):
            artigo['ranking'] = idx

            if artigo['relevancia_score'] >= 85:
                artigo['categoria'] = 'Muito Alto'
            elif artigo['relevancia_score'] >= 70:
                artigo['categoria'] = 'Alto'
            elif artigo['relevancia_score'] >= 50:
                artigo['categoria'] = 'Moderado'
            else:
                artigo['categoria'] = 'Baixo'

        self.artigos_ranqueados = self.artigos_unicos
        return True

    def salvar_ranqueado(self):
        """Salva artigos ranqueados em CSV"""
        arquivo_saida = PROCESSED_PATH / "artigos_ranqueados.csv"

        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'ranking', 'artigo_id', 'titulo', 'relevancia_score', 'categoria',
                'ano', 'autores', 'revista', 'doi', 'citacoes',
                'palavras_positivas', 'palavras_negativas', 'abstract'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for artigo in self.artigos_ranqueados:
                row = {field: artigo.get(field, '') for field in fieldnames}
                writer.writerow(row)

        print(f"✅ Ranking salvo em: {arquivo_saida}")

    def salvar_duplicatas(self):
        """Salva duplicatas removidas"""
        arquivo_saida = PROCESSED_PATH / "duplicatas_removidas.csv"

        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['artigo_id', 'titulo', 'doi', 'razao_exclusao']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for dup in self.duplicatas:
                row = {
                    'artigo_id': dup.get('artigo_id', ''),
                    'titulo': dup.get('titulo', ''),
                    'doi': dup.get('doi', ''),
                    'razao_exclusao': dup.get('razao_exclusao', '')
                }
                writer.writerow(row)

        print(f"✅ Duplicatas salvas em: {arquivo_saida}")

    def gerar_relatorio(self):
        """Gera relatório de análise"""
        arquivo_saida = OUTPUT_PATH / "relatorio_ranking.md"

        total = len(self.artigos_ranqueados)
        muito_alto = sum(1 for a in self.artigos_ranqueados if a['relevancia_score'] >= 85)
        alto = sum(1 for a in self.artigos_ranqueados if 70 <= a['relevancia_score'] < 85)
        moderado = sum(1 for a in self.artigos_ranqueados if 50 <= a['relevancia_score'] < 70)
        baixo = total - muito_alto - alto - moderado

        score_medio = (
            sum(a['relevancia_score'] for a in self.artigos_ranqueados) / total 
            if total > 0 else 0
        )

        relatorio = f"""# 📊 Relatório de Ranking Pré-Fichamento

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

**Total Processado**: {len(self.artigos_originais)} artigos

**Duplicatas Removidas**: {len(self.duplicatas)}

**Artigos Únicos**: {total}

**Score Médio**: {score_medio:.1f}/100

---

## 📈 Distribuição de Relevância

| Categoria | Quantidade | % | Score |
|-----------|-----------|-----|-------|
| 🔴 Muito Alto | {muito_alto} | {muito_alto*100/total:.1f}% | ≥ 85 |
| 🟠 Alto | {alto} | {alto*100/total:.1f}% | 70-85 |
| 🟡 Moderado | {moderado} | {moderado*100/total:.1f}% | 50-70 |
| 🔵 Baixo | {baixo} | {baixo*100/total:.1f}% | < 50 |

---

## 🎯 Recomendações

### Próximos Passos

1. **Revisar TOP {muito_alto + alto}** artigos (Muito Alto + Alto)
2. **Considerar** {moderado} moderados se tempo
3. **Descartar** {baixo} baixos com confiança
4. **Documentar exclusões** (PRISMA exige rastreabilidade)

### Economia de Tempo

- Sem ranking: 100% dos {total} artigos precisam revisão
- Com ranking: Revisar apenas ~{muito_alto*100//total if total > 0 else 0}% (TOP {muito_alto})
- **Economia: {100 - (muito_alto*100//total) if total > 0 else 0}%**

---

## 📁 Outputs Gerados

- `artigos_ranqueados.csv` - Todos artigos com score e ranking
- `duplicatas_removidas.csv` - Rastreamento de exclusões (PRISMA)

---

*Gerado automaticamente pelo script 06-ranking_relevancia.py*
"""

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(relatorio)

        print(f"✅ Relatório salvo em: {arquivo_saida}")


def main():
    """Função principal"""
    print("\n" + "=" * 70)
    print("  RANKING PRÉ-FICHAMENTO - ANÁLISE LÉXICA")
    print("=" * 70 + "\n")

    analisador = AnalisadorRelevanciaPreFichamento()

    # Buscar arquivo de entrada
    arquivo_csv = PROCESSED_PATH / "artigos_consolidados.csv"

    if not arquivo_csv.exists():
        print(f"❌ Arquivo não encontrado: {arquivo_csv}")
        print("   Execute primeiro: python scripts/01-busca_artigos.py")
        return

    # Executar pipeline
    if analisador.executar_pipeline(str(arquivo_csv)):
        print("\n💾 Salvando outputs...")
        analisador.salvar_ranqueado()
        analisador.salvar_duplicatas()
        analisador.gerar_relatorio()

        print("\n" + "=" * 70)
        print("✅ RANKING CONCLUÍDO COM SUCESSO")
        print("=" * 70)
        print("\n📁 Outputs:")
        print("   - data/processed/artigos_ranqueados.csv")
        print("   - data/processed/duplicatas_removidas.csv")
        print("   - analysis/relevancia/relatorio_ranking.md")
        print("\n👉 Próximos passos:")
        print("   1. Abra: data/processed/artigos_ranqueados.csv")
        print("   2. Revise TOP relevantes (Muito Alto)")
        print("   3. Baixe PDFs selecionados")
        print("   4. Execute: python scripts/00-calibragem_prompts.py")
        print("   5. Depois: python scripts/02-pdf_to_markdown.py\n")
    else:
        print("\n❌ Erro no ranking")


if __name__ == "__main__":
    main()