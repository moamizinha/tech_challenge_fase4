"""
Demonstração do módulo de áudio do Tech Challenge Fase 4.

Este script executa a análise das transcrições simuladas de consultas médicas,
identifica termos críticos e gera uma saída em JSON.
"""

import json
import sys
from pathlib import Path


sys.path.append("src")

from audio_analysis import analisar_base_transcricoes


def salvar_resultado_audio(resultados: list, caminho_saida: str) -> None:
    """
    Salva os resultados da análise de áudio em arquivo JSON.
    """

    caminho = Path(caminho_saida)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=4)


def exibir_resumo(resultados: list) -> None:
    """
    Exibe um resumo simples da análise de áudio.
    """

    print("\n====================================")
    print("DEMONSTRAÇÃO DO MÓDULO DE ÁUDIO")
    print("====================================")

    for resultado in resultados:
        print("\n------------------------------------")
        print(f"Áudio ID: {resultado.get('audio_id')}")
        print(f"Paciente: {resultado.get('paciente_id')}")
        print(f"Arquivo simulado: {resultado.get('arquivo_audio_simulado')}")
        print(f"Gravidade detectada: {resultado.get('gravidade')}")
        print(f"Gravidade esperada: {resultado.get('gravidade_esperada')}")
        print(f"Transcrição: {resultado.get('descricao')}")

        termos = resultado.get("termos_detectados", [])

        if termos:
            print("Termos detectados:")
            for termo in termos:
                print(
                    f"- {termo['termo']} | "
                    f"{termo['categoria']} | "
                    f"{termo['gravidade']}"
                )
        else:
            print("Termos detectados: nenhum")


def main() -> None:
    """
    Executa a demonstração do módulo de áudio.
    """

    resultados = analisar_base_transcricoes()

    salvar_resultado_audio(
        resultados,
        "outputs/resultado_audio.json"
    )

    exibir_resumo(resultados)

    print("\nArquivo gerado com sucesso:")
    print("outputs/resultado_audio.json")


if __name__ == "__main__":
    main()