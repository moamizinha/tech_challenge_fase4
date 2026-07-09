"""
Módulo de análise de áudio e texto.

Este arquivo é responsável por:
- receber uma transcrição de consulta médica;
- carregar termos críticos a partir de data/termos_criticos.csv;
- identificar termos de risco na fala do paciente;
- classificar a gravidade;
- gerar uma saída padronizada para o pipeline multimodal.
"""

import csv
import json
import unicodedata
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CAMINHO_TERMOS_CRITICOS = BASE_DIR / "data" / "termos_criticos.csv"
CAMINHO_TRANSCRICOES = BASE_DIR / "data" / "transcricoes_audio_simuladas.csv"


MAPA_GRAVIDADE = {
    "normal": "normal",
    "atencao": "atenção",
    "atenção": "atenção",
    "alto": "alto",
    "critico": "crítico",
    "crítico": "crítico",
}


ORDEM_GRAVIDADE = {
    "normal": 0,
    "atenção": 1,
    "alto": 2,
    "crítico": 3,
}


def normalizar_texto(texto: str) -> str:
    """
    Remove acentos e converte o texto para minúsculas.
    Isso ajuda a comparar termos como 'crítico' e 'critico'.
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
    Padroniza os nomes das gravidades utilizadas no projeto.
    """

    gravidade_normalizada = normalizar_texto(gravidade)
    return MAPA_GRAVIDADE.get(gravidade_normalizada, "normal")


def carregar_termos_criticos(caminho_csv: Path = CAMINHO_TERMOS_CRITICOS) -> list:
    """
    Carrega a lista de termos críticos a partir de um arquivo CSV.

    O arquivo esperado deve conter as colunas:
    - termo
    - categoria
    - gravidade
    - descricao
    """

    termos = []

    with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            termo = linha.get("termo", "").strip()

            if not termo:
                continue

            termos.append({
                "termo": termo,
                "termo_normalizado": normalizar_texto(termo),
                "categoria": linha.get("categoria", "").strip(),
                "gravidade": padronizar_gravidade(linha.get("gravidade", "normal")),
                "descricao": linha.get("descricao", "").strip()
            })

    return termos


def termo_esta_negado(transcricao_normalizada: str, termo_normalizado: str) -> bool:
    """
    Verifica se o termo aparece em contexto de negação.

    Exemplo:
    'sem falta de ar' não deve gerar alerta crítico.
    """

    padroes_negacao = [
        f"sem {termo_normalizado}",
        f"sem sinais de {termo_normalizado}",
        f"nega {termo_normalizado}",
        f"nao relata {termo_normalizado}",
        f"nao apresenta {termo_normalizado}",
        f"sem queixa de {termo_normalizado}",
    ]

    return any(padrao in transcricao_normalizada for padrao in padroes_negacao)


def definir_gravidade_final(termos_detectados: list) -> str:
    """
    Define a maior gravidade encontrada entre os termos detectados.
    """

    if not termos_detectados:
        return "normal"

    maior_gravidade = "normal"

    for termo in termos_detectados:
        gravidade = termo["gravidade"]

        if ORDEM_GRAVIDADE[gravidade] > ORDEM_GRAVIDADE[maior_gravidade]:
            maior_gravidade = gravidade

    return maior_gravidade

def analisar_transcricao(transcricao: str) -> dict:
    """
    Analisa uma transcrição de áudio e identifica termos críticos.

    A busca prioriza termos maiores primeiro para evitar duplicidade.
    Exemplo:
    Se "cansaço extremo" for detectado, o termo menor "cansaço"
    não será duplicado na mesma análise.
    """

    termos_criticos = carregar_termos_criticos()
    transcricao_normalizada = normalizar_texto(transcricao)

    termos_detectados_temp = []

    termos_ordenados = sorted(
        termos_criticos,
        key=lambda item: len(item["termo_normalizado"]),
        reverse=True
    )

    for item in termos_ordenados:
        termo_normalizado = item["termo_normalizado"]

        if termo_normalizado in transcricao_normalizada:
            if termo_esta_negado(transcricao_normalizada, termo_normalizado):
                continue

            termo_ja_contemplado = any(
                termo_normalizado in detectado["termo_normalizado"]
                for detectado in termos_detectados_temp
            )

            if termo_ja_contemplado:
                continue

            termos_detectados_temp.append({
                "termo": item["termo"],
                "termo_normalizado": termo_normalizado,
                "categoria": item["categoria"],
                "gravidade": item["gravidade"],
                "descricao": item["descricao"]
            })

    termos_detectados = []

    for item in termos_detectados_temp:
        termos_detectados.append({
            "termo": item["termo"],
            "categoria": item["categoria"],
            "gravidade": item["gravidade"],
            "descricao": item["descricao"]
        })

    gravidade_final = definir_gravidade_final(termos_detectados)

    return {
        "tipo_dado": "audio_texto",
        "evento": "analise_de_transcricao",
        "gravidade": gravidade_final,
        "timestamp": datetime.now().isoformat(),
        "descricao": transcricao,
        "termos_detectados": termos_detectados
    }

def analisar_base_transcricoes(caminho_csv: Path = CAMINHO_TRANSCRICOES) -> list:
    """
    Analisa todas as transcrições simuladas disponíveis na base CSV.
    """

    resultados = []

    with open(caminho_csv, mode="r", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            resultado = analisar_transcricao(linha["transcricao"])

            resultado["audio_id"] = linha.get("audio_id")
            resultado["paciente_id"] = linha.get("paciente_id")
            resultado["arquivo_audio_simulado"] = linha.get("arquivo_audio_simulado")
            resultado["gravidade_esperada"] = linha.get("gravidade_esperada")

            resultados.append(resultado)

    return resultados


if __name__ == "__main__":
    resultados_audio = analisar_base_transcricoes()

    print(json.dumps(
        resultados_audio,
        ensure_ascii=False,
        indent=4
    ))
