# Módulo de Sinais Vitais

## 1. Objetivo

O módulo de sinais vitais tem como objetivo identificar possíveis anomalias clínicas a partir de dados fisiológicos do paciente.

Nesta versão do projeto, a análise considera duas fontes principais:

- dados simulados em CSV;
- imagem de monitor multiparamétrico.

O módulo contribui para a solução multimodal do Tech Challenge Fase 4 ao gerar alertas estruturados que podem ser integrados com áudio, vídeo, texto e prescrições médicas.

## 2. Entrada de Dados

A análise de sinais vitais utiliza os seguintes arquivos:

```text
data/sinais_vitais_simulados.csv
data/images/monitor_sinais_vitais.png
```

O arquivo CSV contém dados simulados de pacientes em diferentes condições clínicas.

A imagem representa um monitor hospitalar multiparamétrico com sinais vitais exibidos visualmente.

## 3. Arquivos Principais

A análise de sinais vitais por dados estruturados é realizada pelo arquivo:

```text
src/anomaly_detection.py
```

A análise baseada na imagem do monitor é realizada pelo arquivo:

```text
src/vital_signs_image_analysis.py
```

A execução demonstrável da análise da imagem é feita pelo script:

```text
run_vital_image_demo.py
```

## 4. Sinais Vitais Considerados

Os principais sinais vitais analisados são:

| Sinal Vital | Descrição |
|---|---|
| Frequência cardíaca | Batimentos cardíacos por minuto |
| Pressão arterial | Pressão sistólica e diastólica |
| Saturação de oxigênio | Percentual de oxigenação no sangue |
| Temperatura corporal | Temperatura em graus Celsius |
| Frequência respiratória | Respirações por minuto |
| ETCO2 | Dióxido de carbono ao final da expiração |
| PVC | Pressão venosa central |

## 5. Análise por CSV

O arquivo `data/sinais_vitais_simulados.csv` contém exemplos de pacientes em diferentes condições clínicas.

Exemplos de cenários:

| Paciente | Condição simulada | Gravidade esperada |
|---|---|---|
| PACIENTE_001 | Sinais vitais normais | normal |
| PACIENTE_002 | Frequência cardíaca elevada, pressão alta, baixa saturação e febre | crítico |
| PACIENTE_003 | Frequência cardíaca baixa | alto |
| PACIENTE_004 | Saturação reduzida e sinais de atenção | atenção |

A análise por CSV permite validar as regras de detecção de anomalias em dados estruturados, como frequência cardíaca, pressão arterial, saturação de oxigênio e temperatura.

## 6. Análise por Imagem do Monitor

Além do CSV, foi criada uma análise baseada em imagem de monitor multiparamétrico.

A imagem utilizada está em:

```text
data/images/monitor_sinais_vitais.png
```

Nesta versão acadêmica, os valores exibidos no monitor são extraídos de forma estruturada assistida.

Isso significa que a imagem é utilizada como evidência visual do cenário clínico, enquanto os valores observados no monitor são organizados no código para a análise de anomalias.

Em uma evolução futura, essa etapa pode ser automatizada com OCR ou serviços de visão computacional, como Azure Computer Vision.

## 7. Valores Extraídos da Imagem

A imagem do monitor apresenta aproximadamente os seguintes sinais vitais:

| Parâmetro | Valor |
|---|---|
| Frequência cardíaca | 120 bpm |
| SpO2 | 98% |
| Frequência respiratória | 24 rpm |
| ETCO2 | 35 mmHg |
| Temperatura | 36.7 °C |
| Pressão arterial | 119/79 mmHg |
| PVC média | 14 mmHg |

O monitor também apresenta alertas visuais, como:

```text
FC ALTA
PVC ALTA
```

Esses alertas são considerados como evidências adicionais para a classificação de risco.

## 8. Critérios de Anomalia

Foram utilizadas regras simples para classificar alterações nos sinais vitais.

| Condição | Gravidade |
|---|---|
| Frequência cardíaca menor que 50 bpm | alto |
| Frequência cardíaca maior que 120 bpm | alto |
| Pressão arterial maior que 160/100 mmHg | alto |
| Pressão arterial menor que 90/60 mmHg | atenção |
| Saturação de oxigênio menor que 90% | crítico |
| Saturação de oxigênio entre 90% e 93% | alto |
| Temperatura maior ou igual a 38 °C | atenção |
| Temperatura menor que 35 °C | alto |
| Frequência respiratória acima de 22 rpm | atenção |
| PVC média elevada | alto |
| Alerta visual de FC alta no monitor | alto |
| Alerta visual de PVC alta no monitor | alto |

A prioridade dos níveis de gravidade segue a ordem:

```text
crítico > alto > atenção > normal
```

Quando mais de uma anomalia é identificada, a gravidade final é definida pela maior gravidade detectada.

## 9. Saída do Módulo

A saída do módulo segue o padrão utilizado no pipeline multimodal:

```text
tipo_dado
evento
gravidade
timestamp
sinais_extraidos
alertas
descricao
```

Exemplo simplificado de saída:

```json
{
    "tipo_dado": "imagem_sinais_vitais",
    "evento": "analise_imagem_monitor",
    "gravidade": "alto",
    "descricao": "Análise estruturada de imagem de monitor multiparamétrico."
}
```

## 10. Execução

Para executar a análise da imagem de sinais vitais, utiliza-se o script:

```text
run_vital_image_demo.py
```

Comando de execução:

```powershell
python run_vital_image_demo.py
```

A saída estruturada é salva em:

```text
outputs/resultado_imagem_sinais_vitais.json
```

A evidência da execução em terminal pode ser salva em:

```text
outputs/resultado_imagem_sinais_vitais.txt
```

Para salvar a evidência em TXT, pode-se executar:

```powershell
python run_vital_image_demo.py | Out-File -FilePath outputs\resultado_imagem_sinais_vitais.txt -Encoding utf8
```

## 11. Exemplo de Resultado Esperado

Ao executar o script de demonstração com a imagem do monitor, espera-se obter um resumo semelhante a:

```text
DEMONSTRAÇÃO COM IMAGEM DE SINAIS VITAIS

Sinais vitais extraídos da imagem:
FC: 120 bpm
SpO2: 98%
RESP: 24 rpm
ETCO2: 35 mmHg
PVC média: 14 mmHg
TEMP: 36.7 °C
PNI: 119/79 mmHg

Gravidade final:
alto
```

Exemplos de alertas detectados:

| Evento | Gravidade | Descrição |
|---|---|---|
| frequencia_respiratoria_elevada | atenção | Frequência respiratória elevada |
| pvc_elevada | alto | PVC média elevada |
| alerta_visual_fc_alta | alto | Monitor apresentou alerta visual de FC alta |
| alerta_visual_pvc_alta | alto | Monitor apresentou alerta visual de PVC alta |

## 12. Integração com o Pipeline Multimodal

O resultado da análise de sinais vitais é integrado ao pipeline principal:

```text
src/multimodal_pipeline.py
```

No pipeline completo, os sinais vitais são combinados com:

- áudio e texto;
- vídeo clínico;
- prescrições médicas.

Exemplo de fusão:

```text
Áudio: crítico
Vídeo: alto
Sinais vitais por imagem: alto
Prescrições: crítico
        ↓
Gravidade final: crítico
```

A gravidade final do alerta multimodal é definida com base no evento mais severo identificado entre os módulos.

## 13. Relação com o Tech Challenge

O desafio da Fase 4 solicita a detecção de anomalias em sinais vitais, prescrições e evolução clínica, além da integração de diferentes tipos de dados médicos.

Este módulo atende à parte de sinais vitais ao demonstrar:

- análise de dados estruturados em CSV;
- análise de imagem de monitor multiparamétrico;
- identificação de anomalias fisiológicas;
- geração de alertas estruturados;
- integração com o pipeline multimodal.

## 14. Limitações

A análise da imagem ainda não utiliza OCR automático.

Nesta versão, os valores são extraídos de forma estruturada assistida a partir da imagem do monitor.

A solução possui finalidade acadêmica e não substitui avaliação médica real.

Em uma aplicação clínica real, seria necessário validar os limites utilizados com protocolos hospitalares e profissionais da saúde.

Também seria necessário considerar histórico do paciente, idade, condição clínica, medicamentos em uso, contexto do atendimento e integração com sistemas hospitalares reais.

## 15. Evoluções Futuras

Como melhorias futuras, o módulo pode ser expandido para:

- extração automática dos valores da imagem com OCR;
- integração com Azure Computer Vision;
- leitura direta de monitores hospitalares;
- análise temporal dos sinais vitais;
- uso de modelos de machine learning para detecção de anomalias;
- análise de séries temporais com bases públicas, como PhysioNet;
- geração de alertas em tempo real para a equipe médica;
- integração com dashboards clínicos.

## 16. Conclusão

O módulo de sinais vitais amplia a solução multimodal ao permitir a identificação de alterações fisiológicas relevantes a partir de dados estruturados e imagem de monitor hospitalar.

A implementação demonstrou que é possível representar um cenário clínico mais realista ao utilizar uma imagem de monitor multiparamétrico como evidência visual e transformar os valores observados em uma saída estruturada.

Com isso, o projeto passa a integrar sinais vitais ao fluxo multimodal de alerta, juntamente com áudio, vídeo e prescrições médicas.
