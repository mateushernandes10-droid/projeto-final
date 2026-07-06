# Grupo: Mateus H e Robson
from __future__ import annotations

from dataclasses import dataclass
import heapq
import math
from pathlib import Path
import random
from typing import Optional

import arcade


# CONFIGURACOES GERAIS

LARGURA_TELA = 1180
ALTURA_TELA = 720
TITULO_TELA = "Projeto Final - Base de Extracao"

TAMANHO_TILE = 64
COLUNAS_MAPA = 42
LINHAS_MAPA = 28
LARGURA_MUNDO = COLUNAS_MAPA * TAMANHO_TILE
ALTURA_MUNDO = LINHAS_MAPA * TAMANHO_TILE

VIDA_MAXIMA = 100
CURA_KIT_VIDA = 35
RAIO_COLETA = 38
DANO_BOMBA = 34
DANO_ESPINHO = 10
RAIO_EXPLOSAO_BOMBA = 118
RECARGA_DANO_ESPINHO = 1.0

VELOCIDADE_JOGADOR = 280
VELOCIDADE_TIRO_JOGADOR = 660
DANO_TIRO_JOGADOR = 22
RECARGA_TIRO_JOGADOR = 0.28

VELOCIDADE_GUARDA = 118
VELOCIDADE_CACADOR = 152
VELOCIDADE_COMANDANTE = 132
VELOCIDADE_TIRO_INIMIGO = 430
DANO_TIRO_INIMIGO = 11
RECARGA_TIRO_INIMIGO = 0.95

DISTANCIA_VISAO = 390
ANGULO_CAMPO_VISAO = 78
ALCANCE_TIRO_INIMIGO = 330
DISTANCIA_ATIVAR_ASTAR = 850

TOTAL_PECAS = 4
MELHOR_PONTUACAO = 0
MELHOR_TEMPO: Optional[float] = None
DEBUG_IA_INICIAL = False


# Assets usados pelo jogo. Eles ficam dentro da pasta do projeto para facilitar a entrega em .zip.
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ASSETS = PASTA_PROJETO / "assets"


def caminho_asset(caminho: str) -> str:
    return str(PASTA_ASSETS / caminho)


TEXTURA_JOGADOR = caminho_asset("images/topdown_tanks/tank_blue.png")
TEXTURA_GUARDA = caminho_asset("images/topdown_tanks/tank_red.png")
TEXTURA_CACADOR = caminho_asset("images/topdown_tanks/tank_dark.png")
TEXTURA_COMANDANTE = caminho_asset("images/topdown_tanks/tank_sand.png")
TEXTURA_GRAMA_1 = caminho_asset("images/topdown_tanks/tileGrass1.png")
TEXTURA_GRAMA_2 = caminho_asset("images/topdown_tanks/tileGrass2.png")
TEXTURA_AREIA_1 = caminho_asset("images/topdown_tanks/tileSand1.png")
TEXTURA_AREIA_2 = caminho_asset("images/topdown_tanks/tileSand2.png")
TEXTURA_RUA_HORIZONTAL = caminho_asset("images/topdown_tanks/tileGrass_roadEast.png")
TEXTURA_RUA_VERTICAL = caminho_asset("images/topdown_tanks/tileGrass_roadNorth.png")
TEXTURA_RUA_CRUZAMENTO = caminho_asset("images/topdown_tanks/tileGrass_roadCrossing.png")
TEXTURA_MURO = caminho_asset("images/tiles/brickGrey.png")
TEXTURA_CAIXA = caminho_asset("images/tiles/boxCrate_double.png")
TEXTURA_ROCHA = caminho_asset("images/tiles/rock.png")
TEXTURA_BOMBA = caminho_asset("images/tiles/bomb.png")
TEXTURA_SPIKES = caminho_asset("images/tiles/spikes.png")
TEXTURA_VIDA = caminho_asset("onscreen_controls/shaded_dark/wrench.png")
TEXTURA_ENGRENAGEM = caminho_asset("onscreen_controls/shaded_dark/gear.png")
TEXTURA_SAIDA = caminho_asset("images/items/flagGreen2.png")
TEXTURA_MENU = caminho_asset("images/menu/tank_battle_menu.png")

COR_FUNDO = (12, 16, 24)
COR_HUD = (16, 22, 32)
COR_HUD_BORDA = (74, 89, 112)
BRANCO = (238, 242, 250)
CINZA = (154, 166, 188)
CINZA_ESCURO = (62, 76, 96)
COR_JOGADOR = (74, 151, 255)
COR_GUARDA = (239, 89, 79)
COR_CACADOR = (115, 126, 146)
COR_COMANDANTE = (255, 154, 74)
COR_VIDA = (74, 213, 126)
COR_PECA = (255, 218, 88)
COR_EXTRACAO_FECHADA = (142, 145, 154)
COR_EXTRACAO_ABERTA = (77, 224, 151)
COR_ALERTA = (255, 91, 91)
COR_ASTAR = (96, 214, 255)
COR_UTILIDADE = (187, 126, 255)
COR_EXPLOSAO = (255, 176, 64)


# FUNCOES AUXILIARES

def limitar(valor: float, minimo: float, maximo: float) -> float:
    """Mantem um valor dentro de um intervalo."""
    return max(minimo, min(maximo, valor))


def calcular_distancia(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)


def formatar_tempo(segundos: float) -> str:
    minutos = int(segundos // 60)
    segundos_restantes = int(segundos % 60)
    centesimos = int((segundos - int(segundos)) * 100)
    return f"{minutos:02d}:{segundos_restantes:02d}.{centesimos:02d}"


def normalizar(vetor_x: float, vetor_y: float) -> tuple[float, float]:
    tamanho = math.hypot(vetor_x, vetor_y)
    if tamanho == 0:
        return 0, 0
    return vetor_x / tamanho, vetor_y / tamanho


def angulo_do_vetor(vetor_x: float, vetor_y: float) -> float:
    """Converte uma direcao em angulo para sprites que originalmente apontam para baixo."""
    return math.degrees(math.atan2(-vetor_x, -vetor_y))


def retangulo_centralizado(x: float, y: float, largura: float, altura: float) -> arcade.Rect:
    return arcade.Rect(
        left=x - largura / 2,
        right=x + largura / 2,
        bottom=y - altura / 2,
        top=y + altura / 2,
        width=largura,
        height=altura,
        x=x,
        y=y,
    )


def vetor_do_sprite(sprite: arcade.Sprite) -> tuple[float, float]:
    """Recupera a direcao para onde o sprite esta apontando."""
    angulo = math.radians(sprite.angle)
    return -math.sin(angulo), -math.cos(angulo)


def criar_sprite_tile(textura: arcade.Texture, x: float, y: float) -> arcade.Sprite:
    escala = TAMANHO_TILE / textura.width
    sprite = arcade.Sprite(textura, scale=escala)
    sprite.center_x = x
    sprite.center_y = y
    return sprite


def criar_sprite_item(textura: arcade.Texture, x: float, y: float, tamanho: int) -> arcade.Sprite:
    escala = tamanho / textura.width
    sprite = arcade.Sprite(textura, scale=escala)
    sprite.center_x = x
    sprite.center_y = y
    return sprite


def desenhar_sprite_solto(sprite: arcade.Sprite) -> None:
    """Desenha um Sprite que nao esta dentro de uma SpriteList."""
    arcade.draw_texture_rect(
        texture=sprite.texture,
        rect=retangulo_centralizado(sprite.center_x, sprite.center_y, sprite.width, sprite.height),
        angle=sprite.angle,
    )


def criar_sprite_contorno(sprite: arcade.Sprite, dx: float, dy: float) -> arcade.Sprite:
    """Cria uma copia escura do sprite para ser usada como contorno em SpriteList."""
    contorno = arcade.Sprite()
    contorno.texture = sprite.texture
    contorno.center_x = sprite.center_x + dx
    contorno.center_y = sprite.center_y + dy
    contorno.width = sprite.width
    contorno.height = sprite.height
    contorno.angle = sprite.angle
    contorno.color = (12, 14, 18)
    contorno.alpha = 220
    return contorno


def manter_no_mundo(sprite: arcade.Sprite) -> None:
    """Mantem o sprite dentro da area interna, antes da borda de muros."""
    metade_largura = sprite.width * 0.38
    metade_altura = sprite.height * 0.40
    sprite.center_x = limitar(sprite.center_x, TAMANHO_TILE + metade_largura, LARGURA_MUNDO - TAMANHO_TILE - metade_largura)
    sprite.center_y = limitar(sprite.center_y, TAMANHO_TILE + metade_altura, ALTURA_MUNDO - TAMANHO_TILE - metade_altura)


def sprite_colide_com_mapa(sprite: arcade.Sprite, mapa: list[list[str]]) -> bool:
    """Verifica colisao usando a matriz do mapa, nao o formato visual do PNG."""
    metade_largura = sprite.width * 0.38
    metade_altura = sprite.height * 0.40

    esquerda = sprite.center_x - metade_largura + 1
    direita = sprite.center_x + metade_largura - 1
    baixo = sprite.center_y - metade_altura + 1
    cima = sprite.center_y + metade_altura - 1

    coluna_min = int(limitar(esquerda // TAMANHO_TILE, 0, COLUNAS_MAPA - 1))
    coluna_max = int(limitar(direita // TAMANHO_TILE, 0, COLUNAS_MAPA - 1))
    linha_min = LINHAS_MAPA - 1 - int(limitar(cima // TAMANHO_TILE, 0, LINHAS_MAPA - 1))
    linha_max = LINHAS_MAPA - 1 - int(limitar(baixo // TAMANHO_TILE, 0, LINHAS_MAPA - 1))

    for linha in range(linha_min, linha_max + 1):
        for coluna in range(coluna_min, coluna_max + 1):
            if celula_bloqueada(mapa, linha, coluna):
                return True
    return False


def mover_com_colisao(sprite: arcade.Sprite, dx: float, dy: float, mapa: list[list[str]]) -> None:
    """Move em pequenos passos, bloqueando muros, caixas e rochas da matriz."""
    passos = max(1, math.ceil(max(abs(dx), abs(dy)) / 8))
    passo_x = dx / passos
    passo_y = dy / passos

    for _ in range(passos):
        x_anterior = sprite.center_x
        sprite.center_x += passo_x
        manter_no_mundo(sprite)
        if sprite_colide_com_mapa(sprite, mapa):
            sprite.center_x = x_anterior

        y_anterior = sprite.center_y
        sprite.center_y += passo_y
        manter_no_mundo(sprite)
        if sprite_colide_com_mapa(sprite, mapa):
            sprite.center_y = y_anterior


def direcao_para_alvo(sprite: arcade.Sprite, alvo_x: float, alvo_y: float) -> tuple[float, float]:
    return normalizar(alvo_x - sprite.center_x, alvo_y - sprite.center_y)


def celula_para_posicao(linha: int, coluna: int) -> tuple[float, float]:
    x = coluna * TAMANHO_TILE + TAMANHO_TILE / 2
    y = ALTURA_MUNDO - (linha * TAMANHO_TILE + TAMANHO_TILE / 2)
    return x, y


def posicao_para_celula(x: float, y: float) -> tuple[int, int]:
    coluna = int(limitar(x // TAMANHO_TILE, 0, COLUNAS_MAPA - 1))
    linha_invertida = int(limitar(y // TAMANHO_TILE, 0, LINHAS_MAPA - 1))
    linha = LINHAS_MAPA - 1 - linha_invertida
    return linha, coluna


def celula_bloqueada(mapa: list[list[str]], linha: int, coluna: int) -> bool:
    if linha < 0 or linha >= LINHAS_MAPA or coluna < 0 or coluna >= COLUNAS_MAPA:
        return True
    return mapa[linha][coluna] in ("M", "C", "B")


def criar_matriz_mapa() -> list[list[str]]:
    """Cria a fase como matriz. Cada caractere vira tile, obstaculo ou entidade."""
    mapa = [["." for _ in range(COLUNAS_MAPA)] for _ in range(LINHAS_MAPA)]

    # Bordas do mapa.
    for linha in range(LINHAS_MAPA):
        mapa[linha][0] = "M"
        mapa[linha][COLUNAS_MAPA - 1] = "M"
    for coluna in range(COLUNAS_MAPA):
        mapa[0][coluna] = "M"
        mapa[LINHAS_MAPA - 1][coluna] = "M"

    # Ruas principais que guiam a leitura visual do mapa.
    for linha in (4, 12, 20, 25):
        for coluna in range(1, COLUNAS_MAPA - 1):
            mapa[linha][coluna] = "R"
    for coluna in (4, 15, 27, 37):
        for linha in range(1, LINHAS_MAPA - 1):
            mapa[linha][coluna] = "R"

    # Remove os pedacos de asfalto soltos atras do jogador no inicio da fase.
    for linha, coluna in (
        (24, 4),
        (25, 1),
        (25, 2),
        (25, 3),
        (25, 4),
        (25, 5),
    ):
        mapa[linha][coluna] = "."

    def colocar_parede(linha1: int, coluna1: int, linha2: int, coluna2: int) -> None:
        for linha in range(linha1, linha2 + 1):
            for coluna in range(coluna1, coluna2 + 1):
                mapa[linha][coluna] = "M"

    def colocar_caixa(linha: int, coluna: int) -> None:
        mapa[linha][coluna] = "C"

    def colocar_barreira(linha: int, coluna: int) -> None:
        mapa[linha][coluna] = "B"

    # Laboratorio superior esquerdo.
    colocar_parede(6, 7, 6, 14)
    colocar_parede(10, 7, 10, 14)
    colocar_parede(6, 7, 10, 7)
    colocar_parede(6, 14, 10, 14)
    for coluna in (9, 10, 11):
        mapa[10][coluna] = "."
    for coluna in (11, 12):
        mapa[6][coluna] = "."

    # Galpao central.
    colocar_parede(15, 18, 15, 26)
    colocar_parede(19, 18, 19, 26)
    colocar_parede(15, 18, 19, 18)
    colocar_parede(15, 26, 19, 26)
    for coluna in (21, 22, 23):
        mapa[19][coluna] = "."
        mapa[15][coluna] = "."
    for linha in (17, 18):
        mapa[linha][18] = "."
        mapa[linha][26] = "."

    # Base final.
    colocar_parede(3, 30, 3, 38)
    colocar_parede(8, 30, 8, 38)
    colocar_parede(3, 30, 8, 30)
    colocar_parede(3, 38, 8, 38)
    for linha in (4, 5):
        mapa[linha][38] = "R"
    for coluna in (33, 34, 35):
        mapa[8][coluna] = "."

    # Obstaculos soltos para forcar desvio e dar utilidade ao A*.
    for posicao in (
        (22, 8), (22, 9), (23, 12), (21, 13),
        (17, 6), (18, 6), (18, 9), (16, 12),
        (11, 20), (12, 21), (13, 21), (13, 25),
        (6, 21), (7, 21), (9, 24), (5, 25),
        (22, 31), (23, 32), (21, 34), (18, 35),
    ):
        colocar_caixa(*posicao)

    # Barreiras e rochas quebram linhas retas e tambem bloqueiam visao/caminho.
    for posicao in (
        (24, 18), (23, 20), (22, 22),
        (14, 12), (13, 14), (12, 16),
        (10, 29), (11, 31), (12, 33),
        (5, 20), (6, 23), (7, 26),
        (20, 32), (21, 36),
    ):
        colocar_barreira(*posicao)

    # Personagens, itens e objetivo.
    especiais = {
        (25, 2): "P",
        (23, 9): "1",
        (17, 22): "2",
        (8, 10): "3",
        (6, 34): "4",
        (4, 39): "E",
        (21, 5): "H",
        (13, 23): "H",
        (6, 31): "H",
        (24, 34): "H",
        (20, 11): "V",
        (12, 30): "V",
        (16, 20): "A",
        (9, 34): "U",
    }

    for (linha, coluna), caractere in especiais.items():
        mapa[linha][coluna] = caractere

    return mapa


def procurar_celulas(mapa: list[list[str]], alvo: str) -> list[tuple[int, int]]:
    celulas = []
    for linha in range(LINHAS_MAPA):
        for coluna in range(COLUNAS_MAPA):
            if mapa[linha][coluna] == alvo:
                celulas.append((linha, coluna))
    return celulas


def astar(mapa: list[list[str]], inicio: tuple[int, int], destino: tuple[int, int]) -> list[tuple[int, int]]:
    """Busca caminho em grid usando A*. Retorna uma lista de celulas."""
    if celula_bloqueada(mapa, destino[0], destino[1]):
        return []

    def heuristica(celula: tuple[int, int]) -> int:
        return abs(celula[0] - destino[0]) + abs(celula[1] - destino[1])

    contador = 0
    fronteira: list[tuple[int, int, tuple[int, int]]] = []
    heapq.heappush(fronteira, (0, contador, inicio))
    veio_de: dict[tuple[int, int], Optional[tuple[int, int]]] = {inicio: None}
    custo_ate: dict[tuple[int, int], int] = {inicio: 0}

    while fronteira:
        _, _, atual = heapq.heappop(fronteira)
        if atual == destino:
            break

        linha, coluna = atual
        for vizinho in ((linha - 1, coluna), (linha + 1, coluna), (linha, coluna - 1), (linha, coluna + 1)):
            if celula_bloqueada(mapa, vizinho[0], vizinho[1]):
                continue

            novo_custo = custo_ate[atual] + 1
            if vizinho not in custo_ate or novo_custo < custo_ate[vizinho]:
                custo_ate[vizinho] = novo_custo
                prioridade = novo_custo + heuristica(vizinho)
                contador += 1
                heapq.heappush(fronteira, (prioridade, contador, vizinho))
                veio_de[vizinho] = atual

    if destino not in veio_de:
        return []

    caminho = []
    atual: Optional[tuple[int, int]] = destino
    while atual is not None:
        caminho.append(atual)
        atual = veio_de[atual]
    caminho.reverse()
    return caminho


@dataclass
class PontuacaoUtilidade:
    nome: str
    valor: float
    cor: tuple[int, int, int]


class ParticulaFlutuante(arcade.Sprite):
    def __init__(self, x: float, y: float, cor: tuple[int, int, int], velocidade: float = 150) -> None:
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(
            diameter=random.randint(8, 14),
            color=(cor[0], cor[1], cor[2], 255),
            center_alpha=255,
            outer_alpha=0,
        )
        angulo = random.uniform(0, math.tau)
        self.center_x = x
        self.center_y = y
        self.change_x = math.cos(angulo) * random.uniform(velocidade * 0.25, velocidade)
        self.change_y = math.sin(angulo) * random.uniform(velocidade * 0.25, velocidade)
        self.tempo = random.uniform(0.30, 0.65)
        self.tempo_inicial = self.tempo

    def update(self, delta_time: float = 1 / 60) -> None:
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.change_x *= 0.90
        self.change_y *= 0.90
        self.tempo -= delta_time
        self.alpha = int(255 * limitar(self.tempo / self.tempo_inicial, 0, 1))
        if self.tempo <= 0:
            self.remove_from_sprite_lists()


class Tiro(arcade.Sprite):
    def __init__(
        self,
        x: float,
        y: float,
        alvo_x: float,
        alvo_y: float,
        velocidade: float,
        dano: float,
        cor: tuple[int, int, int],
        dono: str,
    ) -> None:
        super().__init__()
        direcao_x, direcao_y = normalizar(alvo_x - x, alvo_y - y)
        if direcao_x == 0 and direcao_y == 0:
            direcao_y = 1

        self.texture = arcade.make_soft_circle_texture(
            diameter=16,
            color=(cor[0], cor[1], cor[2], 255),
            center_alpha=255,
            outer_alpha=30,
        )
        self.center_x = x + direcao_x * 32
        self.center_y = y + direcao_y * 32
        self.change_x = direcao_x * velocidade
        self.change_y = direcao_y * velocidade
        self.angle = angulo_do_vetor(direcao_x, direcao_y)
        self.dano = dano
        self.dono = dono
        self.tempo_vida = 1.8

    def update(self, delta_time: float = 1 / 60) -> None:
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time
        self.tempo_vida -= delta_time
        fora = (
            self.center_x < -60
            or self.center_x > LARGURA_MUNDO + 60
            or self.center_y < -60
            or self.center_y > ALTURA_MUNDO + 60
        )
        if fora or self.tempo_vida <= 0:
            self.remove_from_sprite_lists()


class KitVida:
    def __init__(self, x: float, y: float, textura: arcade.Texture) -> None:
        self.x = x
        self.y = y
        self.sprite = criar_sprite_item(textura, x, y, 42)
        self.ativo = True
        self.tempo_respawn = 0.0
        self.pulso = random.uniform(0, math.tau)

    def atualizar(self, delta_time: float) -> None:
        self.pulso += delta_time * 4
        if not self.ativo:
            self.tempo_respawn -= delta_time
            if self.tempo_respawn <= 0:
                self.ativo = True

    def coletar(self) -> None:
        self.ativo = False
        self.tempo_respawn = 8.0

    def desenhar(self) -> None:
        if self.ativo:
            self.sprite.center_y = self.y + math.sin(self.pulso) * 2
            desenhar_sprite_solto(self.sprite)
        else:
            return


class Peca:
    def __init__(self, numero: int, x: float, y: float, textura: arcade.Texture) -> None:
        self.numero = numero
        self.x = x
        self.y = y
        self.sprite = criar_sprite_item(textura, x, y, 66)
        self.texto = arcade.Text(f"Peca {self.numero}", self.x, self.y - 52, BRANCO, 12, anchor_x="center")
        self.coletada = False
        self.pulso = random.uniform(0, math.tau)

    def atualizar(self, delta_time: float) -> None:
        self.pulso += delta_time * 3
        self.sprite.angle += 55 * delta_time
        self.sprite.center_y = self.y + math.sin(self.pulso) * 4

    def desenhar(self) -> None:
        if self.coletada:
            return
        raio = 35 + math.sin(self.pulso) * 4
        arcade.draw_circle_filled(self.x, self.y, raio, (163, 128, 37, 80))
        arcade.draw_circle_outline(self.x, self.y, raio, COR_PECA, 2)
        desenhar_sprite_solto(self.sprite)
        self.texto.draw()


class PerigoCenario:
    def __init__(self, tipo: str, sprite: arcade.Sprite) -> None:
        self.tipo = tipo
        self.sprite = sprite
        self.ativo = True
        self.recarga_jogador = 0.0
        self.recargas_inimigos: dict[int, float] = {}

    def atualizar(self, delta_time: float) -> None:
        self.recarga_jogador = max(0, self.recarga_jogador - delta_time)
        for chave in list(self.recargas_inimigos):
            self.recargas_inimigos[chave] = max(0, self.recargas_inimigos[chave] - delta_time)


class Jogador:
    def __init__(self, x: float, y: float) -> None:
        self.sprite = arcade.Sprite(TEXTURA_JOGADOR, scale=1.0)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = -90
        self.vida = VIDA_MAXIMA
        self.recarga_tiro = 0.0
        self.teclas = {
            arcade.key.W: False,
            arcade.key.A: False,
            arcade.key.S: False,
            arcade.key.D: False,
            arcade.key.UP: False,
            arcade.key.LEFT: False,
            arcade.key.DOWN: False,
            arcade.key.RIGHT: False,
        }

    def pressionar(self, tecla: int) -> None:
        if tecla in self.teclas:
            self.teclas[tecla] = True

    def soltar(self, tecla: int) -> None:
        if tecla in self.teclas:
            self.teclas[tecla] = False

    def atualizar(self, delta_time: float, mapa: list[list[str]]) -> None:
        movimento_x = 0
        movimento_y = 0
        if self.teclas[arcade.key.D] or self.teclas[arcade.key.RIGHT]:
            movimento_x += 1
        if self.teclas[arcade.key.A] or self.teclas[arcade.key.LEFT]:
            movimento_x -= 1
        if self.teclas[arcade.key.W] or self.teclas[arcade.key.UP]:
            movimento_y += 1
        if self.teclas[arcade.key.S] or self.teclas[arcade.key.DOWN]:
            movimento_y -= 1

        direcao_x, direcao_y = normalizar(movimento_x, movimento_y)
        if direcao_x != 0 or direcao_y != 0:
            self.sprite.angle = angulo_do_vetor(direcao_x, direcao_y)

        mover_com_colisao(
            self.sprite,
            direcao_x * VELOCIDADE_JOGADOR * delta_time,
            direcao_y * VELOCIDADE_JOGADOR * delta_time,
            mapa,
        )
        self.recarga_tiro = max(0, self.recarga_tiro - delta_time)

    def atirar(self, alvo_x: float, alvo_y: float) -> Optional[Tiro]:
        if self.recarga_tiro > 0:
            return None

        direcao_x, direcao_y = direcao_para_alvo(self.sprite, alvo_x, alvo_y)
        if direcao_x != 0 or direcao_y != 0:
            self.sprite.angle = angulo_do_vetor(direcao_x, direcao_y)

        self.recarga_tiro = RECARGA_TIRO_JOGADOR
        return Tiro(
            self.sprite.center_x,
            self.sprite.center_y,
            alvo_x,
            alvo_y,
            VELOCIDADE_TIRO_JOGADOR,
            DANO_TIRO_JOGADOR,
            COR_JOGADOR,
            "jogador",
        )


class InimigoBase:
    def __init__(self, textura: str, x: float, y: float, escala: float, vida: int, nome: str, cor: tuple[int, int, int], pontos: int) -> None:
        self.sprite = arcade.Sprite(textura, scale=escala)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = 0
        self.vida = vida
        self.vida_maxima = vida
        self.nome = nome
        self.cor = cor
        self.pontos = pontos
        self.ativo = True
        self.recarga_tiro = random.uniform(0.2, 0.8)
        self.estado_texto = "Patrulha"

    def atualizar(self, jogo: "TelaJogo", delta_time: float) -> list[Tiro]:
        return []

    def sofrer_dano(self, dano: float) -> bool:
        if not self.ativo:
            return False

        self.vida = limitar(self.vida - dano, 0, self.vida_maxima)
        if self.vida <= 0:
            self.ativo = False
            self.sprite.remove_from_sprite_lists()
            return True
        return False

    def mover_para(self, alvo_x: float, alvo_y: float, velocidade: float, delta_time: float, jogo: "TelaJogo") -> None:
        direcao_x, direcao_y = direcao_para_alvo(self.sprite, alvo_x, alvo_y)
        if direcao_x != 0 or direcao_y != 0:
            self.sprite.angle = angulo_do_vetor(direcao_x, direcao_y)
        mover_com_colisao(
            self.sprite,
            direcao_x * velocidade * delta_time,
            direcao_y * velocidade * delta_time,
            jogo.mapa,
        )

    def tentar_atirar(self, jogador: Jogador) -> Optional[Tiro]:
        if self.recarga_tiro > 0:
            return None
        self.recarga_tiro = RECARGA_TIRO_INIMIGO
        return Tiro(
            self.sprite.center_x,
            self.sprite.center_y,
            jogador.sprite.center_x,
            jogador.sprite.center_y,
            VELOCIDADE_TIRO_INIMIGO,
            DANO_TIRO_INIMIGO,
            self.cor,
            "inimigo",
        )

    def desenhar_barra_vida(self) -> None:
        largura = 52
        altura = 7
        proporcao = self.vida / self.vida_maxima
        x = self.sprite.center_x
        y = self.sprite.center_y + 42
        arcade.draw_lrbt_rectangle_filled(x - largura / 2, x + largura / 2, y, y + altura, (42, 48, 60))
        arcade.draw_lrbt_rectangle_filled(x - largura / 2, x - largura / 2 + largura * proporcao, y, y + altura, self.cor)


class GuardaCampoVisao(InimigoBase):
    """Guarda com Campo de Visao + Raycasting/Linha de Visao."""

    def __init__(self, x: float, y: float, pontos_patrulha: list[tuple[float, float]]) -> None:
        super().__init__(TEXTURA_GUARDA, x, y, 1.0, 75, "Guarda FOV", COR_GUARDA, 100)
        self.pontos_patrulha = pontos_patrulha
        self.indice_patrulha = 0
        self.jogador_detectado = False

    def jogador_no_campo_de_visao(self, jogo: "TelaJogo") -> bool:
        jogador = jogo.jogador
        distancia = calcular_distancia(
            self.sprite.center_x,
            self.sprite.center_y,
            jogador.sprite.center_x,
            jogador.sprite.center_y,
        )
        if distancia > DISTANCIA_VISAO:
            return False

        frente_x, frente_y = vetor_do_sprite(self.sprite)
        alvo_x, alvo_y = direcao_para_alvo(self.sprite, jogador.sprite.center_x, jogador.sprite.center_y)
        produto = limitar(frente_x * alvo_x + frente_y * alvo_y, -1, 1)
        angulo = math.degrees(math.acos(produto))
        if angulo > ANGULO_CAMPO_VISAO / 2:
            return False

        return jogo.linha_de_visao_livre(
            self.sprite.center_x,
            self.sprite.center_y,
            jogador.sprite.center_x,
            jogador.sprite.center_y,
        )

    def atualizar(self, jogo: "TelaJogo", delta_time: float) -> list[Tiro]:
        self.recarga_tiro = max(0, self.recarga_tiro - delta_time)
        tiros = []
        self.jogador_detectado = self.jogador_no_campo_de_visao(jogo)

        if self.jogador_detectado:
            self.estado_texto = "FOV viu jogador"
            direcao_x, direcao_y = direcao_para_alvo(self.sprite, jogo.jogador.sprite.center_x, jogo.jogador.sprite.center_y)
            self.sprite.angle = angulo_do_vetor(direcao_x, direcao_y)
            tiro = self.tentar_atirar(jogo.jogador)
            if tiro is not None:
                tiros.append(tiro)
        else:
            self.estado_texto = "Patrulha FOV"
            alvo_x, alvo_y = self.pontos_patrulha[self.indice_patrulha]
            if calcular_distancia(self.sprite.center_x, self.sprite.center_y, alvo_x, alvo_y) < 20:
                self.indice_patrulha = (self.indice_patrulha + 1) % len(self.pontos_patrulha)
                alvo_x, alvo_y = self.pontos_patrulha[self.indice_patrulha]
            self.mover_para(alvo_x, alvo_y, VELOCIDADE_GUARDA, delta_time, jogo)

        return tiros

    def desenhar_debug(self, jogo: "TelaJogo") -> None:
        frente_x, frente_y = vetor_do_sprite(self.sprite)
        angulo_frente = math.atan2(frente_y, frente_x)
        meio = math.radians(ANGULO_CAMPO_VISAO / 2)
        pontos = [(self.sprite.center_x, self.sprite.center_y)]
        for indice in range(11):
            angulo = angulo_frente - meio + (2 * meio) * indice / 10
            pontos.append(
                (
                    self.sprite.center_x + math.cos(angulo) * DISTANCIA_VISAO,
                    self.sprite.center_y + math.sin(angulo) * DISTANCIA_VISAO,
                )
            )

        cor = (255, 82, 82, 70) if self.jogador_detectado else (255, 213, 91, 36)
        arcade.draw_polygon_filled(pontos, cor)
        arcade.draw_polygon_outline(pontos, (255, 230, 126, 120), 2)

        distancia_jogador = calcular_distancia(
            self.sprite.center_x,
            self.sprite.center_y,
            jogo.jogador.sprite.center_x,
            jogo.jogador.sprite.center_y,
        )
        if distancia_jogador <= DISTANCIA_VISAO:
            cor_linha = COR_ALERTA if self.jogador_detectado else CINZA_ESCURO
            arcade.draw_line(
                self.sprite.center_x,
                self.sprite.center_y,
                jogo.jogador.sprite.center_x,
                jogo.jogador.sprite.center_y,
                cor_linha,
                2,
            )


class CacadorAEstrela(InimigoBase):
    """Inimigo que persegue usando A* para contornar obstaculos."""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(TEXTURA_CACADOR, x, y, 1.0, 95, "Cacador A*", COR_CACADOR, 180)
        self.caminho: list[tuple[int, int]] = []
        self.tempo_recalculo = 0.0
        self.ativo_por_distancia = False

    def atualizar(self, jogo: "TelaJogo", delta_time: float) -> list[Tiro]:
        self.recarga_tiro = max(0, self.recarga_tiro - delta_time)
        tiros = []
        distancia = calcular_distancia(
            self.sprite.center_x,
            self.sprite.center_y,
            jogo.jogador.sprite.center_x,
            jogo.jogador.sprite.center_y,
        )
        self.ativo_por_distancia = distancia < DISTANCIA_ATIVAR_ASTAR or jogo.pecas_coletadas >= 1

        if not self.ativo_por_distancia:
            self.estado_texto = "A* aguardando"
            return tiros

        self.estado_texto = "A* perseguindo"
        self.tempo_recalculo -= delta_time
        if self.tempo_recalculo <= 0:
            inicio = posicao_para_celula(self.sprite.center_x, self.sprite.center_y)
            destino = posicao_para_celula(jogo.jogador.sprite.center_x, jogo.jogador.sprite.center_y)
            self.caminho = astar(jogo.mapa, inicio, destino)
            self.tempo_recalculo = 0.45

        if len(self.caminho) > 1:
            proxima_celula = self.caminho[1]
            alvo_x, alvo_y = celula_para_posicao(proxima_celula[0], proxima_celula[1])
            self.mover_para(alvo_x, alvo_y, VELOCIDADE_CACADOR, delta_time, jogo)

        if distancia < ALCANCE_TIRO_INIMIGO and jogo.linha_de_visao_livre(
            self.sprite.center_x,
            self.sprite.center_y,
            jogo.jogador.sprite.center_x,
            jogo.jogador.sprite.center_y,
        ):
            tiro = self.tentar_atirar(jogo.jogador)
            if tiro is not None:
                tiros.append(tiro)

        return tiros

    def desenhar_debug(self) -> None:
        if len(self.caminho) <= 1:
            return
        pontos = [celula_para_posicao(linha, coluna) for linha, coluna in self.caminho[:18]]
        for indice in range(len(pontos) - 1):
            arcade.draw_line(pontos[indice][0], pontos[indice][1], pontos[indice + 1][0], pontos[indice + 1][1], COR_ASTAR, 3)
        for x, y in pontos:
            arcade.draw_circle_filled(x, y, 6, (96, 214, 255, 150))


class ComandanteUtilidade(InimigoBase):
    """Inimigo que escolhe comportamento com Utility AI."""

    ATACAR = "Atacar"
    BUSCAR_VIDA = "Buscar vida"
    FUGIR = "Fugir"
    PATRULHAR = "Patrulhar"

    def __init__(self, x: float, y: float, pontos_patrulha: list[tuple[float, float]]) -> None:
        super().__init__(TEXTURA_COMANDANTE, x, y, 1.18, 145, "Comandante", COR_COMANDANTE, 300)
        self.pontos_patrulha = pontos_patrulha
        self.indice_patrulha = 0
        self.acao_atual = self.PATRULHAR
        self.pontuacoes: list[PontuacaoUtilidade] = []
        self.alvo_x = x
        self.alvo_y = y

    def calcular_utilidades(self, jogo: "TelaJogo") -> None:
        distancia_jogador = calcular_distancia(
            self.sprite.center_x,
            self.sprite.center_y,
            jogo.jogador.sprite.center_x,
            jogo.jogador.sprite.center_y,
        )
        jogador_perto = 1 - limitar((distancia_jogador - 90) / 360, 0, 1)
        jogador_longe = limitar((distancia_jogador - 240) / 520, 0, 1)
        vida_percentual = self.vida / self.vida_maxima
        vida_baixa = 1 - vida_percentual
        jogador_fraco = 1 - (jogo.jogador.vida / VIDA_MAXIMA)

        kit = jogo.encontrar_kit_mais_perto(self.sprite.center_x, self.sprite.center_y)
        pontuacao_kit = 0
        if kit is not None:
            distancia_kit = calcular_distancia(self.sprite.center_x, self.sprite.center_y, kit.x, kit.y)
            pontuacao_kit = 1 - limitar(distancia_kit / 650, 0, 1)

        visao_livre = jogo.linha_de_visao_livre(
            self.sprite.center_x,
            self.sprite.center_y,
            jogo.jogador.sprite.center_x,
            jogo.jogador.sprite.center_y,
        )
        bonus_visao = 0.16 if visao_livre else -0.12

        pontuacao_atacar = limitar(
            0.10 + jogador_perto * 0.60 + vida_percentual * 0.22 + jogador_fraco * 0.20 + bonus_visao - vida_baixa * 0.36,
            0,
            1,
        )
        pontuacao_buscar_vida = limitar(
            vida_baixa * 0.82 + pontuacao_kit * 0.28 - jogador_perto * 0.18,
            0,
            1,
        )
        pontuacao_fugir = limitar(
            vida_baixa * 0.62 + jogador_perto * 0.36 - pontuacao_kit * 0.14,
            0,
            1,
        )
        pontuacao_patrulhar = limitar(
            0.20 + jogador_longe * 0.44 + vida_percentual * 0.18 - jogador_perto * 0.32 - vida_baixa * 0.18,
            0,
            1,
        )

        if kit is None or self.vida >= self.vida_maxima * 0.88:
            pontuacao_buscar_vida = 0

        self.pontuacoes = [
            PontuacaoUtilidade(self.ATACAR, pontuacao_atacar, COR_ALERTA),
            PontuacaoUtilidade(self.BUSCAR_VIDA, pontuacao_buscar_vida, COR_VIDA),
            PontuacaoUtilidade(self.FUGIR, pontuacao_fugir, COR_ASTAR),
            PontuacaoUtilidade(self.PATRULHAR, pontuacao_patrulhar, COR_UTILIDADE),
        ]
        self.acao_atual = max(self.pontuacoes, key=lambda item: item.valor).nome
        self.estado_texto = f"Utility: {self.acao_atual}"

    def atualizar(self, jogo: "TelaJogo", delta_time: float) -> list[Tiro]:
        self.recarga_tiro = max(0, self.recarga_tiro - delta_time)
        tiros = []
        self.calcular_utilidades(jogo)

        if self.acao_atual == self.ATACAR:
            self.alvo_x = jogo.jogador.sprite.center_x
            self.alvo_y = jogo.jogador.sprite.center_y
            distancia = calcular_distancia(self.sprite.center_x, self.sprite.center_y, self.alvo_x, self.alvo_y)
            if distancia > 240:
                self.mover_para(self.alvo_x, self.alvo_y, VELOCIDADE_COMANDANTE, delta_time, jogo)
            else:
                direcao_x, direcao_y = direcao_para_alvo(self.sprite, self.alvo_x, self.alvo_y)
                self.sprite.angle = angulo_do_vetor(direcao_x, direcao_y)
            if distancia < ALCANCE_TIRO_INIMIGO and jogo.linha_de_visao_livre(self.sprite.center_x, self.sprite.center_y, self.alvo_x, self.alvo_y):
                tiro = self.tentar_atirar(jogo.jogador)
                if tiro is not None:
                    tiros.append(tiro)

        elif self.acao_atual == self.BUSCAR_VIDA:
            kit = jogo.encontrar_kit_mais_perto(self.sprite.center_x, self.sprite.center_y)
            if kit is not None:
                self.alvo_x = kit.x
                self.alvo_y = kit.y
                self.mover_para(self.alvo_x, self.alvo_y, VELOCIDADE_COMANDANTE, delta_time, jogo)

        elif self.acao_atual == self.FUGIR:
            self.alvo_x, self.alvo_y = jogo.encontrar_ponto_seguro(self.sprite.center_x, self.sprite.center_y)
            self.mover_para(self.alvo_x, self.alvo_y, VELOCIDADE_COMANDANTE + 35, delta_time, jogo)

        else:
            self.alvo_x, self.alvo_y = self.pontos_patrulha[self.indice_patrulha]
            if calcular_distancia(self.sprite.center_x, self.sprite.center_y, self.alvo_x, self.alvo_y) < 22:
                self.indice_patrulha = (self.indice_patrulha + 1) % len(self.pontos_patrulha)
                self.alvo_x, self.alvo_y = self.pontos_patrulha[self.indice_patrulha]
            self.mover_para(self.alvo_x, self.alvo_y, VELOCIDADE_COMANDANTE, delta_time, jogo)

        return tiros

    def desenhar_debug(self) -> None:
        arcade.draw_line(self.sprite.center_x, self.sprite.center_y, self.alvo_x, self.alvo_y, COR_UTILIDADE, 4)
        arcade.draw_circle_outline(self.alvo_x, self.alvo_y, 18, COR_UTILIDADE, 3)


class TelaMenu(arcade.View):
    def __init__(self) -> None:
        super().__init__()
        self.textura_menu = arcade.load_texture(TEXTURA_MENU)

    def on_show_view(self) -> None:
        arcade.set_background_color(COR_FUNDO)

    def on_draw(self) -> None:
        self.clear()

        # A imagem tem proporcao larga, entao ela e ampliada ate cobrir a tela.
        escala = max(LARGURA_TELA / self.textura_menu.width, ALTURA_TELA / self.textura_menu.height)
        largura_fundo = self.textura_menu.width * escala
        altura_fundo = self.textura_menu.height * escala
        arcade.draw_texture_rect(
            texture=self.textura_menu,
            rect=retangulo_centralizado(LARGURA_TELA / 2, ALTURA_TELA / 2, largura_fundo, altura_fundo),
        )

        # Camadas escuras deixam o texto legivel sem esconder totalmente a arte.
        arcade.draw_lrbt_rectangle_filled(0, LARGURA_TELA, 0, ALTURA_TELA, (4, 7, 12, 80))
        arcade.draw_lrbt_rectangle_filled(0, 650, 0, ALTURA_TELA, (4, 7, 12, 155))

        arcade.draw_text("TANK COLLECTION", 58, 535, BRANCO, 45, anchor_x="left")
        arcade.draw_text(
            "Colete as engrenagens e sobreviva aos tanques inimigos.",
            62,
            480,
            CINZA,
            17,
            anchor_x="left",
        )
        arcade.draw_text("Depois avance até a zona de extração.", 62, 452, CINZA, 17, anchor_x="left")

        arcade.draw_text("ENTER - iniciar missão", 62, 340, COR_PECA, 24, anchor_x="left")
        arcade.draw_text("WASD - mover", 62, 288, BRANCO, 16, anchor_x="left")
        arcade.draw_text("Mouse - mirar e atirar", 62, 260, BRANCO, 16, anchor_x="left")
        arcade.draw_text("R - reiniciar partida", 62, 232, BRANCO, 16, anchor_x="left")
        arcade.draw_text("E - mostrar/ocultar debug", 62, 204, BRANCO, 16, anchor_x="left")

        textos_ia = [
            "IAs usadas:",
            "Campo de visão + Raycasting",
            "A* para perseguuir o jogador",
            "Utility AI para decidir a ação",
        ]
        for indice, texto in enumerate(textos_ia):
            arcade.draw_text(texto, 62, 132 - indice * 24, CINZA, 14, anchor_x="left")

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER:
            self.window.show_view(TelaJogo())


class TelaFim(arcade.View):
    def __init__(self, venceu: bool, pecas: int, pontuacao: int, tempo_jogo: float) -> None:
        super().__init__()
        global MELHOR_PONTUACAO, MELHOR_TEMPO

        self.textura_menu = arcade.load_texture(TEXTURA_MENU)
        self.venceu = venceu
        self.pecas = pecas
        self.pontuacao = pontuacao
        self.tempo_jogo = tempo_jogo

        if self.venceu:
            melhor_por_pontos = self.pontuacao > MELHOR_PONTUACAO
            empate_com_tempo_melhor = self.pontuacao == MELHOR_PONTUACAO and (MELHOR_TEMPO is None or self.tempo_jogo < MELHOR_TEMPO)
            if melhor_por_pontos or empate_com_tempo_melhor:
                MELHOR_PONTUACAO = self.pontuacao
                MELHOR_TEMPO = self.tempo_jogo

    def on_show_view(self) -> None:
        arcade.set_background_color(COR_FUNDO)

    def on_draw(self) -> None:
        self.clear()
        titulo = "MISSAO CONCLUIDA" if self.venceu else "MISSAO FALHOU"
        cor = COR_EXTRACAO_ABERTA if self.venceu else COR_ALERTA
        melhor = "Melhor: ainda nao concluida"
        if MELHOR_TEMPO is not None:
            melhor = f"Melhor: {MELHOR_PONTUACAO} pts em {formatar_tempo(MELHOR_TEMPO)}"

        escala = max(LARGURA_TELA / self.textura_menu.width, ALTURA_TELA / self.textura_menu.height)
        largura_fundo = self.textura_menu.width * escala
        altura_fundo = self.textura_menu.height * escala
        arcade.draw_texture_rect(
            texture=self.textura_menu,
            rect=retangulo_centralizado(LARGURA_TELA / 2, ALTURA_TELA / 2, largura_fundo, altura_fundo),
        )
        arcade.draw_lrbt_rectangle_filled(0, LARGURA_TELA, 0, ALTURA_TELA, (4, 7, 12, 95))
        arcade.draw_lrbt_rectangle_filled(0, 650, 0, ALTURA_TELA, (4, 7, 12, 165))

        arcade.draw_text(titulo, 62, 505, cor, 40, anchor_x="left")
        arcade.draw_text(f"Pecas coletadas: {self.pecas}/{TOTAL_PECAS}", 64, 425, BRANCO, 22, anchor_x="left")
        arcade.draw_text(f"Pontuacao: {self.pontuacao} pts", 64, 382, COR_PECA, 21, anchor_x="left")
        arcade.draw_text(f"Tempo: {formatar_tempo(self.tempo_jogo)}", 64, 342, BRANCO, 19, anchor_x="left")
        arcade.draw_text(melhor, 64, 300, CINZA, 16, anchor_x="left")
        arcade.draw_text("ENTER - jogar novamente", 64, 212, COR_PECA, 21, anchor_x="left")
        arcade.draw_text("ESC - voltar ao menu", 64, 174, CINZA, 16, anchor_x="left")

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER:
            self.window.show_view(TelaJogo())
        elif key == arcade.key.ESCAPE:
            self.window.show_view(TelaMenu())


class TelaJogo(arcade.View):
    """Tela principal. Aqui ficam mapa, camera, entidades e sistemas de IA."""

    def __init__(self) -> None:
        super().__init__()
        self.camera = arcade.Camera2D()
        self.mapa = criar_matriz_mapa()

        self.lista_chao = arcade.SpriteList()
        self.lista_obstaculos = arcade.SpriteList(use_spatial_hash=True)
        self.lista_contorno_muros = arcade.SpriteList()
        self.lista_decoracao = arcade.SpriteList()
        self.lista_contorno_objetos = arcade.SpriteList()
        self.contornos_por_sprite: dict[arcade.Sprite, list[arcade.Sprite]] = {}
        self.lista_jogador = arcade.SpriteList()
        self.lista_inimigos = arcade.SpriteList()
        self.lista_tiros_jogador = arcade.SpriteList()
        self.lista_tiros_inimigos = arcade.SpriteList()
        self.lista_particulas = arcade.SpriteList()

        self.jogador: Jogador
        self.inimigos: list[InimigoBase] = []
        self.kits: list[KitVida] = []
        self.pecas: list[Peca] = []
        self.perigos: list[PerigoCenario] = []
        self.sprite_extracao = arcade.SpriteSolidColor(104, 104, 0, 0, (72, 224, 146, 95))
        self.sprite_bandeira_extracao = criar_sprite_item(arcade.load_texture(TEXTURA_SAIDA), 0, 0, 58)
        self.texto_extracao = arcade.Text("EXTRACAO", 0, 0, BRANCO, 12, anchor_x="center")

        self.pecas_coletadas = 0
        self.pontuacao = 0
        self.tempo_jogo = 0.0
        self.mensagem_objetivo = "Colete as 4 engrenagens"
        self.tempo_mensagem = 0.0
        self.texto_hud = arcade.Text("", 255, ALTURA_TELA - 52, BRANCO, 15)
        self.tempo_atualizar_hud = 0.0
        self.mostrar_debug_ia = DEBUG_IA_INICIAL

        self.texturas = {
            "grama1": arcade.load_texture(TEXTURA_GRAMA_1),
            "grama2": arcade.load_texture(TEXTURA_GRAMA_2),
            "areia1": arcade.load_texture(TEXTURA_AREIA_1),
            "areia2": arcade.load_texture(TEXTURA_AREIA_2),
            "rua_h": arcade.load_texture(TEXTURA_RUA_HORIZONTAL),
            "rua_v": arcade.load_texture(TEXTURA_RUA_VERTICAL),
            "rua_x": arcade.load_texture(TEXTURA_RUA_CRUZAMENTO),
            "muro": arcade.load_texture(TEXTURA_MURO),
            "caixa": arcade.load_texture(TEXTURA_CAIXA),
            "rocha": arcade.load_texture(TEXTURA_ROCHA),
            "bomba": arcade.load_texture(TEXTURA_BOMBA),
            "spikes": arcade.load_texture(TEXTURA_SPIKES),
            "tanque_destruido": arcade.load_texture(TEXTURA_CACADOR),
            "vida": arcade.load_texture(TEXTURA_VIDA),
            "engrenagem": arcade.load_texture(TEXTURA_ENGRENAGEM),
            "saida": arcade.load_texture(TEXTURA_SAIDA),
        }

        self.setup()

    def setup(self) -> None:
        self.lista_chao = arcade.SpriteList()
        self.lista_obstaculos = arcade.SpriteList(use_spatial_hash=True)
        self.lista_contorno_muros = arcade.SpriteList()
        self.lista_decoracao = arcade.SpriteList()
        self.lista_contorno_objetos = arcade.SpriteList()
        self.contornos_por_sprite = {}
        self.lista_jogador = arcade.SpriteList()
        self.lista_inimigos = arcade.SpriteList()
        self.lista_tiros_jogador = arcade.SpriteList()
        self.lista_tiros_inimigos = arcade.SpriteList()
        self.lista_particulas = arcade.SpriteList()
        self.inimigos = []
        self.kits = []
        self.pecas = []
        self.perigos = []
        self.pecas_coletadas = 0
        self.pontuacao = 0
        self.tempo_jogo = 0.0
        self.mensagem_objetivo = "Colete as 4 engrenagens"
        self.tempo_atualizar_hud = 0.0
        self.mostrar_debug_ia = DEBUG_IA_INICIAL

        posicao_jogador = celula_para_posicao(25, 2)
        self.jogador = Jogador(*posicao_jogador)
        self.lista_jogador.append(self.jogador.sprite)

        self.montar_tilemap()
        self.criar_entidades_do_mapa()
        self.criar_decoracoes_do_cenario()
        self.centralizar_camera(1.0)

    def montar_tilemap(self) -> None:
        for linha in range(LINHAS_MAPA):
            for coluna in range(COLUNAS_MAPA):
                caractere = self.mapa[linha][coluna]
                x, y = celula_para_posicao(linha, coluna)

                textura_chao = self.escolher_textura_chao(linha, coluna)
                self.lista_chao.append(criar_sprite_tile(textura_chao, x, y))

                if caractere == "M":
                    muro = criar_sprite_tile(self.texturas["muro"], x, y)
                    contorno_muro = arcade.SpriteSolidColor(
                        TAMANHO_TILE + 2,
                        TAMANHO_TILE + 2,
                        x,
                        y,
                        (12, 14, 18, 165),
                    )
                    self.lista_contorno_muros.append(contorno_muro)
                    self.lista_obstaculos.append(muro)
                elif caractere == "C":
                    caixa = criar_sprite_tile(self.texturas["caixa"], x, y)
                    caixa.angle = random.choice([-8, -4, 5, 10])
                    self.adicionar_contorno_objeto(caixa, 2)
                    self.lista_obstaculos.append(caixa)
                elif caractere == "B":
                    rocha = criar_sprite_item(self.texturas["rocha"], x, y, 58)
                    rocha.angle = random.choice([-14, -6, 8, 16])
                    self.adicionar_contorno_objeto(rocha, 2)
                    self.lista_obstaculos.append(rocha)

    def adicionar_contorno_objeto(self, sprite: arcade.Sprite, espessura: int) -> None:
        """Prepara o contorno uma vez, em vez de redesenhar oito copias a cada frame."""
        deslocamentos = (
            (-espessura, 0),
            (espessura, 0),
            (0, -espessura),
            (0, espessura),
            (-espessura, -espessura),
            (-espessura, espessura),
            (espessura, -espessura),
            (espessura, espessura),
        )
        contornos = [criar_sprite_contorno(sprite, dx, dy) for dx, dy in deslocamentos]
        self.contornos_por_sprite[sprite] = contornos
        for contorno in contornos:
            self.lista_contorno_objetos.append(contorno)

    def escolher_textura_chao(self, linha: int, coluna: int) -> arcade.Texture:
        caractere = self.mapa[linha][coluna]
        if caractere == "R":
            horizontal = self.celula_parece_rua(linha, coluna - 1) or self.celula_parece_rua(linha, coluna + 1)
            vertical = self.celula_parece_rua(linha - 1, coluna) or self.celula_parece_rua(linha + 1, coluna)
            if horizontal and vertical:
                return self.texturas["rua_x"]
            if horizontal:
                return self.texturas["rua_h"]
            return self.texturas["rua_v"]
        area_areia = (
            (linha >= 18 and coluna >= 18)
            or (linha <= 9 and coluna >= 18)
            or (10 <= linha <= 18 and 8 <= coluna <= 18)
            or (20 <= linha <= 24 and 5 <= coluna <= 14)
            or (5 <= linha <= 12 and 27 <= coluna <= 39)
        )
        if area_areia:
            if (linha + coluna) % 3 == 0:
                return self.texturas["areia2"]
            return self.texturas["areia1"]
        if (linha + coluna) % 4 == 0:
            return self.texturas["grama2"]
        return self.texturas["grama1"]

    def celula_parece_rua(self, linha: int, coluna: int) -> bool:
        if linha < 0 or linha >= LINHAS_MAPA or coluna < 0 or coluna >= COLUNAS_MAPA:
            return False
        return self.mapa[linha][coluna] == "R"

    def criar_entidades_do_mapa(self) -> None:
        for numero in range(1, TOTAL_PECAS + 1):
            celula = procurar_celulas(self.mapa, str(numero))[0]
            x, y = celula_para_posicao(celula[0], celula[1])
            self.pecas.append(Peca(numero, x, y, self.texturas["engrenagem"]))

        for linha, coluna in procurar_celulas(self.mapa, "H"):
            x, y = celula_para_posicao(linha, coluna)
            self.kits.append(KitVida(x, y, self.texturas["vida"]))

        celula_saida = procurar_celulas(self.mapa, "E")[0]
        self.sprite_extracao.center_x, self.sprite_extracao.center_y = celula_para_posicao(celula_saida[0], celula_saida[1])
        self.sprite_bandeira_extracao.center_x = self.sprite_extracao.center_x
        self.sprite_bandeira_extracao.center_y = self.sprite_extracao.center_y + 8
        self.texto_extracao.x = self.sprite_extracao.center_x
        self.texto_extracao.y = self.sprite_extracao.center_y - 78

        guarda_1_x, guarda_1_y = celula_para_posicao(20, 7)
        guarda_1 = GuardaCampoVisao(
            guarda_1_x,
            guarda_1_y,
            [
                celula_para_posicao(20, 5),
                celula_para_posicao(20, 10),
                celula_para_posicao(24, 10),
                celula_para_posicao(24, 5),
            ],
        )
        guarda_2_x, guarda_2_y = celula_para_posicao(13, 30)
        guarda_2 = GuardaCampoVisao(
            guarda_2_x,
            guarda_2_y,
            [celula_para_posicao(13, 28), celula_para_posicao(13, 36), celula_para_posicao(17, 36), celula_para_posicao(17, 28)],
        )
        guarda_3_x, guarda_3_y = celula_para_posicao(8, 9)
        guarda_3 = GuardaCampoVisao(
            guarda_3_x,
            guarda_3_y,
            [
                celula_para_posicao(8, 9),
                celula_para_posicao(8, 12),
                celula_para_posicao(9, 12),
                celula_para_posicao(9, 9),
            ],
        )
        cacador_x, cacador_y = celula_para_posicao(16, 20)
        cacador = CacadorAEstrela(cacador_x, cacador_y)
        comandante_x, comandante_y = celula_para_posicao(9, 34)
        comandante = ComandanteUtilidade(
            comandante_x,
            comandante_y,
            [celula_para_posicao(9, 34), celula_para_posicao(9, 37), celula_para_posicao(12, 37), celula_para_posicao(12, 34)],
        )

        self.inimigos = [guarda_1, guarda_2, guarda_3, cacador, comandante]
        for inimigo in self.inimigos:
            self.lista_inimigos.append(inimigo.sprite)

    def criar_decoracoes_do_cenario(self) -> None:
        """Adiciona objetos de guerra que nao precisam virar classe propria."""
        decoracoes = [
            ("bomba", 23, 7, 36, -28),
            ("spikes", 23, 14, 54, 35),
            ("bomba", 21, 29, 42, -12),
            ("bomba", 7, 20, 38, 15),
            ("spikes", 24, 27, 58, 0),
            ("spikes", 12, 15, 58, 90),
            ("tanque_destruido", 18, 33, 60, -28),
            ("tanque_destruido", 5, 23, 58, 35),
            ("rocha", 20, 30, 46, 8),
            ("rocha", 9, 28, 44, -15),
        ]

        for nome_textura, linha, coluna, tamanho, angulo in decoracoes:
            x, y = celula_para_posicao(linha, coluna)
            sprite = criar_sprite_item(self.texturas[nome_textura], x, y, tamanho)
            sprite.angle = angulo
            if nome_textura == "tanque_destruido":
                sprite.alpha = 170
            self.adicionar_contorno_objeto(sprite, 2)
            self.lista_decoracao.append(sprite)
            if nome_textura in ("bomba", "spikes"):
                self.perigos.append(PerigoCenario(nome_textura, sprite))

    def on_resize(self, width: int, height: int) -> None:
        super().on_resize(width, height)
        self.camera.match_window()

    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.desenhar_mundo()

        with self.window.default_camera.activate():
            self.desenhar_hud()

    def desenhar_mundo(self) -> None:
        self.lista_chao.draw()
        self.desenhar_extracao()
        self.lista_contorno_muros.draw()
        self.lista_contorno_objetos.draw()
        self.lista_decoracao.draw()

        if self.mostrar_debug_ia:
            for inimigo in self.inimigos:
                if inimigo.ativo and isinstance(inimigo, GuardaCampoVisao) and self.sprite_perto_camera(inimigo.sprite, DISTANCIA_VISAO + 80):
                    inimigo.desenhar_debug(self)

        if self.mostrar_debug_ia:
            for inimigo in self.inimigos:
                if not inimigo.ativo or not self.sprite_perto_camera(inimigo.sprite, DISTANCIA_VISAO + 80):
                    continue
                if isinstance(inimigo, CacadorAEstrela):
                    inimigo.desenhar_debug()
                elif isinstance(inimigo, ComandanteUtilidade):
                    inimigo.desenhar_debug()

        for kit in self.kits:
            kit.desenhar()

        self.lista_obstaculos.draw()
        self.lista_tiros_jogador.draw()
        self.lista_tiros_inimigos.draw()
        self.lista_jogador.draw()
        self.lista_inimigos.draw()
        for peca in self.pecas:
            peca.desenhar()
        self.lista_particulas.draw()

        for inimigo in self.inimigos:
            if inimigo.ativo:
                inimigo.desenhar_barra_vida()

    def desenhar_extracao(self) -> None:
        ativa = self.pecas_coletadas >= TOTAL_PECAS
        cor = COR_EXTRACAO_ABERTA if ativa else COR_EXTRACAO_FECHADA
        arcade.draw_circle_filled(self.sprite_extracao.center_x, self.sprite_extracao.center_y, 62, (cor[0], cor[1], cor[2], 72))
        arcade.draw_circle_outline(self.sprite_extracao.center_x, self.sprite_extracao.center_y, 64, cor, 4)
        self.texto_extracao.draw()
        desenhar_sprite_solto(self.sprite_bandeira_extracao)

    def desenhar_hud(self) -> None:
        arcade.draw_lrbt_rectangle_filled(0, LARGURA_TELA, ALTURA_TELA - 76, ALTURA_TELA, COR_HUD)
        arcade.draw_lrbt_rectangle_outline(0, LARGURA_TELA, ALTURA_TELA - 76, ALTURA_TELA, COR_HUD_BORDA, 2)

        y_texto = ALTURA_TELA - 52
        self.desenhar_barra(24, ALTURA_TELA - 48, 210, 18, self.jogador.vida / VIDA_MAXIMA, COR_JOGADOR)
        if self.tempo_atualizar_hud <= 0:
            texto_debug = "  |  Debug IA: ON" if self.mostrar_debug_ia else ""
            self.texto_hud.text = (
                f"Vida: {int(self.jogador.vida)}  |  Pecas: {self.pecas_coletadas}/{TOTAL_PECAS}  |  "
                f"Pontos: {self.pontuacao}  |  Tempo: {formatar_tempo(self.tempo_jogo)}  |  "
                f"Missao: {self.mensagem_objetivo}{texto_debug}"
            )
            self.tempo_atualizar_hud = 0.15
        self.texto_hud.y = y_texto
        self.texto_hud.draw()

    def desenhar_barra(self, x: float, y: float, largura: float, altura: float, proporcao: float, cor: tuple[int, int, int]) -> None:
        arcade.draw_lrbt_rectangle_filled(x, x + largura, y, y + altura, (42, 50, 64))
        arcade.draw_lrbt_rectangle_filled(x, x + largura * limitar(proporcao, 0, 1), y, y + altura, cor)
        arcade.draw_lrbt_rectangle_outline(x, x + largura, y, y + altura, BRANCO, 1)

    def sprite_perto_camera(self, sprite: arcade.Sprite, margem: float) -> bool:
        metade_largura = self.camera.viewport_width / 2 + margem
        metade_altura = self.camera.viewport_height / 2 + margem
        return (
            abs(sprite.center_x - self.camera.position[0]) <= metade_largura
            and abs(sprite.center_y - self.camera.position[1]) <= metade_altura
        )

    def on_update(self, delta_time: float) -> None:
        self.tempo_mensagem = max(0, self.tempo_mensagem - delta_time)
        self.tempo_atualizar_hud = max(0, self.tempo_atualizar_hud - delta_time)
        self.tempo_jogo += delta_time

        self.jogador.atualizar(delta_time, self.mapa)
        for peca in self.pecas:
            peca.atualizar(delta_time)
        for kit in self.kits:
            kit.atualizar(delta_time)
        for perigo in self.perigos:
            perigo.atualizar(delta_time)

        self.atualizar_inimigos(delta_time)
        self.lista_tiros_jogador.update(delta_time)
        self.lista_tiros_inimigos.update(delta_time)
        self.lista_particulas.update(delta_time)

        self.verificar_colisoes_tiros()
        self.verificar_perigos_do_cenario()
        self.verificar_coleta_pecas()
        self.verificar_coleta_kits()
        self.verificar_fim_de_jogo()
        self.centralizar_camera(0.13)

    def atualizar_inimigos(self, delta_time: float) -> None:
        for inimigo in self.inimigos:
            if not inimigo.ativo:
                continue
            tiros = inimigo.atualizar(self, delta_time)
            for tiro in tiros:
                self.lista_tiros_inimigos.append(tiro)
                self.criar_particulas(inimigo.sprite.center_x, inimigo.sprite.center_y, inimigo.cor, 6, 90)

    def verificar_colisoes_tiros(self) -> None:
        for tiro in list(self.lista_tiros_jogador):
            if arcade.check_for_collision_with_list(tiro, self.lista_obstaculos):
                tiro.remove_from_sprite_lists()
                continue

            for inimigo in self.inimigos:
                if inimigo.ativo and arcade.check_for_collision(tiro, inimigo.sprite):
                    tiro.remove_from_sprite_lists()
                    inimigo_eliminado = inimigo.sofrer_dano(tiro.dano)
                    if inimigo_eliminado:
                        self.pontuacao += inimigo.pontos
                    self.criar_particulas(inimigo.sprite.center_x, inimigo.sprite.center_y, COR_PECA, 18, 170)
                    break

        for tiro in list(self.lista_tiros_inimigos):
            if arcade.check_for_collision_with_list(tiro, self.lista_obstaculos):
                tiro.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision(tiro, self.jogador.sprite):
                tiro.remove_from_sprite_lists()
                self.jogador.vida = limitar(self.jogador.vida - tiro.dano, 0, VIDA_MAXIMA)
                self.criar_particulas(self.jogador.sprite.center_x, self.jogador.sprite.center_y, COR_ALERTA, 16, 165)

    def verificar_perigos_do_cenario(self) -> None:
        for perigo in list(self.perigos):
            if not perigo.ativo:
                continue

            if perigo.tipo == "bomba":
                if arcade.check_for_collision(self.jogador.sprite, perigo.sprite):
                    self.explodir_bomba(perigo)
                    continue

                for inimigo in self.inimigos:
                    if inimigo.ativo and arcade.check_for_collision(inimigo.sprite, perigo.sprite):
                        self.explodir_bomba(perigo)
                        break

            elif perigo.tipo == "spikes":
                if perigo.recarga_jogador <= 0 and arcade.check_for_collision(self.jogador.sprite, perigo.sprite):
                    self.jogador.vida = limitar(self.jogador.vida - DANO_ESPINHO, 0, VIDA_MAXIMA)
                    perigo.recarga_jogador = RECARGA_DANO_ESPINHO
                    self.criar_particulas(self.jogador.sprite.center_x, self.jogador.sprite.center_y, COR_ALERTA, 10, 130)

                for inimigo in self.inimigos:
                    if not inimigo.ativo:
                        continue
                    chave = id(inimigo)
                    if perigo.recargas_inimigos.get(chave, 0) <= 0 and arcade.check_for_collision(inimigo.sprite, perigo.sprite):
                        inimigo_eliminado = inimigo.sofrer_dano(DANO_ESPINHO)
                        if inimigo_eliminado:
                            self.pontuacao += inimigo.pontos
                        perigo.recargas_inimigos[chave] = RECARGA_DANO_ESPINHO
                        self.criar_particulas(inimigo.sprite.center_x, inimigo.sprite.center_y, COR_ALERTA, 8, 120)

    def explodir_bomba(self, perigo: PerigoCenario) -> None:
        perigo.ativo = False
        perigo.sprite.remove_from_sprite_lists()
        for contorno in self.contornos_por_sprite.pop(perigo.sprite, []):
            contorno.remove_from_sprite_lists()
        if perigo in self.perigos:
            self.perigos.remove(perigo)

        x = perigo.sprite.center_x
        y = perigo.sprite.center_y
        self.criar_particulas(x, y, COR_EXPLOSAO, 44, 260)

        if calcular_distancia(self.jogador.sprite.center_x, self.jogador.sprite.center_y, x, y) <= RAIO_EXPLOSAO_BOMBA:
            self.jogador.vida = limitar(self.jogador.vida - DANO_BOMBA, 0, VIDA_MAXIMA)

        for inimigo in self.inimigos:
            if inimigo.ativo and calcular_distancia(inimigo.sprite.center_x, inimigo.sprite.center_y, x, y) <= RAIO_EXPLOSAO_BOMBA:
                inimigo_eliminado = inimigo.sofrer_dano(DANO_BOMBA)
                if inimigo_eliminado:
                    self.pontuacao += inimigo.pontos

    def verificar_coleta_pecas(self) -> None:
        for peca in self.pecas:
            if peca.coletada:
                continue
            if calcular_distancia(self.jogador.sprite.center_x, self.jogador.sprite.center_y, peca.x, peca.y) <= RAIO_COLETA:
                peca.coletada = True
                self.pecas_coletadas += 1
                self.criar_particulas(peca.x, peca.y, COR_PECA, 28, 190)
                if self.pecas_coletadas < TOTAL_PECAS:
                    self.mensagem_objetivo = f"Faltam {TOTAL_PECAS - self.pecas_coletadas} engrenagens"
                else:
                    self.mensagem_objetivo = "Va para a area de extracao"

    def verificar_coleta_kits(self) -> None:
        self.tentar_coletar_kit(self.jogador.sprite, "jogador")
        for inimigo in self.inimigos:
            if inimigo.ativo:
                self.tentar_coletar_kit(inimigo.sprite, "inimigo", inimigo)

    def tentar_coletar_kit(self, sprite: arcade.Sprite, dono: str, inimigo: Optional[InimigoBase] = None) -> None:
        vida_atual = self.jogador.vida if dono == "jogador" else inimigo.vida if inimigo is not None else VIDA_MAXIMA
        vida_maxima = VIDA_MAXIMA if dono == "jogador" else inimigo.vida_maxima if inimigo is not None else VIDA_MAXIMA
        if vida_atual >= vida_maxima:
            return

        for kit in self.kits:
            if not kit.ativo:
                continue
            if calcular_distancia(sprite.center_x, sprite.center_y, kit.x, kit.y) <= RAIO_COLETA:
                if dono == "jogador":
                    self.jogador.vida = limitar(self.jogador.vida + CURA_KIT_VIDA, 0, VIDA_MAXIMA)
                elif inimigo is not None:
                    inimigo.vida = limitar(inimigo.vida + CURA_KIT_VIDA, 0, inimigo.vida_maxima)
                kit.coletar()
                self.criar_particulas(kit.x, kit.y, COR_VIDA, 20, 150)
                return

    def verificar_fim_de_jogo(self) -> None:
        if self.jogador.vida <= 0:
            self.window.show_view(TelaFim(False, self.pecas_coletadas, self.pontuacao, self.tempo_jogo))
            return

        if self.pecas_coletadas >= TOTAL_PECAS and arcade.check_for_collision(self.jogador.sprite, self.sprite_extracao):
            self.window.show_view(TelaFim(True, self.pecas_coletadas, self.pontuacao, self.tempo_jogo))

    def criar_particulas(self, x: float, y: float, cor: tuple[int, int, int], quantidade: int, velocidade: float) -> None:
        for _ in range(quantidade):
            self.lista_particulas.append(ParticulaFlutuante(x, y, cor, velocidade))

    def centralizar_camera(self, suavidade: float) -> None:
        metade_largura = self.camera.viewport_width / 2
        metade_altura = self.camera.viewport_height / 2
        alvo_x = limitar(self.jogador.sprite.center_x, metade_largura, LARGURA_MUNDO - metade_largura)
        alvo_y = limitar(self.jogador.sprite.center_y, metade_altura, ALTURA_MUNDO - metade_altura)
        self.camera.position = arcade.math.lerp_2d(self.camera.position, (alvo_x, alvo_y), suavidade)

    def linha_de_visao_livre(self, x1: float, y1: float, x2: float, y2: float) -> bool:
        distancia = calcular_distancia(x1, y1, x2, y2)
        passos = max(1, int(distancia / 16))
        for indice in range(1, passos):
            t = indice / passos
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            linha, coluna = posicao_para_celula(x, y)
            if celula_bloqueada(self.mapa, linha, coluna):
                return False
        return True

    def encontrar_kit_mais_perto(self, x: float, y: float) -> Optional[KitVida]:
        ativos = [kit for kit in self.kits if kit.ativo]
        if not ativos:
            return None
        return min(ativos, key=lambda kit: calcular_distancia(x, y, kit.x, kit.y))

    def encontrar_ponto_seguro(self, x: float, y: float) -> tuple[float, float]:
        candidatos = [
            celula_para_posicao(23, 3),
            celula_para_posicao(21, 15),
            celula_para_posicao(13, 36),
            celula_para_posicao(5, 31),
            celula_para_posicao(24, 38),
        ]
        return max(candidatos, key=lambda ponto: calcular_distancia(ponto[0], ponto[1], self.jogador.sprite.center_x, self.jogador.sprite.center_y))

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.R:
            self.window.show_view(TelaJogo())
            return
        if key == arcade.key.E:
            self.mostrar_debug_ia = not self.mostrar_debug_ia
            self.tempo_atualizar_hud = 0
            return
        if key == arcade.key.ESCAPE:
            self.window.show_view(TelaMenu())
            return
        if key == arcade.key.SPACE:
            alvo = self.encontrar_inimigo_mais_perto()
            if alvo is not None:
                tiro = self.jogador.atirar(alvo.sprite.center_x, alvo.sprite.center_y)
                if tiro is not None:
                    self.lista_tiros_jogador.append(tiro)
                    self.criar_particulas(self.jogador.sprite.center_x, self.jogador.sprite.center_y, COR_JOGADOR, 6, 90)
            return
        self.jogador.pressionar(key)

    def on_key_release(self, key: int, modifiers: int) -> None:
        self.jogador.soltar(key)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        mundo = self.camera.unproject((x, y))
        tiro = self.jogador.atirar(mundo.x, mundo.y)
        if tiro is not None:
            self.lista_tiros_jogador.append(tiro)
            self.criar_particulas(self.jogador.sprite.center_x, self.jogador.sprite.center_y, COR_JOGADOR, 6, 90)

    def encontrar_inimigo_mais_perto(self) -> Optional[InimigoBase]:
        ativos = [inimigo for inimigo in self.inimigos if inimigo.ativo]
        if not ativos:
            return None
        return min(
            ativos,
            key=lambda inimigo: calcular_distancia(
                self.jogador.sprite.center_x,
                self.jogador.sprite.center_y,
                inimigo.sprite.center_x,
                inimigo.sprite.center_y,
            ),
        )


def main() -> None:
    janela = arcade.Window(LARGURA_TELA, ALTURA_TELA, TITULO_TELA)
    janela.show_view(TelaMenu())
    arcade.run()


if __name__ == "__main__":
    main()
