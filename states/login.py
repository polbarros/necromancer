import db
import models
from states.state import State
from states.choose import Choose
import pygame_gui
import pygame

class Login(State):
    """Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de login."""
    def __init__(self, game):
        State.__init__(self, game)

        """Establecemos el "manager" de la librería pygame_gui para poder operar con ella en los límites de la ventana
                 e indicamos el archivo JSON para hacer el theming de los elementos de la librería."""
        self.manager_login = pygame_gui.UIManager((self.game.W, self.game.H), "theme.json")

        # Cajas de texto para inputs
        self.box_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.game.W // 2 - 45,
                                                                                       self.game.H // 2),
                                                                                      (150, 30)),
                                                            manager=self.game.manager,
                                                            object_id='#name_text_entry')
        self.box_spell = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((self.game.W // 2 - 45,
                                                                                       self.game.H // 2 + 30),
                                                                                      (150, 30)),
                                                             manager=self.game.manager,
                                                             object_id='#spell_text_entry')
        self.box_spell.set_text_hidden(is_hidden=True) # Para ocultar el texto del password

        # Mensaje para comunicarse con el usuario (jugador).
        self.message = ''

        # Botones
        self.button_summon = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W // 2 - 94,
                                                                                     self.game.H // 2 + 75),
                                                                                    (200, 40)),
                                                          text="S U M M O N",
                                                          manager=self.game.manager,
                                                          object_id='#button_summon')
        self.button_new_necromancer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W // 2 - 94,
                                                                                     self.game.H // 2 + 120),
                                                                                    (200, 25)),
                                                          text="New Necromancer",
                                                          manager=self.game.manager,
                                                          object_id='#button_new_necromancer')

        # Establecemos que todos los jugadores registrados no están seleccionados
        self.players = db.session.query(models.Login).all()
        for player in self.players:
            player.selection = False
        db.session.commit()

        #Datos del jugador que inicia la partida
        self.necromancer = None



    def update(self, delta_time):

        # Obtenemos los contenidos de las cajas de texto.
        text_name = self.box_name.get_text() # Nombre
        text_spell = self.box_spell.get_text() # Password

        # Comprobamos que las cajas de texto estén llenas correctamente antes de pulsar los botones.
        if (len(text_name) == 0 or len(text_spell) < 8) and (self.button_summon.check_pressed() or
                                                                     self.button_new_necromancer.check_pressed()):
            self.message = "Write a name and a 8 caract. spell"


        # Comprobamos la existencia de los datos tras pulsar "SUMMON" y en caso positivo entramos al juego.
        elif (len(text_name) != 0 or len(text_spell) >= 8) and self.button_summon.check_pressed():
            self.necromancer = db.session.query(models.Login).filter_by(name=text_name, password=text_spell).first()
            if self.necromancer:
                self.necromancer.selection = True # Indicamos que el jugador está seleccionado
                db.session.commit()
                new_state = Choose(self.game) # Creamos estado nuevo. Objeto de la clase Choose.
                new_state.enter_state() # Entramos en el estado Choose.
            else:
                self.message = "Necromancer not found"

        # Comprobamos la existencia de los datos tras pulsar "New necromancer" y en caso negativo los registramos.
        elif (len(text_name) != 0 or len(text_spell) >= 8) and self.button_new_necromancer.check_pressed():
            necromancer_exist = db.session.query(models.Login).filter_by(name=text_name, password=text_spell).first()
            if necromancer_exist:
                self.message = "Necromancer already exist"
            else:
                # Creamos un nuevo objeto de la clase modelo Login que incluiremos en la base de datos.
                new_necromancer = models.Login(name=text_name, password=text_spell, max_score=0, selection=False)
                db.session.add(new_necromancer)
                self.message = "Necromancer registered successfully"
                db.session.commit()
        else:
            pass

    def render(self, display):

        # Color de fondo
        display.fill((197, 178, 189))
        # Texto de Lore y órdenes para el jugador
        self.game.draw_text(display, "You, Necromancer", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 200)
        self.game.draw_text(display, "Your mission is to fight", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 175)
        self.game.draw_text(display, "against the Shogun.", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 160)
        self.game.draw_text(display, "Rise a death warrior", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 135)
        self.game.draw_text(display, "with your dark powers.", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 120)
        self.game.draw_text(display, "Write down your name,", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 95)
        self.game.draw_text(display, "and your secret spell.", (57, 44, 49), self.game.W // 2, self.game.H // 2 - 80)
        # Área para mensajes para el usuario
        self.game.draw_text(display, self.message, (206, 9, 43), self.game.W // 2, self.game.H // 2 - 15)
        # Texto para los títulos de las cajas de texto.
        self.game.draw_text(display, "Name", (57, 44, 49), self.game.W // 2 - 75, self.game.H // 2 + 15)
        self.game.draw_text(display, "Spell", (57, 44, 49), self.game.W // 2 - 75, self.game.H // 2 + 45)
        # Función para dibujar todos los elementos de pygame_gui iniciados en el constructor (__init__).
        self.game.manager.draw_ui(display)
