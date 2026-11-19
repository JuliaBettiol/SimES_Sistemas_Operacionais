# Relatório — SimES: simulador de E/S e de sistema de arquivos

**Integrantes:** Júlia Bettiol de Oliveira; Thomaz Szeckir

**Repositório:** https://github.com/JuliaBettiol/SimES_Sistemas_Operacionais

<!--
INSTRUÇÕES DO MODELO (apaguem este bloco antes de entregar)
- Este relatório é a entrega: exportem-no para PDF e CADA integrante envia o PDF no Moodle.
- Nomes completos de todos os integrantes e o link do repositório público são obrigatórios
  (linhas acima). Não coloquem matrícula, e-mail, telefone ou outro dado pessoal.
- Mantenham EXATAMENTE os títulos numerados (## 0. ... ## 8.) e os campos em negrito.
- Na seção 3, mantenham X1 a X5 e só as seções dos experimentos do escopo do grupo
  (M1 = X6, M2 = X7, M3 = X8, M4 = X9, M5 = X10, M6 = X11, integração = X12, bônus = X13).
  Apaguem as seções dos experimentos que o grupo não fez.
- Substituam todo texto entre colchetes [ ... ] pelo conteúdo do grupo.
- O campo **Veredito:** aceita só: CONFIRMADA, PARCIALMENTE CONFIRMADA ou REFUTADA.
- Em **Evidências:**, citem arquivos que existam no repositório (resultados/..., graficos/...).
- Antes de entregar, rodem:  python3 ferramentas/validar_entrega.py
-->

## 0. Resumo

[Até 10 linhas: o que o grupo implementou, quais módulos escolheu e os 3 resultados mais importantes.]

## 1. Escopo realizado

| Parte | Situação | Observação |
|---|---|---|
| N1 · Dispositivo (fornecido) | usado | — |
| N2 · Subsistema de E/S (SSTF, SCAN, polling, interrupção) | [completo / parcial] | [ ] |
| N3 · Sistema de arquivos | [completo / parcial] | [ ] |
| N4 · Experimentos X1–X5 e relatório | [completo / parcial] | [ ] |
| [M? · nome do módulo] | [completo / parcial] | [ ] |
| [Integração (grupos de 4)] | [completo / parcial] | [ ] |
| [Bônus flash] | [completo / parcial / não feito] | [ ] |

Resultado dos testes automáticos (`python3 executar.py testes`): [cole a última linha, ex.: "Ran 26 tests ... OK (skipped=6)"]

## 2. Implementação

### N2 — Subsistema de E/S

**Onde:** [arquivos e funções]

**Decisões:** [como implementaram SSTF, SCAN, polling e interrupção; casos especiais]

**Dificuldades:** [o que deu trabalho e como resolveram]

### N3 — Sistema de arquivos

**Onde:** [arquivos e funções]

**Decisões:** [resolução de caminhos, tabelas de arquivos abertos, leitura e escrita, unlink com arquivo aberto]

**Dificuldades:** [ ]

### [M? — nome do módulo]

**Onde:** [ ]

**Decisões:** [ ]

**Dificuldades:** [ ]

## 3. Experimentos

### X1 — Escalonadores sob quatro padrões de carga

**Hipótese:** Espera-se que os algoritmos SSTF e SCAN apresentem menor deslocamento total da cabeça de leitura e menor tempo médio de resposta do que o FCFS, principalmente em cargas aleatórias e concentradas. Em cargas sequenciais, a diferença entre os algoritmos deverá ser menor.

**Fundamentação:** O FCFS atende às requisições na ordem de chegada, sem considerar sua localização física no disco. O SSTF prioriza a requisição mais próxima da posição atual da cabeça, enquanto o SCAN organiza o atendimento conforme a direção de movimentação do braço. Como o tempo de busca depende da distância percorrida entre cilindros, a redução dos deslocamentos tende a diminuir o tempo total de atendimento. Entretanto, o SSTF pode provocar esperas prolongadas para determinadas requisições.

**Configuração:** Comparação dos escalonadores FCFS, SSTF e SCAN em um disco HDD, utilizando interrupções e quatro padrões de carga: sequencial, aleatória, concentrada e rajadas. Serão realizadas 12 simulações, considerando os indicadores de deslocamento total, tempo de resposta, espera máxima e vazão.

**Resultados:** [tabela com os números principais e referência aos gráficos]

**Evidências:** [resultados/es.csv (experimento=X1); graficos/X1_resposta_media_ms.png]

**Análise:** [explicação dos resultados, inclusive o que contrariou a hipótese]

**Veredito:** [CONFIRMADA | PARCIALMENTE CONFIRMADA | REFUTADA]

### X2 — Polling × interrupção conforme o dispositivo

**Hipótese:** Espera-se que o mecanismo de interrupções apresente menor utilização da CPU com operações de entrada e saída do que o polling, especialmente no disco HDD. No dispositivo rápido, a diferença deverá diminuir devido ao menor tempo de atendimento das requisições.

**Fundamentação:** No polling, a CPU verifica repetidamente se o dispositivo concluiu a operação, consumindo processamento durante a espera. Com interrupções, a CPU pode executar outras atividades e somente precisa tratar a conclusão quando o dispositivo sinaliza o término. O modelo considera um custo de 0,015 ms para o tratamento de cada interrupção, enquanto o dispositivo rápido elimina os custos de busca e latência rotacional.

**Configuração:** Comparação entre polling e interrupções, utilizando o escalonador FCFS, dois dispositivos (HDD e rápido) e duas cargas (aleatória e sequencial). Serão realizadas oito simulações, com foco no percentual de CPU dedicado à entrada e saída e nos tempos de atendimento.

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X3 — Acesso sequencial × direto

**Hipótese:** Espera-se que a carga de acesso sequencial, representada pelo compilador, apresente menor custo médio por operação de leitura do que a carga de acesso direto, representada pelo banco de dados.

**Fundamentação:** O acesso sequencial tende a aproveitar a continuidade dos blocos e a posição corrente do arquivo, reduzindo a necessidade de reposicionamentos. O acesso direto utiliza operações de posicionamento para alcançar regiões específicas, podendo aumentar a quantidade de blocos distintos acessados. Entretanto, como o simulador também contabiliza a resolução de caminhos e as atualizações de diretórios, o custo total dependerá da combinação de operações presente em cada carga.

**Configuração:** Execução das cargas de sistema de arquivos denominadas compilador e banco_dados, utilizando alocação contígua e bloqueio consultivo. Serão comparados o número de operações, os acessos ao disco, o tempo médio por operação e os custos por tipo de operação.

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X4 — Custo de resolver caminhos conforme a profundidade

**Hipótese:** Espera-se que o custo de resolução de caminhos aumente conforme a profundidade da estrutura de diretórios, aproximadamente de forma linear em relação ao número de diretórios percorridos.

**Fundamentação:** Para localizar um arquivo, o sistema precisa percorrer os componentes do caminho e consultar os diretórios intermediários. Na implementação do núcleo, a resolução de caminhos contabiliza leituras dos diretórios visitados. Assim, caminhos mais profundos tendem a exigir mais acessos e maior tempo de processamento.

**Configuração:** Execução de dez cargas geradas pela função fs_profundidade, com profundidades de 1 a 10 diretórios. Todas utilizarão alocação contígua e bloqueio consultivo. Serão observados os acessos médios por operação e o tempo médio de execução.

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X5 — Tabelas de arquivos abertos com vários processos

**Hipótese:** Espera-se que a execução da carga de servidor web demonstre o compartilhamento de entradas na tabela global de arquivos abertos, permitindo que diferentes processos mantenham descritores próprios associados a um mesmo arquivo. Assim, o número de entradas nas tabelas por processo poderá superar o número de entradas distintas na tabela global.

**Fundamentação:** O sistema de arquivos utiliza uma tabela global para representar arquivos abertos e tabelas individuais para armazenar os descritores de cada processo. Quando vários processos abrem o mesmo arquivo, suas entradas individuais podem referenciar uma única entrada global, cujo contador registra as aberturas existentes. Essa organização permite compartilhar informações sobre o arquivo sem exigir uma estrutura global independente para cada abertura.

**Configuração:** Execução da carga servidor_web, com alocação contígua e bloqueio consultivo. Serão observados os valores máximos da tabela global, das tabelas por processo, da soma dessas tabelas e do contador de aberturas.

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X6 — Cache de blocos (M1)

**Hipótese:** Espera-se que a utilização de cache reduza o tempo de atendimento das requisições em comparação com a execução sem cache, principalmente quando houver reutilização de blocos. A política LRU deverá apresentar desempenho igual ou superior ao FIFO em cargas com localidade temporal. Capacidades maiores deverão favorecer a taxa de acertos, embora os ganhos possam diminuir após determinado tamanho. A estratégia write-back deverá reduzir o número de escritas físicas em determinadas situações, mas poderá provocar perda de dados ainda não sincronizados durante uma queda de energia.

**Fundamentação:** A cache mantém blocos recentemente utilizados na memória, permitindo atender determinados acessos sem consultar o disco. A política LRU remove o bloco menos recentemente utilizado, enquanto a FIFO remove o bloco armazenado há mais tempo. No write-through, as escritas são encaminhadas imediatamente ao dispositivo. No write-back, os blocos modificados permanecem temporariamente na memória e são gravados posteriormente. O simulador considera um custo de 0,001 ms por acerto na cache e um intervalo de sincronização de 5.000 ms.

**Configuração:** Utilização da carga reuso, com escalonador FCFS, HDD e interrupções. Serão comparadas as políticas LRU e FIFO, capacidades de 64, 128, 256, 512, 1.024 e 2.048 blocos e estratégias write-through e write-back. O experimento também inclui uma execução sem cache e uma queda de energia no instante correspondente à chegada da requisição central da carga, totalizando 25 simulações. Serão analisados a taxa de acertos, o tempo de atendimento, as escritas físicas e os blocos perdidos na queda.

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X7 — Escalonadores avançados e inanição (M2)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X8 — DMA e buffering (M3)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X9 — Links e compartilhamento (M4)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X10 — Proteção e travas (M5)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X11 — Métodos de alocação (M6)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X12 — Integração ponta a ponta

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

### X13 — Armazenamento flash (bônus)

**Hipótese:** [ ]

**Fundamentação:** [ ]

**Configuração:** [ ]

**Resultados:** [ ]

**Evidências:** [ ]

**Análise:** [ ]

**Veredito:** [ ]

## 4. Relação com sistemas reais

[Para cada tema do escopo, relacionem o que o simulador mostrou com o que Windows, Linux e
macOS fazem de fato. Exemplos: escalonadores de E/S do Linux (mq-deadline, BFQ, none); cache
de páginas e gravação periódica; cache de diretórios (dentry cache); FAT/exFAT nos pendrives;
estruturas do ext4, do NTFS e do APFS; travas mandatórias do Windows × consultivas do Linux.]

## 5. Limitações do simulador

[O que o modelo simplifica e como isso pode ter afetado as conclusões.]

## 6. Conclusões

[3 a 6 conclusões objetivas.]

## 7. Referências

- SILBERSCHATZ, A.; GALVIN, P. B.; GAGNE, G. *Operating System Concepts*. 9. ed. Wiley, 2013.
- [Outras fontes consultadas, com link]

## 8. Declaração de autoria e uso de IA

**Quem fez o quê:** [divisão do trabalho entre os integrantes]

**Uso de ferramentas de IA:**

| Ferramenta | Finalidade | Onde foi usada (arquivos ou seções) |
|---|---|---|
| [ex.: nenhuma] | [ ] | [ ] |
