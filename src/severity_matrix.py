"""
Módulo de matriz de severidade para depressão pós-parto (DPP).

Este arquivo é responsável por:
- definir os níveis de risco para análise de áudio em consultas pós-parto;
- classificar a gravidade com base em termos críticos detectados;
- aplicar regras de escalada por flags clínicas;
- determinar se revisão humana é obrigatória;
- gerar uma saída padronizada para o pipeline multimodal.
"""

from datetime import datetime


# ─────────────────────────────────────────────
# Níveis de gravidade (alinhados ao padrão do projeto)
# ─────────────────────────────────────────────

NIVEIS_RISCO = ["HIGH_RISK", "MONITORING", "LOW_RISK"]

ROTULO_EXIBICAO = {
    "HIGH_RISK": "Alto Risco",
    "MONITORING": "Monitorar paciente",
    "LOW_RISK": "Baixo Risco",
}

# Mapeamento para a escala de gravidade do pipeline multimodal do grupo
MAPA_GRAVIDADE_PIPELINE = {
    "HIGH_RISK": "crítico",
    "MONITORING": "atenção",
    "LOW_RISK": "normal",
}

ORDEM_GRAVIDADE = {
    "normal": 0,
    "atenção": 1,
    "alto": 2,
    "crítico": 3,
}


# ─────────────────────────────────────────────
# Limiares de confiança para revisão humana
# ─────────────────────────────────────────────

LIMIAR_REVISAO_HUMANA = {
    "HIGH_RISK": 1.0,     # sempre revisão (qualquer confiança)
    "MONITORING": 0.75,   # revisão se confiança < 75%
    "LOW_RISK": 0.55,     # revisão se confiança < 55%
}

# Limiar para escalada por flag clínica
LIMIAR_ESCALADA_FLAG_CLINICA = 0.20


# ─────────────────────────────────────────────
# Flags Clínicas de Alto Risco
# ─────────────────────────────────────────────

HIGH_RISK_PHRASES = [
    # Ideação suicida passiva
    "não estar aqui",
    "não estivesse aqui",
    "melhor sem mim",
    "seria melhor sem mim",
    "estariam melhor sem mim",
    "quero desaparecer",
    "quero sumir",
    "não quero mais viver",
    "não quero viver",
    "vontade de morrer",
    "penso em morrer",
    "pensamentos suicidas",
    # Risco de dano ao bebê
    "me machucar",
    "machucar meu filho",
    "machucar o bebê",
    "fazer algo ruim",
    # Psicose (alucinações)
    "ouço vozes",
    "vejo coisas",
    "ouço coisas",
    "perdendo a sanidade",
    "perco a sanidade",
    # Dissociação / despersonalização
    "saio do meu corpo",
    "saindo do meu corpo",
    "fora do meu corpo",
    "não me reconheço no espelho",
    # Automutilação / abandono
    "aperto meu braço",
    "abandonar o bebê",
    "pensamentos intrusivos",
    "imagem de machucar",
    "indo embora de dentro",
    # Ideação suicida passiva — indireta
    "seria melhor para todo mundo",
    "seria melhor se eu",
    "melhor para todos se eu",
    "se eu simplesmente sumisse",
    "se eu desaparecesse",
    # Dissociação — continuação
    "não sou mais eu",
    "estou desaparecendo",
    "desaparecendo aos poucos",
    # Medo de perda de controle
    "com medo de mim mesma",
    "com medo de mim mesmo",
    "medo de mim mesma",
    "medo de mim mesmo",
    "com medo de mim",
    # Pensamentos intrusivos de dano
    "pensamentos horríveis",
    "pensamento horrível",
    "imaginando coisas ruins",
    "coisas ruins acontecendo",
    "imagino coisas ruins",
]


# ─────────────────────────────────────────────
# Flags Clínicas de Monitoramento
# ─────────────────────────────────────────────

MONITORING_PHRASES = [
    "verificando se está respirando",
    "verifico se está respirando",
    "choro sem motivo",
    "choro sem razão",
    "não sou boa mãe",
    "não me sinto boa mãe",
    "não consigo relaxar",
    "me sinto culpada",
    "sentimento de culpa",
    "ansiedade constante",
    "dias bons e dias ruins",
]


# ─────────────────────────────────────────────
# Definição da Matriz de Severidade
# ─────────────────────────────────────────────

MATRIZ_SEVERIDADE = [
    {
        "nivel": "HIGH_RISK",
        "rotulo": "Alto Risco",
        "gravidade_pipeline": "crítico",
        "sinais_tipicos": [
            "Ideação suicida (ativa ou passiva)",
            "Medo de machucar o bebê",
            "Psicose puerperal (alucinações auditivas/visuais)",
            "Dissociação / despersonalização",
            "Pensamentos intrusivos de dano",
            "Negligência grave com o bebê",
            "Perda total de funcionalidade",
        ],
        "revisao_humana": "sempre",
        "acao_clinica": (
            "Encaminhamento IMEDIATO para avaliação psiquiátrica/psicológica presencial. "
            "Contato ativo com a paciente em até 24h. "
            "Avaliar necessidade de internação."
        ),
        "prioridade": 1,
    },
    {
        "nivel": "MONITORING",
        "rotulo": "Monitorar paciente",
        "gravidade_pipeline": "atenção",
        "sinais_tipicos": [
            "Ansiedade constante / preocupação excessiva",
            "Culpa recorrente (amamentação, maternidade)",
            "Choro sem motivo aparente",
            "Insônia não explicada por cuidados com o bebê",
            "Dificuldade funcional leve",
            "Sentimento de não ser 'boa mãe'",
            "Isolamento social leve",
            "Irritabilidade desproporcional",
        ],
        "revisao_humana": "condicional (confiança < 75%)",
        "acao_clinica": (
            "Acompanhamento próximo com reavaliação em 1-2 semanas. "
            "Reforço de rede de apoio. Aplicar escala EPDS na próxima consulta."
        ),
        "prioridade": 2,
    },
    {
        "nivel": "LOW_RISK",
        "rotulo": "Baixo Risco",
        "gravidade_pipeline": "normal",
        "sinais_tipicos": [
            "Adaptação normal ao pós-parto",
            "Cansaço compatível com privação de sono",
            "Momentos de choro com recuperação rápida",
            "Funcionalidade preservada",
            "Vínculo com o bebê presente",
            "Rede de apoio ativa",
        ],
        "revisao_humana": "condicional (confiança < 55%)",
        "acao_clinica": (
            "Monitoramento de rotina. "
            "Orientação sobre sinais de alerta para retorno antecipado."
        ),
        "prioridade": 3,
    },
]


# ─────────────────────────────────────────────
# Funções de classificação
# ─────────────────────────────────────────────

def detectar_flags_clinicas(texto: str) -> dict:
    """
    Detecta flags clínicas de alto risco e monitoramento no texto.

    Retorna contagem de flags disparadas por categoria.
    """
    texto_lower = texto.lower()

    flags_high = [frase for frase in HIGH_RISK_PHRASES if frase in texto_lower]
    flags_monitoring = [frase for frase in MONITORING_PHRASES if frase in texto_lower]

    return {
        "high_risk_flags": flags_high,
        "monitoring_flags": flags_monitoring,
        "total_high_risk": len(flags_high),
        "total_monitoring": len(flags_monitoring),
    }


def classificar_gravidade_dpp(texto: str) -> dict:
    """
    Classifica a gravidade de uma transcrição de consulta pós-parto
    com base nas flags clínicas detectadas.

    Esta é uma classificação preliminar baseada em regras.
    O modelo de ML (TF-IDF + LDA + LogReg) refina essa classificação.

    Retorna uma saída padronizada compatível com o pipeline multimodal.
    """
    flags = detectar_flags_clinicas(texto)

    if flags["total_high_risk"] > 0:
        nivel = "HIGH_RISK"
    elif flags["total_monitoring"] > 0:
        nivel = "MONITORING"
    else:
        nivel = "LOW_RISK"

    gravidade_pipeline = MAPA_GRAVIDADE_PIPELINE[nivel]
    revisao_humana = requer_revisao_humana(nivel, confianca=1.0, flags_disparadas=flags["total_high_risk"])

    return {
        "tipo_dado": "audio_texto_dpp",
        "evento": "classificacao_risco_dpp",
        "gravidade": gravidade_pipeline,
        "nivel_risco": nivel,
        "rotulo": ROTULO_EXIBICAO[nivel],
        "revisao_humana_obrigatoria": revisao_humana,
        "timestamp": datetime.now().isoformat(),
        "descricao": texto,
        "flags_clinicas": flags,
    }


def deve_escalar_risco(nivel_atual: str, prob_high_risk: float, flags_high_risk: int) -> str:
    """
    Aplica regras de escalada da matriz de severidade.

    Regras:
    1. Flag HIGH_RISK + nível LOW_RISK → eleva para MONITORING ou HIGH_RISK
    2. Flag HIGH_RISK + nível MONITORING → eleva para HIGH_RISK se prob >= limiar
    3. LOW_RISK nunca pode coexistir com flag clínica ativa
    """
    if flags_high_risk > 0:
        if nivel_atual == "LOW_RISK":
            if prob_high_risk >= LIMIAR_ESCALADA_FLAG_CLINICA:
                return "HIGH_RISK"
            else:
                return "MONITORING"

        if nivel_atual == "MONITORING":
            if prob_high_risk >= LIMIAR_ESCALADA_FLAG_CLINICA:
                return "HIGH_RISK"

    return nivel_atual


def requer_revisao_humana(nivel: str, confianca: float, flags_disparadas: int) -> bool:
    """
    Determina se o caso requer revisão humana obrigatória.

    Revisão é obrigatória quando:
    - Nível é HIGH_RISK (sempre)
    - Confiança abaixo do limiar para o nível
    - Qualquer flag clínica foi disparada
    """
    if flags_disparadas > 0:
        return True

    if nivel == "HIGH_RISK":
        return True

    limiar = LIMIAR_REVISAO_HUMANA.get(nivel, 0.75)
    return confianca < limiar


# ─────────────────────────────────────────────
# Demonstração
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("MATRIZ PRELIMINAR DE SEVERIDADE — Depressão Pós-Parto")
    print("=" * 70)

    for nivel in MATRIZ_SEVERIDADE:
        print(f"\n{'─' * 70}")
        print(f"  NÍVEL: {nivel['rotulo']} ({nivel['nivel']}) — Prioridade {nivel['prioridade']}")
        print(f"  Gravidade no pipeline: {nivel['gravidade_pipeline']}")
        print(f"  Revisão humana: {nivel['revisao_humana']}")
        print(f"{'─' * 70}")
        print(f"  Sinais típicos:")
        for sinal in nivel["sinais_tipicos"]:
            print(f"    • {sinal}")
        print(f"\n  Ação clínica:")
        print(f"    {nivel['acao_clinica']}")

    print(f"\n{'─' * 70}")
    print(f"\n  FLAGS DE ALTO RISCO: {len(HIGH_RISK_PHRASES)} frases")
    print(f"  FLAGS DE MONITORAMENTO: {len(MONITORING_PHRASES)} frases")

    # Demonstração com texto exemplo
    print(f"\n{'=' * 70}")
    print("DEMONSTRAÇÃO — Classificação de texto")
    print("=" * 70)

    exemplos = [
        "Eu tenho vontade de morrer, não aguento mais essa situação.",
        "Me sinto culpada por não conseguir amamentar, choro sem motivo.",
        "Estou cansada mas feliz, o bebê está crescendo bem.",
    ]

    for texto in exemplos:
        resultado = classificar_gravidade_dpp(texto)
        print(f"\n  Texto: \"{texto}\"")
        print(f"  Nível: {resultado['rotulo']} ({resultado['nivel_risco']})")
        print(f"  Gravidade pipeline: {resultado['gravidade']}")
        print(f"  Revisão humana: {'SIM' if resultado['revisao_humana_obrigatoria'] else 'NÃO'}")
        if resultado["flags_clinicas"]["high_risk_flags"]:
            print(f"  Flags HIGH_RISK: {resultado['flags_clinicas']['high_risk_flags']}")
        if resultado["flags_clinicas"]["monitoring_flags"]:
            print(f"  Flags MONITORING: {resultado['flags_clinicas']['monitoring_flags']}")
