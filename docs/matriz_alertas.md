# Matriz de Alertas - Tech Challenge Fase 4

## 1. Objetivo

A matriz de alertas define os critérios utilizados pelo sistema para classificar eventos clínicos detectados a partir de dados multimodais.

A solução considera dados de:

- Áudio e texto;
- Vídeo;
- Sinais vitais;
- Prescrições e evolução clínica.

A partir da análise desses dados, o sistema classifica a gravidade do evento e gera uma recomendação para a equipe médica.

## 2. Níveis de Gravidade

| Nível | Descrição | Ação Recomendada |
|---|---|---|
| Normal | Nenhuma alteração relevante foi identificada. | Manter monitoramento de rotina. |
| Atenção | Pequenas alterações ou sinais leves foram identificados. | Manter paciente em observação. |
| Alto | Alterações importantes foram detectadas e podem indicar risco clínico. | Encaminhar para avaliação clínica urgente. |
| Crítico | Sinais graves ou combinação de anomalias indicam risco elevado. | Acionar equipe médica imediatamente. |

## 3. Critérios para Áudio e Texto

| Evento Detectado | Exemplo de Termo | Gravidade |
|---|---|---|
| Sintoma respiratório grave | falta de ar | Crítico |
| Possível evento cardiovascular | dor no peito | Crítico |
| Perda de consciência | desmaio | Crítico |
| Alteração neurológica | confusão mental | Crítico |
| Cansaço intenso | cansaço extremo | Alto |
| Alteração de equilíbrio | tontura | Alto |
| Cansaço persistente | fadiga | Atenção |
| Redução de força | fraqueza | Atenção |

## 4. Critérios para Sinais Vitais

| Sinal Vital | Condição | Gravidade |
|---|---|---|
| Frequência cardíaca | Menor que 50 bpm | Alto |
| Frequência cardíaca | Maior que 120 bpm | Alto |
| Pressão arterial | Maior que 160/100 mmHg | Alto |
| Pressão arterial | Menor que 90/60 mmHg | Atenção |
| Saturação de oxigênio | Menor que 90% | Crítico |
| Saturação de oxigênio | Entre 90% e 93% | Alto |
| Temperatura | Maior ou igual a 38 °C | Atenção |
| Temperatura | Menor que 35 °C | Alto |

## 5. Critérios para Vídeo

| Evento Detectado | Descrição | Gravidade |
|---|---|---|
| Queda | Paciente cai ou perde completamente o equilíbrio. | Alto |
| Perda de equilíbrio | Instabilidade durante movimentação ou fisioterapia. | Alto |
| Movimento brusco | Movimento fora do padrão esperado. | Alto |
| Imobilidade | Ausência de movimento por período inesperado. | Alto |
| Tremor intenso | Movimento repetitivo e anormal. | Alto |
| Movimento moderado | Variação leve ou moderada durante atividade. | Atenção |
| Movimento esperado | Execução normal da atividade. | Normal |

## 6. Regra de Fusão Multimodal

A gravidade final do alerta é definida pela maior gravidade identificada entre os módulos analisados.

A prioridade segue a ordem:

```text
crítico > alto > atenção > normal
