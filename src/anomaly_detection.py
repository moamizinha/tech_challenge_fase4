"""
Módulo de detecção de anomalias em sinais vitais.

Este arquivo será responsável por:
- analisar sinais vitais simulados;
- identificar valores fora do padrão esperado;
- classificar a gravidade do evento;
- gerar uma saída padronizada para o pipeline multimodal.
"""

from datetime import datetime


def detectar_anomalias_sinais_vitais(sinais: dict) -> dict:
    """
    Detecta anomalias simples em sinais vitais.

    Parâmetros esperados:
    - frequencia_cardiaca
    - pressao_sistolica
    - pressao_diastolica
    - saturacao_oxigenio
    - temperatura
    """

    alertas = []

    frequencia = sinais.get("frequencia_cardiaca")
    pressao_sistolica = sinais.get("pressao_sistolica")
    pressao_diastolica = sinais.get("pressao_diastolica")
    saturacao = sinais.get("saturacao_oxigenio")
    temperatura = sinais.get("temperatura")

    if frequencia is not None:
        if frequencia < 50:
            alertas.append({
                "evento": "bradicardia",
                "gravidade": "alto",
                "descricao": f"Frequência cardíaca baixa: {frequencia} bpm."
            })
        elif frequencia > 120:
            alertas.append({
                "evento": "taquicardia",
                "gravidade": "alto",
                "descricao": f"Frequência cardíaca elevada: {frequencia} bpm."
            })

    if pressao_sistolica is not None and pressao_diastolica is not None:
        if pressao_sistolica > 160 or pressao_diastolica > 100:
            alertas.append({
                "evento": "pressao_alta",
                "gravidade": "alto",
                "descricao": f"Pressão arterial elevada: {pressao_sistolica}/{pressao_diastolica} mmHg."
            })
        elif pressao_sistolica < 90 or pressao_diastolica < 60:
            alertas.append({
                "evento": "pressao_baixa",
                "gravidade": "atenção",
                "descricao": f"Pressão arterial baixa: {pressao_sistolica}/{pressao_diastolica} mmHg."
            })

    if saturacao is not None:
        if saturacao < 90:
            alertas.append({
                "evento": "hipoxemia",
                "gravidade": "crítico",
                "descricao": f"Saturação de oxigênio crítica: {saturacao}%."
            })
        elif saturacao < 94:
            alertas.append({
                "evento": "queda_saturacao",
                "gravidade": "alto",
                "descricao": f"Saturação de oxigênio abaixo do esperado: {saturacao}%."
            })

    if temperatura is not None:
        if temperatura >= 38:
            alertas.append({
                "evento": "febre",
                "gravidade": "atenção",
                "descricao": f"Temperatura elevada: {temperatura} °C."
            })
        elif temperatura < 35:
            alertas.append({
                "evento": "hipotermia",
                "gravidade": "alto",
                "descricao": f"Temperatura corporal baixa: {temperatura} °C."
            })

    if any(alerta["gravidade"] == "crítico" for alerta in alertas):
        gravidade_final = "crítico"
    elif any(alerta["gravidade"] == "alto" for alerta in alertas):
        gravidade_final = "alto"
    elif alertas:
        gravidade_final = "atenção"
    else:
        gravidade_final = "normal"

    return {
        "tipo_dado": "sinais_vitais",
        "evento": "deteccao_de_anomalias",
        "gravidade": gravidade_final,
        "timestamp": datetime.now().isoformat(),
        "sinais_analisados": sinais,
        "alertas": alertas
    }


if __name__ == "__main__":
    exemplo = {
        "frequencia_cardiaca": 132,
        "pressao_sistolica": 165,
        "pressao_diastolica": 105,
        "saturacao_oxigenio": 88,
        "temperatura": 38.2
    }

    resultado = detectar_anomalias_sinais_vitais(exemplo)
    print(resultado)
