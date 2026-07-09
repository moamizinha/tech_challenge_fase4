"""
Arquivo principal de demonstração do Tech Challenge Fase 4.

Este script executa o pipeline multimodal integrando:
- análise de áudio/texto;
- análise de vídeo;
- detecção de anomalias em sinais vitais;
- geração de alerta final para a equipe médica.

A saída é salva em outputs/exemplos_alertas.json.
"""

import json
import os
import sys
from pathlib import Path


# Permite importar os arquivos da pasta src
sys.path.append("src")

from multimodal_pipeline import executar_pipeline_multimodal


def salvar_alerta_json(alerta: dict, caminho_saida: str) -> None:
    """
    Salva o alerta final em um arquivo JSON.
    """

    pasta_saida = Path(caminho_saida).parent
    pasta_saida.mkdir(parents=True, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(alerta, arquivo, ensure_ascii=False, indent=4)


def exibir_resumo_alerta(alerta: dict) -> None:
    """
    Exibe um resumo do alerta no terminal.
    """

    print("\n==============================")
    print("DEMONSTRAÇÃO DO PIPELINE")
    print("==============================")

    print(f"Paciente: {alerta['paciente_id']}")
    print(f"Timestamp: {alerta['timestamp']}")
    print(f"Gravidade final: {alerta['gravidade_final']}")
    print(f"Recomendação: {alerta['recomendacao']}")

    print("\nResultados por módulo:")

    for resultado in alerta["resultados_modulos"]:
        print("------------------------------")
        print(f"Tipo de dado: {resultado['tipo_dado']}")
        print(f"Evento: {resultado['evento']}")
        print(f"Gravidade: {resultado['gravidade']}")
        print(f"Descrição: {resultado.get('descricao', 'Sem descrição')}")


def main() -> None:
    """
    Executa a demonstração completa.
    """

    alerta_final = executar_pipeline_multimodal()

    caminho_saida = os.path.join("outputs", "exemplos_alertas.json")

    salvar_alerta_json(alerta_final, caminho_saida)

    exibir_resumo_alerta(alerta_final)

    print("\nArquivo gerado com sucesso:")
    print(caminho_saida)


if __name__ == "__main__":
    main()
