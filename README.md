 # Tech Challenge Fase 4 - Monitoramento Multimodal em Contexto Médico

## 📌 Descrição do Projeto

Este projeto foi desenvolvido como parte do **Tech Challenge - Fase 4 da Pós Tech**.

O objetivo é construir uma solução multimodal aplicada ao contexto médico, integrando dados de **áudio, texto, vídeo, sinais vitais, imagem de monitor multiparamétrico e prescrições médicas** para identificar possíveis anomalias clínicas e gerar alertas estruturados para apoio à equipe médica.

A proposta simula um sistema de monitoramento preventivo capaz de analisar diferentes fontes de dados do paciente e consolidar os resultados em um pipeline único de classificação de risco.

> ⚠️ Este projeto possui finalidade exclusivamente acadêmica. Os dados utilizados são simulados ou gerados para demonstração e não representam diagnóstico médico real.

---

## 🎯 Objetivos

- Processar áudios simulados de consultas médicas.
- Transcrever áudio real com **Azure Speech to Text**.
- Analisar sentimento e frases-chave com **Azure Text Analytics**.
- Identificar termos críticos relacionados a sintomas clínicos.
- Detectar anomalias em sinais vitais.
- Analisar imagem de monitor multiparamétrico de sinais vitais.
- Simular análise de vídeo clínico.
- Detectar anomalias em prescrições médicas.
- Integrar os resultados em um pipeline multimodal.
- Gerar alertas automáticos com classificação de gravidade.
- Produzir saídas estruturadas em JSON e evidências em TXT.

---

## 🧠 Contexto do Desafio

O desafio propõe um cenário em que uma instituição hospitalar deseja monitorar continuamente pacientes utilizando inteligência artificial e dados multimodais.

A solução deve considerar diferentes tipos de dados médicos, como:

- áudio de consultas;
- transcrições textuais;
- vídeos clínicos;
- sinais vitais;
- imagem de monitor hospitalar;
- prescrições médicas;
- evolução clínica.

A partir dessas informações, o sistema deve detectar sinais precoces de risco e emitir alertas preventivos para a equipe médica.

---

## 🏗️ Arquitetura Geral da Solução

O fluxo multimodal desenvolvido segue a lógica:

```text
Áudio real ou simulado
        ↓
Azure Speech to Text / SpeechRecognition
        ↓
Transcrição textual
        ↓
Azure Text Analytics + Classificador local
        ↓
Termos críticos, sentimento e gravidade


Imagem de monitor de sinais vitais
        ↓
Extração estruturada assistida
        ↓
Detecção de anomalias fisiológicas


Prescrições simuladas
        ↓
Análise de alterações terapêuticas
        ↓
Detecção de aumento de dose, duplicidade e suspensão


Vídeo clínico simulado
        ↓
Análise de evento/movimento
        ↓
Classificação de risco


Todos os módulos
        ↓
Pipeline multimodal
        ↓
Gravidade final
        ↓
Alerta para equipe médica
```

A gravidade final é definida pela maior severidade detectada entre os módulos:

```text
crítico > alto > atenção > normal
```

---

## 📁 Estrutura do Repositório

```text
tech_challenge_fase4/
│
├── data/
│   ├── audios/
│   │   └── consulta_audio_real.wav
│   │
│   ├── images/
│   │   └── monitor_sinais_vitais.png
│   │
│   ├── cenarios_clinicos.csv
│   ├── prescricoes_simuladas.csv
│   ├── sinais_vitais_simulados.csv
│   ├── termos_criticos.csv
│   └── transcricoes_audio_simuladas.csv
│
├── docs/
│   ├── checklist_entrega.md
│   ├── fluxo_multimodal.png
│   ├── matriz_alertas.md
│   ├── modulo_audio.md
│   ├── modulo_prescricoes.md
│   ├── modulo_sinais_vitais.md
│   ├── relatorio_tecnico.md
│   └── roteiro_video.md
│
├── outputs/
│   ├── exemplos_alertas.json
│   ├── resultado_audio.json
│   ├── resultado_audio.txt
│   ├── resultado_audio_real.json
│   ├── resultado_audio_real.txt
│   ├── resultado_audio_azure.json
│   ├── resultado_audio_azure.txt
│   ├── resultado_imagem_sinais_vitais.json
│   ├── resultado_pipeline_completo.txt
│   ├── resultado_prescricoes.json
│   └── resultado_prescricoes.txt
│
├── src/
│   ├── __init__.py
│   ├── anomaly_detection.py
│   ├── audio_analysis.py
│   ├── multimodal_pipeline.py
│   ├── prescription_analysis.py
│   ├── video_analysis.py
│   └── vital_signs_image_analysis.py
│
├── .gitignore
├── README.md
├── requirements.txt
├── run_audio_demo.py
├── run_azure_audio_demo.py
├── run_demo.py
├── run_prescription_demo.py
├── run_real_audio_demo.py
└── run_vital_image_demo.py
```

---

## 👥 Integrantes e Responsabilidades

| Integrante | Responsabilidade Principal |
|---|---|
| Karim | Módulo de vídeo e apoio à detecção de anomalias |
| Michele | Módulo de áudio, integração técnica, organização do Git e vídeo final |
| Wellington | Curadoria dos dados, cenários clínicos e massa de testes |
| Rúben | Relatório técnico, fluxo multimodal, matriz de alertas e roteiro |

---

## 🔊 Módulo de Áudio e Texto

O módulo de áudio foi implementado com três abordagens:

1. **Transcrições simuladas**
2. **Áudio real com SpeechRecognition**
3. **Áudio real com Azure Speech to Text e Azure Text Analytics**

### Funcionalidades

- Transcrição automática de áudio.
- Identificação de termos críticos.
- Análise de sentimento com Azure.
- Extração de frases-chave com Azure.
- Classificação de gravidade.
- Tratamento de negação.
- Remoção de duplicidade entre termos semelhantes.
- Geração de saída JSON.

### Arquivos relacionados

```text
src/audio_analysis.py
run_audio_demo.py
run_real_audio_demo.py
run_azure_audio_demo.py
data/termos_criticos.csv
data/transcricoes_audio_simuladas.csv
outputs/resultado_audio_azure.json
```

### Exemplo de áudio analisado

```text
Paciente relata falta de ar, tontura e cansaço extremo durante a consulta.
```

### Resultado com Azure

A execução com Azure obteve:

```text
Transcrição:
Paciente relata falta de ar, tontura e cansaço extremo durante a consulta.

Sentimento Azure:
negative

Termos críticos detectados:
- cansaço extremo | alto
- falta de ar | crítico
- tontura | alto

Gravidade final:
crítico
```

---

## ☁️ Integração com Azure

O projeto utiliza serviços Azure na análise de áudio.

### Serviços utilizados

- **Azure Speech to Text**
  - Responsável pela transcrição do áudio real.

- **Azure Text Analytics**
  - Responsável pela análise de sentimento e extração de frases-chave.

### Variáveis de ambiente

As credenciais Azure devem ser armazenadas localmente no arquivo `.env`.

Crie um arquivo `.env` na raiz do projeto com o seguinte formato:

```env
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth

AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=https://seu-endpoint.cognitiveservices.azure.com/
```

> ⚠️ O arquivo `.env` não deve ser enviado ao GitHub.

---

## 🫀 Módulo de Sinais Vitais

O módulo de sinais vitais analisa dados fisiológicos a partir de duas fontes:

1. Base simulada em CSV;
2. Imagem de monitor multiparamétrico.

### Arquivos relacionados

```text
src/anomaly_detection.py
src/vital_signs_image_analysis.py
run_vital_image_demo.py
data/sinais_vitais_simulados.csv
data/images/monitor_sinais_vitais.png
outputs/resultado_imagem_sinais_vitais.json
```

### Sinais vitais considerados

- Frequência cardíaca;
- Pressão arterial;
- Saturação de oxigênio;
- Temperatura;
- Frequência respiratória;
- ETCO2;
- PVC.

### Valores utilizados na imagem do monitor

| Parâmetro | Valor |
|---|---|
| Frequência cardíaca | 120 bpm |
| SpO2 | 98% |
| Frequência respiratória | 24 rpm |
| ETCO2 | 35 mmHg |
| Temperatura | 36.7 °C |
| Pressão arterial | 119/79 mmHg |
| PVC média | 14 mmHg |

Alertas visuais considerados:

```text
FC ALTA
PVC ALTA
```

> Nesta versão, a imagem é usada como evidência visual e os valores são extraídos de forma estruturada assistida. Como evolução futura, a extração pode ser automatizada com OCR ou Azure Computer Vision.

---

## 💊 Módulo de Prescrições Médicas

O módulo de prescrições identifica possíveis anomalias em alterações terapêuticas.

### Arquivos relacionados

```text
src/prescription_analysis.py
run_prescription_demo.py
data/prescricoes_simuladas.csv
outputs/resultado_prescricoes.json
```

### Anomalias detectadas

- Aumento inesperado de dose;
- Duplicidade de medicamento;
- Suspensão inesperada;
- Medicamento de maior atenção.

### Medicamentos de maior atenção

| Medicamento | Motivo |
|---|---|
| Insulina | Alterações de dose podem causar risco metabólico |
| Heparina | Anticoagulante com risco em caso de duplicidade |
| Morfina | Opioide com risco associado ao aumento de dose |
| Midazolam | Sedativo com potencial risco respiratório |

### Validação

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

---

## 🎥 Módulo de Vídeo

O módulo de vídeo simula a análise de eventos clínicos relacionados à movimentação do paciente.

### Arquivos relacionados

```text
src/video_analysis.py
```

### Eventos considerados

- Queda;
- Perda de equilíbrio;
- Movimento brusco;
- Imobilidade;
- Tremor intenso.

Nesta versão, a análise de vídeo é simulada por meio de descrição do evento observado e intensidade de movimento. Como evolução futura, o módulo pode ser expandido com OpenCV, YOLOv8, OpenPose ou MediaPipe.

---

## 🔄 Pipeline Multimodal

O pipeline principal integra os módulos de:

- áudio e texto;
- vídeo clínico;
- sinais vitais por imagem;
- prescrições médicas.

### Arquivos relacionados

```text
src/multimodal_pipeline.py
run_demo.py
outputs/exemplos_alertas.json
outputs/resultado_pipeline_completo.txt
```

### Fluxo final

```text
Áudio/texto
+ Vídeo
+ Sinais vitais por imagem
+ Prescrições
        ↓
Pipeline multimodal
        ↓
Classificação de gravidade
        ↓
Recomendação para equipe médica
```

### Exemplo de recomendação

```text
Acionar equipe médica imediatamente e priorizar atendimento.
```

---

## ⚙️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/moamizinha/tech_challenge_fase4.git
cd tech_challenge_fase4
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```powershell
.venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Azure

Crie o arquivo `.env` na raiz do projeto com as credenciais Azure.

```env
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth

AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=https://seu-endpoint.cognitiveservices.azure.com/
```

---

## ▶️ Scripts de Demonstração

### Pipeline completo

```bash
python run_demo.py
```

### Módulo de áudio com transcrições simuladas

```bash
python run_audio_demo.py
```

### Módulo de áudio real com SpeechRecognition

```bash
python run_real_audio_demo.py
```

### Módulo de áudio com Azure

```bash
python run_azure_audio_demo.py
```

### Módulo de sinais vitais por imagem

```bash
python run_vital_image_demo.py
```

### Módulo de prescrições

```bash
python run_prescription_demo.py
```

---

## 📤 Saídas Geradas

As principais saídas são armazenadas na pasta `outputs/`.

| Arquivo | Descrição |
|---|---|
| `exemplos_alertas.json` | Alerta multimodal final |
| `resultado_audio.json` | Resultado da análise de transcrições simuladas |
| `resultado_audio_real.json` | Resultado da análise de áudio real local |
| `resultado_audio_azure.json` | Resultado da análise de áudio com Azure |
| `resultado_imagem_sinais_vitais.json` | Resultado da análise da imagem do monitor |
| `resultado_prescricoes.json` | Resultado da análise de prescrições |
| `resultado_pipeline_completo.txt` | Evidência da execução do pipeline completo |

---

## ✅ Status Atual

| Item | Status |
|---|---|
| Estrutura do GitHub | ✅ Concluído |
| README inicial | ✅ Concluído |
| Dados simulados | ✅ Concluído |
| Módulo de áudio | ✅ Concluído |
| Integração com Azure Speech to Text | ✅ Concluído |
| Integração com Azure Text Analytics | ✅ Concluído |
| Módulo de sinais vitais | ✅ Concluído |
| Imagem de monitor multiparamétrico | ✅ Concluído |
| Módulo de prescrições | ✅ Concluído |
| Pipeline multimodal | ✅ Concluído |
| Documentação técnica | ✅ Em desenvolvimento |
| Vídeo final | ⏳ Pendente |

---

## 📚 Documentação

A pasta `docs/` contém os principais documentos do projeto:

| Documento | Descrição |
|---|---|
| `relatorio_tecnico.md` | Relatório técnico principal |
| `modulo_audio.md` | Documentação detalhada do módulo de áudio |
| `modulo_sinais_vitais.md` | Documentação detalhada do módulo de sinais vitais |
| `modulo_prescricoes.md` | Documentação detalhada do módulo de prescrições |
| `matriz_alertas.md` | Matriz de severidade e regras de alerta |
| `roteiro_video.md` | Roteiro da apresentação final |
| `fluxo_multimodal.png` | Diagrama do fluxo da solução |

---

## 🔐 Segurança e Privacidade

- O arquivo `.env` contém credenciais Azure e não deve ser enviado ao GitHub.
- O projeto utiliza dados simulados ou gerados para demonstração.
- Não devem ser utilizados dados reais de pacientes.
- A solução não substitui avaliação médica real.

---

## ⚠️ Limitações

- As regras de classificação são simplificadas.
- A análise de vídeo ainda é simulada.
- A análise da imagem do monitor não utiliza OCR automático.
- Os dados são simulados ou gerados para demonstração.
- A análise de sentimento não deve ser interpretada como diagnóstico clínico.
- Em uma aplicação real, seria necessário validar regras, limites e fluxos com profissionais da saúde.

---


---

