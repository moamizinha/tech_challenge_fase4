"""
Módulo de especificação do fluxo multimodal para DPP.

Este arquivo é responsável por:
- definir as etapas do pipeline de processamento de áudio para DPP;
- especificar entrada, saída e serviço de cada etapa;
- listar os serviços Azure integrados;
- gerar uma visualização do fluxo para documentação.

Integra com o pipeline multimodal do grupo (src/multimodal_pipeline.py)
adicionando o módulo de análise de áudio especializado em saúde da mulher.
"""

from datetime import datetime


# ─────────────────────────────────────────────
# Etapas do pipeline de áudio para DPP
# ─────────────────────────────────────────────

PIPELINE_AUDIO_DPP = [
    {
        "etapa": 1,
        "nome": "ingestao",
        "descricao": "Recebe áudio WAV (upload) ou texto JSON (transcrição pronta)",
        "entrada": "Arquivo WAV ou string de texto",
        "saida": "Bytes de áudio em memória OU texto para análise direta",
        "servico_local": "Backend FastAPI (porta 8000)",
        "servico_azure": "Azure Container App: ppd-dev-backend",
    },
    {
        "etapa": 2,
        "nome": "transcricao_stt",
        "descricao": "Converte áudio em texto usando Speech-to-Text (pt-BR)",
        "entrada": "Bytes de áudio WAV",
        "saida": "Texto transcrito em português brasileiro",
        "servico_local": "faster-whisper (modelo small, CPU)",
        "servico_azure": "Azure AI Speech SDK (pt-BR-FranciscaNeural)",
    },
    {
        "etapa": 3,
        "nome": "nlp_classificacao",
        "descricao": (
            "Classifica o texto em 3 níveis de risco "
            "(HIGH_RISK / MONITORING / LOW_RISK) usando TF-IDF + LDA + "
            "Regressão Logística com override por flags clínicas"
        ),
        "entrada": "Texto transcrito",
        "saida": "Label de risco, probabilidades por classe, flags clínicas",
        "servico_local": "nlp-model (container Docker, porta 8001)",
        "servico_azure": "Azure Container App: ppd-dev-nlp-model",
    },
    {
        "etapa": 4,
        "nome": "risk_engine",
        "descricao": (
            "Calibra probabilidades com StandardScaler + Regressão Logística. "
            "Aplica regras de confiança para revisão humana."
        ),
        "entrada": "Probabilidades por classe (HIGH_RISK_score, MONITORING_score, LOW_RISK_score)",
        "saida": "Nível de risco final, confiança, revisão humana obrigatória, top sinais",
        "servico_local": "risk-engine (container Docker, porta 8002)",
        "servico_azure": "Azure Container App: ppd-dev-risk-engine",
    },
    {
        "etapa": 5,
        "nome": "salvaguarda_clinica",
        "descricao": (
            "Segunda camada de defesa: se flags clínicas dispararam, "
            "força revisão humana e impede resultado LOW_RISK"
        ),
        "entrada": "Resultado do risk_engine + flags clínicas do NLP",
        "saida": "Resultado final ajustado (nível pode ser elevado)",
        "servico_local": "Backend (_run_pipeline)",
        "servico_azure": "Azure Container App: ppd-dev-backend",
    },
    {
        "etapa": 6,
        "nome": "alerta_equipe_medica",
        "descricao": (
            "Enfileira resultado na fila de revisão humana. "
            "HIGH_RISK = alerta obrigatório. "
            "Frontend exibe banner e fila para profissionais de saúde."
        ),
        "entrada": "Resultado final com flag de revisão humana",
        "saida": "Registro na fila de revisão (Blob ou memória local)",
        "servico_local": "Backend (review_store) + Frontend (React)",
        "servico_azure": "Azure Blob Storage (review-queue) + Azure Function",
    },
]


# ─────────────────────────────────────────────
# Pipeline assíncrono (produção via Event Grid)
# ─────────────────────────────────────────────

PIPELINE_ASSINCRONO = [
    {
        "etapa": 1,
        "nome": "upload_blob",
        "descricao": "Áudio enviado ao Blob Storage (container audio-uploads)",
        "entrada": "Arquivo WAV",
        "saida": "Blob criado → dispara Event Grid",
        "servico_azure": "Azure Storage Account",
    },
    {
        "etapa": 2,
        "nome": "function_process_audio",
        "descricao": "Azure Function transcreve o áudio via Speech SDK",
        "entrada": "Evento Event Grid (blob URL do áudio)",
        "saida": "JSON com transcrição gravado em transcripts/",
        "servico_azure": "Azure Function: process_audio",
    },
    {
        "etapa": 3,
        "nome": "function_analyze_transcript",
        "descricao": "Azure Function chama NLP + Risk Engine e grava resultado",
        "entrada": "Evento Event Grid (blob URL da transcrição)",
        "saida": "JSON em results/ + enfileiramento em review-queue",
        "servico_azure": "Azure Function: analyze_transcript",
    },
]


# ─────────────────────────────────────────────
# Serviços Azure integrados
# ─────────────────────────────────────────────

SERVICOS_AZURE = [
    {"servico": "Azure AI Speech Service", "uso": "Transcrição de áudio pt-BR"},
    {"servico": "Azure Language Service", "uso": "Análise de sentimento (provisionado)"},
    {"servico": "Azure Container Apps", "uso": "Deploy dos 4 microsserviços"},
    {"servico": "Azure Storage Account", "uso": "Modelos, dados, fila de revisão, áudios"},
    {"servico": "Azure Functions", "uso": "Pipeline assíncrono (Event Grid)"},
    {"servico": "Azure Event Grid", "uso": "Triggers entre Blob e Functions"},
    {"servico": "Azure Container Registry", "uso": "Registro de imagens Docker"},
    {"servico": "Azure AI Foundry", "uso": "Workspace para rotulagem futura"},
]


# ─────────────────────────────────────────────
# Integração com o pipeline multimodal do grupo
# ─────────────────────────────────────────────

def gerar_resultado_para_pipeline(texto: str) -> dict:
    """
    Gera um resultado no formato padrão do pipeline multimodal do grupo.

    Compatível com a função definir_gravidade_final() de
    src/multimodal_pipeline.py que espera:
    - tipo_dado
    - evento
    - gravidade (normal | atenção | alto | crítico)
    - timestamp
    - descricao
    """
    from severity_matrix import classificar_gravidade_dpp

    resultado = classificar_gravidade_dpp(texto)

    return {
        "tipo_dado": resultado["tipo_dado"],
        "evento": resultado["evento"],
        "gravidade": resultado["gravidade"],
        "timestamp": resultado["timestamp"],
        "descricao": resultado["descricao"],
        "detalhes_dpp": {
            "nivel_risco": resultado["nivel_risco"],
            "rotulo": resultado["rotulo"],
            "revisao_humana": resultado["revisao_humana_obrigatoria"],
            "flags_clinicas": resultado["flags_clinicas"],
        },
    }


# ─────────────────────────────────────────────
# Visualização do pipeline
# ─────────────────────────────────────────────

def imprimir_pipeline():
    """Imprime o fluxo multimodal de áudio para DPP."""
    print("=" * 70)
    print("FLUXO MULTIMODAL — Análise de Áudio para Depressão Pós-Parto")
    print("=" * 70)

    print("\n▶ FLUXO SÍNCRONO (Backend FastAPI):\n")
    for etapa in PIPELINE_AUDIO_DPP:
        print(f"  {etapa['etapa']}. [{etapa['nome']}]")
        print(f"     {etapa['descricao']}")
        print(f"     Entrada: {etapa['entrada']}")
        print(f"     Saída:   {etapa['saida']}")
        print(f"     Local:   {etapa['servico_local']}")
        print(f"     Azure:   {etapa['servico_azure']}")
        print()

    print("\n▶ FLUXO ASSÍNCRONO (Azure Functions + Event Grid):\n")
    for etapa in PIPELINE_ASSINCRONO:
        print(f"  {etapa['etapa']}. [{etapa['nome']}]")
        print(f"     {etapa['descricao']}")
        print(f"     Entrada: {etapa['entrada']}")
        print(f"     Saída:   {etapa['saida']}")
        print(f"     Azure:   {etapa['servico_azure']}")
        print()

    print("\n▶ SERVIÇOS AZURE INTEGRADOS:\n")
    for svc in SERVICOS_AZURE:
        print(f"  • {svc['servico']}: {svc['uso']}")

    print("\n" + "=" * 70)
    print("FLUXO RESUMIDO:")
    print("=" * 70)
    print("""
    Áudio WAV (consulta pós-parto)
            │
            ▼
    Azure Speech to Text / Whisper (transcrição pt-BR)
            │
            ▼
    NLP Model (TF-IDF + LDA + LogReg + Flags Clínicas)
            │
            ▼
    Risk Engine (StandardScaler + LogReg → calibração)
            │
            ▼
    Salvaguarda Clínica (defesa em profundidade)
            │
            ▼
    Alerta para Equipe Médica (fila de revisão humana)
    """)


if __name__ == "__main__":
    imprimir_pipeline()
