# Roteiro do Vídeo Final - Tech Challenge Fase 4

## Tempo máximo

Até 15 minutos.

## 1. Abertura

Olá, este vídeo apresenta a solução desenvolvida para o Tech Challenge Fase 4.

O projeto tem como objetivo criar um sistema de monitoramento multimodal em contexto médico, integrando dados de áudio, vídeo, texto e sinais vitais para identificar possíveis anomalias e gerar alertas para a equipe médica.

## 2. Contexto do Problema

O desafio propõe um cenário em que uma instituição hospitalar deseja utilizar inteligência artificial para monitorar continuamente pacientes.

A solução deve ser capaz de analisar diferentes tipos de dados, como:

- vídeos clínicos;
- áudios de consultas;
- textos e transcrições;
- sinais vitais;
- prescrições e evolução clínica.

A partir dessas informações, o sistema deve identificar sinais precoces de risco e emitir alertas preventivos.

## 3. Apresentação do Repositório

Nesta etapa, apresentar rapidamente a estrutura do GitHub.

Mostrar as principais pastas:

- `src`: contém os módulos Python da solução;
- `data`: contém os dados simulados;
- `outputs`: contém exemplos de alertas gerados;
- `docs`: contém relatório técnico, roteiro e documentação;
- `requirements.txt`: contém as bibliotecas utilizadas;
- `README.md`: apresenta a visão geral do projeto.

## 4. Explicação do Fluxo Multimodal

Explicar que a solução foi dividida em três módulos principais:

1. Análise de áudio e texto;
2. Análise de vídeo;
3. Detecção de anomalias em sinais vitais.

Depois, os resultados são integrados em um pipeline multimodal, que calcula a gravidade final e gera uma recomendação para a equipe médica.

## 5. Demonstração do Módulo de Áudio e Texto

Mostrar o arquivo:

`src/audio_analysis.py`

Explicar que o módulo recebe uma transcrição de consulta médica e busca termos críticos, como:

- falta de ar;
- dor no peito;
- desmaio;
- tontura;
- cansaço extremo;
- fadiga.

Exemplo de fala:

"O módulo de áudio e texto simula a análise de uma consulta médica. A partir da transcrição, o sistema identifica termos críticos e classifica o risco do paciente."

## 6. Demonstração do Módulo de Sinais Vitais

Mostrar o arquivo:

`src/anomaly_detection.py`

Explicar que o módulo analisa sinais vitais simulados, como:

- frequência cardíaca;
- pressão arterial;
- saturação de oxigênio;
- temperatura.

Exemplo de fala:

"Nesta etapa, o sistema avalia sinais vitais e identifica possíveis anomalias, como taquicardia, pressão elevada, hipoxemia ou febre."

## 7. Demonstração do Módulo de Vídeo

Mostrar o arquivo:

`src/video_analysis.py`

Explicar que o módulo simula a análise de vídeo clínico, como uma sessão de fisioterapia.

Eventos analisados:

- queda;
- perda de equilíbrio;
- movimento brusco;
- imobilidade;
- tremor intenso.

Exemplo de fala:

"O módulo de vídeo simula a identificação de movimentos fora do padrão esperado, permitindo detectar possíveis situações de risco durante a movimentação do paciente."

## 8. Demonstração do Pipeline Multimodal

Mostrar o arquivo:

`src/multimodal_pipeline.py`

Explicar que esse é o módulo principal, responsável por integrar os resultados dos três módulos.

Exemplo de fala:

"O pipeline multimodal consolida as informações de áudio, vídeo e sinais vitais. A partir da maior gravidade encontrada, o sistema define o alerta final e gera uma recomendação para a equipe médica."

## 9. Exemplo de Alerta Gerado

Mostrar o arquivo:

`outputs/exemplos_alertas.json`

Explicar que o alerta final contém:

- identificação do paciente;
- timestamp;
- gravidade final;
- recomendação;
- resultados individuais de cada módulo.

Exemplo de fala:

"Neste exemplo, o paciente apresentou falta de ar, tontura, queda de saturação, pressão elevada e movimento brusco. Por isso, o sistema classificou o caso como crítico e recomendou o acionamento imediato da equipe médica."

## 10. Integração com Azure

Explicar que a arquitetura prevê integração com serviços gerenciados em nuvem, como:

- Azure Speech to Text;
- Azure Text Analytics;
- serviços de armazenamento e processamento em nuvem.

Exemplo de fala:

"A solução foi estruturada para permitir integração com serviços Azure. O Azure Speech to Text pode ser utilizado para transcrever os áudios das consultas, enquanto o Azure Text Analytics pode apoiar a identificação de termos críticos e sentimentos."

## 11. Resultados Obtidos

Apresentar que a solução conseguiu:

- organizar os dados multimodais;
- simular a análise de áudio, vídeo e sinais vitais;
- identificar anomalias;
- gerar alertas estruturados;
- classificar a gravidade dos eventos.

## 12. Limitações

Explicar que o projeto possui finalidade acadêmica.

Os dados utilizados são simulados ou públicos, e o sistema não deve ser usado como diagnóstico médico real.

As regras de detecção são simplificadas para demonstrar o conceito da solução.

## 13. Conclusão

Finalizar dizendo:

"A solução desenvolvida demonstra como dados multimodais podem ser integrados em um fluxo único para apoiar o monitoramento preventivo de pacientes. A combinação de áudio, vídeo, texto e sinais vitais permite gerar alertas mais completos e apoiar a tomada de decisão da equipe médica."

## 14. Encerramento

Agradecer e finalizar a apresentação.
