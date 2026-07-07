# Roteiro de apresentacao - Projeto Final

Tempo sugerido: 8 a 12 minutos.

Grupo: Mateus H e Robson

## 1. Abertura

Fala sugerida:

> O nosso projeto e um jogo top-down feito em Python com a biblioteca Arcade. O jogador controla um tanque azul em uma base de guerra, precisa coletar 4 engrenagens espalhadas pelo mapa e depois chegar ate a area de extracao. No caminho existem inimigos com tecnicas diferentes de inteligencia artificial, itens de reparo, bombas, espinhos e obstaculos.

Pontos para mostrar:

- Tela inicial com a imagem de combate.
- Legenda dos itens: engrenagem, ferramenta, bomba e espinho.
- Controles principais: WASD, mouse, R, ESC e E para debug.

## 2. Objetivo do jogo

Fala sugerida:

> O objetivo principal e coletar todas as engrenagens e ir ate a extracao. O jogador perde se a vida chegar a zero. Alem disso, existe pontuacao por eliminar inimigos e um temporizador, entao da para comparar o desempenho das tentativas.

Durante a demonstracao:

- Mostre uma engrenagem no mapa.
- Mostre o HUD com vida, pecas, pontos, tempo e missao.
- Explique que a ferramenta repara o tanque.
- Explique que bomba e espinho causam dano tanto no jogador quanto nos inimigos.

## 3. Como o jogo foi montado

Fala sugerida:

> A fase foi montada usando uma matriz de caracteres. Cada caractere representa uma coisa do mapa. Depois o codigo percorre a matriz e cria os sprites correspondentes. Isso facilita explicar o mapa, porque uma letra pode virar rua, muro, caixa, rocha, item, inimigo ou ponto de extracao.

Principais letras da matriz:

- `R`: rua.
- `M`: muro com colisao.
- `C`: caixa com colisao.
- `B`: rocha/barreira com colisao.
- `H`: kit de reparo.
- `1`, `2`, `3`, `4`: pecas coletaveis.
- `V`: guarda com campo de visao.
- `A`: cacador com A*.
- `U`: comandante/boss com Utility AI.
- `E`: extracao.

Partes importantes do codigo:

- `criar_matriz_mapa`: monta a fase.
- `montar_tilemap`: transforma a matriz em sprites.
- `TelaMenu`, `TelaJogo` e `TelaFim`: organizam as telas com `arcade.View`.
- `Camera2D`: faz o mapa grande se movimentar com o jogador.
- `mover_com_colisao`: impede atravessar muros, caixas e rochas.

## 4. IA 1 - Campo de visao + Raycasting

Fala sugerida:

> A primeira tecnica de IA aparece nos guardas vermelhos. Eles patrulham pontos fixos e possuem um cone de visao. O jogador so e detectado se estiver dentro da distancia, dentro do angulo do cone e se nao existir obstaculo bloqueando a linha de visao.

Como explicar:

- Distancia: o jogador precisa estar perto o suficiente.
- Angulo: o jogador precisa estar na frente do tanque.
- Raycasting: o codigo testa pontos entre o guarda e o jogador para ver se existe parede, caixa ou rocha no caminho.

Na demonstracao:

- Aperte `E` para ligar o debug.
- Mostre o cone de visao.
- Fique atras de uma parede e explique que a parede bloqueia a visao.
- Entre no cone sem obstaculo e mostre o guarda atirando.

## 5. IA 2 - A* Pathfinding

Fala sugerida:

> A segunda tecnica e o A*, usado pelo cacador. Ele nao anda simplesmente em linha reta ate o jogador. O mapa e convertido em celulas e o algoritmo calcula um caminho pelas celulas livres, desviando de paredes e obstaculos.

Como explicar o A*:

- O jogo transforma a posicao do inimigo e do jogador em celulas da matriz.
- O A* avalia caminhos possiveis.
- Ele usa uma soma entre custo ja percorrido e estimativa ate o destino.
- O resultado e uma lista de celulas que o inimigo deve seguir.

Formula simples para falar:

```text
prioridade = custo ate aqui + estimativa ate o destino
```

Na demonstracao:

- Aperte `E` para mostrar o caminho.
- Mostre as linhas/pontos azuis.
- Explique que o inimigo esta seguindo pontos do caminho, nao atravessando parede.

## 6. IA 3 - Utility AI

Fala sugerida:

> A terceira tecnica e a Utility AI, usada pelo comandante, que funciona como boss. Em vez de ter uma unica acao fixa, ele calcula pontuacoes para algumas opcoes e escolhe a que tem maior utilidade naquele momento.

Acoes avaliadas:

- Atacar.
- Buscar reparo.
- Fugir.
- Patrulhar.

Como explicar:

> Cada acao recebe uma nota de 0 a 1. Se o jogador esta perto e o boss tem vida, atacar fica mais util. Se o boss esta com pouca vida e existe ferramenta perto, buscar reparo pode ganhar. Se esta em desvantagem, fugir pode ter nota maior. Se nada urgente acontece, ele patrulha.

Importante:

- A decisao e feita por pontuacao.
- O comportamento muda conforme distancia, vida, vida do jogador, kit disponivel e linha de visao.
- Quando o boss escolhe buscar reparo ou fugir, ele tambem usa A* para nao ficar preso em paredes.

Na demonstracao:

- Mostre o boss patrulhando fora da base final.
- Diminua a vida dele atirando.
- Mostre que ele tenta buscar a ferramenta.
- Com debug ligado, mostre o alvo e o caminho verde.

## 7. Itens, perigos e sons

Fala sugerida:

> Alem das IAs, o jogo tem alguns elementos para deixar a fase mais completa. As engrenagens sao o objetivo, a ferramenta repara o tanque, as bombas explodem e os espinhos causam dano. Os sons ajudam o jogador a perceber tiro, reparo, explosao, coleta e dano.

Sons usados:

- `1918.mp3`: musica do menu e da tela final.
- `hit1.wav`: disparo.
- `fall3.wav`: espinhos e derrota dos inimigos.
- `explosion1.wav`: explosao.
- `coin3.wav`: coleta de engrenagem.
- `upgrade1.wav`: reparo.

## 8. Tela inicial, tela final e HUD

Fala sugerida:

> O jogo foi dividido em telas usando `arcade.View`. A tela inicial apresenta o jogo, controles e legenda dos itens. A tela de jogo concentra a partida. A tela final mostra se a missao foi concluida ou falhou, alem da pontuacao, tempo e melhor resultado da sessao.

Pontos para comentar:

- A mesma imagem e usada no menu e na tela final para manter identidade visual.
- O HUD mostra apenas informacoes importantes para o jogador.
- A tecla `E` liga e desliga o debug das IAs.

## 9. De onde tiramos as informacoes

Fala sugerida:

> As informacoes vieram principalmente dos materiais passados em aula e dos recursos da propria biblioteca Arcade. A proposta do trabalho final orientou que o projeto deveria continuar usando Arcade e aplicar mais de uma tecnica de IA. Os materiais da atividade anterior ajudaram com a estrutura basica do Arcade, como sprites, telas, colisao, camera e uso de assets.

Fontes usadas no projeto:

- `Referencias/Projeto2_Final.pdf`: documento da proposta do trabalho final.
- `Referencias/Atividade anterior/ApopstilaDG2D_v014_BETA.pdf`: material de apoio sobre desenvolvimento 2D e Arcade.
- `Referencias/Atividade anterior/SlidesArcade.pdf`: slides usados em aula.
- `Referencias/Atividade anterior/Semina769rios_Arcade_T2.pdf`: documento da atividade anterior.
- `Referencias/Atividade anterior/TutorialArcade_Co769digos.py`: exemplos de codigo em Arcade.
- Recursos padrao do Arcade: imagens de tanques, tiles, itens e sons copiados da pasta `arcade/resources/assets`.
- O codigo do trabalho anterior serviu como base de aprendizado para evoluir a ideia para uma fase maior com varias IAs.

Como falar isso sem parecer decorado:

> Primeiro usamos os materiais de aula para entender a estrutura do Arcade: janela, sprites, eventos, colisao e camera. Depois usamos a proposta do trabalho final para definir que precisava ser uma fase maior com varias tecnicas de IA. Por fim, usamos os recursos padrao do Arcade para os assets e implementamos no codigo as tecnicas de campo de visao, A* e Utility AI.

## 10. Ordem sugerida para demonstrar

1. Abrir a tela inicial e explicar objetivo/itens.
2. Comecar a partida e mostrar HUD/camera.
3. Coletar ou chegar perto da primeira peca.
4. Ligar debug com `E`.
5. Mostrar guarda com campo de visao.
6. Mostrar cacador usando A*.
7. Mostrar boss com Utility AI.
8. Mostrar reparo, bomba ou espinho.
9. Coletar as pecas e ir para extracao.
10. Mostrar tela final com pontuacao e tempo.

## 11. Possiveis perguntas do professor

Pergunta: Qual foi a diferenca entre o trabalho anterior e este?

Resposta sugerida:

> No trabalho anterior o foco era uma unica tecnica de IA. Neste projeto usamos varias tecnicas juntas em uma fase maior: campo de visao com raycasting, A* e Utility AI.

Pergunta: Por que usar matriz para montar o mapa?

Resposta sugerida:

> Porque a matriz deixa o mapa facil de controlar. A mesma informacao serve para desenhar o cenario, controlar colisao e calcular caminhos com A*.

Pergunta: O boss tambem usa A*?

Resposta sugerida:

> Sim. A decisao principal dele e Utility AI, mas quando a acao escolhida e buscar reparo ou fugir, ele usa A* para chegar ao destino sem ficar preso em obstaculos.

Pergunta: Para que serve a tecla `E`?

Resposta sugerida:

> Ela liga e desliga o modo debug. Esse modo mostra visualmente as IAs: cones de visao, caminhos calculados e alvo atual do boss.

Pergunta: Os assets foram feitos manualmente?

Resposta sugerida:

> A maioria dos sprites e sons foi copiada dos recursos padrao da biblioteca Arcade para dentro da pasta `assets`, para que o projeto possa ser entregue completo. A imagem do menu foi gerada para dar uma identidade visual ao jogo.
