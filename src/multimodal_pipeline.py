"""
Pipeline multimodal do Tech Challenge Fase 4.

Este arquivo integra:
- análise de áudio/texto;
- análise de vídeo;
- detecção de anomalias em sinais vitais;
- geração de alerta final para a equipe médica.
"""

from datetime import datetime

from audio_analysis import analisar_transcricao
from video_analysis import analisar_video_clinico
from anomaly_detection import detectar_anomalias_sinais_vitais


def definir_gravidade_final(resultados: list) -> str:
    """
    Define a gravidade final com base nos resultados dos módulos.
    """

    gravidades = [resultado["gravidade"] for resultado in resultados]

    if "crítico" in gravidades:
        return "crítico"
    elif "alto" in gravidades:
        return "alto"
    elif "atenção" in gravidades:
        return "atenção"
    else:
        return "normal"


def gerar_recomendacao(gravidade: str) -> str:
    """
    Gera uma recomendação simples para a equipe médica.
    """

    if gravidade == "crítico":
        return "Acionar equipe médica imediatamente e priorizar atendimento."
    elif gravidade == "alto":
        return "Encaminhar alerta para avaliação clínica urgente."
    elif gravidade == "atenção":
        return "Manter paciente em observação e revisar sinais clínicos."
    else:
        return "Sem anomalias relevantes detectadas no momento."


def executar_pipeline_multimodal() -> dict:
    """
    Executa uma demonstração integrada do pipeline multimodal.
    """

    transcricao_audio = (
        "Paciente relata falta de ar, tontura e cansaço extremo durante a consulta."
    )

    sinais_vitais = {
        "frequencia_cardiaca": 132,
        "pressao_sistolica": 165,
        "pressao_diastolica": 105,
        "saturacao_oxigenio": 88,
        "temperatura": 38.2
    }

    evento_video = "Paciente apresentou movimento brusco durante exercício de fisioterapia."
    intensidade_movimento = 0.82

    resultado_audio = analisar_transcricao(transcricao_audio)

    resultado_sinais = detectar_anomalias_sinais_vitais(sinais_vitais)

    resultado_video = analisar_video_clinico(
        evento_observado=evento_video,
        intensidade_movimento=intensidade_movimento
    )

    resultados = [
        resultado_audio,
        resultado_sinais,
        resultado_video
    ]

    gravidade_final = definir_gravidade_final(resultados)

    alerta_final = {
        "paciente_id": "PACIENTE_SIMULADO_001",
        "timestamp": datetime.now().isoformat(),
        "gravidade_final": gravidade_final,
        "recomendacao": gerar_recomendacao(gravidade_final),
        "resultados_modulos": resultados
    }

    return alerta_final


if __name__ == "__main__":
    alerta = executar_pipeline_multimodal()
    print(alerta)
