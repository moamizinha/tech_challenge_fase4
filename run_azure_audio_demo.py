"""
Demonstração do módulo de áudio usando serviços Azure.

Este script:
1. Lê um arquivo de áudio WAV;
2. Transcreve o áudio com Azure Speech to Text;
3. Analisa sentimento e frases-chave com Azure Text Analytics;
4. Classifica termos críticos usando o módulo audio_analysis.py;
5. Gera uma saída JSON em outputs/resultado_audio_azure.json.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


sys.path.append("src")

from audio_analysis import analisar_transcricao


CAMINHO_AUDIO = Path("data/audios/consulta_audio_real.wav")
CAMINHO_SAIDA = Path("outputs/resultado_audio_azure.json")


def carregar_variaveis_ambiente() -> dict:
    """
    Carrega as credenciais do Azure a partir do arquivo .env.
    """

    load_dotenv()

    credenciais = {
        "speech_key": os.getenv("AZURE_SPEECH_KEY"),
        "speech_region": os.getenv("AZURE_SPEECH_REGION"),
        "language_key": os.getenv("AZURE_LANGUAGE_KEY"),
        "language_endpoint": os.getenv("AZURE_LANGUAGE_ENDPOINT"),
    }

    faltando = [
        nome for nome, valor in credenciais.items()
        if not valor
    ]

    if faltando:
        raise ValueError(
            "Variáveis ausentes no arquivo .env: "
            + ", ".join(faltando)
        )

    return credenciais


def transcrever_audio_azure(caminho_audio: Path, speech_key: str, speech_region: str) -> str:
    """
    Transcreve um arquivo WAV usando Azure Speech to Text.
    """

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )

    speech_config.speech_recognition_language = "pt-BR"

    audio_config = speechsdk.audio.AudioConfig(
        filename=str(caminho_audio)
    )

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    resultado = recognizer.recognize_once_async().get()

    if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
        return resultado.text

    if resultado.reason == speechsdk.ResultReason.NoMatch:
        raise RuntimeError("Azure Speech não conseguiu reconhecer fala no áudio.")

    if resultado.reason == speechsdk.ResultReason.Canceled:
        detalhes = resultado.cancellation_details
        raise RuntimeError(
            f"Transcrição cancelada pelo Azure Speech: {detalhes.reason}. "
            f"Detalhes: {detalhes.error_details}"
        )

    raise RuntimeError("Erro desconhecido na transcrição com Azure Speech.")


def analisar_texto_azure(transcricao: str, language_key: str, language_endpoint: str) -> dict:
    """
    Analisa sentimento e frases-chave usando Azure Text Analytics.
    """

    client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=AzureKeyCredential(language_key)
    )

    resultado_sentimento = client.analyze_sentiment(
        documents=[transcricao],
        language="pt"
    )[0]

    resultado_frases = client.extract_key_phrases(
        documents=[transcricao],
        language="pt"
    )[0]

    if resultado_sentimento.is_error:
        sentimento = "erro"
        confianca = {}
    else:
        sentimento = resultado_sentimento.sentiment
        confianca = {
            "positivo": resultado_sentimento.confidence_scores.positive,
            "neutro": resultado_sentimento.confidence_scores.neutral,
            "negativo": resultado_sentimento.confidence_scores.negative,
        }

    if resultado_frases.is_error:
        frases_chave = []
    else:
        frases_chave = list(resultado_frases.key_phrases)

    return {
        "sentimento": sentimento,
        "confianca_sentimento": confianca,
        "frases_chave": frases_chave
    }


def salvar_json(resultado: dict, caminho_saida: Path) -> None:
    """
    Salva o resultado final em JSON.
    """

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=4)


def main() -> None:
    """
    Executa a demonstração completa com Azure.
    """

    print("\n======================================")
    print("DEMONSTRAÇÃO DE ÁUDIO COM AZURE")
    print("======================================")

    if not CAMINHO_AUDIO.exists():
        print("Arquivo de áudio não encontrado.")
        print(f"Coloque o arquivo neste caminho: {CAMINHO_AUDIO}")
        return

    try:
        credenciais = carregar_variaveis_ambiente()

        print("\nTranscrevendo áudio com Azure Speech to Text...")

        transcricao = transcrever_audio_azure(
            CAMINHO_AUDIO,
            credenciais["speech_key"],
            credenciais["speech_region"]
        )

        print("\nTranscrição obtida:")
        print(transcricao)

        print("\nAnalisando texto com Azure Text Analytics...")

        analise_azure = analisar_texto_azure(
            transcricao,
            credenciais["language_key"],
            credenciais["language_endpoint"]
        )

        print("\nResultado do Azure Text Analytics:")
        print(f"Sentimento: {analise_azure['sentimento']}")
        print(f"Frases-chave: {analise_azure['frases_chave']}")

        print("\nClassificando termos críticos com o módulo local...")

        analise_termos = analisar_transcricao(transcricao)

        resultado_final = {
            "tipo_dado": "audio_azure",
            "evento": "analise_audio_com_azure",
            "arquivo_audio": str(CAMINHO_AUDIO),
            "metodo_transcricao": "Azure Speech to Text",
            "metodo_texto": "Azure Text Analytics",
            "transcricao": transcricao,
            "sentimento_azure": analise_azure["sentimento"],
            "confianca_sentimento": analise_azure["confianca_sentimento"],
            "frases_chave_azure": analise_azure["frases_chave"],
            "gravidade": analise_termos["gravidade"],
            "termos_detectados": analise_termos["termos_detectados"],
            "resultado_classificador_local": analise_termos
        }

        salvar_json(resultado_final, CAMINHO_SAIDA)

        print("\nResultado final:")
        print(f"Gravidade: {resultado_final['gravidade']}")
        print(f"Termos detectados: {resultado_final['termos_detectados']}")

        print("\nArquivo gerado com sucesso:")
        print(CAMINHO_SAIDA)

    except Exception as erro:
        print("\nErro durante a execução com Azure:")
        print(erro)


if __name__ == "__main__":
    main()