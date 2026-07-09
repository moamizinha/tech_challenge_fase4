"""
Módulo de análise de áudio e texto.

Este arquivo será responsável por:
- receber uma transcrição de consulta médica;
- identificar termos críticos;
- classificar o nível de risco;
- gerar uma saída padronizada para o pipeline multimodal.
"""

from datetime import datetime


TERMOS_CRITICOS = {
    "falta de ar": "crítico",
    "dor no peito": "crítico",
    "desmaio": "crítico",
    "cansaço extremo": "alto",
    "tontura": "alto",
    "fadiga": "atenção",
    "fraqueza": "atenção",
}


def analisar_transcricao(transcricao: str) -> dict:
    """
    Analisa uma transcrição de áudio e identifica termos críticos.
    """

    transcricao_lower = transcricao.lower()
    termos_detectados = []

    for termo, gravidade in TERMOS_CRITICOS.items():
        if termo in transcricao_lower:
            termos_detectados.append({
                "termo": termo,
                "gravidade": gravidade
            })

    if any(item["gravidade"] == "crítico" for item in termos_detectados):
        gravidade_final = "crítico"
    elif any(item["gravidade"] == "alto" for item in termos_detectados):
        gravidade_final = "alto"
    elif termos_detectados:
        gravidade_final = "atenção"
    else:
        gravidade_final = "normal"

    return {
        "tipo_dado": "audio_texto",
        "evento": "analise_de_transcricao",
        "gravidade": gravidade_final,
        "timestamp": datetime.now().isoformat(),
        "descricao": transcricao,
        "termos_detectados": termos_detectados,
    }


if __name__ == "__main__":
    exemplo = "Paciente relata falta de ar, tontura e cansaço extremo durante a consulta."
    resultado = analisar_transcricao(exemplo)
    print(resultado)
