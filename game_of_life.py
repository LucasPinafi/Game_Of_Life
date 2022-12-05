from __future__ import annotations
import pygame
from typing import Tuple, List
from button import Button

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
CELL_SIZE = 10, 10
ALIVE = (178, 184, 180)  # cor da célula viva em RGB


# Função para desativar/ativar o clique nas células após iniciar/pausar
def start_simulation():
    global started_simulation
    started_simulation = not started_simulation


# Função para mostrar a quantidade da população
def get_screen_text():
    global started_simulation, time, n_population
    n_alive = 0
    for cells in cell_lists:
        for cell in cells:
            if cell.color == ALIVE:
                n_alive += 1
    if n_population != n_alive:
        time = pygame.time.get_ticks()
        n_population = n_alive
    text_render = text_surf.render(f'Population: {n_alive}', True, (255, 255, 255))
    text_rect = text_render.get_rect(topleft=(SCREEN_WIDTH - 175, SCREEN_HEIGHT + 25))
    aux_rect = text_rect
    aux_rect.width += 50
    pygame.draw.rect(screen, color='black', rect=aux_rect)
    screen.blit(text_render, text_rect)


# Função para obter a lista de lista de células
def get_cell_lists() -> None:
    global started_simulation
    for line in range(SCREEN_WIDTH // CELL_SIZE[0]):
        cell_list = []
        for collumn in range(SCREEN_HEIGHT // CELL_SIZE[0]):
            cell_list.append(Cell(
                (line * CELL_SIZE[0], collumn * CELL_SIZE[0])
            ))
        cell_lists.append(cell_list)


def restart() -> None:
    global started_simulation
    started_simulation = False
    grid.clear_grid()


# Class base das células. Representa cada quadradinho desenhado. Herda uma classe chamada Sprite do pygame
class Cell(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int], color: str = 'black') -> None:
        super().__init__()  # Chama o construtor de Sprite()
        self.image = pygame.Surface(CELL_SIZE)  # É a imagem do quadrado que será impresso na tela
        self._position = pygame.math.Vector2(position)  # É a posição do quadradinho na tela
        self.rect = self.image.get_rect(topleft=self._position)  # É o retângulo que representa o quadrado
        self.color = color
        self._time_clicked = 0  # Variável auxiliar para não poder dar dois cliques mto rápido
        self.can_click = True

    #  Método que irá fazer o update da tela ao clicar
    def update_by_click(self) -> None:
        if pygame.mouse.get_pressed()[0] and self.can_click:
            self.can_click = False
            # get_ticks() retorna quanto tempo, em milessegundos, desde que o programa começou
            self._time_clicked = pygame.time.get_ticks()
            # Pega exatamente a posição de onde clica e muda a cor
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.color == 'black':
                    self.color = ALIVE
                else:
                    self.color = 'black'
                # Essa linha efetivamente preenche o quadrado com a cor escolhida
                self.image.fill(self.color)
                # Essa linha desenha na tela o quadrado
                screen.blit(self.image, self.rect)
        # Se passar mais que 500 ms desde que clicou, o quadrado estará liberado novamente para ser clicado
        if pygame.time.get_ticks() - self._time_clicked > 500:
            self.can_click = True

    def restart(self) -> None:
        self.color = 'black'
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

    def update_simulation(self) -> None:
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

    def get_position(self) -> Tuple[int, int]:
        return int(self._position.x), int(self._position.y)


# Class que representa a malha como um todo
class Grid:
    def __init__(self, _cell_list: List[List[Cell]]) -> None:
        self._cell_list = _cell_list

    # Desenha a malha na tela
    def draw_grid(self) -> None:
        for _line in range(SCREEN_WIDTH // CELL_SIZE[0]):
            for _collumn in range(SCREEN_HEIGHT // CELL_SIZE[0]):
                pygame.draw.rect(screen,
                                 color='purple',
                                 rect=self._cell_list[_line][_collumn].rect,
                                 width=1)

    # A cada frame essa função irá rodar para dar o update na malha
    def update(self) -> None:
        # Se a simulação ainda não começou, deverá chamar a update_by_click() de cada célula
        if not started_simulation:
            for _cell_list in self._cell_list:
                for cell in _cell_list:
                    cell.update_by_click()
        # Caso a simulação tenha começado, deverá chamar update_simulation() de cada célula
        else:
            cell_lists_aux: List[List[Cell]] = []
            for _l in range(SCREEN_WIDTH // CELL_SIZE[0]):
                aux = []
                for _c in range(SCREEN_HEIGHT // CELL_SIZE[0]):
                    aux.append(Cell(self._cell_list[_l][_c].get_position(), self._cell_list[_l][_c].color))
                cell_lists_aux.append(aux)

            for _l in range(1, SCREEN_WIDTH // CELL_SIZE[0] - 1):
                for _c in range(1, SCREEN_HEIGHT // CELL_SIZE[0] - 1):
                    neighboors = [
                        [cell_lists_aux[_l-1][_c-1], cell_lists_aux[_l-1][_c], cell_lists_aux[_l-1][_c+1]],
                        [cell_lists_aux[_l][_c-1], cell_lists_aux[_l][_c], cell_lists_aux[_l][_c+1]],
                        [cell_lists_aux[_l+1][_c-1], cell_lists_aux[_l+1][_c], cell_lists_aux[_l+1][_c+1]]
                    ]
                    num_alive = 0
                    for i in range(3):
                        for j in range(3):
                            if (i, j) != (1, 1) and neighboors[i][j].color == ALIVE:
                                num_alive += 1
                    if num_alive < 2 and self._cell_list[_l][_c].color == ALIVE:
                        self._cell_list[_l][_c].color = 'black'
                    if (num_alive == 2 or num_alive == 3) and self._cell_list[_l][_c].color == ALIVE:
                        self._cell_list[_l][_c].color = ALIVE
                    if num_alive > 3 and self._cell_list[_l][_c].color == ALIVE:
                        self._cell_list[_l][_c].color = 'black'
                    if num_alive == 3 and self._cell_list[_l][_c].color == 'black':
                        self._cell_list[_l][_c].color = ALIVE

            for _l in range(1, SCREEN_WIDTH // CELL_SIZE[0] - 1):
                for _c in range(1, SCREEN_HEIGHT // CELL_SIZE[0] - 1):
                    self._cell_list[_l][_c].update_simulation()

    def clear_grid(self) -> None:
        for _l in range(1, SCREEN_WIDTH // CELL_SIZE[0] - 1):
            for _c in range(1, SCREEN_HEIGHT // CELL_SIZE[0] - 1):
                self._cell_list[_l][_c].restart()

# O programa começa efetivamente aqui. Aqui é criada uma lista de listas de células (Matriz NxM de células)
cell_lists: List[List[Cell]] = []
get_cell_lists()

grid = Grid(cell_lists)
pygame.init()

# Aqui é definida a tela e as suas dimensões
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + 75))
# Essa variável é apenas para controlar o FPS do jogo
clock = pygame.time.Clock()
# Variável que mantém controle se fechamos ou não a tela do jogo
running = True
# Variável que mantém controle se iniciamos ou não a simulação
started_simulation = False
# Botão que fica em baixo
start_button = Button(screen=screen, text="Start", width=100, height=40,
                      pos=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT + 15),
                      elevation=2, top_collor='red', top_color_hover='blue',
                      on_pressed=start_simulation, font_size=15,
                      font='subatomic.ttf')
# Botão para reiniciar
restart_button = Button(screen=screen, text="Restart", width=120, height=40,
                        pos=(40, SCREEN_HEIGHT + 15), elevation=1, top_collor='gray',
                        top_color_hover='green', on_pressed=restart, font_size=12,
                        font='subatomic.ttf')
# Superfície do texto
text_surf = pygame.font.Font('subatomic.ttf', 15)
time = 0
n_population = 0

# Loop do jogo
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid.update()
    if started_simulation:
        clock.tick(10)
        start_button.text = 'Pause'
    else:
        start_button.text = 'Start'

    grid.draw_grid()
    start_button.draw()
    restart_button.draw()
    pygame.display.update()
    get_screen_text()
