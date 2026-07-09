"""
Módulo de análise de vídeo.

Este arquivo será responsável por:
- simular a análise de vídeos clínicos;
- identificar movimentos ou eventos fora do padrão esperado;
- classificar a gravidade do evento;
- gerar uma saída padronizada para o pipeline multimodal.
"""

from datetime import datetime


def analisar_video_clinico(evento_observado: str, intensidade_movimento: float) -> dict:
    """
    Analisa um evento observado em vídeo clínico simulado.

    Parâmetros:
    - evento_observado: descrição do evento identificado no vídeo.
    - intensidade_movimento: valor numérico simulando intensidade do movimento.
      Exemplo:
      0.0 a 0.3 = movimento baixo/normal
      0.4 a 0.7 = atenção
      acima de 0.7 = possível evento anômalo
    """

    evento_lower = evento_observado.lower()

    termos_criticos_video = [
        "queda",
        "perda de equilibrio",
        "movimento brusco",
        "imobilidade",
        "tremor intenso"
    ]

    evento_critico_detectado = any(
        termo in evento_lower for termo in termos_criticos_video
    )

    if evento_critico_detectado or intensidade_movimento > 0.7:
        gravidade = "alto"
        descricao = "Movimento ou evento fora do padrão esperado detectado no vídeo."
    elif intensidade_movimento > 0.4:
        gravidade = "atenção"
        descricao = "Movimento com variação moderada identificado no vídeo."
    else:
        gravidade = "normal"
        descricao = "Nenhum evento anômalo relevante foi identificado no vídeo."

    return {
        "tipo_dado": "video",
        "evento": "analise_de_video_clinico",
        "gravidade": gravidade,
        "timestamp": datetime.now().isoformat(),
        "evento_observado": evento_observado,
        "intensidade_movimento": intensidade_movimento,
        "descricao": descricao
    }


if __name__ == "__main__":
    resultado = analisar_video_clinico(
        evento_observado="Paciente apresentou movimento brusco durante exercício de fisioterapia.",
        intensidade_movimento=0.82
    )

    print(resultado)
