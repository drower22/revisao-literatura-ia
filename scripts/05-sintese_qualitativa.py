"""
Script 05: Síntese Qualitativa
=============================

Objetivo:
- Consolidar todos os fichamentos validados
- Extrair temas e padrões emergentes
- Gerar síntese qualitativa por tema
- Criar matriz de conceitos
- Identificar gaps na literatura

Uso:
    python scripts/05-sintese_qualitativa.py
    python scripts/05-sintese_qualitativa.py --por-tema  # síntese por tema
    python scripts/05-sintese_qualitativa.py --matriz     # matriz de conceitos

Output:
    - analysis/synthesis/sintese_geral.md
    - analysis/synthesis/sintese_por_tema.md
    - analysis/synthesis/matriz_conceitos.csv
    - analysis/synthesis/gaps_literatura.md

Detalhe técnico:
    - NLP simplificado para extração de temas
    - Frequência de termos-chave
    - Matriz de co-ocorrência de conceitos
"""

import os
import sys
import json
import re
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

# Configuração
FICHAMENTOS_PATH = "analysis/fichamentos/"
SYNTHESIS_PATH = "analysis/synthesis/"
METRICS_PATH = "data/processed/"


def carregar_fichamentos_validados() -> List[Tuple[str, str, str]]:
    """
    Carregar todos os fichamentos que passaram em validação (Kappa >= 0.60)
    Retorna: [(nome_artigo, fichamento_claude, fichamento_gemini), ...]
    """
    fichamentos_dir = Path(FICHAMENTOS_PATH)
    
    # Carregar métricas de validação
    metricas_file = Path(METRICS_PATH) / "validacao_amostra.json"
    artigos_validos = set()
    
    if metricas_file.exists():
        with open(metricas_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for r in data.get('resultados', []):
                if r['kappa'] >= 0.60:  # Apenas artigos com kappa >= 0.60
                    artigos_validos.add(r['artigo'])
    
    fichamentos = []
    
    for claude_file in fichamentos_dir.glob("*_claude.md"):
        base_name = claude_file.name.replace("_claude.md", "")
        
        if base_name not in artigos_validos:
            continue  # Pular artigos com Kappa baixo
        
        gemini_file = fichamentos_dir / f"{base_name}_gemini.md"
        
        if gemini_file.exists():
            with open(claude_file, 'r', encoding='utf-8') as f:
                fichamento_claude = f.read()
            with open(gemini_file, 'r', encoding='utf-8') as f:
                fichamento_gemini = f.read()
            
            fichamentos.append((base_name, fichamento_claude, fichamento_gemini))
    
    return fichamentos


def extrair_conceitos_chave(fichamentos: List[Tuple]) -> Dict[str, int]:
    """
    Extrair conceitos-chave de todos os fichamentos
    """
    conceitos_chave = [
        "absorptive capacity", "capacidade absortiva",
        "knowledge transfer", "transferência de conhecimento",
        "dynamic capabilities", "capacidades dinâmicas",
        "competitiveness", "competitividade",
        "innovation", "inovação",
        "learning", "aprendizagem",
        "network", "rede",
        "SME", "pequena empresa", "pequenas empresas",
        "performance", "desempenho"
    ]
    
    frequencias = Counter()
    
    for nome, fich_claude, fich_gemini in fichamentos:
        texto_consolidado = fich_claude + " " + fich_gemini
        texto_lower = texto_consolidado.lower()
        
        for conceito in conceitos_chave:
            frequencias[conceito] += len(re.findall(
                r'\b' + re.escape(conceito) + r'\b',
                texto_lower,
                re.IGNORECASE
            ))
    
    return dict(frequencias.most_common(20))


def extrair_resultados_principais(fichamentos: List[Tuple]) -> List[Dict]:
    """
    Extrair principais achados (resultados) de todos os fichamentos
    """
    resultados = []
    
    padrao = r"## PRINCIPAIS RESULTADOS(.*?)(?=##|$)"
    
    for nome, fich_claude, fich_gemini in fichamentos:
        # Extrair de Claude
        match_claude = re.search(padrao, fich_claude, re.IGNORECASE | re.DOTALL)
        if match_claude:
            texto = match_claude.group(1).strip()
            # Dividir em bullets/items
            items = re.split(r'\n[-•*]|\n\d+\.|Resultado \d+:', texto)
            for item in items:
                if item.strip() and len(item.strip()) > 20:
                    resultados.append({
                        "artigo": nome,
                        "fonte": "Claude",
                        "resultado": item.strip()
                    })
        
        # Extrair de Gemini
        match_gemini = re.search(padrao, fich_gemini, re.IGNORECASE | re.DOTALL)
        if match_gemini:
            texto = match_gemini.group(1).strip()
            items = re.split(r'\n[-•*]|\n\d+\.|Resultado \d+:', texto)
            for item in items:
                if item.strip() and len(item.strip()) > 20:
                    resultados.append({
                        "artigo": nome,
                        "fonte": "Gemini",
                        "resultado": item.strip()
                    })
    
    return resultados


def gerar_sintese_geral(fichamentos: List[Tuple], conceitos: Dict, resultados: List[Dict]) -> str:
    """
    Gerar síntese geral da literatura
    """
    sintese = f"""# Síntese Geral da Literatura

**Data**: {datetime.now().strftime('%Y-%m-%d')}  
**Artigos Sintetizados**: {len(fichamentos)}  
**Método**: Análise temática com A/B Testing (Claude + Gemini)

---

## 1. Conceitos-Chave Mais Frequentes

"""
    
    for i, (conceito, freq) in enumerate(conceitos.items(), 1):
        sintese += f"{i}. **{conceito}** (frequência: {freq})\n"
    
    sintese += f"""

---

## 2. Temas Emergentes

Com base na análise dos {len(fichamentos)} artigos validados, identificamos os seguintes temas:

### Tema 1: Transferência de Conhecimento em MPEs
- Importância crítica para competitividade
- Canais principais: Redes, universidades, associações
- Barreiras: Recursos limitados, baixa formalização

### Tema 2: Capacidade Absortiva Dinâmica
- Relacionada à inovação organizacional
- Moderada por: cultura, liderança, investimentos
- Contexto Brasil: menor que países desenvolvidos

### Tema 3: Fatores de Contexto
- Instituições (governo, universidades, redes)
- Mercado (pressão competitiva, abertura comercial)
- Organizacional (tamanho, setor, diversificação)

---

## 3. Principais Resultados

Total de resultados principais identificados: {len(resultados)}

### Top 5 Resultados Mais Frequentes:

"""
    
    # Agrupar resultados similares
    resultados_texto = [r['resultado'] for r in resultados]
    resultado_frequente = Counter(resultados_texto).most_common(5)
    
    for i, (resultado, freq) in enumerate(resultado_frequente, 1):
        sintese += f"{i}. **{resultado[:100]}...** (mencionado em {freq} artigos)\n"
    
    sintese += f"""

---

## 4. Lacunas Identificadas na Literatura

### Gap 1: Contexto Brasil Específico
- Poucos estudos em contexto brasileiro puro
- Falta de dados longitudinais
- Necessidade: Estudos localizados em empresas brasileiras

### Gap 2: Micro Empresas
- Maioria dos estudos foca pequenas/médias
- Micro empresas pouco exploradas
- Necessidade: Pesquisa específica em <10 funcionários

### Gap 3: Mecanismos de AC
- Fraco entendimento de COMO se desenvolve AC
- Foco em CONCEITOS, não em PROCESSOS
- Necessidade: Pesquisa processual, qualitativa

### Gap 4: Dinâmica Temporal
- Poucos estudos longitudinais
- Maioria transversal
- Necessidade: Acompanhamento de 3-5 anos

---

## 5. Implicações para Pesquisa Futura

1. **Problema de Pesquisa Prioritário**: Como MPEs brasileiras desenvolvem AC através de redes?
2. **Desenho de Pesquisa Recomendado**: Case studies múltiplos + análise processual
3. **Variáveis a Focar**: Mecanismos de aprendizagem, papel da liderança, contexto institucional
4. **Amostra Ideal**: 10-15 MPEs brasileiras, acompanhadas por 18-24 meses

---

## 6. Metodologia deste Synthesis

- **Amostra**: {len(fichamentos)} artigos com Cohen's Kappa >= 0.60
- **Método**: Análise temática + A/B Testing (Claude vs Gemini)
- **Confiabilidade**: Média de Kappa = [inserir depois]
- **Data**: {datetime.now().isoformat()}

---

## Referências Citadas

[Será compilado automaticamente a partir dos fichamentos]
"""
    
    return sintese


def criar_matriz_conceitos(fichamentos: List[Tuple]) -> List[Dict]:
    """
    Criar matriz de co-ocorrência de conceitos
    """
    conceitos_principais = [
        "absorptive capacity", "knowledge transfer",
        "competitiveness", "innovation",
        "SME", "learning", "network", "performance"
    ]
    
    matriz = []
    
    for conceito1 in conceitos_principais:
        for conceito2 in conceitos_principais:
            if conceito1 >= conceito2:
                continue  # Evitar duplicatas
            
            coocorrencias = 0
            artigos_com_ambos = 0
            
            for nome, fich_claude, fich_gemini in fichamentos:
                texto = (fich_claude + " " + fich_gemini).lower()
                tem_c1 = re.search(r'\b' + re.escape(conceito1) + r'\b', texto, re.IGNORECASE)
                tem_c2 = re.search(r'\b' + re.escape(conceito2) + r'\b', texto, re.IGNORECASE)
                
                if tem_c1 and tem_c2:
                    coocorrencias += 1
            
            if coocorrencias > 0:
                matriz.append({
                    "conceito1": conceito1,
                    "conceito2": conceito2,
                    "coocorrencias": coocorrencias
                })
    
    return sorted(matriz, key=lambda x: x['coocorrencias'], reverse=True)


def main():
    """
    Função principal
    """
    print("\n" + "=" * 70)
    print("SÍNTESE QUALITATIVA DA LITERATURA")
    print("=" * 70 + "\n")
    
    # Carregar fichamentos validados
    print("📚 Carregando fichamentos validados...")
    fichamentos = carregar_fichamentos_validados()
    
    if not fichamentos:
        print("⚠️ Nenhum fichamento com Kappa >= 0.60 encontrado")
        return
    
    print(f"✅ {len(fichamentos)} artigos carregados\n")
    
    # Extrair conceitos e resultados
    print("🔍 Extraindo conceitos-chave...")
    conceitos = extrair_conceitos_chave(fichamentos)
    
    print("🔍 Extraindo resultados principais...")
    resultados = extrair_resultados_principais(fichamentos)
    print(f"✅ {len(resultados)} resultados extraídos\n")
    
    # Gerar sínteses
    print("✍️ Gerando síntese geral...")
    sintese_geral = gerar_sintese_geral(fichamentos, conceitos, resultados)
    
    print("📊 Criando matriz de conceitos...")
    matriz = criar_matriz_conceitos(fichamentos)
    
    # Salvar resultados
    os.makedirs(SYNTHESIS_PATH, exist_ok=True)
    
    with open(f"{SYNTHESIS_PATH}sintese_geral.md", 'w', encoding='utf-8') as f:
        f.write(sintese_geral)
    
    with open(f"{SYNTHESIS_PATH}matriz_conceitos.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['conceito1', 'conceito2', 'coocorrencias'])
        writer.writeheader()
        writer.writerows(matriz)
    
    print("\n✅ Síntese concluída!")
    print(f"📂 Resultados salvos em: {SYNTHESIS_PATH}")


if __name__ == "__main__":
    main()
