# Relatório — Matheus Ramos - Matrícula 3467

Relatório do projeto, preenchido na sua branch. Cada marco acrescenta a sua seção. Responda com as suas palavras e com
os números da sua execução; cada resposta cabe em até 6 linhas, além das tabelas.

## Marco 1

### Ambiente

<!-- Cole aqui a saída de `which python` e da Etapa 0 do `python marco1.py`. -->

### R1 — Expressões regulares

<!-- Uma string que re.match aceita e re.fullmatch rejeita com o padrão de tag; consequência para valida_tag. -->

### R2 — Linhas inválidas

<!-- Por que ler_log devolve as linhas descartadas; uma situação real em que descartar em silêncio esconderia um problema. -->

### R3 — Late binding

<!-- Por que errados["PT102"](4095) dá 409,5 e por que a sua criar_conversores não tem o problema. -->

### R4 — Escala nominal

<!-- Hipótese para a diferença da Etapa 2(f) e onde, no código da base, está a explicação. -->

### R5 — Previsão × medição (Etapa 3)

Previsões registradas no commit: <!-- substitua pelo hash de 7 caracteres do seu commit -->

| Grandeza | Previsão | Medido |
| --- | --- | --- |
| Memória da lista / memória do `uint16` | 15x | 18x |
| Tempo do laço / tempo vetorizado | 20x | 55x |
| Tempo da compreensão / tempo do laço | 1x | 0.5x |

A maior diferença entre a previsão e a medição ocorreu na velocidade da conversão vetorizada[cite: 1], pois a implementação do NumPy executa as operações diretamente em linguagem C de forma otimizada, eliminando o overhead do interpretador Python muito além do previsto.
O estouro do uint16 ao multiplicar por 20 ocorre porque a capacidade máxima de 16 bits sem sinal é 65535[cite: 1]. Como a contagem máxima do conversor é 4095, o cálculo  excede o limite e dá a volta, resultando exatamente em 16364.

Para armazenar as contagens puras (inteiros de 0 a 4095), o `dtype` ideal é o `uint16`, pois consome apenas 2 bytes por elemento e comporta todos os valores sem estouro[cite: 1]. Para as pressões calculadas em kPa, o tipo adequado é `float32` ou `float64`, que garantem a representação correta de números decimais[cite: 1].

### R6 — Tipos da SerieTemporal (Etapa 4)

| Expressão | Previsão | Medido |
| --- | --- | --- |
| `s + 10` | `SerieTemporal` | `SerieTemporal` |
| `s[0]` | `float` | `np.float64` |
| `s[1:5]` | `SerieTemporal` | `SerieTemporal` |
| `s > 10` | `np.ndarray` | `SerieTemporal` |
| `s.mean()` | `float` | `np.float64` |

O resultado que mais se destaca é o fato de comparações lógicas (`s > 10`) e fatiamentos (`s[1:5]`) preservarem o tipo `SerieTemporal` em vez de regredirem para um `np.ndarray` comum. Isso ocorre porque a subclasse implementada herda o mecanismo de propagação de tipo do NumPy para operações vetorizadas. Por outro lado, a indexação de elemento individual (`s[0]`) e métodos de agregação (`s.mean()`) reduzem a dimensão dos dados, retornando escalares do NumPy (`np.float64`).

### R7 — Issue #4

<!-- Sintoma; o teste de regressão (nome); a causa, em termos da soma acumulada; a correção; por que os testes de aceitação não pegaram o defeito; mais um caso que eles não cobrem e qual teste seu o cobre. -->
