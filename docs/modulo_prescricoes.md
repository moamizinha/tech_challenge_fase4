# Módulo de Prescrições Médicas

## 1. Objetivo

O módulo de prescrições médicas tem como objetivo identificar possíveis anomalias em alterações de tratamento, como aumento inesperado de dose, duplicidade de medicamento, suspensão inesperada e uso de medicamentos de maior atenção.

Este módulo complementa a solução multimodal do Tech Challenge Fase 4, permitindo que o sistema analise não apenas áudio, vídeo e sinais vitais, mas também informações relacionadas à evolução terapêutica do paciente.

## 2. Entrada de Dados

A entrada do módulo é uma base simulada de prescrições médicas, armazenada no arquivo:

```text
data/prescricoes_simuladas.csv
```

Cada registro contém:

- identificação da prescrição;
- identificação do paciente;
- timestamp;
- medicamento;
- dose atual;
- dose anterior;
- unidade;
- frequência;
- tipo de alteração;
- observação;
- gravidade esperada.

## 3. Arquivo Principal

A análise das prescrições é realizada pelo arquivo:

```text
src/prescription_analysis.py
```

Esse módulo lê a base simulada, aplica regras de detecção de anomalias e gera uma saída estruturada para integração com o pipeline multimodal.

## 4. Tipos de Anomalias Detectadas

O módulo considera os seguintes tipos de alterações:

| Tipo de Alteração | Descrição | Exemplo |
|---|---|---|
| sem_alteracao | Prescrição mantida sem mudança relevante | Dipirona 500 mg mantida |
| aumento_dose | Aumento da dose em relação à anterior | Morfina de 2 mg para 10 mg |
| duplicidade | Possível duplicidade de medicamento | Heparina duplicada |
| suspensao | Suspensão inesperada de medicamento | Antibiótico suspenso |

## 5. Medicamentos de Maior Atenção

Alguns medicamentos foram classificados como medicamentos de maior atenção devido ao risco associado ao uso ou à alteração de dose.

Nesta versão, foram considerados:

| Medicamento | Motivo de Atenção |
|---|---|
| Insulina | Alterações de dose podem causar risco metabólico |
| Heparina | Anticoagulante com risco em caso de duplicidade |
| Morfina | Opioide com risco associado ao aumento de dose |
| Midazolam | Sedativo com potencial risco respiratório |

## 6. Critérios de Classificação

A classificação de gravidade segue regras simples criadas para fins acadêmicos e demonstração do conceito.

| Situação Detectada | Gravidade |
|---|---|
| Prescrição sem alteração relevante | normal |
| Aumento leve de dose | atenção |
| Aumento expressivo de dose | alto |
| Aumento expressivo em medicamento de maior atenção | crítico |
| Duplicidade de medicamento de maior atenção | crítico |
| Suspensão inesperada de medicamento ativo | alto |
| Uso de medicamento de maior atenção sem outra alteração | atenção |

A prioridade dos níveis de gravidade segue a ordem:

```text
crítico > alto > atenção > normal
```

Quando mais de um alerta é identificado na mesma prescrição, a gravidade final da prescrição é definida pela maior gravidade encontrada.

## 7. Exemplos da Base Simulada

| Prescrição | Medicamento | Alteração | Gravidade Esperada |
|---|---|---|---|
| PRESC_001 | Dipirona | Sem alteração | normal |
| PRESC_002 | Insulina | Aumento de dose | alto |
| PRESC_003 | Heparina | Duplicidade | crítico |
| PRESC_004 | Morfina | Aumento relevante de dose | crítico |
| PRESC_005 | Losartana | Sem alteração | normal |
| PRESC_006 | Antibiótico | Suspensão inesperada | alto |
| PRESC_007 | Midazolam | Aumento de sedativo | crítico |
| PRESC_008 | Paracetamol | Aumento leve de dose | atenção |

## 8. Saída do Módulo

A saída do módulo segue o padrão utilizado no projeto:

```text
tipo_dado
evento
prescricao_id
paciente_id
timestamp
medicamento
dose_atual
dose_anterior
unidade
frequencia
tipo_alteracao
gravidade
gravidade_esperada
alertas
descricao
```

Exemplo de saída:

```json
{
    "tipo_dado": "prescricao",
    "evento": "analise_de_prescricao",
    "prescricao_id": "PRESC_004",
    "paciente_id": "PACIENTE_004",
    "medicamento": "Morfina",
    "dose_atual": 10.0,
    "dose_anterior": 2.0,
    "unidade": "mg",
    "frequencia": "4/4h",
    "tipo_alteracao": "aumento_dose",
    "gravidade": "crítico",
    "gravidade_esperada": "crítico",
    "descricao": "Aumento relevante de opioide"
}
```

## 9. Execução

Para executar a análise de prescrições, utiliza-se o script:

```text
run_prescription_demo.py
```

Comando de execução:

```powershell
python run_prescription_demo.py
```

A saída estruturada é salva em:

```text
outputs/resultado_prescricoes.json
```

A evidência da execução em terminal pode ser salva em:

```text
outputs/resultado_prescricoes.txt
```

Para salvar a evidência em TXT, pode-se executar:

```powershell
python run_prescription_demo.py | Out-File -FilePath outputs\resultado_prescricoes.txt -Encoding utf8
```

## 10. Validação

A execução do módulo comparou a gravidade detectada com a gravidade esperada em cada cenário simulado.

Resultado da validação:

| Prescrição | Gravidade Detectada | Gravidade Esperada | Status |
|---|---|---|---|
| PRESC_001 | normal | normal | validado |
| PRESC_002 | alto | alto | validado |
| PRESC_003 | crítico | crítico | validado |
| PRESC_004 | crítico | crítico | validado |
| PRESC_005 | normal | normal | validado |
| PRESC_006 | alto | alto | validado |
| PRESC_007 | crítico | crítico | validado |
| PRESC_008 | atenção | atenção | validado |

## 11. Exemplos de Alertas Detectados

Durante os testes, foram identificados diferentes tipos de alertas.

### PRESC_002 - Insulina

- Tipo de alteração: aumento de dose;
- Dose anterior: 8 UI;
- Dose atual: 20 UI;
- Gravidade detectada: alto;
- Justificativa: aumento expressivo de dose em medicamento de maior atenção.

### PRESC_003 - Heparina

- Tipo de alteração: duplicidade;
- Gravidade detectada: crítico;
- Justificativa: possível duplicidade de anticoagulante, classificado como medicamento de maior atenção.

### PRESC_004 - Morfina

- Tipo de alteração: aumento de dose;
- Dose anterior: 2 mg;
- Dose atual: 10 mg;
- Gravidade detectada: crítico;
- Justificativa: aumento expressivo de opioide.

### PRESC_006 - Antibiótico

- Tipo de alteração: suspensão;
- Gravidade detectada: alto;
- Justificativa: suspensão inesperada de medicamento em tratamento ativo.

### PRESC_007 - Midazolam

- Tipo de alteração: aumento de dose;
- Dose anterior: 5 mg;
- Dose atual: 15 mg;
- Gravidade detectada: crítico;
- Justificativa: aumento expressivo de sedativo com potencial risco respiratório.

## 12. Integração com o Pipeline Multimodal

O resultado do módulo de prescrições é integrado ao pipeline principal:

```text
src/multimodal_pipeline.py
```

No pipeline completo, a análise de prescrições é combinada com:

- análise de áudio e texto;
- análise de vídeo;
- análise de imagem de sinais vitais.

A gravidade final do alerta multimodal é definida com base na maior gravidade detectada entre os módulos.

Exemplo de fusão:

```text
Áudio: crítico
Vídeo: alto
Sinais vitais por imagem: alto
Prescrições: crítico
        ↓
Gravidade final: crítico
```

## 13. Relação com o Tech Challenge

O desafio da Fase 4 solicita a detecção de anomalias em diferentes fontes de dados médicos, incluindo sinais vitais, prescrições e evolução clínica.

Este módulo atende à parte de prescrições ao demonstrar a identificação de alterações inesperadas no tratamento e a geração de alertas estruturados para a equipe médica.

A saída do módulo é compatível com o padrão utilizado nos demais componentes da solução multimodal.

## 14. Limitações

Este módulo utiliza uma base simulada e regras simplificadas para fins acadêmicos.

Em uma aplicação real, a análise de prescrições deveria considerar:

- protocolos clínicos;
- histórico do paciente;
- interações medicamentosas;
- alergias;
- peso;
- idade;
- função renal;
- função hepática;
- via de administração;
- duração do tratamento;
- validação por profissionais da saúde.

A solução não substitui avaliação médica ou farmacêutica real.

## 15. Evoluções Futuras

Como melhorias futuras, o módulo pode ser expandido para:

- análise de interações medicamentosas;
- detecção de alergias;
- avaliação de dose por peso corporal;
- integração com prontuário eletrônico;
- uso de modelos de machine learning;
- validação com bases clínicas reais ou protocolos hospitalares;
- integração com serviços em nuvem para análise contínua;
- geração de alertas em tempo real para a equipe médica.

## 16. Conclusão

O módulo de prescrições médicas amplia a solução multimodal ao incluir a análise de alterações terapêuticas como fonte adicional de risco clínico.

A implementação demonstrou que é possível identificar, de forma estruturada, situações como aumento inesperado de dose, duplicidade de medicamento e suspensão inesperada.

Com isso, o projeto passa a integrar áudio, vídeo, sinais vitais, imagem de monitor e prescrições em um fluxo único de alerta para apoio ao monitoramento preventivo de pacientes.
