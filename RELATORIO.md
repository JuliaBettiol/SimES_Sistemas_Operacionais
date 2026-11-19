# Relatório — SimES: simulador de E/S e de sistema de arquivos

**Integrantes:** Júlia Bettiol de Oliveira; Thomaz Szeckir

**Repositório:** https://github.com/JuliaBettiol/SimES_Sistemas_Operacionais

## 0. Resumo

O grupo utilizou o dispositivo N1 fornecido e implementou os subsistemas N2 (escalonamento de E/S e modos de atendimento), N3 (operações de arquivos) e o módulo opcional M1 (cache de blocos). Foram executados 26 testes automatizados, sem falhas e com oito testes ignorados referentes a funcionalidades fora do escopo. Os seis experimentos do escopo somaram 58 execuções bem-sucedidas. Em X1, o SSTF reduziu a resposta média da carga aleatória de 50,1041 para 20,9874 ms em relação ao FCFS. Em X2, interrupções reduziram o uso de CPU de 86,2832% para 1,1213% no HDD com carga aleatória. Em X6, o cache LRU de 1.024 blocos com write-through atingiu 67,0588% de acertos, enquanto o write-back reduziu escritas físicas, mas apresentou perda de blocos na queda simulada.

## 1. Escopo realizado

| Parte | Situação | Observação |
|---|---|---|
| N1 · Dispositivo (fornecido) | usado | — |
| N2 · Subsistema de E/S (SSTF, SCAN, polling, interrupção) | completo | Escalonamento e modos de atendimento exercitados em X1 e X2. |
| N3 · Sistema de arquivos | completo | Operações e tabelas exercitadas em X3–X5. |
| N4 · Experimentos X1–X5 e relatório | completo | Experimentos executados e documentados. |
| M1 · Cache de blocos | completo | LRU/FIFO, write-through/write-back, experimento X6. |

Resultado dos testes automáticos (`python3 executar.py testes`): 26 testes executados, 0 falhas, 8 pulados (conforme `ferramentas/validar_entrega.py`).

## 2. Implementação

### N2 — Subsistema de E/S

**Onde:** `simes/es/escalonadores.py` e `simes/es/simulador.py`.

**Decisões:** O SSTF escolhe a requisição mais próxima do cilindro atual; o SCAN considera a direção do movimento. Os modos polling e interrupção distinguem o custo de ocupação da CPU. O experimento mantém o mesmo dispositivo e a mesma carga em cada comparação.

**Dificuldades:** A implementação exige manter coerentes a posição do cabeçote, a direção do SCAN e a contabilização de tempo/CPU. A consistência foi verificada por testes automatizados e pelos experimentos X1 e X2.

### N3 — Sistema de arquivos

**Onde:** `simes/arquivos/sistema.py`, `simes/arquivos/estruturas.py` e `simes/arquivos/simulador.py`.

**Decisões:** Resolução de caminhos por componentes de diretório, controle de descritores por processo e entradas globais compartilhadas; leitura/escrita a partir do deslocamento corrente e posicionamento explícito com `seek`. O ciclo de vida do arquivo considera a remoção de nome e a existência de descritores ainda abertos.

**Dificuldades:** Conciliar contagens de acessos, resolução de caminhos e descritores compartilhados; o comportamento foi conferido com os testes e com X3–X5.

### M1 — Cache de blocos

**Onde:** `simes/es/cache.py`, integrado a `simes/es/simulador.py`.

**Decisões:** Implementação de LRU/FIFO, capacidades configuráveis, write-through/write-back, sincronização e registro de blocos perdidos em queda.

**Dificuldades:** Coordenar substituição, gravação de blocos sujos e contagem de acertos e escritas; verificação em X6 e testes automatizados.

## 3. Experimentos

### X1 — Escalonadores sob quatro padrões de carga

**Hipótese:** Espera-se que os algoritmos SSTF e SCAN apresentem menor deslocamento total da cabeça de leitura e menor tempo médio de resposta do que o FCFS, principalmente em cargas aleatórias e concentradas. Em cargas sequenciais, a diferença entre os algoritmos deverá ser menor.

**Fundamentação:** O FCFS atende às requisições na ordem de chegada, sem considerar sua localização física no disco. O SSTF prioriza a requisição mais próxima da posição atual da cabeça, enquanto o SCAN organiza o atendimento conforme a direção de movimentação do braço. Como o tempo de busca depende da distância percorrida entre cilindros, a redução dos deslocamentos tende a diminuir o tempo total de atendimento. Entretanto, o SSTF pode provocar esperas prolongadas para determinadas requisições.

**Configuração:** Comparação dos escalonadores FCFS, SSTF e SCAN em um disco HDD, utilizando interrupções e quatro padrões de carga: sequencial, aleatória, concentrada e rajadas. Serão realizadas 12 simulações, considerando os indicadores de deslocamento total, tempo de resposta, espera máxima e vazão.

**Resultados:** | Carga | FCFS (ms) | SSTF (ms) | SCAN (ms) |
|---|---:|---:|---:|
| Sequencial | 10.241,0482 | 17,3917 | 23,2085 |
| Aleatória | 50,1041 | 20,9874 | 31,5329 |
| Concentrada | 19,7984 | 15,0220 | 33,1956 |
| Rajadas | 266,9744 | 147,4873 | 148,6205 |

Os deslocamentos totais na carga aleatória foram 3.316.472 (FCFS), 2.631.714 (SSTF) e 3.372.680 (SCAN). Na carga concentrada, o SCAN teve espera máxima de 118,752 ms, contra 96,023 ms no FCFS e 130,519 ms no SSTF.

**Evidências:** `resultados/es.csv` (X1); `graficos/X1_resposta_media_ms.png`, `graficos/X1_deslocamento_total.png` e `graficos/X1_espera_max_ms.png`.

**Análise:** O SSTF reduziu a resposta média em todas as quatro cargas, com destaque para a sequencial. O SCAN também superou o FCFS em três cargas, mas foi pior na concentrada (33,1956 contra 19,7984 ms), com maior deslocamento total (3.338.708 contra 1.864.164). A hipótese de vantagem geral dos dois algoritmos não valeu em todos os padrões. O SSTF apresentou espera máxima maior que o FCFS na carga concentrada, indicando um compromisso entre eficiência média e justiça.

**Veredito:** PARCIALMENTE CONFIRMADA

### X2 — Polling × interrupção conforme o dispositivo

**Hipótese:** Espera-se que o mecanismo de interrupções apresente menor utilização da CPU com operações de entrada e saída do que o polling, especialmente no disco HDD. No dispositivo rápido, a diferença deverá diminuir devido ao menor tempo de atendimento das requisições.

**Fundamentação:** No polling, a CPU verifica repetidamente se o dispositivo concluiu a operação, consumindo processamento durante a espera. Com interrupções, a CPU pode executar outras atividades e somente precisa tratar a conclusão quando o dispositivo sinaliza o término. O modelo considera um custo de 0,015 ms para o tratamento de cada interrupção, enquanto o dispositivo rápido elimina os custos de busca e latência rotacional.

**Configuração:** Comparação entre polling e interrupções, utilizando o escalonador FCFS, dois dispositivos (HDD e rápido) e duas cargas (aleatória e sequencial). Serão realizadas oito simulações, com foco no percentual de CPU dedicado à entrada e saída e nos tempos de atendimento.

**Resultados:** | Dispositivo / carga | Polling: CPU E/S (%) | Interrupção: CPU E/S (%) | Resposta média (ms), ambos |
|---|---:|---:|---:|
| HDD / aleatória | 86,2832 | 1,1213 | 50,1041 |
| HDD / sequencial | 99,9977 | 0,8361 | 10.241,0482 |
| Rápido / aleatória | 0,5280 | 1,1219 | 0,0642 |
| Rápido / sequencial | 1,0739 | 2,2821 | 0,0643 |

**Evidências:** `resultados/es.csv` (X2); `graficos/X2_cpu.png`.

**Análise:** No HDD, a interrupção reduziu fortemente a ocupação da CPU, pois evitou espera ativa durante operações lentas. No dispositivo rápido, porém, o custo fixo de tratar interrupções superou o tempo de espera do polling: interrupções consumiram mais CPU nas duas cargas. A resposta média permaneceu idêntica entre os modos em cada par, indicando que a diferença principal observada foi no custo de CPU, não na latência do dispositivo.

**Veredito:** CONFIRMADA

### X3 — Acesso sequencial × direto

**Hipótese:** Espera-se que a carga de acesso sequencial, representada pelo compilador, apresente menor custo médio por operação de leitura do que a carga de acesso direto, representada pelo banco de dados.

**Fundamentação:** O acesso sequencial tende a aproveitar a continuidade dos blocos e a posição corrente do arquivo, reduzindo a necessidade de reposicionamentos. O acesso direto utiliza operações de posicionamento para alcançar regiões específicas, podendo aumentar a quantidade de blocos distintos acessados. Entretanto, como o simulador também contabiliza a resolução de caminhos e as atualizações de diretórios, o custo total dependerá da combinação de operações presente em cada carga.

**Configuração:** Execução das cargas de sistema de arquivos denominadas compilador e banco_dados, utilizando alocação contígua e bloqueio consultivo. Serão comparados o número de operações, os acessos ao disco, o tempo médio por operação e os custos por tipo de operação.

**Resultados:** | Indicador | Compilador | Banco de dados |
|---|---:|---:|
| Operações | 3.904 | 6.602 |
| Acessos totais | 5.400 | 3.610 |
| Acessos por operação | 1,3832 | 0,5468 |
| Tempo médio por operação (ms) | 3,0704 | 3,0062 |
| Leituras: tempo médio (ms) | 1,4828 | 5,4918 |
| Escritas: tempo médio (ms) | 0,9068 | 5,5425 |

A carga de banco de dados executou 3.000 operações `seek`, contabilizadas com zero acessos e zero tempo no modelo.

**Evidências:** `resultados/arquivos.csv` (X3); `resultados/arquivos_por_operacao.csv` (X3); `graficos/X3_tempo_por_operacao.png`.

**Análise:** A leitura sequencial do compilador foi aproximadamente 3,70 vezes mais rápida que a leitura do banco de dados (1,4828 contra 5,4918 ms), conforme previsto. Entretanto, o tempo médio agregado por operação foi ligeiramente menor no banco de dados (3,0062 contra 3,0704 ms), porque a carga inclui muitos `seek` sem custo modelado. Portanto, comparar apenas a média global esconderia o custo maior das leituras diretas.

**Veredito:** CONFIRMADA

### X4 — Custo de resolver caminhos conforme a profundidade

**Hipótese:** Espera-se que o custo de resolução de caminhos aumente conforme a profundidade da estrutura de diretórios, aproximadamente de forma linear em relação ao número de diretórios percorridos.

**Fundamentação:** Para localizar um arquivo, o sistema precisa percorrer os componentes do caminho e consultar os diretórios intermediários. Na implementação do núcleo, a resolução de caminhos contabiliza leituras dos diretórios visitados. Assim, caminhos mais profundos tendem a exigir mais acessos e maior tempo de processamento.

**Configuração:** Execução de dez cargas geradas pela função fs_profundidade, com profundidades de 1 a 10 diretórios. Todas utilizarão alocação contígua e bloqueio consultivo. Serão observados os acessos médios por operação e o tempo médio de execução.

**Resultados:** | Profundidade | Acessos médios por `open` | Tempo médio de `open` (ms) |
|---|---:|---:|
| 1 | 2 | 4,25 |
| 2 | 3 | 4,29 |
| 3 | 4 | 4,33 |
| 4 | 5 | 4,37 |
| 5 | 6 | 4,41 |
| 6 | 7 | 4,45 |
| 7 | 8 | 4,49 |
| 8 | 9 | 4,53 |
| 9 | 10 | 4,57 |
| 10 | 11 | 4,61 |

Os acessos médios totais por operação cresceram de 1,0645 (profundidade 1) para 4,6056 (profundidade 10).

**Evidências:** `resultados/arquivos_por_operacao.csv` (X4, operação `open`); `resultados/arquivos.csv` (X4); `graficos/X4_open_por_profundidade.png`.

**Análise:** Cada nível adicional acrescentou exatamente um acesso médio à operação `open`, evidenciando crescimento linear no custo de resolução do caminho. O tempo médio de `open` cresceu 0,04 ms por nível no modelo. A média global por operação também aumentou, embora as cargas tenham quantidades totais de operações ligeiramente diferentes.

**Veredito:** CONFIRMADA

### X5 — Tabelas de arquivos abertos com vários processos

**Hipótese:** Espera-se que a execução da carga de servidor web demonstre o compartilhamento de entradas na tabela global de arquivos abertos, permitindo que diferentes processos mantenham descritores próprios associados a um mesmo arquivo. Assim, o número de entradas nas tabelas por processo poderá superar o número de entradas distintas na tabela global.

**Fundamentação:** O sistema de arquivos utiliza uma tabela global para representar arquivos abertos e tabelas individuais para armazenar os descritores de cada processo. Quando vários processos abrem o mesmo arquivo, suas entradas individuais podem referenciar uma única entrada global, cujo contador registra as aberturas existentes. Essa organização permite compartilhar informações sobre o arquivo sem exigir uma estrutura global independente para cada abertura.

**Configuração:** Execução da carga servidor_web, com alocação contígua e bloqueio consultivo. Serão observados os valores máximos da tabela global, das tabelas por processo, da soma dessas tabelas e do contador de aberturas.

**Resultados:** | Indicador | Valor máximo |
|---|---:|
| Entradas na tabela global | 12 |
| Entradas na tabela de um processo | 3 |
| Soma das entradas das tabelas dos processos | 24 |
| Contador de aberturas | 6 |

Foram realizadas 6.279 operações, sem erros, com 17.824 acessos e tempo médio de 1,4897 ms por operação.

**Evidências:** `resultados/arquivos.csv` (X5); `resultados/arquivos_por_operacao.csv` (X5); `graficos/X5_tabelas.png`.

**Análise:** A soma máxima de entradas por processo (24) foi superior ao máximo de entradas globais (12), consistente com descritores distintos compartilhando estruturas globais. O contador máximo de seis aberturas reforça a ocorrência de referências simultâneas a arquivos. Como os valores são máximos coletados ao longo da simulação, não se deve presumir que todos ocorreram exatamente no mesmo instante.

**Veredito:** CONFIRMADA

### X6 — Cache de blocos (M1)

**Hipótese:** Espera-se que a utilização de cache reduza o tempo de atendimento das requisições em comparação com a execução sem cache, principalmente quando houver reutilização de blocos. A política LRU deverá apresentar desempenho igual ou superior ao FIFO em cargas com localidade temporal. Capacidades maiores deverão favorecer a taxa de acertos, embora os ganhos possam diminuir após determinado tamanho. A estratégia write-back deverá reduzir o número de escritas físicas em determinadas situações, mas poderá provocar perda de dados ainda não sincronizados durante uma queda de energia.

**Fundamentação:** A cache mantém blocos recentemente utilizados na memória, permitindo atender determinados acessos sem consultar o disco. A política LRU remove o bloco menos recentemente utilizado, enquanto a FIFO remove o bloco armazenado há mais tempo. No write-through, as escritas são encaminhadas imediatamente ao dispositivo. No write-back, os blocos modificados permanecem temporariamente na memória e são gravados posteriormente. O simulador considera um custo de 0,001 ms por acerto na cache e um intervalo de sincronização de 5.000 ms.

**Configuração:** Utilização da carga reuso, com escalonador FCFS, HDD e interrupções. Serão comparadas as políticas LRU e FIFO, capacidades de 64, 128, 256, 512, 1.024 e 2.048 blocos e estratégias write-through e write-back. O experimento também inclui uma execução sem cache e uma queda de energia no instante correspondente à chegada da requisição central da carga, totalizando 25 simulações. Serão analisados a taxa de acertos, o tempo de atendimento, as escritas físicas e os blocos perdidos na queda.

**Resultados:** | Configuração | Acertos (%) | Resposta média (ms) | Escritas físicas | Perdidos na queda |
|---|---:|---:|---:|---:|
| Sem cache | — | 3.499,9548 | 1.045 | 0 |
| LRU 64 / write-through | 39,6419 | 74,6575 | 1.045 | 0 |
| FIFO 64 / write-through | 31,3043 | 436,1072 | 1.045 | 0 |
| LRU 1.024 / write-through | 67,0588 | 16,8856 | 1.045 | 0 |
| FIFO 1.024 / write-through | 67,0588 | 16,8856 | 1.045 | 0 |
| LRU 1.024 / write-back | 67,0077 | 38,9341 | 541 | 55 |
| FIFO 1.024 / write-back | 67,0077 | 39,7302 | 541 | 55 |

Com 2.048 blocos, as métricas de acerto e resposta foram iguais às de 1.024 blocos nas respectivas políticas e modos de escrita. A queda foi configurada em 11.733,221 ms.

**Evidências:** `resultados/es.csv` (X6); `graficos/X6_acerto.png` e `graficos/X6_escrita.png`.

**Análise:** O cache reduziu muito a resposta média frente à execução sem cache. Em capacidades pequenas, o LRU obteve mais acertos que o FIFO; a vantagem desapareceu em 1.024 blocos, quando ambos alcançaram o mesmo patamar. O write-back reduziu escritas físicas de 1.045 para 541 na capacidade 1.024, mas registrou 55 blocos perdidos na queda, contra zero no write-through. O write-back não foi sempre mais rápido: em 1.024 blocos, a resposta média foi maior que no write-through. Isso mostra que menos escritas físicas não garante menor latência de resposta em todas as condições da simulação.

**Veredito:** CONFIRMADA

## 4. Relação com sistemas reais

Os experimentos ilustram princípios presentes em sistemas reais, embora não reproduzam integralmente suas implementações. No Linux, a camada de blocos utiliza escalonadores como `mq-deadline`, `BFQ` e `none`, com decisões influenciadas por latência, justiça e tipo de dispositivo; o X1 representa apenas estratégias didáticas de movimentação de cabeçote. Os modos de espera ativa e interrupção de X2 refletem o compromisso entre ocupação de CPU e custo de notificação, importante sobretudo em dispositivos rápidos. Linux, Windows e macOS mantêm estruturas para descritores e objetos de arquivos abertos, distinguindo referências por processo de estruturas compartilhadas; X5 abstrai esse princípio. A resolução de nomes em sistemas reais usa mecanismos de cache de diretórios e metadados, ausentes da comparação simplificada de X4. O cache de blocos do X6 se relaciona ao cache de páginas e às políticas de escrita diferida de sistemas operacionais, nas quais sincronização e durabilidade exigem mecanismos adicionais. Sistemas como ext4, NTFS e APFS têm recursos de journaling, cópia na escrita ou outros mecanismos de recuperação que não são modelados aqui.

## 5. Limitações do simulador

O disco HDD usa tempos fixos de busca, rotação e transferência; não modela filas de controladoras reais, caches de hardware, variação mecânica nem interferência de processos. O dispositivo rápido de X2 abstrai um dispositivo sem partes móveis e não equivale a um SSD completo. O simulador trata `seek` como operação sem acesso ou tempo, o que altera médias agregadas no X3. A profundidade em X4 não considera caches reais de nomes e metadados. O X5 informa máximos de tabelas, não uma fotografia simultânea de todas elas. O cache de X6 utiliza políticas e sincronização simplificadas, e a queda simulada não substitui testes reais de persistência e recuperação. Os experimentos são determinísticos nas cargas fornecidas e não permitem generalizar os números para hardware real.

## 6. Conclusões

1. O SSTF reduziu a resposta média em todas as cargas de X1, mas o SCAN não superou o FCFS na carga concentrada; eficiência depende do padrão de acesso.
2. Interrupções economizaram CPU no HDD, mas tiveram custo proporcionalmente maior que polling no dispositivo rápido.
3. Leituras diretas do banco de dados foram mais lentas que as sequenciais do compilador, apesar de a média global de operações não refletir essa diferença.
4. Cada nível adicional de diretório acrescentou um acesso médio ao `open`, conforme o modelo.
5. As tabelas de arquivos abertos permitiram mais descritores por processo do que entradas globais distintas.
6. O cache reduziu latências; LRU foi vantajoso em capacidades pequenas e write-back diminuiu escritas físicas ao custo de perda de blocos na queda simulada.

## 7. Referências

- SILBERSCHATZ, A.; GALVIN, P. B.; GAGNE, G. *Operating System Concepts*. 9. ed. Wiley, 2013.
- Documentação e código fornecidos pelo professor: `experimentos.py`, `simes/parametros.py` e demais arquivos do projeto SimES.
- Resultados experimentais do grupo: `resultados/es.csv`, `resultados/arquivos.csv` e `resultados/arquivos_por_operacao.csv`.

## 8. Declaração de autoria e uso de IA

## 8. Declaração de autoria e uso de IA

**Quem fez o quê:**

**Júlia Bettiol de Oliveira:** Responsável pelo desenvolvimento dos algoritmos de escalonamento de disco (SSTF e SCAN), implementação dos mecanismos de polling e interrupções e desenvolvimento do módulo M1 (cache de blocos com políticas LRU e FIFO). Também participou da execução dos testes automatizados, identificação e correção de erros e validação das funcionalidades.

**Thomaz Szeckir:** Responsável pela implementação das funcionalidades do sistema de arquivos, incluindo resolução de caminhos, gerenciamento das tabelas de arquivos abertos e operações de leitura, escrita e exclusão de arquivos. Também participou da execução dos experimentos, geração dos gráficos, organização dos resultados e análise das métricas obtidas.

**Atividades realizadas em conjunto:** Planejamento das soluções, integração dos componentes, revisão do código, análise dos resultados experimentais, elaboração do relatório técnico e conferência dos requisitos de entrega.

**Uso de ferramentas de IA:**

| Ferramenta | Finalidade | Onde foi usada (arquivos ou seções) |
|---|---|---|
| ChatGPT | Apoio na identificação e correção de erros, esclarecimento de dúvidas técnicas, sugestões de melhorias na implementação, interpretação dos resultados dos testes e auxílio na organização e revisão da documentação. | Desenvolvimento e depuração dos módulos N2, N3 e M1; análise dos experimentos X1–X6; elaboração e revisão do `RELATORIO.md`. |

As ferramentas de inteligência artificial foram utilizadas como recurso de apoio ao desenvolvimento, principalmente para esclarecimento de dúvidas, identificação de possíveis erros e sugestões de melhorias. A dupla ficou responsável pela execução dos testes, análise dos resultados e validação do funcionamento do simulador.