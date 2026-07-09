"""
Demonstração do módulo de análise de prescrições médicas.

Este script:
1. Lê a base de prescrições simuladas;
2. Detecta anomalias em prescrições;
3. Classifica a gravidade;
4. Salva os resultados em JSON e TXT.
"""

import json
import sys
from pathlib import Path


sys.path.append("src")

from prescription_analysis import analisar_base_prescricoes


CAMINHO_JSON = Path("outputs/resultado_prescricoes.json")


def salvar_json(resultados: list, caminho_saida: Path) -> None:
    """
    Salva os resultados da análise de prescrições em JSON.
    """

    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=4)


def exibir_resumo(resultados: list) -> None:
    """
    Exibe resumo da análise de prescrições no terminal.
    """

    print("\n==========================================")
    print("DEMONSTRAÇÃO DO MÓDULO DE PRESCRIÇÕES")
    print("==========================================")

    for resultado in resultados:
        print("\n------------------------------------------")
        print(f"Prescrição ID: {resultado['prescricao_id']}")
        print(f"Paciente: {resultado['paciente_id']}")
        print(f"Medicamento: {resultado['medicamento']}")
        print(f"Dose anterior: {resultado['dose_anterior']} {resultado['unidade']}")
        print(f"Dose atual: {resultado['dose_atual']} {resultado['unidade']}")
        print(f"Tipo de alteração: {resultado['tipo_alteracao']}")
        print(f"Gravidade detectada: {resultado['gravidade']}")
        print(f"Gravidade esperada: {resultado['gravidade_esperada']}")

        alertas = resultado.get("alertas", [])

        if alertas:
            print("Alertas detectados:")
            for alerta in alertas:
                print(
                    f"- {alerta['evento']} | "
                    f"{alerta['gravidade']} | "
                    f"{alerta['descricao']}"
                )
        else:
            print("Alertas detectados: nenhum")


def main() -> None:
    """
    Executa a demonstração do módulo de prescrições.
    """

    resultados = analisar_base_prescricoes()

    salvar_json(resultados, CAMINHO_JSON)

    exibir_resumo(resultados)

    print("\nArquivo gerado com sucesso:")
    print(CAMINHO_JSON)


if __name__ == "__main__":
    main()