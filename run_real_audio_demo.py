"""
Demonstração com arquivo de áudio real.

Este script:
1. Lê um arquivo de áudio em WAV;
2. Transcreve o áudio usando SpeechRecognition;
3. Analisa a transcrição com o módulo audio_analysis.py;
4. Gera uma saída JSON em outputs/resultado_audio_real.json.
"""

import json
import sys
from pathlib import Path

import speech_recognition as sr


sys.path.append("src")

from audio_analysis import analisar_transcricao


CAMINHO_AUDIO = Path("data/audios/consulta_audio_real.wav")
CAMINHO_SAIDA = Path("outputs/resultado_audio_real.json")


def transcrever_audio(caminho_audio: Path) -> str:
    """
    Transcreve um arquivo de áudio WAV para texto.
    """

    reconhecedor = sr.Recognizer()

    with sr.AudioFile(str(caminho_audio)) as fonte_audio:
        audio = reconhecedor.record(fonte_audio)

    transcricao = reconhecedor.recognize_google(
        audio,
        language="pt-BR"
    )

    return transcricao


def salvar_resultado(resultado: dict, caminho_saida: Path) -> None:
    """
    Salva o resultado da análise em JSON.
    """

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=4)


def main() -> None:
    """
    Executa a demonstração com áudio real.
    """

    if not CAMINHO_AUDIO.exists():
        print("Arquivo de áudio não encontrado.")
        print(f"Coloque o áudio neste caminho: {CAMINHO_AUDIO}")
        return

    print("\n====================================")
    print("DEMONSTRAÇÃO COM ÁUDIO REAL")
    print("====================================")

    try:
        transcricao = transcrever_audio(CAMINHO_AUDIO)

        print("\nTranscrição obtida:")
        print(transcricao)

        resultado = analisar_transcricao(transcricao)

        resultado["arquivo_audio"] = str(CAMINHO_AUDIO)
        resultado["metodo_transcricao"] = "SpeechRecognition - Google Web Speech API"

        salvar_resultado(resultado, CAMINHO_SAIDA)

        print("\nResultado da análise:")
        print(f"Gravidade: {resultado['gravidade']}")
        print(f"Termos detectados: {resultado['termos_detectados']}")

        print("\nArquivo gerado com sucesso:")
        print(CAMINHO_SAIDA)

    except sr.UnknownValueError:
        print("Não foi possível entender o áudio. Tente gravar mais claro e sem ruído.")
    except sr.RequestError as erro:
        print("Erro ao acessar o serviço de reconhecimento de fala.")
        print(erro)
    except Exception as erro:
        print("Erro inesperado:")
        print(erro)


if __name__ == "__main__":
    main()