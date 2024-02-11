import random
import db
import models
from sqlalchemy import desc
import pygame, os
from states.state import State
import ui

class Reward(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self,game)

        # Establecemos el fondo del menú
        self.menu_bg = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "reward_bg.png"))
        self.menu_rect = self.menu_bg.get_rect()
        self.menu_rect.center = (self.game.GAME_W * 0.5, self.game.GAME_H * 0.5)

        #Posibles recompensas
        #Botón de recompensa ofensiva
        self.offensive_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "offensive.png"))
        self.offensive_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro que ocupa el espacio de la transparencia.
        self.offensive_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "offensive_h.png"))
        self.offensive_img_h.set_colorkey([0, 0, 0])  #Quitar el fondo negro de la transparencia.
        self.offensive_button = ui.Button((500 // 2) - 200, 800 - 130, self.offensive_img, self.offensive_img_h, 1)
        #Botón de recompensa defensiva
        self.defensive_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "defensive.png"))
        self.defensive_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro que ocupa el espacio de la transparencia.
        self.defensive_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "defensive_h.png"))
        self.defensive_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro de la transparencia.
        self.defensive_button = ui.Button((500 // 2) - 200, 800 - 130, self.defensive_img, self.defensive_img_h, 1)
        #Diccionarios de recompensas
        self.offensive_dict = {1:"Increase Physical Damage +1",
                               2:"Get +1 Bomb",
                               3:"Recover Strategic attack",
                               4:"Recover Powerful Strike",
                               5:"Get +1 d20 Attack Roll recovery"}
        self.defensive_dict = {1:"Increase +10 HP Max",
                               2:"Instant complete healing",
                               3:"Get +1 Heal",
                               4:"Increase Armor +1",
                               5:"Get +1 Stance recovery"}

        # -- Recogemos información de la BD --
        # Toma de la información de la BD sobre el guerrero escogido
        self.warrior = db.session.query(models.Warrior).filter_by(type="player").first()
        # Toma de la información de la BD sobre el último enemigo generado
        self.last_enemy = db.session.query(models.Warrior).filter_by(type="enemy").order_by(
            desc(models.Warrior.id)).first()

        # Recompensas ofrecidas
        self.offensive_offer = random.randint(1, 5)
        if ((self.offensive_offer == 3 and self.warrior.strategy_attack == True) or
                (self.offensive_offer == 4 and self.warrior.power_strike == True)):
            self.offensive_offer = 1
        self.defensive_offer = random.randint(1, 5)

        #Llamamos a la función lvl_up para subir el nivel del guerrero seleccionado
        self.lvl_up(self.last_enemy.hp_max)

        # Textos básicos
        self.title_txt = "Enemy slayed"
        self.exp_text = "{} won {} EXP".format(self.warrior.name, self.last_enemy.hp_max)
        self.choose_text = "Choose a reward"

    def lvl_up(self, exp):
        #Función para hacer subir el nivel del guerrero seleccionado, dependiendo de la vida máxima último enemigo.
        for i in range(exp):
            if exp %100 == 0:
                self.warrior.level += 1

    def update(self, delta_time):
        if self.offensive_button.action():
            if self.offensive_offer == 1:
                self.warrior.dmg_base += 1
            elif self.offensive_offer == 2:
                self.warrior.bomb += 1
            elif self.offensive_offer == 3:
                self.warrior.strategy_attack = True
            elif self.offensive_offer == 4:
                self.warrior.power_strike = True
            elif self.offensive_offer == 5:
                self.warrior.roll_recovery += 1
            else:
                pass
            self.come_back()
        elif self.defensive_button.action():
            if self.defensive_offer == 1:
                self.warrior.hp_max += 10
            elif self.defensive_offer == 2:
                self.warrior.hp_current = self.warrior.hp_max
            elif self.defensive_offer == 3:
                self.warrior.heal += 1
            elif self.defensive_offer == 4:
                self.warrior.armor += 1
            elif self.defensive_offer == 5:
                self.warrior.stance_recovery += 1
            else:
                pass
            self.come_back()

    def come_back(self):
        db.session.commit()
        while len(self.game.state_stack) > 1:
            self.game.state_stack.pop()

    def render(self, display):
        #Renderizamos la pantalla de combate detrás del menu de recompensa
        self.prev_state.render(display)
        display.blit(self.menu_bg, self.menu_rect)

        #Renderizamos botones de selección de recompensa
        self.offensive_button.draw(display)
        self.defensive_button.draw(display)

        #Renderizamos texto básico
        self.game.draw_text(display, self.title_txt, (57, 44, 49), self.game.W // 2,
                                self.game.H - 150)
        self.game.draw_text(display, self.exp_text, (57, 44, 49), self.game.W // 2,
                            self.game.H - 150)
        self.game.draw_text(display, self.choose_text, (57, 44, 49), self.game.W // 2,
                            self.game.H - 150)

        #Renderizamos texto explicativo de recompensa
        if self.offensive_button.hovered:
            self.game.draw_text(display, self.offensive_dict[self.offensive_offer], (57, 44, 49), self.game.W // 2,
                                self.game.H - 150)
        elif self.defensive_button.hovered:
            self.game.draw_text(display, self.defensive_dict[self.defensive_offer], (57, 44, 49), self.game.W // 2,
                                self.game.H - 150)

