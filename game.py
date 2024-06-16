import os
import pygame
import pygame_gui
import sys
import time
import db
import models
from states.combat import Combat
from states.title import Title


class Game():
    """El proposito de esta clase es encapsular todos los elementos recursivos que se desarrollan en el juego.
     Consideramos que un juego siempre desarrolla un loop basado en:
      > Entrada/recogida de eventos
      > Actualización de datos
      > Representación gráfica de los elementos implicados que deben ser visualizados por el jugador."""
    def __init__(self):
        pygame.init() # Iniciación del framework PyGame
        # Establecemos unas constantes para el ancho y el alto de la ventana principal y el canvas.
        self.W, self.H = 500, 800
        # El canvas es un objeto de la clase Surface de pygame en la que se "pintan los elementos".
        self.canvas = pygame.Surface((self.W, self.H))
        # La screen es un elemento de pygame de tipo único (display) que representa la ventana.
        self.screen = pygame.display.set_mode((self.W, self.H)) # Iniciamos la ventana.
        self.caption = pygame.display.set_caption("Necromancer") # Establecemos el nombre de la ventana (caption)
        # Establecemos el icono del juego (en el dock en Mac y en la ventana en Windows).
        icon = pygame.image.load("assets/sprites/icon-samurai.png")
        self.icon = pygame.display.set_icon(icon)
        # Creamos dos variables para ver si el programa está funcionando y si el jugador está jugando.
        self.running, self.playing = True, True
        # Establecemos dos variables para registrar Deltatime y el tiempo para no depender de los FPS.
        self.dt, self.prev_time = 0, 0
        # Declaramos la pila de estados. Una lista en la que se acumulan los estados (states) para manejarlos.
        self.state_stack = []
        # Invocamos un método de esta misma clase para cargar los assets.
        self.load_assets()
        # Invocamos un método de esta misma clase para cargar los estados (el primero, como mínimo).
        self.load_states()

        """Establecemos el "manager" de la librería pygame_gui para poder operar con ella en los límites de la ventana
         e indicamos el archivo JSON para hacer el 'theming' de los elementos de la librería."""
        self.manager = pygame_gui.UIManager((self.W, self.H), "theme.json")

        # Indicando a SQLAlquemy que cree, si no existen, las tablas de todos los modelos que encuentre en models.py
        self.data_bases = db.Base.metadata.create_all(db.engine) # Creamos el modelo de datos

    def game_loop(self):
        '''Este método mantendrá un loop constante siempre que el juego funcione (self.playing == True).
        Activando y reactivando los métodos de la clase Game que mantienen el funcionamiento básico del juego (objeto):
        captar, actualizar y mostrar.'''
        while self.playing:
            self.get_dt() # Obtener DeltaTime
            self.get_events() # Obtener los eventos del juego
            self.update() # Actualizar los elementos implicados
            self.render() # Dibujar en pantalla los elementos gráficos

    def get_events(self):
        # Este método revisará los eventos a captar en el juego (inputs) mediante un bucle.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Si cerramos la ventana mediante la cruz de la esquina finalizamos el juego.
                db.session.query(models.Warrior).delete()  # Borramos los datos sobre guerreros de la BD
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()

            '''Esta sección permite especificar que el procesamiento de eventos sea por defecto el general del 
            manager del archivo game.py, (como en login.py), pero que invoque una función de procesamiento de eventos 
            especifica situada en el estado actual  para evitar conflictos'''
            if self.state_stack:
                current_state = self.state_stack[-1]
                if isinstance(current_state, Combat):
                    current_state.process_gui_events(event) # Revisión de eventos del manager del estado Combat
                else:
                    self.manager.process_events(event) # Revisión de eventos propios de los elementos de pygame_gui.

        """NOTA: en nuestro juego casi todos los eventos de tipo input recogidos por acciones del jugador serán clicks 
        de ratón. La comprobación de esos inputs se realizará internamente en la clase botón generada para crear objetos
        botón de forma recurrente. No será necesario establecer varias lógicas para el uso del teclado."""

    def update(self):
        # "Refrescamos" el último elemento de la pila de estados. Invocamos el método update de cada estado (clases).
        self.state_stack[-1].update(self.dt)
        self.manager.update(self.dt) # "Refrescamos" los elementos de la librería pygame_gui

    def render(self):
        # Muestra el estado actual en pantalla.
        self.state_stack[-1].render(self.canvas) # Mandamos el lienzo como parámetro en el método render de cada estado.
        # "Proyectamos" el canvas en la ventana en las coordenadas 0,0.
        self.screen.blit(self.canvas, (0, 0))

        pygame.display.update() # Actualizamos gráficamente los elementos de la ventana. Todos, si no hay parámetros.

    def get_dt(self):
        # Función para calcular Deltatime
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        # Función que nos permite escribir texto en pantalla (a partir del centro).
        text_surface = self.font.render(text, True, color)
        #text_surface.set_colorkey((0, 0, 0)) # A usar en caso de fuentes con problemas de transparencias.
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_text_left(self, surface, text, color, x, y):
        # Función que nos permite escribir texto en pantalla (justificado a la izquierda).
        text_surface = self.font.render(text, True, color)
        #text_surface.set_colorkey((0, 0, 0)) # A usar en caso de fuentes con problemas de transparencias.
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_text_right(self, surface, text, color, x, y):
        # Función que nos permite escribir texto en pantalla (justificado a la izquierda).
        text_surface = self.font.render(text, True, color)
        #text_surface.set_colorkey((0, 0, 0)) # A usar en caso de fuentes con problemas de transparencias.
        text_rect = text_surface.get_rect()
        text_rect.topright = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        # Creamos punteros a carpetas y subcarpetas con los archivos de assets mediante el módulo os.
        self.assets_dir = os.path.join("assets")
        self.sprite_dir = os.path.join(self.assets_dir, "sprites")
        self.font_dir = os.path.join(self.assets_dir, "font")
        # Cargamos un objeto font con tamaño de letra de 12
        self.font = pygame.font.Font(os.path.join(self.font_dir, "Retro Gaming.ttf"), 12)

    def load_states(self):
        # Creamos el primer estado/pantalla (el título) y lo incluimos como primer elemento de la pila de estados.
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)


if __name__ == "__main__":

    g = Game() # Creamos una instancia (objeto) de la clase Game.
    # Siempre que el objeto se cree la función init establecerá que el juego corre "self.running == True"
    while g.running:
        g.game_loop() # Si el juego "corre" invocamos la función del bucle básico.
