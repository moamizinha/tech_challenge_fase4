# Relatório Técnico - Tech Challenge Fase 4

## 1. Introdução

Este projeto tem como objetivo desenvolver uma solução multimodal aplicada ao contexto médico, integrando dados de áudio, vídeo, texto, sinais vitais e prescrições médicas para apoiar a identificação precoce de riscos clínicos.

A proposta simula um sistema de monitoramento preventivo capaz de analisar diferentes fontes de dados e gerar alertas automáticos para a equipe médica. A solução foi construída com finalidade acadêmica, utilizando dados simulados, arquivos estruturados e exemplos controlados para demonstrar o fluxo completo de análise e fusão multimodal.

## 2. Objetivo do Projeto

O objetivo principal é realizar a análise e fusão de dados médicos multimodais para detectar possíveis anomalias em pacientes.

A solução considera:

- análise de vídeos clínicos simulados;
- processamento de áudios de consultas médicas;
- identificação de termos críticos em transcrições;
- análise de sinais vitais;
- análise de imagem de monitor multiparamétrico;
- análise de prescrições médicas simuladas;
- geração de alertas automáticos;
- integração dos resultados em um pipeline multimodal.

## 3. Fluxo Multimodal da Solução

O fluxo da solução foi organizado em etapas:

1. Entrada dos dados simulados;
2. Análise de áudio e texto;
3. Análise de vídeo clínico;
4. Detecção de anomalias em sinais vitais;
5. Análise estruturada de imagem de monitor multiparamétrico;
6. Análise de prescrições médicas;
7. Integração dos resultados;
8. Classificação da gravidade final;
9. Geração do alerta para a equipe médica.

O fluxo geral pode ser representado da seguinte forma:

```text
Áudio / Texto
+ Vídeo Clínico
+ Sinais Vitais
+ Imagem de Monitor
+ Prescrições Médicas
        ↓
Pipeline Multimodal
        ↓
Classificação de Gravidade
        ↓
Alerta para Equipe Médica
```

## 4. Módulo de Áudio e Texto

O módulo de áudio e texto tem como objetivo analisar transcrições de consultas médicas.

A análise considera a identificação de termos críticos, como:

- falta de ar;
- dor no peito;
- desmaio;
- tontura;
- cansaço extremo;
- fadiga;
- fraqueza;
- dificuldade para falar;
- respiração ofegante;
- confusão mental.

Cada termo identificado é associado a uma categoria clínica e a um nível de gravidade, permitindo classificar o risco do paciente.

A base de termos críticos está armazenada em:

```text
data/termos_criticos.csv
```

O módulo principal está implementado em:

```text
src/audio_analysis.py
```

## 5. Módulo de Vídeo

O módulo de vídeo tem como objetivo simular a análise de vídeos clínicos, como sessões de fisioterapia ou movimentação de pacientes.

A análise considera eventos como:

- queda;
- perda de equilíbrio;
- movimento brusco;
- imobilidade;
- tremor intenso.

O sistema classifica o evento observado e gera uma saída estruturada com o tipo de dado, evento, gravidade, timestamp e descrição.

O módulo principal está implementado em:

```text
src/video_analysis.py
```

Nesta versão, a análise de vídeo é simulada por meio de descrição do evento observado e intensidade de movimento. Como evolução futura, o módulo pode ser expandido com OpenCV, YOLOv8, OpenPose ou MediaPipe para análise automática de frames, postura e movimentos.

## 6. Detecção de Anomalias em Sinais Vitais

O módulo de detecção de anomalias analisa sinais vitais simulados, como:

- frequência cardíaca;
- pressão arterial;
- saturação de oxigênio;
- temperatura corporal.

Foram criadas regras iniciais para identificar situações como:

- taquicardia;
- bradicardia;
- pressão arterial elevada;
- pressão arterial baixa;
- hipoxemia;
- febre;
- hipotermia.

A base simulada está armazenada em:

```text
data/sinais_vitais_simulados.csv
```

O módulo principal está implementado em:

```text
src/anomaly_detection.py
```

## 7. Pipeline Multimodal

O pipeline multimodal integra os resultados dos módulos de áudio, vídeo, sinais vitais, imagem de monitor e prescrições médicas.

A gravidade final é definida com base na maior severidade identificada entre os módulos analisados.

Os níveis considerados são:

- normal;
- atenção;
- alto;
- crítico.

A prioridade utilizada é:

```text
crítico > alto > atenção > normal
```

O pipeline principal está implementado em:

```text
src/multimodal_pipeline.py
```

A execução geral do projeto é feita pelo arquivo:

```text
run_demo.py
```

## 8. Exemplo de Alerta Gerado

Um exemplo de alerta crítico pode ocorrer quando o paciente apresenta:

- relato de falta de ar;
- tontura;
- cansaço extremo;
- alteração detectada em sinais vitais;
- movimento brusco durante fisioterapia;
- alteração crítica em prescrição médica.

Nesse caso, o sistema gera uma recomendação para acionar a equipe médica imediatamente.

A saída final é salva em:

```text
outputs/exemplos_alertas.json
```

## 9. Tecnologias Utilizadas

As tecnologias utilizadas e previstas para o desenvolvimento da solução são:

- Python;
- CSV e JSON para organização dos dados;
- SpeechRecognition para transcrição automática de áudio;
- Google Web Speech API como alternativa viável para reconhecimento de fala;
- OpenCV como tecnologia prevista para evolução da análise de vídeo;
- Azure Speech to Text como serviço previsto para integração em nuvem;
- Azure Text Analytics como serviço previsto para análise textual;
- Azure Computer Vision como possibilidade futura para extração automática de sinais vitais em imagens;
- GitHub para versionamento;
- VS Code para desenvolvimento;
- Jupyter Notebook como alternativa para demonstração.

## 10. Implementação do Módulo de Áudio

O módulo de áudio foi implementado com duas abordagens:

1. Análise de transcrições simuladas;
2. Análise de um arquivo de áudio real em formato WAV.

Na primeira abordagem, o sistema lê o arquivo:

```text
data/transcricoes_audio_simuladas.csv
```

Esse arquivo contém falas simuladas de pacientes, termos esperados e gravidade esperada.

Na segunda abordagem, foi utilizado o script:

```text
run_real_audio_demo.py
```

Esse script realiza o seguinte fluxo:

```text
arquivo de áudio → transcrição automática → análise de termos críticos → classificação de risco
```

A transcrição obtida no teste com áudio real foi:

```text
paciente relata falta de ar tontura e cansaço extremo durante a consulta
```

O sistema identificou os seguintes termos críticos:

| Termo | Categoria | Gravidade |
|---|---|---|
| falta de ar | respiratório | crítico |
| tontura | neurológico | alto |
| cansaço extremo | geral | alto |

A gravidade final do módulo de áudio foi classificada como:

```text
crítico
```

O resultado estruturado foi salvo em:

```text
outputs/resultado_audio_real.json
```

A evidência da execução foi registrada em:

```text
outputs/resultado_audio_real.txt
```

## 11. Implementação do Módulo de Sinais Vitais

O módulo de sinais vitais foi implementado a partir de duas fontes:

1. Base simulada em CSV;
2. Imagem de monitor multiparamétrico.

A base simulada está armazenada em:

```text
data/sinais_vitais_simulados.csv
```

A imagem do monitor está armazenada em:

```text
data/images/monitor_sinais_vitais.png
```

A análise por imagem foi implementada no arquivo:

```text
src/vital_signs_image_analysis.py
```

Nesta versão acadêmica, os valores exibidos na imagem do monitor foram extraídos de forma estruturada assistida. Em uma evolução futura, essa etapa pode ser automatizada com OCR ou serviços de visão computacional, como Azure Computer Vision.

Os sinais vitais considerados na imagem foram:

| Parâmetro | Valor |
|---|---|
| Frequência cardíaca | 120 bpm |
| Saturação de oxigênio | 98% |
| Frequência respiratória | 24 rpm |
| ETCO2 | 35 mmHg |
| Temperatura | 36.7 °C |
| Pressão arterial | 119/79 mmHg |
| PVC média | 14 mmHg |

O monitor também apresentou alertas visuais, como:

```text
FC ALTA
PVC ALTA
```

Com base nesses valores, o módulo identificou alterações relacionadas à frequência cardíaca, frequência respiratória e PVC elevada.

A execução da análise da imagem pode ser feita pelo script:

```text
run_vital_image_demo.py
```

O resultado estruturado é salvo em:

```text
outputs/resultado_imagem_sinais_vitais.json
```

## 12. Implementação do Módulo de Prescrições

Além dos sinais vitais, foi implementado um módulo de análise de prescrições médicas simuladas.

A base utilizada está em:

```text
data/prescricoes_simuladas.csv
```

O código principal está em:

```text
src/prescription_analysis.py
```

O objetivo desse módulo é detectar anomalias em prescrições, como:

- aumento inesperado de dose;
- duplicidade de medicamento;
- suspensão inesperada;
- uso de medicamento de maior atenção.

Foram considerados medicamentos de maior atenção, como:

| Medicamento | Motivo de Atenção |
|---|---|
| Insulina | Alterações de dose podem causar risco metabólico |
| Heparina | Anticoagulante com risco em caso de duplicidade |
| Morfina | Opioide com risco associado ao aumento de dose |
| Midazolam | Sedativo com potencial risco respiratório |

A execução do módulo validou os seguintes cenários:

| Prescrição | Gravidade Detectada | Gravidade Esperada |
|---|---|---|
| PRESC_001 | normal | normal |
| PRESC_002 | alto | alto |
| PRESC_003 | crítico | crítico |
| PRESC_004 | crítico | crítico |
| PRESC_005 | normal | normal |
| PRESC_006 | alto | alto |
| PRESC_007 | crítico | crítico |
| PRESC_008 | atenção | atenção |

O resultado estruturado foi salvo em:

```text
outputs/resultado_prescricoes.json
```

A evidência da execução foi registrada em:

```text
outputs/resultado_prescricoes.txt
```

## 13. Pipeline Multimodal Integrado

O pipeline multimodal foi atualizado para integrar os seguintes módulos:

- áudio e texto;
- vídeo clínico simulado;
- imagem de monitor de sinais vitais;
- prescrições médicas simuladas.

O arquivo principal do pipeline é:

```text
src/multimodal_pipeline.py
```

A execução geral é realizada por meio do script:

```text
run_demo.py
```

O pipeline completo realiza o seguinte fluxo:

```text
áudio/texto
+ vídeo clínico
+ imagem de sinais vitais
+ prescrições médicas
→ fusão multimodal
→ classificação de gravidade
→ alerta final para equipe médica
```

A gravidade final é definida pela maior severidade identificada entre os módulos.

A ordem de prioridade utilizada é:

```text
crítico > alto > atenção > normal
```

Na demonstração completa, o sistema classificou o caso como crítico, pois foram identificados eventos críticos no áudio e nas prescrições, além de eventos de alto risco em sinais vitais e vídeo.

A saída final é salva em:

```text
outputs/exemplos_alertas.json
```

A evidência da execução completa é registrada em:

```text
outputs/resultado_pipeline_completo.txt
```

## 14. Resultados Obtidos

Os principais resultados obtidos foram:

- criação da estrutura completa do repositório GitHub;
- implementação do módulo de áudio com transcrição automática;
- validação do áudio com transcrições simuladas e arquivo real em WAV;
- identificação de termos críticos e classificação de risco;
- tratamento de negação em frases como “sem falta de ar”;
- remoção de duplicidade em termos, como “cansaço” e “cansaço extremo”;
- análise de sinais vitais simulados;
- análise estruturada de imagem de monitor multiparamétrico;
- análise de prescrições médicas simuladas;
- integração dos módulos em um pipeline multimodal;
- geração de alertas estruturados em JSON;
- registro de evidências de execução em arquivos TXT.

## 15. Exemplos de Anomalias Detectadas

Durante os testes, foram detectadas anomalias como:

| Tipo de dado | Evento | Gravidade |
|---|---|---|
| Áudio/texto | Falta de ar | crítico |
| Áudio/texto | Tontura | alto |
| Áudio/texto | Cansaço extremo | alto |
| Sinais vitais | Frequência respiratória elevada | atenção |
| Sinais vitais | PVC elevada | alto |
| Vídeo | Movimento brusco durante fisioterapia | alto |
| Prescrição | Duplicidade de Heparina | crítico |
| Prescrição | Aumento relevante de Morfina | crítico |
| Prescrição | Suspensão inesperada de antibiótico | alto |

## 16. Limitações

A solução apresentada possui finalidade acadêmica.

Os dados utilizados são simulados ou gerados para demonstração. O sistema não deve ser utilizado para diagnóstico médico real.

A análise da imagem do monitor ainda não utiliza OCR automático. Os valores foram extraídos de forma estruturada assistida a partir da imagem.

As regras de classificação foram simplificadas para demonstrar o conceito da solução.

Em uma aplicação real, seria necessário validar os critérios com profissionais da saúde, protocolos hospitalares, bases clínicas reais e requisitos de segurança e privacidade de dados.

## 17. Conclusão

O projeto demonstra a viabilidade de uma solução multimodal para apoio ao monitoramento clínico preventivo.

A integração entre áudio, vídeo, sinais vitais, imagem de monitor e prescrições permite ampliar a capacidade de identificação de riscos e gerar alertas mais completos para a equipe médica.

A implementação mostrou que é possível processar um arquivo de áudio real, transcrever automaticamente o conteúdo, identificar termos críticos e combinar essa análise com outros módulos clínicos.

Como evolução futura, a solução pode ser aprimorada com integração direta aos serviços Azure, uso de OCR automático para leitura de monitores, modelos de machine learning para detecção de anomalias e validação com especialistas da área da saúde.
