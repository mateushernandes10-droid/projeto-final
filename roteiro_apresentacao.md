# Roteiro de apresentacao

Tempo sugerido: 8 a 12 minutos.

## 1. Ideia geral

O jogo se chama Base de Extracao. O jogador controla um tanque azul em uma base de guerra vista de cima. A fase e maior que a tela, entao a camera acompanha o jogador. O objetivo e coletar 4 engrenagens e chegar ate a extracao.

## 2. Estrutura pedida no trabalho

- O jogo usa Python e Arcade 3.3.3.
- O genero e top-down.
- Existe tela inicial, tela de jogo e tela final com `arcade.View`.
- O mapa e maior que a janela e usa scroll de camera.
- O mapa e construido por matriz e convertido em tiles.
- Existem colisoes com muros, caixas e rochas.
- Ha condicao de vitoria e derrota.
- O HUD mostra vida, pecas coletadas, missao, pontuacao e tempo.

## 3. Como o mapa funciona

A funcao `criar_matriz_mapa` monta uma matriz de caracteres. Cada caractere representa um elemento:

- `R` vira rua;
- `M` vira muro com colisao;
- `C` vira caixa com colisao;
- `B` vira rocha/barreira com colisao;
- `H` vira kit de reparo/vida;
- `1`, `2`, `3`, `4` viram engrenagens;
- `V`, `A`, `U` viram inimigos diferentes;
- `E` vira area de extracao.

Depois a funcao `montar_tilemap` percorre essa matriz e cria os sprites correspondentes.

## 4. IA 1 - Campo de Visao + Raycasting

Os guardas vermelhos patrulham pontos fixos. Eles possuem um cone de visao desenhado no mapa.

O guarda detecta o jogador apenas se tres condicoes forem verdadeiras:

1. o jogador esta dentro da distancia maxima;
2. o jogador esta dentro do angulo do cone;
3. nao existe muro, caixa ou rocha bloqueando a linha entre guarda e jogador.

A terceira condicao e a parte de raycasting/linha de visao. O codigo amostra pontos entre o guarda e o jogador e verifica se alguma celula da matriz e bloqueada.

## 5. IA 2 - A*

O cacador escuro usa A* para perseguir o jogador. Ele transforma a posicao do jogador e do inimigo em celulas da matriz, calcula o caminho ate o alvo e segue o proximo ponto.

Para apresentar visualmente, aperte `E` durante o jogo. Com o debug ligado, aparecem os cones de visao dos guardas, o caminho do A* com pontos/linhas azuis e o alvo atual do comandante. Isso ajuda a demonstrar que os inimigos nao estao atravessando obstaculos; eles estao tomando decisoes de IA.

## 6. IA 3 - Utility AI

O comandante calcula pontuacoes para quatro acoes:

- atacar;
- buscar vida;
- fugir;
- patrulhar.

Cada acao recebe uma nota de 0 a 1. A maior nota vence e define o comportamento atual. No jogo final, essa decisao aparece pelo comportamento do comandante, enquanto o HUD fica focado nas informacoes do jogador.

Exemplo de explicacao:

> Se o jogador esta perto e o comandante tem vida, atacar fica mais forte. Se o comandante esta com pouca vida e existe kit perto, buscar vida pode vencer.

Quando ele escolhe buscar reparo ou fugir, o movimento usa A*. Assim o boss nao tenta andar em linha reta contra paredes; ele calcula um caminho pelas celulas livres.

## 7. Kits de reparo compartilhados

Os kits com icone de chave de boca podem ser usados pelo jogador e pelos inimigos. Como todos sao tanques, a recuperacao de vida representa um reparo. Se alguem encosta no kit com vida abaixo do maximo, recupera vida e o kit entra em respawn.

## 8. Level Design

As 4 engrenagens foram distribuidas em zonas diferentes:

1. primeira peca perto do inicio, para ensinar o objetivo;
2. segunda peca na area central, com obstaculos e cacador A*;
3. terceira peca em uma area vigiada por guarda com campo de visao;
4. quarta peca perto do comandante com Utility AI.

Assim a fase tem progressao: o jogador aprende, explora, enfrenta IA mais clara e depois busca a extracao.

## 9. Game Feel

O projeto usa movimento continuo com `delta_time`, tiros rapidos, particulas quando existe dano/coleta, objetos de guerra com contorno, bombas que explodem ao toque, espinhos que causam dano, pontuacao por inimigos eliminados, temporizador e HUD com feedback direto. A camera acompanha o jogador para reforcar a sensacao de mapa grande.
