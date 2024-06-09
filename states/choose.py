import db
import models
from states.state import State
from states.combat import Combat
import ui
import os
import pygame

class Choose(State):
    '''Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de selección
    de personaje.'''

    first_time = True

    def __init__(self, game):
        State.__init__(self, game)

        #Opciones de personajes

        #SAMURAI
        self.samurai_button_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "samurai_tiny.png"))
        self.samurai_button_img.set_colorkey([0, 0, 0]) # Quitar el fondo negro.
        self.samurai_button_img_h = pygame.image.load(os.path.join(self.game.assets_dir,
                                                                   "sprites", "samurai_tiny_h.png"))
        self.samurai_button_img_h.set_colorkey([0, 0, 0]) # Quitar el fondo negro.
        self.samurai_button = ui.Button(70, 110,
                                        self.samurai_button_img, self.samurai_button_img_h, 1)
        self.samurai_stance_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_1.png"))

        #KUNOICHI
        self.kunoichi_button_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "kunoichi_tiny.png"))
        self.kunoichi_button_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.kunoichi_button_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites",
                                                                    "kunoichi_tiny_h.png"))
        self.kunoichi_button_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.kunoichi_button = ui.Button((500 // 2) + 65, 110,
                                        self.kunoichi_button_img, self.kunoichi_button_img_h, 1)
        self.kunoichi_stance_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_2.png"))

        #ASHIGARU
        self.ashigaru_button_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "ashigaru_tiny.png"))
        self.ashigaru_button_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.ashigaru_button_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites",
                                                                    "ashigaru_tiny_h.png"))
        self.ashigaru_button_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.ashigaru_button = ui.Button(75, 365,
                                         self.ashigaru_button_img, self.ashigaru_button_img_h, 1)
        self.ashigaru_stance_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_3.png"))

        #INUGAMI
        self.inugami_button_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "inugami_tiny.png"))
        self.inugami_button_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.inugami_button_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites",
                                                                   "inugami_tiny_h.png"))
        self.inugami_button_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.inugami_button = ui.Button((500 // 2) + 60, 360,
                                         self.inugami_button_img, self.inugami_button_img_h, 1)
        self.inugami_stance_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_4.png"))

        # -- ESCENARIO DE COMBATE --
        self.scenario = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "combat_bg_cover.png"))
        self.scenario.set_colorkey([0, 0, 0])  # Quitar el fondo negro.


    def update(self, delta_time):

        if not Choose.first_time:
            new_state = Combat(self.game)  # Creamos un objeto de la clase estado de combate.
            new_state.enter_state()  # El nuevo estado se añade a la pila de estados.

        else:
            if self.samurai_button.action():
                new_samurai = models.Warrior(name= "Samurai",
                                                 level=1,
                                                 exp= 0,
                                                 hp_max=50,
                                                 hp_current=50,
                                                 dmg_base=0,
                                                 dmg_necrotic=1,
                                                 dmg_radiant=1,
                                                 bomb=1,
                                                 heal=1,
                                                 strategy_attack=True,
                                                 power_strike=True,
                                                 res_radiant=1,
                                                 res_necrotic=2,
                                                 armor=3,
                                                 stance=1,
                                                 stance_weak=False,
                                                 stance_recovery=1,
                                                 attack_roll=20,
                                                 roll_recovery=1,
                                                 type="player")

                db.session.query(models.Warrior).delete()
                db.session.add(new_samurai)
                db.session.commit()
                new_state = Combat(self.game) # Creamos un objeto de la clase estado de combate.
                new_state.enter_state() # El nuevo estado se añade a la pila de estados.
            elif self.kunoichi_button.action():
                new_kunoichi = models.Warrior(name="Kunoichi",
                                                  level=1,
                                                  exp=0,
                                                  hp_max=50,
                                                  hp_current=50,
                                                  dmg_base=0,
                                                  dmg_necrotic=2,
                                                  dmg_radiant=1,
                                                  bomb=1,
                                                  heal=1,
                                                  strategy_attack=True,
                                                  power_strike=True,
                                                  res_radiant=0,
                                                  res_necrotic=1,
                                                  armor=1,
                                                  stance=2,
                                                  stance_weak=False,
                                                  stance_recovery=1,
                                                  attack_roll=20,
                                                  roll_recovery=1,
                                                  type="player")

                db.session.query(models.Warrior).delete()
                db.session.add(new_kunoichi)
                db.session.commit()
                new_state = Combat(self.game) # Creamos un objeto de la clase estado de combate.
                new_state.enter_state() # El nuevo estado se añade a la pila de estados.
            elif self.ashigaru_button.action():
                new_ashigaru = models.Warrior(name="Ashigaru",
                                                  level=1,
                                                  exp=0,
                                                  hp_max=50,
                                                  hp_current=50,
                                                  dmg_base=0,
                                                  dmg_necrotic=0,
                                                  dmg_radiant=0,
                                                  bomb=1,
                                                  heal=1,
                                                  strategy_attack=True,
                                                  power_strike=True,
                                                  res_radiant=1,
                                                  res_necrotic=0,
                                                  armor=2,
                                                  stance=3,
                                                  stance_weak=False,
                                                  stance_recovery=1,
                                                  attack_roll=20,
                                                  roll_recovery=1,
                                                  type="player")

                db.session.query(models.Warrior).delete()
                db.session.add(new_ashigaru)
                db.session.commit()
                new_state = Combat(self.game) # Creamos un objeto de la clase estado de combate.
                new_state.enter_state() # El nuevo estado se añade a la pila de estados.
            elif self.inugami_button.action():
                new_inugami = models.Warrior(name="Inugami",
                                                 level=1,
                                                 exp=0,
                                                 hp_max=50,
                                                 hp_current=50,
                                                 dmg_base=0,
                                                 dmg_necrotic=5,
                                                 dmg_radiant=1,
                                                 bomb=1,
                                                 heal=1,
                                                 strategy_attack=True,
                                                 power_strike=True,
                                                 res_radiant=2,
                                                 res_necrotic=3,
                                                 armor=1,
                                                 stance=4,
                                                 stance_weak=False,
                                                 stance_recovery=1,
                                                 attack_roll=20,
                                                 roll_recovery=1,
                                                 type="player")

                db.session.query(models.Warrior).delete()
                db.session.add(new_inugami)
                db.session.commit()
                new_state = Combat(self.game) # Creamos un objeto de la clase estado de combate.
                new_state.enter_state() # El nuevo estado se añade a la pila de estados.

    def render(self, display):

        if not Choose.first_time:
            # Color de fondo
            display.fill((197, 178, 189))
            # ESCENARIO
            display.blit(self.scenario, (0, 0))
        else:
            # Color de fondo
            display.fill((197, 178, 189))
            # Texto superior
            self.game.draw_text(display, "Choose your warrior", (57, 44, 49), self.game.W // 2, 65)
            # Botones (dibujados)
            self.samurai_button.draw(display)
            self.kunoichi_button.draw(display)
            self.ashigaru_button.draw(display)
            self.inugami_button.draw(display)
            # Texto: rasgos de los guerreros (se muestran al pasar el cursor por encima)
            if self.samurai_button.hovered:
                self.game.draw_text(display, "SAMURAI", (57, 44, 49), self.game.W // 2, self.game.H - 150)
                self.game.draw_text_left(display, "Armament:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 120)
                self.game.draw_text_left(display, "Uchigatana and wakisashi 2d6", (98, 105, 106), self.game.W // 2 - 47, self.game.H - 120)
                self.game.draw_text_left(display, "Strategic attack:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 105)
                self.game.draw_text_left(display, "Vampire slash", (98, 105, 106), self.game.W // 2 + 10, self.game.H - 105)
                self.game.draw_text_left(display, "Powerful strike:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 90)
                self.game.draw_text_left(display, "Triple death", (98, 105, 106), self.game.W // 2, self.game.H - 90)
                self.game.draw_text_left(display, "Stance:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 75)
                display.blit(self.samurai_stance_img, (self.game.W // 2 - 60, self.game.H - 72))
                self.game.draw_text_left(display, "Armor:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 60)
                self.game.draw_text_left(display, "3", (98, 105, 106), self.game.W // 2 - 73, self.game.H - 60)
            if self.kunoichi_button.hovered:
                self.game.draw_text(display, "KUNOICHI", (57, 44, 49), self.game.W // 2, self.game.H - 150)
                self.game.draw_text_left(display, "Armament: ", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 120)
                self.game.draw_text_left(display, "Kusarigama and kunai 3d4", (98, 105, 106), self.game.W // 2 - 47, self.game.H - 120)
                self.game.draw_text_left(display, "Strategic attack:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 105)
                self.game.draw_text_left(display, "Fatal flaw", (98, 105, 106), self.game.W // 2 + 10, self.game.H - 105)
                self.game.draw_text_left(display, "Powerful strike: ", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 90)
                self.game.draw_text_left(display, "Wasp rain", (98, 105, 106), self.game.W // 2, self.game.H - 90)
                self.game.draw_text_left(display, "Stance:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 75)
                display.blit(self.kunoichi_stance_img, (self.game.W // 2 - 60, self.game.H - 72))
                self.game.draw_text_left(display, "Armor:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 60)
                self.game.draw_text_left(display, "1", (98, 105, 106), self.game.W // 2 - 73, self.game.H - 60)
            if self.ashigaru_button.hovered:
                self.game.draw_text(display, "ASHIGARU", (57, 44, 49), self.game.W // 2, self.game.H - 150)
                self.game.draw_text_left(display, "Armament:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 120)
                self.game.draw_text_left(display, "Yari and arquebus 1d12", (98, 105, 106), self.game.W // 2 - 47, self.game.H - 120)
                self.game.draw_text_left(display, "Strategic attack:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 105)
                self.game.draw_text_left(display, "Direct shot", (98, 105, 106), self.game.W // 2 + 10, self.game.H - 105)
                self.game.draw_text_left(display, "Powerful strike:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 90)
                self.game.draw_text_left(display, "Force and fire", (98, 105, 106), self.game.W // 2, self.game.H - 90)
                self.game.draw_text_left(display, "Stance:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 75)
                display.blit(self.ashigaru_stance_img, (self.game.W // 2 - 60, self.game.H - 72))
                self.game.draw_text_left(display, "Armor:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 60)
                self.game.draw_text_left(display, "2", (98, 105, 106), self.game.W // 2 - 73, self.game.H - 60)
            if self.inugami_button.hovered:
                self.game.draw_text(display, "INUGAMI", (57, 44, 49), self.game.W // 2, self.game.H - 150)
                self.game.draw_text_left(display, "Armament:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 120)
                self.game.draw_text_left(display, "Kojyutsu sorcery 2d4", (98, 105, 106), self.game.W // 2 - 47, self.game.H - 120)
                self.game.draw_text_left(display, "Strategic attack:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 105)
                self.game.draw_text_left(display, "Curse of revenge", (98, 105, 106), self.game.W // 2 + 10, self.game.H - 105)
                self.game.draw_text_left(display, "Powerful strike:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 90)
                self.game.draw_text_left(display, "Putrid bite", (98, 105, 106), self.game.W // 2, self.game.H - 90)
                self.game.draw_text_left(display, "Stance:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 75)
                display.blit(self.inugami_stance_img, (self.game.W // 2 - 60, self.game.H - 72))
                self.game.draw_text_left(display, "Armor:", (57, 44, 49), self.game.W // 2 - 130, self.game.H - 60)
                self.game.draw_text_left(display, "1", (98, 105, 106), self.game.W // 2 - 73, self.game.H - 60)
