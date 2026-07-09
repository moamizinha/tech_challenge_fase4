"""
Módulo de análise de prescrições médicas simuladas.

Este arquivo é responsável por:
- ler prescrições simuladas;
- identificar alterações inesperadas de dose;
- detectar duplicidade de medicamento;
- detectar suspensão inesperada;
- classificar gravidade;
- gerar saída estruturada para integração multimodal.
"""

import csv
import json
import unicodedata
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CAMINHO_PRESCRICOES = BASE_DIR / "data" / "prescricoes_simuladas.csv"


ORDEM_GRAVIDADE = {
    "normal": 0,
    "atenção": 1,
    "alto": 2,
    "crítico": 3,
}


MEDICAMENTOS_ALTO_RISCO = [
    "insulina",
    "heparina",
    "morfina",
    "midazolam",
]


def normalizar_texto(texto: str) -> str:
    """
    Remove acentos, espaços extras e converte texto para minúsculas.
    """

    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )
    return texto


def padronizar_gravidade(gravidade: str) -> str:
    """
    Padroniza os níveis de gravidade.
    """

    gravidade_normalizada = normalizar_texto(gravidade)

    mapa = {
        "normal": "normal",
        "atencao": "atenção",
        "alto": "alto",
        "critico": "crítico",
    }

    return mapa.get(gravidade_normalizada, "normal")


def definir_gravidade_final(alertas: list) -> str:
    """
    Define a gravidade final considerando o alerta mais severo.
    """

    if not alertas:
        return "normal"

    maior = "normal"

    for alerta in alertas:
        gravidade = alerta["gravidade"]

        if ORDEM_GRAVIDADE[gravidade] > ORDEM_GRAVIDADE[maior]:
            maior = gravidade

    return maior


def converter_float(valor: str) -> float:
    """
    Converte valores numéricos em float com segurança.
    """

    try:
        return float(str(valor).replace(",", "."))
    except ValueError:
        return 0.0


def analisar_prescricao(prescricao: dict) -> dict:
    """
    Analisa uma prescrição individual e identifica possíveis anomalias.
    """

    medicamento = prescricao.get("medicamento", "")
    medicamento_normalizado = normalizar_texto(medicamento)

    dose_atual = converter_float(prescricao.get("dose_atual", 0))
    dose_anterior = converter_float(prescricao.get("dose_anterior", 0))

    tipo_alteracao = normalizar_texto(prescricao.get("tipo_alteracao", ""))

    medicamento_alto_risco = medicamento_normalizado in MEDICAMENTOS_ALTO_RISCO

    alertas = []

    if tipo_alteracao == "duplicidade":
        gravidade = "crítico" if medicamento_alto_risco else "alto"

        alertas.append({
            "evento": "duplicidade_prescricao",
            "gravidade": gravidade,
            "descricao": f"Possível duplicidade identificada para {medicamento}."
        })

    if tipo_alteracao == "suspensao":
        alertas.append({
            "evento": "suspensao_inesperada",
            "gravidade": "alto",
            "descricao": f"Suspensão inesperada de {medicamento} em tratamento ativo."
        })

    if tipo_alteracao == "aumento_dose":
        if dose_anterior > 0:
            fator_aumento = dose_atual / dose_anterior
        else:
            fator_aumento = 0

        aumento_percentual = (fator_aumento - 1) * 100 if fator_aumento > 0 else 0

        if medicamento_alto_risco and fator_aumento >= 3:
            gravidade = "crítico"
        elif medicamento_alto_risco and fator_aumento >= 2:
            gravidade = "alto"
        elif aumento_percentual >= 100:
            gravidade = "alto"
        elif aumento_percentual > 0:
            gravidade = "atenção"
        else:
            gravidade = "normal"

        if gravidade != "normal":
            alertas.append({
                "evento": "aumento_dose",
                "gravidade": gravidade,
                "descricao": (
                    f"Aumento de dose de {medicamento}: "
                    f"{dose_anterior:g} para {dose_atual:g} "
                    f"{prescricao.get('unidade', '')}."
                )
            })

    if medicamento_alto_risco:
        alertas.append({
            "evento": "medicamento_alto_risco",
            "gravidade": "atenção",
            "descricao": f"{medicamento} é classificado como medicamento de maior atenção."
        })

    gravidade_final = definir_gravidade_final(alertas)

    return {
        "tipo_dado": "prescricao",
        "evento": "analise_de_prescricao",
        "prescricao_id": prescricao.get("prescricao_id"),
        "paciente_id": prescricao.get("paciente_id"),
        "timestamp": datetime.now().isoformat(),
        "medicamento": medicamento,
        "dose_atual": dose_atual,
        "dose_anterior": dose_anterior,
        "unidade": prescricao.get("unidade"),
        "frequencia": prescricao.get("frequencia"),
        "tipo_alteracao": prescricao.get("tipo_alteracao"),
        "gravidade": gravidade_final,
        "gravidade_esperada": padronizar_gravidade(
            prescricao.get("gravidade_esperada", "normal")
        ),
        "alertas": alertas,
        "descricao": prescricao.get("observacao", "")
    }


def analisar_base_prescricoes(caminho_csv: Path = CAMINHO_PRESCRICOES) -> list:
    """
    Analisa todas as prescrições simuladas disponíveis no CSV.
    """

    resultados = []

    with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            resultado = analisar_prescricao(linha)
            resultados.append(resultado)

    return resultados


if __name__ == "__main__":
    resultados = analisar_base_prescricoes()

    print(json.dumps(
        resultados,
        ensure_ascii=False,
        indent=4
    ))