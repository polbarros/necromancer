from states.state import State
from states.login import Login
import ui
import pygame, os

class Title(State):
    """Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de título."""
    def __init__(self, game):
        State.__init__(self, game) # Tomamos la inicialización de la superclase State.

        # Imagen de fondo
        self.background_img = pygame.image.load(os.path.join(self.game.sprite_dir, "bg_samurai.png"))
        self.title_img = pygame.image.load(os.path.join(self.game.sprite_dir, "title_necromancer.png"))
        self.start_button_img = pygame.image.load(os.path.join(self.game.sprite_dir, "start_normal.png"))
        self.start_button_img.set_colorkey([0, 0, 0]) # Quitar el fondo negro que ocupa el espacio de la transparencia.
        # Botón de Inicio
        self.start_button_img_h = pygame.image.load(os.path.join(self.game.sprite_dir, "start_hovered.png"))
        self.start_button_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro que ocupa el espacio de transparencia.
        self.start_button = ui.Button((500//2) - 200, 800 - 130, self.start_button_img, self.start_button_img_h, 1)

    def update(self, delta_time):
        if self.start_button.action():
            new_state = Login(self.game) # Creamos un nuevo estado (objeto) de la clase Login.
            new_state.enter_state() # Entramos al nuevo estado Login invocando el método común de la superclase State.


    def render(self, display):
        # Color de fondo
        display.fill((197, 178, 189))
        # Imágen de samurai
        display.blit(self.background_img, (0, - 40))
        # Imagen de título
        display.blit(self.title_img, (0, 477))
        # Imagen del botón START
        self.start_button.draw(display)