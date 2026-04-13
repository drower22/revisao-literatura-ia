"""
analise_lexical.py
Dicionários e Análise Léxica para Ranking de Relevância
========================================================

Define palavras-chave positivas e negativas usadas para scoring automático.
Fácil atualização conforme projeto evolui.
"""

from typing import Dict, List


class PalavrasChavePositivas:
    """Palavras que aumentam score de relevância"""
    
    # CORE DO PROJETO - Peso 3.0 (maior impacto)
    CORE_PROJETO = [
        # Capacidade absortiva
        'absorptive capacity',
        'capacidade absortiva',
        'AC',  # Cuidado com ambiguidade
        'absorção conhecimento',
        'absorbing knowledge',
        
        # Capacidades dinâmicas
        'dynamic capabilities',
        'capacidades dinâmicas',
        'DC',
        'dynamic capability',
        
        # Aprendizagem organizacional
        'organizational learning',
        'aprendizagem organizacional',
        'organizational learning process',
        'organizational knowledge',
        
        # Inovação e competitividade
        'competitividade',
        'competitiveness',
        'competitive advantage',
        'inovação',
        'innovation',
        'innovativeness',
    ]
    
    # CONTEXTO MPE/PME - Peso 2.5
    CONTEXTO_MPE = [
        'pme', 'mpe', 'sme', 'small medium enterprise',
        'pequena empresa', 'pequena e média',
        'micro empresa', 'microbusiness',
        'startup', 'startups',
        'medium enterprise', 'médium business',
        'smb', 'pmi', 'pmes', 'pequenos negócios',
        'small business', 'medium business',
    ]
    
    # MECANISMOS DE TRANSFERÊNCIA - Peso 2.0
    MECANISMOS = [
        # Redes e parcerias
        'redes', 'networks', 'network', 'rede de negócios',
        'business networks', 'business network',
        'parcerias', 'partnerships', 'partnership',
        'aliança', 'alianças', 'alliances',
        'clusters', 'cluster',
        
        # Colaboração
        'colaboração', 'collaboration', 'collaborative',
        'cooperação', 'cooperation', 'cooperative',
        'interação', 'interaction',
        
        # Transferência conhecimento
        'transferência conhecimento', 'knowledge transfer',
        'compartilhamento conhecimento', 'knowledge sharing',
        'spillover', 'knowledge spillover',
        'knowledge flow', 'fluxo conhecimento',
        
        # Aprendizagem
        'aprendizagem', 'learning', 'learning process',
        'conhecimento externo', 'external knowledge',
        'external sources',
        
        # Inovação aberta
        'open innovation', 'inovação aberta',
        'open source', 'crowdsourcing',
    ]
    
    # CONTEXTO GEOGRÁFICO - Peso 1.5
    CONTEXTO_GEOGRAFICO = [
        'brasil', 'brazil', 'brazilian', 'brasileiras',
        'américa latina', 'latin america', 'latino-americanas',
        'mercado emergente', 'emerging market',
        'países emergentes', 'emerging economies',
        'países em desenvolvimento', 'developing countries',
        'brics',
    ]
    
    # MÉTODO CIENTÍFICO - Peso 1.0
    METODO_CIENTIFICO = [
        'estudo empírico', 'empirical study', 'empirical research',
        'pesquisa quantitativa', 'quantitative research',
        'pesquisa qualitativa', 'qualitative research',
        'análise regressão', 'regression analysis',
        'modelo teórico', 'theoretical model',
        'survey', 'surveys',
        'entrevista', 'interviews', 'interview',
        'estudo de caso', 'case study',
        'modelo estrutural', 'structural equation model',
        'sem',  # SEM - Structural Equation Model
        'correlação', 'correlation', 'correlational',
        'dados longitudinais', 'longitudinal',
    ]


class PalavrasChaveNegativas:
    """Palavras que diminuem score de relevância"""
    
    # COMPLETAMENTE FORA ESCOPO - Penalidade: -50
    FORA_ESCOPO_FUNDAMENTAL = [
        'apenas revisão', 'only review', 'solely review',
        'revisão literatura', 'literature review',
        'revisão teórica', 'theoretical review',
        'opinion paper', 'artigo opinião',
        'editorial', 'editoriais',
        'news', 'notícia', 'notícias',
        'case study única', 'single case study',
        'commentary', 'comentário', 'comentários',
        'letter', 'carta', 'cartas',
        'book review', 'resenha',
    ]
    
    # TEMPORAL INADEQUADO - Penalidade: -30
    TEMPORAL_INADEQUADO = [
        'pré 2010', 'pre-2010', 'before 2010', 'anterior 2010',
        'antes 2000', 'prior 2000', 'anterior 2000',
        '19[0-9]{2}',  # Padrão regex: século 19
    ]
    
    # CONTEXTO INCOMPATÍVEL - Penalidade: -15
    CONTEXTO_INCOMPATIVEL = [
        'apenas grande empresa', 'only large firms', 'solely large',
        'fortune 500', 'empresas fortune',
        'multinacional apenas', 'multinational only',
        'multinational corporations', 'corporações multinacionais',
        'large corporation', 'large enterprise',
        'enterprise scale', 'escala corporativa',
        'big company', 'big firms', 'grandes empresas',
    ]
    
    # MÉTODO FRACO - Penalidade: -10
    METODO_FRACO = [
        'apenas opinião', 'expert opinion only',
        'suposições', 'assumptions only',
        'teórico apenas', 'purely theoretical', 'only theoretical',
        'sem dados', 'no data', 'sem validação',
        'especulativo', 'speculative',
        'não testado', 'untested',
    ]


class GramaticaAnalise:
    """Regras para análise mais sofisticada"""
    
    # Modificadores que fortalecem palavras-chave
    INTENSIFICADORES = ['muito', 'altamente', 'significativamente', 'critical', 'key', 'principal']
    
    # Negações que invertam sentido
    NEGACOES = ['não', 'não há', 'lacks', 'without', 'insufficient']
    
    # Contextos que fortalecem relevância
    CONTEXTOS_FORTE = [
        'neste estudo',
        'nosso modelo',
        'nossa análise',
        'encontramos',
        'descobrimos',
        'results show',
        'evidence',
    ]


class ConversorInterpretar:
    """Converte scores em interpretações textuais"""
    
    INTERPRETACOES = {
        (85, 100): ("🔴 Muito Alto", "Altamente relevante - core do projeto"),
        (70, 84): ("🟠 Alto", "Relevante - suporte teórico importante"),
        (50, 69): ("🟡 Moderado", "Moderadamente relevante - contexto útil"),
        (0, 49): ("🔵 Baixo", "Baixa relevância - considerar exclusão"),
    }
    
    @staticmethod
    def interpretar_score(score: float) -> tuple:
        """Retorna (emoji_nivel, interpretacao) para um score"""
        for (min_score, max_score), (nivel, desc) in ConversorInterpretar.INTERPRETACOES.items():
            if min_score <= score <= max_score:
                return (nivel, desc)
        return ("❓", "Score inválido")
    
    @staticmethod
    def sugerir_acao(score: float) -> str:
        """Sugere ação baseado no score"""
        if score >= 85:
            return "🔴 REVISAR COM PRIORIDADE 1 - Core do projeto"
        elif score >= 70:
            return "🟠 REVISAR COM PRIORIDADE 2 - Suporte teórico"
        elif score >= 50:
            return "🟡 REVISAR SE TEMPO - Contexto útil"
        else:
            return "🔵 PODE DESCARTAR - Baixa relevância"


# Função para expandir palavras-chave com variações
def gerar_variacoes(palavra: str) -> List[str]:
    """Gera variações de uma palavra-chave"""
    variacoes = [palavra]
    
    # Plurais
    if not palavra.endswith('s'):
        variacoes.append(palavra + 's')
    
    # Variações de espaço/hífen
    if ' ' in palavra:
        variacoes.append(palavra.replace(' ', '-'))
        variacoes.append(palavra.replace(' ', '_'))
    
    return variacoes


# Importar em outros módulos:
# from utils.analise_lexical import PalavrasChavePositivas, PalavrasChaveNegativas
# from utils.analise_lexical import ConversorInterpretar
