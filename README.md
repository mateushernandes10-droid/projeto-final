# Projeto Final - Base de Extracao

Grupo: Mateus H e Marlon

Jogo top-down feito em Python com Arcade 3.3.3. O jogador controla um tanque azul dentro de uma base de guerra, coleta 4 engrenagens e depois precisa chegar ate a area de extracao.

## Como executar

Opcao mais simples no PowerShell:

```powershell
.\executar.ps1
```

Esse script cria uma `.venv` dentro da propria pasta, instala o Arcade pelo `requirements.txt` e inicia o jogo.

Opcao manual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Se estiver usando a `.venv` da pasta anterior:

```powershell
..\.venv\Scripts\python.exe main.py
```

## Controles

- WASD ou setas: mover
- Mouse esquerdo: atirar na direcao do mouse
- Espaco: atirar no inimigo mais proximo
- R: reiniciar
- ESC: voltar ao menu

## Objetivo

1. Coletar as 4 engrenagens espalhadas pelo mapa.
2. Depois que todas forem coletadas, ir ate a area de extracao.
3. O jogador vence ao entrar na extracao com as 4 pecas.
4. O jogador perde se a vida chegar a zero.

## Tecnicas de IA implementadas

### 1. Campo de Visao + Raycasting

Os guardas vermelhos patrulham e possuem um cone de visao. Eles so detectam o jogador se ele estiver dentro do cone e se nao existir parede no caminho. A linha de visao e testada por amostragem entre o guarda e o jogador.

### 2. A* Pathfinding

O cacador escuro usa A* para perseguir o jogador pelo mapa. Ele converte a posicao do jogador e do inimigo para celulas da matriz, calcula o caminho e desenha os pontos do trajeto encontrado.

### 3. Utility AI

O comandante calcula pontuacoes para quatro acoes: atacar, buscar vida, fugir e patrulhar. A maior pontuacao define o comportamento atual. Essa decisao aparece no comportamento do boss, enquanto o HUD mostra apenas informacoes importantes para o jogador.

## HUD e resultado

O HUD mostra:

- vida do jogador;
- quantidade de pecas coletadas;
- pontuacao por eliminar inimigos;
- tempo da tentativa;
- missao atual.

A tela final mostra pontuacao, tempo e melhor resultado da sessao.

## Perigos do cenario

- Bombas explodem ao encostar e causam dano em area no jogador e nos inimigos.
- Espinhos causam dano ao encostar, com intervalo entre danos.
- Muros, caixas, rochas, bombas e espinhos possuem contorno para melhorar a leitura visual.

## Mapa e camera

O mapa e maior que a janela. A fase tem 42 colunas por 28 linhas, cada tile com 64 pixels. A camera segue o jogador usando `arcade.Camera2D`.

O mapa e criado por uma matriz de caracteres:

- `R`: rua
- `M`: muro
- `C`: caixa
- `B`: rocha/barreira
- `P`: jogador
- `H`: kit de vida
- `1`, `2`, `3`, `4`: engrenagens
- `V`: guarda com campo de visao
- `A`: cacador com A*
- `U`: comandante com Utility AI
- `E`: extracao

## Assets utilizados

As imagens usadas no jogo estao dentro da pasta `assets`, entao elas vao junto quando o projeto for compactado em `.zip`.

Essas imagens foram copiadas dos recursos padrao da biblioteca Arcade:

- tanques completos: `images/topdown_tanks`
- ruas, grama e areia: `images/topdown_tanks`
- caixas, muros, rochas, bombas e espinhos: `images/tiles`
- vida: `images/items/gemGreen.png`
- engrenagem: `onscreen_controls/shaded_dark/gear.png`
- bandeira de extracao: `images/items/flagGreen2.png`

## O que enviar

Envie a pasta `projeto final` inteira em `.zip`.

Ela contem:

- codigo-fonte;
- assets usados pelo jogo;
- roteiro de apresentacao;
- README;
- requirements;
- script de execucao.

Nao e necessario enviar uma `.venv` pronta. Ela pode ser criada pelo `executar.ps1` ou pelos comandos manuais acima.
