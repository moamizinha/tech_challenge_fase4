"""
Módulo de análise de imagem de monitor de sinais vitais.

Nesta versão inicial, a imagem é usada como evidência visual e os sinais vitais
são extraídos de forma estruturada a partir dos valores exibidos no monitor.

Em uma evolução futura, essa etapa pode ser automatizada com OCR, como Azure
Computer Vision, Tesseract ou outro serviço de visão computacional.
"""

from datetime import datetime
from pathlib import Path

from anomaly_detection import detectar_anomalias_sinais_vitais


def extrair_sinais_vitais_da_imagem(caminho_imagem: str) -> dict:
    """
    Simula a extração estruturada dos sinais vitais exibidos na imagem do monitor.

    A imagem analisada apresenta:
    - FC/ECG: 120 bpm
    - SpO2: 98%
    - RESP: 24 rpm
    - ETCO2: 35 mmHg
    - PVC: 18/12 mmHg
    - TEMP: 36.7 °C
    - PNI: 119/79 mmHg
    """

    imagem = Path(caminho_imagem)

    if not imagem.exists():
        raise FileNotFoundError(f"Imagem não encontrada: {caminho_imagem}")

    sinais_extraidos = {
        "fonte": "imagem_monitor_multiparametrico",
        "arquivo_imagem": str(imagem),
        "timestamp_analise": datetime.now().isoformat(),

        "frequencia_cardiaca": 120,
        "pressao_sistolica": 119,
        "pressao_diastolica": 79,
        "pressao_media": 90,
        "saturacao_oxigenio": 98,
        "frequencia_respiratoria": 24,
        "etco2": 35,
        "temperatura": 36.7,

        "pvc_sistolica": 18,
        "pvc_diastolica": 12,
        "pvc_media": 14,

        "alertas_visuais_monitor": [
            "FC ALTA",
            "PVC ALTA"
        ]
    }

    return sinais_extraidos


def analisar_imagem_monitor(caminho_imagem: str) -> dict:
    """
    Analisa uma imagem de monitor multiparamétrico e gera alerta clínico.
    """

    sinais = extrair_sinais_vitais_da_imagem(caminho_imagem)

    resultado_anomalias = detectar_anomalias_sinais_vitais(sinais)

    alertas_complementares = []

    if sinais["frequencia_respiratoria"] > 22:
        alertas_complementares.append({
            "evento": "frequencia_respiratoria_elevada",
            "gravidade": "atenção",
            "descricao": f"Frequência respiratória elevada: {sinais['frequencia_respiratoria']} rpm."
        })

    if sinais["pvc_media"] > 12:
        alertas_complementares.append({
            "evento": "pvc_elevada",
            "gravidade": "alto",
            "descricao": f"PVC média elevada: {sinais['pvc_media']} mmHg."
        })

    if "FC ALTA" in sinais["alertas_visuais_monitor"]:
        alertas_complementares.append({
            "evento": "alerta_visual_fc_alta",
            "gravidade": "alto",
            "descricao": "O monitor apresentou alerta visual de frequência cardíaca alta."
        })

    if "PVC ALTA" in sinais["alertas_visuais_monitor"]:
        alertas_complementares.append({
            "evento": "alerta_visual_pvc_alta",
            "gravidade": "alto",
            "descricao": "O monitor apresentou alerta visual de PVC alta."
        })

    todos_alertas = resultado_anomalias.get("alertas", []) + alertas_complementares

    gravidades = [alerta["gravidade"] for alerta in todos_alertas]

    if "crítico" in gravidades:
        gravidade_final = "crítico"
    elif "alto" in gravidades:
        gravidade_final = "alto"
    elif "atenção" in gravidades:
        gravidade_final = "atenção"
    else:
        gravidade_final = "normal"

    return {
        "tipo_dado": "imagem_sinais_vitais",
        "evento": "analise_imagem_monitor",
        "gravidade": gravidade_final,
        "timestamp": datetime.now().isoformat(),
        "sinais_extraidos": sinais,
        "alertas": todos_alertas,
        "descricao": "Análise estruturada de imagem de monitor multiparamétrico."
    }


if __name__ == "__main__":
    caminho = "data/images/monitor_sinais_vitais.png"
    resultado = analisar_imagem_monitor(caminho)
    print(resultado)