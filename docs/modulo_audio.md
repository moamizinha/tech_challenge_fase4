# Módulo de Áudio e Texto

## 1. Objetivo

O módulo de áudio e texto tem como objetivo processar áudios de consultas médicas, realizar a transcrição automática da fala do paciente, identificar termos críticos, analisar sentimento e classificar o nível de risco associado ao conteúdo transcrito.

Este módulo faz parte da solução multimodal do Tech Challenge Fase 4, contribuindo para a geração de alertas clínicos preventivos a partir da análise de dados de áudio e texto.

## 2. Relação com o Tech Challenge

O desafio da Fase 4 solicita que a solução seja capaz de:

- processar áudios de consultas médicas;
- detectar alterações vocais ou sintomas relatados pelo paciente;
- utilizar Azure Speech to Text para transcrever os áudios;
- identificar termos críticos e sentimentos com Azure Text Analytics;
- integrar os resultados ao pipeline multimodal de alerta médico.

Neste projeto, o módulo de áudio foi implementado com três abordagens:

1. análise de transcrições simuladas;
2. análise de áudio real com SpeechRecognition;
3. análise de áudio real com Azure Speech to Text e Azure Text Analytics.

## 3. Entradas de Dados

O módulo utiliza as seguintes entradas:

```text
data/transcricoes_audio_simuladas.csv
data/termos_criticos.csv
data/audios/consulta_audio_real.wav
```

O arquivo `data/transcricoes_audio_simuladas.csv` contém transcrições simuladas de consultas médicas.

O arquivo `data/termos_criticos.csv` contém a lista de termos críticos, categorias clínicas, gravidades e descrições.

O arquivo `data/audios/consulta_audio_real.wav` representa um áudio real ou simulado gravado para validação do fluxo de transcrição.

## 4. Arquivos Principais

A análise de áudio e texto é implementada principalmente nos arquivos:

```text
src/audio_analysis.py
run_audio_demo.py
run_real_audio_demo.py
run_azure_audio_demo.py
```

A função principal de classificação textual está no arquivo:

```text
src/audio_analysis.py
```

Esse arquivo é responsável por:

- carregar os termos críticos;
- normalizar textos;
- detectar termos na transcrição;
- tratar contextos de negação;
- evitar duplicidade de termos;
- classificar a gravidade final;
- gerar uma saída estruturada.

## 5. Base de Termos Críticos

A base de termos críticos está armazenada em:

```text
data/termos_criticos.csv
```

Cada termo possui:

- termo;
- categoria;
- gravidade;
- descrição.

Exemplos de termos utilizados:

| Termo | Categoria | Gravidade |
|---|---|---|
| falta de ar | respiratório | crítico |
| dor no peito | cardiovascular | crítico |
| desmaio | neurológico | crítico |
| confusão mental | neurológico | crítico |
| respiração ofegante | respiratório | alto |
| cansaço extremo | geral | alto |
| tontura | neurológico | alto |
| fadiga | geral | atenção |
| fraqueza | geral | atenção |
| cansaço | geral | atenção |

## 6. Funcionamento do Classificador Local

O classificador local realiza as seguintes etapas:

1. Carrega a base `data/termos_criticos.csv`;
2. Normaliza a transcrição;
3. Remove acentos para melhorar a comparação textual;
4. Procura termos críticos na fala do paciente;
5. Verifica se o termo aparece em contexto de negação;
6. Evita duplicidade entre termos semelhantes;
7. Define a maior gravidade detectada;
8. Retorna o resultado estruturado.

A prioridade dos níveis de gravidade é:

```text
crítico > alto > atenção > normal
```

Quando mais de um termo é detectado, a maior gravidade encontrada é usada como gravidade final do áudio.

## 7. Tratamento de Negação

O módulo possui uma regra para evitar falsos alertas em frases nas quais o paciente nega um sintoma.

Exemplo:

```text
Paciente relata estar bem, sem dor, sem falta de ar e sem tontura.
```

Nesse caso, os termos “falta de ar” e “tontura” aparecem na frase, mas estão acompanhados da palavra “sem”.

Portanto, o sistema não gera alerta para esses termos.

Exemplos de padrões tratados:

```text
sem falta de ar
nega falta de ar
não relata falta de ar
não apresenta falta de ar
sem queixa de falta de ar
```

## 8. Tratamento de Duplicidade de Termos

Durante os testes, foi identificado que o termo “cansaço” poderia ser detectado dentro de “cansaço extremo”.

Para evitar duplicidade, o código passou a priorizar termos maiores antes de termos menores.

Exemplo:

```text
Paciente relata falta de ar, tontura e cansaço extremo durante a consulta.
```

Termos detectados corretamente:

| Termo | Gravidade |
|---|---|
| cansaço extremo | alto |
| falta de ar | crítico |
| tontura | alto |

O termo simples “cansaço” não é duplicado nesse caso, pois já está contemplado por “cansaço extremo”.

## 9. Execução com Transcrições Simuladas

A execução com transcrições simuladas é feita pelo script:

```text
run_audio_demo.py
```

Comando de execução:

```powershell
python run_audio_demo.py
```

Esse script lê o arquivo:

```text
data/transcricoes_audio_simuladas.csv
```

e gera a saída:

```text
outputs/resultado_audio.json
```

A evidência da execução em terminal pode ser salva com:

```powershell
python run_audio_demo.py | Out-File -FilePath outputs\resultado_audio.txt -Encoding utf8
```

## 10. Validação com Transcrições Simuladas

A base de transcrições simuladas contém diferentes cenários clínicos.

Exemplo de validação:

| Áudio | Gravidade Detectada | Gravidade Esperada | Status |
|---|---|---|---|
| AUDIO_001 | normal | normal | validado |
| AUDIO_002 | crítico | crítico | validado |
| AUDIO_003 | atenção | atenção | validado |
| AUDIO_004 | crítico | crítico | validado |
| AUDIO_005 | crítico | crítico | validado |
| AUDIO_006 | atenção | atenção | validado |

O caso `AUDIO_006` foi ajustado com a inclusão do termo “cansaço” na base de termos críticos.

Resultado validado:

```text
Áudio ID: AUDIO_006
Paciente: PACIENTE_006
Gravidade detectada: atenção
Gravidade esperada: atenção
Termo detectado: cansaço
```

## 11. Execução com Áudio Real usando SpeechRecognition

Além das transcrições simuladas, foi realizado um teste com um arquivo de áudio real em formato WAV.

O script utilizado foi:

```text
run_real_audio_demo.py
```

O fluxo executado foi:

```text
arquivo de áudio
→ transcrição automática
→ análise de termos críticos
→ classificação de risco
→ geração de saída JSON
```

Comando de execução:

```powershell
python run_real_audio_demo.py
```

A transcrição obtida foi:

```text
paciente relata falta de ar tontura e cansaço extremo durante a consulta
```

O sistema identificou os seguintes termos críticos:

| Termo | Categoria | Gravidade |
|---|---|---|
| cansaço extremo | geral | alto |
| falta de ar | respiratório | crítico |
| tontura | neurológico | alto |

A gravidade final detectada foi:

```text
crítico
```

A saída estruturada foi salva em:

```text
outputs/resultado_audio_real.json
```

A evidência da execução em terminal foi registrada em:

```text
outputs/resultado_audio_real.txt
```

## 12. Execução com Azure Speech to Text e Azure Text Analytics

Para atender ao requisito do Tech Challenge, o módulo de áudio também foi validado com serviços Azure.

O script utilizado foi:

```text
run_azure_audio_demo.py
```

O fluxo executado foi:

```text
arquivo de áudio real
→ Azure Speech to Text
→ transcrição automática
→ Azure Text Analytics
→ análise de sentimento e frases-chave
→ classificador local de termos críticos
→ geração de alerta em JSON
```

Essa abordagem utiliza:

- Azure Speech to Text para transcrição do áudio;
- Azure Text Analytics para análise textual;
- classificador local para identificação de termos críticos específicos do projeto.

## 13. Configuração das Credenciais Azure

As credenciais Azure são armazenadas localmente no arquivo:

```text
.env
```

Esse arquivo não deve ser enviado ao GitHub.

O formato utilizado é:

```env
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth

AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=https://seu-endpoint.cognitiveservices.azure.com/
```

O arquivo `.env` está protegido pelo `.gitignore`, evitando exposição de chaves no repositório.

## 14. Resultado da Execução com Azure

A execução com Azure obteve a seguinte transcrição:

```text
Paciente relata falta de ar, tontura e cansaço extremo durante a consulta.
```

O Azure Text Analytics classificou o sentimento como:

```text
negative
```

As frases-chave retornadas foram:

```text
['cansaço', 'Paciente', 'falta', 'ar', 'tontura', 'consulta']
```

Após a transcrição, o classificador local identificou os termos críticos:

| Termo | Categoria | Gravidade |
|---|---|---|
| cansaço extremo | geral | alto |
| falta de ar | respiratório | crítico |
| tontura | neurológico | alto |

A gravidade final foi classificada como:

```text
crítico
```

O resultado estruturado foi salvo em:

```text
outputs/resultado_audio_azure.json
```

A evidência da execução foi registrada em:

```text
outputs/resultado_audio_azure.txt
```

## 15. Exemplo de Saída JSON

Exemplo simplificado da saída gerada pelo script Azure:

```json
{
    "tipo_dado": "audio_azure",
    "evento": "analise_audio_com_azure",
    "metodo_transcricao": "Azure Speech to Text",
    "metodo_texto": "Azure Text Analytics",
    "transcricao": "Paciente relata falta de ar, tontura e cansaço extremo durante a consulta.",
    "sentimento_azure": "negative",
    "gravidade": "crítico",
    "termos_detectados": [
        {
            "termo": "cansaço extremo",
            "categoria": "geral",
            "gravidade": "alto"
        },
        {
            "termo": "falta de ar",
            "categoria": "respiratorio",
            "gravidade": "crítico"
        },
        {
            "termo": "tontura",
            "categoria": "neurologico",
            "gravidade": "alto"
        }
    ]
}
```

## 16. Integração com o Pipeline Multimodal

O resultado do módulo de áudio é integrado ao pipeline principal:

```text
src/multimodal_pipeline.py
```

No pipeline completo, a análise de áudio é combinada com:

- análise de vídeo;
- análise de imagem de sinais vitais;
- análise de prescrições médicas.

Exemplo de fusão:

```text
Áudio: crítico
Vídeo: alto
Sinais vitais por imagem: alto
Prescrições: crítico
        ↓
Gravidade final: crítico
```

A gravidade final do alerta multimodal é definida com base na maior gravidade detectada entre os módulos.

## 17. Saídas Geradas

O módulo de áudio gera os seguintes arquivos de saída:

```text
outputs/resultado_audio.json
outputs/resultado_audio.txt
outputs/resultado_audio_real.json
outputs/resultado_audio_real.txt
outputs/resultado_audio_azure.json
outputs/resultado_audio_azure.txt
```

Essas saídas registram tanto os resultados estruturados em JSON quanto as evidências da execução em terminal.

## 18. Tecnologias Utilizadas

As principais tecnologias utilizadas no módulo de áudio foram:

- Python;
- CSV;
- JSON;
- SpeechRecognition;
- Google Web Speech API;
- Azure Speech to Text;
- Azure Text Analytics;
- python-dotenv;
- Azure SDK for Python.

## 19. Limitações

Este módulo possui finalidade acadêmica.

As transcrições simuladas e o áudio real utilizado foram criados para demonstração, não representando dados reais de pacientes.

O classificador local utiliza regras simples baseadas em palavras-chave, sem substituir avaliação médica real.

A análise de sentimento do Azure pode indicar tendência emocional geral do texto, mas não deve ser interpretada como diagnóstico clínico.

Em uma aplicação real, seria necessário validar os termos, regras, thresholds e fluxos com profissionais da saúde, protocolos clínicos e requisitos de segurança e privacidade.

## 20. Evoluções Futuras

Como melhorias futuras, o módulo pode ser expandido para:

- transcrição contínua em tempo real;
- detecção de pausas, hesitações e alterações vocais;
- análise de intensidade, ritmo e frequência da fala;
- uso de modelos específicos para detecção de fadiga vocal;
- integração com Azure Health Insights;
- integração com prontuário eletrônico;
- armazenamento seguro das transcrições;
- dashboard de alertas em tempo real;
- validação com especialistas da área médica.

## 21. Conclusão

O módulo de áudio e texto atende aos requisitos principais da análise de áudio do Tech Challenge Fase 4.

A implementação demonstrou o processamento de transcrições simuladas, a análise de áudio real com transcrição automática e a integração real com Azure Speech to Text e Azure Text Analytics.

Com isso, o projeto consegue transformar um áudio de consulta médica em texto, analisar sentimento, identificar termos críticos e gerar uma classificação de risco estruturada.

O resultado do módulo é integrado ao pipeline multimodal, contribuindo para a geração de alertas preventivos à equipe médica.
