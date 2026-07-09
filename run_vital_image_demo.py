"""
Demonstração da análise de imagem de monitor de sinais vitais.

Este script:
1. Lê uma imagem de monitor multiparamétrico;
2. Extrai sinais vitais estruturados;
3. Detecta anomalias;
4. Gera saída JSON em outputs/resultado_imagem_sinais_vitais.json.
"""

import json
import sys
from pathlib import Path


sys.path.append("src")

from vital_signs_image_analysis import analisar_imagem_monitor


CAMINHO_IMAGEM = Path("data/images/monitor_sinais_vitais.png")
CAMINHO_SAIDA = Path("outputs/resultado_imagem_sinais_vitais.json")


def salvar_json(resultado: dict, caminho_saida: Path) -> None:
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=4)


def main() -> None:
    if not CAMINHO_IMAGEM.exists():
        print("Imagem não encontrada.")
        print(f"Coloque a imagem neste caminho: {CAMINHO_IMAGEM}")
        return

    print("\n==========================================")
    print("DEMONSTRAÇÃO COM IMAGEM DE SINAIS VITAIS")
    print("==========================================")

    resultado = analisar_imagem_monitor(str(CAMINHO_IMAGEM))

    sinais = resultado["sinais_extraidos"]

    print("\nSinais vitais extraídos da imagem:")
    print(f"FC: {sinais['frequencia_cardiaca']} bpm")
    print(f"SpO2: {sinais['saturacao_oxigenio']}%")
    print(f"RESP: {sinais['frequencia_respiratoria']} rpm")
    print(f"ETCO2: {sinais['etco2']} mmHg")
    print(f"PVC média: {sinais['pvc_media']} mmHg")
    print(f"TEMP: {sinais['temperatura']} °C")
    print(f"PNI: {sinais['pressao_sistolica']}/{sinais['pressao_diastolica']} mmHg")

    print("\nGravidade final:")
    print(resultado["gravidade"])

    print("\nAlertas detectados:")
    for alerta in resultado["alertas"]:
        print(f"- {alerta['evento']} | {alerta['gravidade']} | {alerta['descricao']}")

    salvar_json(resultado, CAMINHO_SAIDA)

    print("\nArquivo gerado com sucesso:")
    print(CAMINHO_SAIDA)


if __name__ == "__main__":
    main()