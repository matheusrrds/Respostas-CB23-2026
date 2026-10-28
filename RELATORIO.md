# Relatório — Matheus Ramos - Matrícula 3467

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

/home/al.matheus.souza/venvs/prog2-venv/bin/python
=== Etapa 0: ambiente ===
Python 3.13.15 | NumPy 2.5.4 | fornecido 4.0

### R1 — Expressões regulares

A string `"PT101 extra"` é aceita por `re.match` com o padrão `[A-Z]{1,2}\d{1,3}` porque ele valida apenas o início da cadeia de caracteres. Já o `re.fullmatch` a rejeita por exigir que a string inteira case com a expressão. Se `valida_tag` utilizasse `match`, entradas com sufixos inválidos ou espaços sobressalentes (como `"PT101 "` ou `"PT1010"`) seriam aceitas incorretamente como tags válidas[cite: 2].

### R2 — Linhas inválidas

A função `ler_log` devolve as linhas descartadas para permitir auditoria, rastreabilidade e diagnóstico de falhas de comunicação[cite: 2]. Em uma operação real, o descarte silencioso esconderia ruídos na rede, pacotes corrompidos ou mal funcionamento de um sensor. Isso levaria a equipe a operar a estação sem notar que leituras críticas estavam sendo perdidas na transmissão[cite: 2].

### R3 — Late binding

O valor `409,5` ocorre porque, na versão errada, o escopo da lambda busca a variável `fator` no momento da execução (*late binding*), fazendo com que todas as funções usem o último fator iterado no dicionário (o do `FT201`, igual a `0,1`, resultando em $4095 \times 0,1 = 409,5$)[cite: 2]. A nossa `criar_conversores` resolve isso usando o parâmetro padrão na lambda (`f=fator`), o que força a vinculação antecipada (*early binding*) do fator exato de cada tag[cite: 2].

### R4 — Escala nominal

A diferença ocorre porque a conversão nominal faz um mapeamento linear simples de 0 a 4095 sobre a faixa do sensor, enquanto a geração real do dado aplica um *offset* e um fator de calibração específico da faixa de operação. A explicação exata dessa calibração está no arquivo `fornecido/simulador.py`, nas funções internas que simulam o comportamento do transmissor de pressão.

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: `aa706fd`

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 15x | 18x |
| Tempo do laço / tempo vetorizado | 20x | 31x |
| Tempo da compreensão / tempo do laço | 1x | 0.90x |

A maior diferença entre a previsão e a medição ocorreu na velocidade da conversão vetorizada, pois a implementação do NumPy executa as operações diretamente em linguagem C de forma otimizada, eliminando o overhead do interpretador Python muito além do previsto.

O estouro do uint16 ao multiplicar por 20 ocorre porque a capacidade máxima de 16 bits sem sinal é 65535. Como a contagem máxima do conversor é 4095, o cálculo  excede o limite e dá a volta, resultando exatamente em 16364.

Para armazenar as contagens puras (inteiros de 0 a 4095), o `dtype` ideal é o `uint16`, pois consome apenas 2 bytes por elemento e comporta todos os valores sem estouro. Para as pressões calculadas em kPa, o tipo adequado é `float32` ou `float64`, que garantem a representação correta de números decimais.

### R6 — Tipos da SerieTemporal (Etapa 4)

| Expressão | Previsão | Medido |
| --- | --- | --- |
| `s + 10` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float` | `np.float64` |
| `s[1:5]` | `SerieTemporal` | `SerieTemporal` |
| `s > 10` | `np.ndarray` | `SerieTemporal` |
| `s.mean()` | `float` | `np.float64` |

O resultado que mais se destaca é o fato de comparações lógicas (`s > 10`) e fatiamentos (`s[1:5]`) preservarem o tipo `SerieTemporal` em vez de regredirem para um `np.ndarray` comum. Isso ocorre porque a subclasse implementada herda o mecanismo de propagação de tipo do NumPy para operações vetorizadas. 

E a indexação de elemento individual (`s[0]`) e métodos de agregação (`s.mean()`) reduzem a dimensão dos dados, retornando escalares do NumPy (`np.float64`).

### R7 — Issue #4

O sintoma era o retorno de N - n elementos em vez de N - n + 1$ (ex.: 570 valores para 600 leituras e janela n=30). O defeito foi identificado pelo teste de regressão `test_media_movel_tamanho_correto`. A causa ocorria no fatiamento incorreto da soma acumulada (`cumsum`), que omitia o termo inicial necessário para calcular a primeira média do intervalo. 

A correção ajustou os índices do fatiamento da `cumsum` (inserindo o zero inicial no cálculo da diferença de janelas), sem laços e preservando o tipo `SerieTemporal`. Os testes de aceitação originais não pegaram o defeito porque comparavam apenas os valores das posições existentes, sem validar o tamanho exato do array retornado. Outro caso não coberto por eles é o de janela de tamanho unitário (n=1), validado pelo teste `test_media_movel_janela_um`.
