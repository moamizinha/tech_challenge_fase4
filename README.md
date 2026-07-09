# Tech Challenge Fase 4 - Monitoramento Multimodal em Contexto Médico

## Descrição do Projeto

Este projeto foi desenvolvido como parte do Tech Challenge - Fase 4 da Pós Tech.

O objetivo é criar uma solução multimodal aplicada ao contexto médico, integrando dados de vídeo, áudio, texto e sinais vitais para identificar possíveis anomalias e gerar alertas para a equipe médica.

A solução busca simular um sistema de monitoramento preventivo capaz de apoiar a tomada de decisão clínica por meio da análise integrada de diferentes fontes de dados.

## Objetivos

- Processar vídeos clínicos, como sessões de fisioterapia ou procedimentos simulados.
- Analisar áudios de consultas médicas.
- Identificar termos críticos em transcrições de áudio e texto.
- Detectar anomalias em sinais vitais.
- Integrar os resultados em um fluxo multimodal.
- Gerar alertas automáticos com nível de severidade.
- Demonstrar a integração com serviços em nuvem, como Azure Cognitive Services.

## Contexto do Desafio

O desafio propõe que uma instituição hospitalar utilize inteligência artificial para monitorar continuamente pacientes por meio de dados multimodais.

O sistema deve ser capaz de analisar:

- Vídeo;
- Áudio;
- Texto;
- Sinais vitais;
- Prescrições;
- Evolução clínica.

A partir dessas informações, o sistema deve detectar padrões fora do esperado e emitir alertas preventivos.

## Estrutura Inicial do Projeto

```text
tech_challenge_fase4/
│
├── data/
│   ├── sinais_vitais_simulados.csv
│   ├── termos_criticos.csv
│   └── cenarios_clinicos.csv
│
├── src/
│   ├── video_analysis.py
│   ├── audio_analysis.py
│   ├── anomaly_detection.py
│   └── multimodal_pipeline.py
│
├── notebooks/
│   ├── demo_video.ipynb
│   ├── demo_audio.ipynb
│   └── demo_multimodal.ipynb
│
├── outputs/
│   └── exemplos_alertas.json
│
├── docs/
│   ├── relatorio_tecnico.md
│   ├── fluxo_multimodal.png
│   └── roteiro_video.md
│
├── requirements.txt
└── README.md
