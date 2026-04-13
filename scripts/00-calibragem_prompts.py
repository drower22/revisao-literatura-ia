#!/usr/bin/env python3
"""
Script 00-calibragem_prompts.py
Calibragem de Prompts com Artigos Seminais
==========================================

Valida qualidade dos prompts usando 15-20 artigos que você já conhece.
Gera matriz de concordância e recomendações de refinamento.

FLUXO:
1. Carrega artigos seminais de data/calibragem/artigos_seminais.txt
2. Executa Claude e Gemini em cada artigo
3. Compara output IA vs sua leitura original (ground truth)
4. Gera matriz de calibragem com scores de concordância
5. Identifica campos que precisam refinamento
6. Recomenda ajustes de prompt

PREREQUISITOS:
- Você já preparou: data/calibragem/leituras_baseline/*.md
- Você listou em: data/calibragem/artigos_seminais.txt
"""

import os
import json
import csv
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from difflib import SequenceMatcher
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
CALIBRAGEM_PATH = Path("data/calibragem/")
OUTPUT_PATH = Path("analysis/calibragem/")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Inicializar clientes
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

if not CLAUDE_API_KEY or not GEMINI_API_KEY:
    print("❌ Variáveis de ambiente não configuradas!")
    print("   Configure: ANTHROPIC_API_KEY e GOOGLE_API_KEY")
    sys.exit(1)

claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)


class CalibradorPrompts:
    """Calibra prompts com artigos seminais"""
    
    def __init__(self):
        self.resultados_calibragem = []
        self.matriz_concordancia = []
    
    @staticmethod
    def calcular_similidade(texto1: str, texto2: str) -> float:
        """Calcula similidade entre dois textos (0-100%)"""
        if not texto1 or not texto2:
            return 0.0
        
        # Normalizar textos
        t1 = texto1.lower().strip()
        t2 = texto2.lower().strip()
        
        # Calcular similaridade
        ratio = SequenceMatcher(None, t1, t2).ratio()
        return min(100.0, ratio * 100)
    
    @staticmethod
    def extrair_secoes_fichamento(texto: str) -> Dict[str, str]:
        """Extrai seções principais do fichamento"""
        secoes = {}
        
        # Padrões para seções
        patterns = {
            'metadados': r'##\s*Metadados.*?(?=##\s*|\Z)',
            'resumo': r'##\s*Resumo Executivo.*?(?=##\s*|\Z)',
            'objetivo': r'##\s*1\.\s*Objetivo.*?(?=##\s*|\Z)',
            'framework': r'##\s*2\.\s*Quadro Teórico.*?(?=##\s*|\Z)',
            'metodologia': r'##\s*3\.\s*Metodologia.*?(?=##\s*|\Z)',
            'achados': r'##\s*4\.\s*Achados.*?(?=##\s*|\Z)',
            'proposicoes': r'##\s*5\.\s*Relacionamento.*?(?=##\s*|\Z)',
            'forcas': r'##\s*6\.\s*Pontos Fortes.*?(?=##\s*|\Z)',
            'limitacoes': r'##\s*7\.\s*Limitações.*?(?=##\s*|\Z)',
        }
        
        for secao, pattern in patterns.items():
            match = re.search(pattern, texto, re.DOTALL | re.IGNORECASE)
            if match:
                secoes[secao] = match.group(0)[:500]  # Limitar a 500 chars
            else:
                secoes[secao] = ""
        
        return secoes
    
    def gerar_prompt_fichamento(self, titulo: str, conteudo: str) -> str:
        """Gera prompt estruturado para fichamento"""
        return f"""Você é um pesquisador especializado em revisão sistemática.

ARTIGO: {titulo}

TAREFA: Gere um FICHAMENTO ESTRUTURADO com análise rigorosa.

INSTRUÇÕES CRÍTICAS:
1. Máxima PRECISÃO e FIDELIDADE ao texto original
2. NÃO interprete além do explícito
3. Cite EXATAMENTE como aparece no artigo
4. Se houver contradição, MENCIONE explicitamente
5. Forneça sínteses concisos mas informativos

CONTEÚDO DO ARTIGO (primeiros 2000 caracteres):
{conteudo[:2000]}...

FORMATO OBRIGATÓRIO:

## Metadados
[Extrair: Autores, Ano, DOI, Periódico]

## Resumo Executivo (100-150 palavras)
[Síntese do que o artigo discute]

## 1. Objetivo/Pergunta Pesquisa
[Qual era a pergunta central?]

## 2. Quadro Teórico
[Quais teorias usadas? Conceitos principais definidos]

## 3. Metodologia
[Delineamento, método, amostra (N=?), contexto, análise]

## 4. Achados Principais
[Máximo 5 achados com evidências específicas]

## 5. Relacionamento com Proposições
[Análise de proposições-chave do projeto]

## 6. Pontos Fortes (máximo 3)
[Força metodológica, contribuições teóricas]

## 7. Limitações (máximo 3)
[Escopo, metodologia, generalização]

## 8. Lacunas Identificadas (máximo 3)
[O que o artigo RECONHECE como não estudado]

## 9. Relevância para Projeto
[Análise de alinhamento com objetivos de pesquisa]

Responda APENAS no formato acima. Máximo 3 páginas.
"""
    
    def executar_fichamento_claude(self, titulo: str, conteudo: str) -> str:
        """Executa fichamento com Claude"""
        try:
            prompt = self.gerar_prompt_fichamento(titulo, conteudo)
            
            message = claude_client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"❌ Erro Claude: {e}")
            return ""
    
    def executar_fichamento_gemini(self, titulo: str, conteudo: str) -> str:
        """Executa fichamento com Gemini"""
        try:
            prompt = self.gerar_prompt_fichamento(titulo, conteudo)
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            print(f"❌ Erro Gemini: {e}")
            return ""
    
    def carregar_artigos_seminais(self) -> List[Dict]:
        """Carrega lista de artigos seminais"""
        arquivo_seminais = CALIBRAGEM_PATH / "artigos_seminais.txt"
        
        if not arquivo_seminais.exists():
            print(f"❌ Arquivo não encontrado: {arquivo_seminais}")
            print("   Crie data/calibragem/artigos_seminais.txt com lista de artigos")
            return []
        
        artigos = []
        with open(arquivo_seminais, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith('#'):
                    continue
                
                # Formato: id|titulo|tipo|arquivo_baseline.md
                partes = linha.split('|')
                if len(partes) >= 4:
                    artigos.append({
                        'id': partes[0].strip(),
                        'titulo': partes[1].strip(),
                        'tipo': partes[2].strip(),
                        'arquivo_baseline': partes[3].strip()
                    })
        
        return artigos
    
    def processar_calibragem(self):
        """Executa calibragem completa"""
        print("🔬 CALIBRAGEM DE PROMPTS")
        print("=" * 60)
        
        # Carregar artigos seminais
        artigos = self.carregar_artigos_seminais()
        if not artigos:
            print("❌ Nenhum artigo seminal encontrado!")
            return False
        
        print(f"✅ Carregados {len(artigos)} artigos seminais\n")
        
        # Processar cada artigo
        for idx, artigo in enumerate(artigos, 1):
            print(f"[{idx}/{len(artigos)}] Processando: {artigo['titulo']}")
            
            # Carregar conteúdo do artigo
            arquivo_md = ARTICLES_PATH / f"{artigo['id']}.md"
            if not arquivo_md.exists():
                print(f"   ⚠️  Artigo não encontrado: {arquivo_md}")
                continue
            
            try:
                with open(arquivo_md, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
            except Exception as e:
                print(f"   ❌ Erro lendo arquivo: {e}")
                continue
            
            # Carregar baseline (sua leitura original)
            arquivo_baseline = CALIBRAGEM_PATH / "leituras_baseline" / artigo['arquivo_baseline']
            baseline_texto = ""
            if arquivo_baseline.exists():
                try:
                    with open(arquivo_baseline, 'r', encoding='utf-8') as f:
                        baseline_texto = f.read()
                except Exception as e:
                    print(f"   ⚠️  Erro lendo baseline: {e}")
            
            # Executar Claude
            print("   ⏳ Claude...")
            fichamento_claude = self.executar_fichamento_claude(artigo['titulo'], conteudo)
            
            # Executar Gemini
            print("   ⏳ Gemini...")
            fichamento_gemini = self.executar_fichamento_gemini(artigo['titulo'], conteudo)
            
            # Salvar fichamentos IA
            saida_claude = OUTPUT_PATH / "fichamentos_ia" / f"{artigo['id']}_claude.md"
            saida_gemini = OUTPUT_PATH / "fichamentos_ia" / f"{artigo['id']}_gemini.md"
            saida_claude.parent.mkdir(parents=True, exist_ok=True)
            
            with open(saida_claude, 'w', encoding='utf-8') as f:
                f.write(fichamento_claude)
            with open(saida_gemini, 'w', encoding='utf-8') as f:
                f.write(fichamento_gemini)
            
            # Calcular concordância
            if baseline_texto:
                concordancia_claude = self.calcular_similidade(baseline_texto, fichamento_claude)
                concordancia_gemini = self.calcular_similidade(baseline_texto, fichamento_gemini)
            else:
                concordancia_claude = 0
                concordancia_gemini = 0
            
            # Concordância entre Claude e Gemini
            concordancia_mutua = self.calcular_similidade(fichamento_claude, fichamento_gemini)
            
            # Armazenar resultado
            resultado = {
                'artigo_id': artigo['id'],
                'titulo': artigo['titulo'],
                'tipo': artigo['tipo'],
                'concordancia_claude_vs_baseline': round(concordancia_claude, 1),
                'concordancia_gemini_vs_baseline': round(concordancia_gemini, 1),
                'concordancia_claude_vs_gemini': round(concordancia_mutua, 1),
                'media_concordancia': round((concordancia_claude + concordancia_gemini + concordancia_mutua) / 3, 1),
                'status': '✅ OK' if (concordancia_claude > 80 and concordancia_gemini > 80) else '⚠️  REVISAR'
            }
            
            self.resultados_calibragem.append(resultado)
            print(f"   ✅ Claude: {concordancia_claude:.1f}% | Gemini: {concordancia_gemini:.1f}% | Mútua: {concordancia_mutua:.1f}%\n")
        
        return True
    
    def gerar_matriz_calibragem(self):
        """Gera matriz de calibragem em CSV"""
        arquivo_saida = OUTPUT_PATH / "matriz_calibragem.csv"
        
        with open(arquivo_saida, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'artigo_id', 'titulo', 'tipo',
                'concordancia_claude_vs_baseline',
                'concordancia_gemini_vs_baseline',
                'concordancia_claude_vs_gemini',
                'media_concordancia', 'status'
            ])
            writer.writeheader()
            writer.writerows(self.resultados_calibragem)
        
        print(f"✅ Matriz salva em: {arquivo_saida}")
    
    def gerar_relatorio_calibragem(self):
        """Gera relatório de calibragem em Markdown"""
        arquivo_saida = OUTPUT_PATH / "relatorio_calibragem.md"
        
        # Calcular estatísticas
        total = len(self.resultados_calibragem)
        claude_media = sum(r['concordancia_claude_vs_baseline'] for r in self.resultados_calibragem) / total if total > 0 else 0
        gemini_media = sum(r['concordancia_gemini_vs_baseline'] for r in self.resultados_calibragem) / total if total > 0 else 0
        mutua_media = sum(r['concordancia_claude_vs_gemini'] for r in self.resultados_calibragem) / total if total > 0 else 0
        
        ok_count = sum(1 for r in self.resultados_calibragem if '✅' in r['status'])
        revisar_count = total - ok_count
        
        # Identificar campos com baixa concordância
        campos_baixa = [r for r in self.resultados_calibragem if r['media_concordancia'] < 80]
        
        relatorio = f"""# 📊 Relatório de Calibragem de Prompts

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Artigos Testados**: {total}  
**Status**: {'✅ PRONTO PARA FICHAMENTO' if ok_count == total else '⚠️ PRECISA REFINAMENTO'}

---

## 📈 Estatísticas Gerais

| Métrica | Valor |
|---------|-------|
| Concordância Claude vs Baseline | {claude_media:.1f}% |
| Concordância Gemini vs Baseline | {gemini_media:.1f}% |
| Concordância Claude vs Gemini | {mutua_media:.1f}% |
| Artigos OK (≥80%) | {ok_count}/{total} |
| Artigos para Revisar (<80%) | {revisar_count}/{total} |

---

## 🎯 Interpretação

### Concordância Claude vs Baseline
- **90%+**: Excelente - Claude captura essência do artigo
- **80-90%**: Bom - Pequenas divergências (aceitável)
- **70-80%**: Moderado - Precisa refinamento
- **<70%**: Fraco - Revisar prompt urgentemente

### Concordância Gemini vs Baseline
- Mesma interpretação acima

### Concordância Claude vs Gemini
- **>85%**: Excelente - Ambas chegam conclusões similares
- **70-85%**: Bom - Diferenças complementares
- **<70%**: Aviso - IAs divergindo demais (artigo ambíguo?)

---

## 🔴 Artigos com Baixa Concordância (<80%)

"""
        
        if campos_baixa:
            for r in campos_baixa:
                relatorio += f"""
### {r['artigo_id']} - {r['titulo']}
- Claude vs Baseline: {r['concordancia_claude_vs_baseline']:.1f}%
- Gemini vs Baseline: {r['concordancia_gemini_vs_baseline']:.1f}%
- Claude vs Gemini: {r['concordancia_claude_vs_gemini']:.1f}%
**Recomendação**: Revisar fichamentos em `analysis/calibragem/fichamentos_ia/`
Identifique discrepâncias e refine prompt conforme necessário.

"""
        else:
            relatorio += "\n✅ Nenhum artigo com baixa concordância!\n"
        
        relatorio += f"""

---

## 📋 Recomendações de Refinamento

### Se Concordância Claude <80%
1. O prompt não está capturando detalhes que você considera importantes
2. Claude pode estar fazendo inferências excessivas
3. **Ação**: Adicione exemplos específicos ao prompt com saída esperada

### Se Concordância Gemini <80%
1. Gemini pode estar "criando" informações não presentes
2. Prompt pode ser ambíguo para Gemini
3. **Ação**: Seja mais específico/restritivo no prompt ("APENAS o que está no artigo")

### Se Concordância Mútua <70%
1. Artigo pode ser ambíguo/contraditório
2. Ou prompts estão direcionando interpretações diferentes
3. **Ação**: Teste prompt com artigo diferente ou refine instruções

---

## ✅ Próximos Passos

1. ✅ Revisar artigos com concordância <80% acima
2. ✅ Abrir correspondentes em: `analysis/calibragem/fichamentos_ia/`
3. ✅ Identificar padrão de discrepância
4. ✅ Editar: `scripts/utils/prompts_calibrados.py`
5. ✅ Reexecutar este script para validar melhoria
6. ✅ Quando média >90%, partir para fichamento em massa: `python scripts/03-fichamento_ia_krippendorff.py`

---

## 📊 Matriz Completa

Ver arquivo: `matriz_calibragem.csv`

---

*Gerado automaticamente pelo script 00-calibragem_prompts.py*
"""
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(relatorio)
        
        print(f"✅ Relatório salvo em: {arquivo_saida}")
    
    def gerar_checklist(self):
        """Gera checklist pré-fichamento"""
        arquivo_saida = OUTPUT_PATH / "CHECKLIST-PRE-FICHAMENTO.md"
        
        total = len(self.resultados_calibragem)
        ok_count = sum(1 for r in self.resultados_calibragem if '✅' in r['status'])
        media_geral = sum(r['media_concordancia'] for r in self.resultados_calibragem) / total if total > 0 else 0
        
        status_pronto = "✅ SIM" if (ok_count == total and media_geral >= 90) else "❌ NÃO"
        
        checklist = f"""# ✅ CHECKLIST PRÉ-FICHAMENTO

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Resultado Calibragem**: {status_pronto}

---

## 📋 Validações Completadas

- [{'x' if ok_count == total else ' '}] Calibragem realizada com {total} artigos seminais
- [{'x' if media_geral >= 90 else ' '}] Concordância média ≥ 90% ({media_geral:.1f}%)
- [{'x' if ok_count == total else ' '}] Todos artigos com ≥ 80% concordância
- [{'x' if True else ' '}] Matriz de calibragem gerada (matriz_calibragem.csv)
- [{'x' if True else ' '}] Relatório de calibragem gerado (relatorio_calibragem.md)

---

## 🔍 Requisitos para Prosseguir

### ✅ OBRIGATÓRIO - Antes de Fichamento em Massa

1. **Concordância Geral**: {media_geral:.1f}% (mínimo: 90%)
   - Status: {'✅ PASSOU' if media_geral >= 90 else '❌ FALHOU - refine prompts'}

2. **Artigos OK**: {ok_count}/{total}
   - Status: {'✅ PASSOU' if ok_count == total else f'❌ FALHOU - {total - ok_count} artigos com <80%'}

3. **Prompts Calibrados**: scripts/utils/prompts_calibrados.py
   - Status: {'✅ CRIADO' if Path('scripts/utils/prompts_calibrados.py').exists() else '❌ AINDA NÃO'}

---

## 🚀 SE TUDO ✅

Execute fichamento em massa:

```bash
python scripts/03-fichamento_ia_krippendorff.py
```

---

## ⚠️ SE ALGO ❌

1. Abra: analysis/calibragem/relatorio_calibragem.md
2. Identifique artigos com <80%
3. Compare fichamentos em: analysis/calibragem/fichamentos_ia/
4. Refine prompts em: scripts/utils/prompts_calibrados.py
5. Reexecute este script:

```bash
python scripts/00-calibragem_prompts.py
```

Repita até concordância ≥ 90%

---

## 📊 Detalhes por Artigo

"""
        
        for r in self.resultados_calibragem:
            status = '✅' if '✅' in r['status'] else '⚠️'
            checklist += f"""
### {status} {r['artigo_id']} - {r['titulo']}
- Tipo: {r['tipo']}
- Concordância: {r['media_concordancia']:.1f}% | {r['status']}
"""
        
        checklist += """

---

*Gerado automaticamente pelo script 00-calibragem_prompts.py*
"""
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(checklist)
        
        print(f"✅ Checklist salvo em: {arquivo_saida}")


def main():
    """Função principal"""
    print("\n" + "=" * 60)
    print("  CALIBRAGEM DE PROMPTS - A/B TESTING")
    print("=" * 60 + "\n")
    
    calibrador = CalibradorPrompts()
    
    # Executar calibragem
    if calibrador.processar_calibragem():
        print("\n✅ Calibragem concluída!")
        print("\n📊 Gerando outputs...")
        
        # Gerar matriz
        calibrador.gerar_matriz_calibragem()
        
        # Gerar relatório
        calibrador.gerar_relatorio_calibragem()
        
        # Gerar checklist
        calibrador.gerar_checklist()
        
        print("\n" + "=" * 60)
        print("✅ CALIBRAGEM CONCLUÍDA COM SUCESSO")
        print("=" * 60)
        print("\n📁 Outputs:")
        print("   - analysis/calibragem/matriz_calibragem.csv")
        print("   - analysis/calibragem/relatorio_calibragem.md")
        print("   - analysis/calibragem/CHECKLIST-PRE-FICHAMENTO.md")
        print("   - analysis/calibragem/fichamentos_ia/*.md")
        print("\n👉 Próximo: Revise relatorio_calibragem.md")
        print("   Se concordância ≥ 90%, execute:")
        print("   python scripts/03-fichamento_ia_krippendorff.py\n")
    else:
        print("\n❌ Erro na calibragem")
        sys.exit(1)


if __name__ == "__main__":
    main()
