"""
Pipeline multimodal do Tech Challenge Fase 4.

Este arquivo integra:
- análise de áudio/texto;
- análise de vídeo;
- análise de imagem de monitor de sinais vitais;
- análise de prescrições médicas;
- geração de alerta final para a equipe médica.
"""

from datetime import datetime
from pathlib import Path

from audio_analysis import analisar_transcricao
from video_analysis import analisar_video_clinico
from vital_signs_image_analysis import analisar_imagem_monitor
from prescription_analysis import analisar_base_prescricoes


BASE_DIR = Path(__file__).resolve().parents[1]
CAMINHO_IMAGEM_MONITOR = BASE_DIR / "data" / "images" / "monitor_sinais_vitais.png"


def definir_gravidade_final(resultados: list) -> str:
    """
    Define a gravidade final com base nos resultados dos módulos.
    """

    ordem = {
        "normal": 0,
        "atenção": 1,
        "alto": 2,
        "crítico": 3,
    }

    maior_gravidade = "normal"

    for resultado in resultados:
        gravidade = resultado.get("gravidade", "normal")

        if ordem.get(gravidade, 0) > ordem[maior_gravidade]:
            maior_gravidade = gravidade

    return maior_gravidade


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


def resumir_prescricoes_criticas(resultados_prescricoes: list) -> dict:
    """
    Resume os resultados das prescrições para entrada no pipeline multimodal.
    """

    prescricoes_com_alerta = [
        item for item in resultados_prescricoes
        if item.get("gravidade") != "normal"
    ]

    gravidade_prescricao = definir_gravidade_final(prescricoes_com_alerta)

    return {
        "tipo_dado": "prescricoes",
        "evento": "analise_de_prescricoes",
        "gravidade": gravidade_prescricao,
        "timestamp": datetime.now().isoformat(),
        "descricao": "Análise de prescrições simuladas para identificação de alterações inesperadas.",
        "total_prescricoes_analisadas": len(resultados_prescricoes),
        "total_prescricoes_com_alerta": len(prescricoes_com_alerta),
        "prescricoes_com_alerta": prescricoes_com_alerta
    }


def executar_pipeline_multimodal() -> dict:
    """
    Executa uma demonstração integrada do pipeline multimodal.
    """

    transcricao_audio = (
        "Paciente relata falta de ar, tontura e cansaço extremo durante a consulta."
    )

    evento_video = (
        "Paciente apresentou movimento brusco durante exercício de fisioterapia."
    )

    intensidade_movimento = 0.82

    resultado_audio = analisar_transcricao(transcricao_audio)

    resultado_video = analisar_video_clinico(
        evento_observado=evento_video,
        intensidade_movimento=intensidade_movimento
    )

    if CAMINHO_IMAGEM_MONITOR.exists():
        resultado_imagem_sinais = analisar_imagem_monitor(
            str(CAMINHO_IMAGEM_MONITOR)
        )
    else:
        resultado_imagem_sinais = {
            "tipo_dado": "imagem_sinais_vitais",
            "evento": "imagem_nao_encontrada",
            "gravidade": "normal",
            "timestamp": datetime.now().isoformat(),
            "descricao": (
                "Imagem do monitor não encontrada. "
                "Coloque o arquivo em data/images/monitor_sinais_vitais.png."
            ),
            "alertas": []
        }

    resultados_prescricoes = analisar_base_prescricoes()
    resultado_prescricoes = resumir_prescricoes_criticas(resultados_prescricoes)

    resultados = [
        resultado_audio,
        resultado_video,
        resultado_imagem_sinais,
        resultado_prescricoes
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