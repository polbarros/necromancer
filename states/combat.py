import animations
import db
import models
from sqlalchemy import desc
from states.state import State
from states.reward import Reward
from states.over import Over
import pygame_gui
import os
import pygame
import random


class Combat(State):
    """Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de combate."""

    def __init__(self, game):
        State.__init__(self, game)
        # El manager de pygame_gui para el estado de combate
        # Debemos crear un nuevo manager porque de lo contrario cargaría los elementos de otros estados.
        self.manager_combat = pygame_gui.UIManager((self.game.W, self.game.H), "theme.json")

        # -- ESCENARIO DE COMBATE --
        self.scenario = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "combat_bg_cover.png"))
        self.scenario.set_colorkey([0, 0, 0])  # Quitar el fondo negro.

        # -- ANIMACIONES --
        # Lista que acumulará las instancias de animaciones para ser incorporadas al grupo de sprites.
        self.sprites = []
        #Hacemos una lista aparte para las animaciones de ataque para poder reproducirlas aparte en otra "capa"
        self.sprites_att =[]

        # -- GUERRERO ESCOGIDO --
        # Toma de la información de la BD sobre el guerrero escogido
        self.warrior = db.session.query(models.Warrior).filter_by(type="player").first()

        # Imágen y animaciones del guerrero escogido
        if self.warrior.name == "Samurai":
            self.warrior_img = pygame.image.load(os.path.join(self.game.sprite_dir, "samurai.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.sprite_dir, "stance_1.png"))
            # Instancias de animaciones del Samurai
            self.warrior_ani_dmg = animations.Animation(-30, self.game.H - 500, "samurai_dmg")
            self.warrior_ani_pwr = animations.Animation(self.game.W - 256, 30, "samurai_pwr")
            self.sprites.append(self.warrior_ani_dmg)
            self.sprites_att.append(self.warrior_ani_pwr)
        elif self.warrior.name == "Kunoichi":
            self.warrior_img = pygame.image.load(os.path.join(self.game.sprite_dir, "kunoichi.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.sprite_dir, "stance_2.png"))
            # Instancias de animaciones de la Kunoichi
            self.warrior_ani_dmg = animations.Animation(15, self.game.H - 446, "kunoichi_dmg")
            self.warrior_ani_pwr = animations.Animation(self.game.W - 320, 60, "kunoichi_pwr")
            self.sprites.append(self.warrior_ani_dmg)
            self.sprites_att.append(self.warrior_ani_pwr)
        elif self.warrior.name == "Ashigaru":
            self.warrior_img = pygame.image.load(os.path.join(self.game.sprite_dir, "ashigaru.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.sprite_dir, "stance_3.png"))
            # Instancias de animaciones del Ashigaru
            self.warrior_ani_dmg = animations.Animation(-85, self.game.H - 524, "ashigaru_dmg")
            self.warrior_ani_pwr = animations.Animation(self.game.W - 256, 0, "ashigaru_pwr")
            self.sprites.append(self.warrior_ani_dmg)
            self.sprites_att.append(self.warrior_ani_pwr)
        elif self.warrior.name == "Inugami":
            self.warrior_img = pygame.image.load(os.path.join(self.game.sprite_dir, "inugami.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.sprite_dir, "stance_4.png"))
            # Instancias de animaciones del Inugami
            self.warrior_ani_dmg = animations.Animation(-30, self.game.H - 476, "inugami_dmg")
            self.warrior_ani_pwr = animations.Animation(self.game.W - 256, 0, "inugami_pwr")
            self.sprites.append(self.warrior_ani_dmg)
            self.sprites_att.append(self.warrior_ani_pwr)

        # -- GUERRERO ENEMIGO --
        # Datos para los enemigos: nivel y puntos de salud.
        level_enemy = random.randint(self.warrior.level, self.warrior.level + 1)
        health_enemy = random.randint(30, 35) + (self.warrior.level * 2)
        dmg_base_enemy = level_enemy // 2
        # Valores posibles de los enemigos. Tuplas con los datos para crear objetos.
        tuple_miko = ("Guardian Miko", level_enemy, 0, health_enemy, health_enemy, dmg_base_enemy,
                      0, 4, 0, 0, True, True, 2, 2, 1, 4, False, 0, 20, 0, "enemy")
        tuple_ministry = ("Swordsman of Ministry", level_enemy, 0, health_enemy, health_enemy, dmg_base_enemy,
                          0, 0, 0, 0, True, True, 1, 1, 2, 1, False, 0, 20, 0, "enemy")
        tuple_shinobi = ("Lone Shinobi", level_enemy, 0, health_enemy, health_enemy, dmg_base_enemy,
                         2, 3, 0, 0, True, True, 1, 2, 1, 2, False, 0, 20, 0, "enemy")
        tuple_kappas = ("Gang of Kappas", level_enemy, 0, health_enemy, health_enemy, dmg_base_enemy,
                        4, 0, 0, 0, True, True, 0, 3, 3, 3, False, 0, 20, 0, "enemy")
        # Diccionario de enemigos
        self.dict_enemies = {1: tuple_miko,
                             2: tuple_ministry,
                             3: tuple_shinobi,
                             4: tuple_kappas}


        # Desempaquetamos las tuplas como parámetros para crear el objeto de la clase Warrior.
        new_enemy = models.Warrior(*self.dict_enemies[random.randint(1, 4)]) # Creamos un nuevo enemigo
        db.session.add(new_enemy) # Añadimos el nuevo enemigo a la base de datos.
        db.session.commit() # Guardamos el registro.

        # Toma de la información de la BD sobre el último enemigo generado
        self.last_enemy = db.session.query(models.Warrior).filter_by(type="enemy").order_by(
            desc(models.Warrior.id)).first()

        # -- ÚLTIMO ENEMIGO --
        # Generamos las instancias de animaciones de los enemigos y añadimos al grupo de sprites.
        if self.last_enemy.name == "Guardian Miko":
            # Instancias de animaciones de la Guardian Miko
            self.last_enemy_ani_dmg = animations.Animation(self.game.W - 256, 40, "miko_dmg")
            self.sprites.append(self.last_enemy_ani_dmg)
        elif self.last_enemy.name == "Swordsman of Ministry":
            # Instancias de animaciones del Swordsman of Ministry
            self.last_enemy_ani_dmg = animations.Animation(self.game.W - 256, 0, "ministry_dmg")
            self.sprites.append(self.last_enemy_ani_dmg)
        elif self.last_enemy.name == "Lone Shinobi":
            # Instancias de animaciones del Lone Shinobi
            self.last_enemy_ani_dmg = animations.Animation(self.game.W - 256, 0, "shinobi_dmg")
            self.sprites.append(self.last_enemy_ani_dmg)
        elif self.last_enemy.name == "Gang of Kappas":
            # Instancias de animaciones del Gang of Kappas
            self.last_enemy_ani_dmg = animations.Animation(self.game.W - 256, 90, "kappas_dmg")
            self.sprites.append(self.last_enemy_ani_dmg)

        # Cargamos las imágenes de las barras de postura de los enemigos
        self.enemy_stancebar_img_1 = pygame.image.load(
            os.path.join(self.game.sprite_dir, "stance_1_enemy.png"))
        self.enemy_stancebar_img_2 = pygame.image.load(
            os.path.join(self.game.sprite_dir, "stance_2_enemy.png"))
        self.enemy_stancebar_img_3 = pygame.image.load(
            os.path.join(self.game.sprite_dir, "stance_3_enemy.png"))
        self.enemy_stancebar_img_4 = pygame.image.load(
            os.path.join(self.game.sprite_dir, "stance_4_enemy.png"))



        # -- OTROS ELEMENTOS --
        # El símbolo para indicar la armadura del guerrero seleccionado y el enemigo
        self.warrior_armor_img = pygame.image.load(os.path.join(self.game.sprite_dir, "armor.png"))
        self.last_enemy_armor_img = pygame.image.load(os.path.join(self.game.sprite_dir, "armor_enemy.png"))
        # Imagen de la barra de postura debilitada
        self.stance_weak_img = pygame.image.load(os.path.join(self.game.sprite_dir, "stance_weak.png"))

        # UI BARRAS DE SALUD
        # Barra de salud del guerrero seleccionado
        self.warrior_health_bar = pygame_gui.elements.ui_status_bar.UIStatusBar(
            relative_rect=pygame.Rect((self.game.W - 180, self.game.H // 2 + 93), (170, 24)),
            manager=self.manager_combat,
            percent_method=self.calculate_health_percent,
            object_id='#warrior_health_bar')

        self.last_enemy_health_bar = pygame_gui.elements.ui_status_bar.UIStatusBar(
            relative_rect=pygame.Rect((28, 93), (170, 24)),
            manager=self.manager_combat,
            percent_method=self.calculate_enemy_health_percent,
            object_id='#last_enemy_health_bar')

        # UI BOTONES DE COMBATE (y animaciones asociadas)
        self.button_attack_1d20 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 180,
                                                                                     self.game.H // 2 + 150),
                                                                                    (167, 40)),
                                                               text="ATTACK ROLL 1d20",
                                                               manager=self.manager_combat,
                                                               tool_tip_text="Roll a dice of <b>20</b> sides to attack",
                                                               object_id='#button_attack_1d20')

        self.button_attack_1d12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 180,
                                                                                          self.game.H // 2 + 150),
                                                                                         (167, 40)),
                                                               text="ATTACK ROLL 1d12",
                                                               manager=self.manager_combat,
                                                               tool_tip_text="Roll a dice of <b>12</b> sides to attack",
                                                               object_id="#button_attack_1d12")

        self.button_strategic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 180,
                                                                                          self.game.H // 2 + 195),
                                                                                         (80, 40)),
                                                               text="STR",
                                                               manager=self.manager_combat,
                                                             tool_tip_text="Execute a\n<b>Strategic attack</b>",
                                                               object_id='#button_strategic')
        self.button_powerful = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 93,
                                                                                        self.game.H // 2 + 195),
                                                                                       (80, 40)),
                                                             text="PWR",
                                                             manager=self.manager_combat,
                                                            tool_tip_text="Execute a\n<b>Powerful strike</b>",
                                                             object_id='#button_powerful')
        self.button_heal = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 179,
                                                                                       self.game.H // 2 + 240),
                                                                                      (40, 40)),
                                                            text="",
                                                            manager=self.manager_combat,
                                                        tool_tip_text="Recover all Hit Points (<i>health</i>)",
                                                            object_id='#button_heal')
        self.button_bomb = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 137,
                                                                                       self.game.H // 2 + 240),
                                                                                      (40, 40)),
                                                            text="",
                                                            manager=self.manager_combat,
                                                        tool_tip_text="Throw a bomb\n(30-50 dmg)",
                                                            object_id='#button_bomb')
        self.bomb_ani = animations.Animation(self.game.W - 256, 0, "bomb")
        self.sprites_att.append(self.bomb_ani)

        self.button_r_stance = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 95,
                                                                                       self.game.H // 2 + 240),
                                                                                      (40, 40)),
                                                            text="",
                                                            manager=self.manager_combat,
                                                            tool_tip_text="Recover Stance",
                                                            object_id='#button_r_stance')
        self.button_r_roll = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 53,
                                                                                       self.game.H // 2 + 240),
                                                                                      (40, 40)),
                                                            text="",
                                                            manager=self.manager_combat,
                                                          tool_tip_text="Recover attack roll",
                                                            object_id='#button_r_roll')

        # Caja de texto para comunicarse con el usuario
        self.text_box = pygame_gui.elements.UITextBox(html_text="<b>FIGHT</b>",
                                                      relative_rect=pygame.Rect((100,
                                                                                 240),
                                                                                (300, 150)),
                                                      manager=self.manager_combat,
                                                      wrap_to_height=True,
                                                      object_id='#text_box_message')
        self.text_box.hide()  # Escondemos la caja de texto para mensajes.

        # Botón de "sacrificio" para salir de la partida
        self.button_sacrifice = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 160,
                                                                                          self.game.H - 40),
                                                                                         (147, 30)),
                                                               text="Sacrifice",
                                                               manager=self.manager_combat,
                                                               tool_tip_text="Discard this warrior",
                                                               object_id="#button_attack_1d12")


        # Elementos operativos para el combate
        self.roll = None # Resultado de la tirada de dados para hacer ataques básicos.
        self.judgment = None # Veredicto tras contraponer la tirada (roll) del attacker con al postura del target.
        self.list_dices = None # Lista de tiradas de dados de la función roll_damage
        self.amount = 0 # Cantidad de puntos de vida para quitar.
        self.ends_player = False # Confirmación de finalización del turno del guerrero seleccionado (jugador)
        self.ends_enemy = True # Confirmación de finalización del turno del último enemigo
        self.space_key = False # Estado del uso de la barra espaciadora
        self.i_message = "" # Mensaje que deberá mostrarse en la text_box.

        # ANIMACIONES (AGRUPACIÓN)
        # Personajes (guerrero y enemigo)
        # Creamos los sprites y los grupos (elementos propios de pygame para animar)
        self.moving_sprites = pygame.sprite.Group() # Se crea un grupo de sprites para manejarlos a la vez.
        self.moving_sprites.add(*self.sprites) # Se añade la lista de animaciones al grupo de sprites.
        # El asterisco (*) descomprime la lista en argumentos individuales

        # Ataques (aparte para poder superponer sobre los sprites de los personajes)
        # Creamos los sprites y los grupos (elementos propios de pygame para animar)
        self.moving_sprites_att = pygame.sprite.Group()  # Se crea un grupo de sprites para manejarlos a la vez.
        self.moving_sprites_att.add(*self.sprites_att)  # Se añade la lista de animaciones al grupo de sprites.
        # El asterisco (*) descomprime la lista en argumentos individuales

        # Agrupación de sprites para textos animados para mostrar los daños
        self.damage_text_group = pygame.sprite.Group()

    def calculate_health_percent(self):
        # Función para calcular el porcentaje de salud del guerrero seleccionado (para la barra de salud).
        return (self.warrior.hp_current/self.warrior.hp_max)*100

    def calculate_enemy_health_percent(self):
        # Función para calcular el porcentaje de salud del último enemigo (para la barra de salud).
        return (self.last_enemy.hp_current/self.last_enemy.hp_max)*100

    def update(self, delta_time):

        # Toma de la información de la BD sobre el último enemigo generado
        self.last_enemy = db.session.query(models.Warrior).filter_by(type="enemy").order_by(
            desc(models.Warrior.id)).first()

        # Actualizador del manager de los elementos pygame_gui
        self.manager_combat.update(delta_time)

        # Actualiza los efectos animados y otros elementos de la caja de texto de mensajes para el jugador
        self.text_box.update(delta_time)
        self.text_box.update_text_effect(delta_time)

        # Actualiza el grupo de sprites y establecemos una velocidad de animación
        self.moving_sprites.update(0.2)
        self.moving_sprites_att.update(0.2)

        # Actualiza los textos que muestran en daño en pantalla
        self.damage_text_group.update()

        # Condiciones para la presentación de botones de ataque simple
        if self.warrior.attack_roll == 20:
            self.button_attack_1d12.hide()
            self.button_attack_1d20.show()
        elif self.warrior.attack_roll == 12:
            self.button_attack_1d20.hide()
            self.button_attack_1d12.show()

        # Condiciones para la presentación de botón de ataque estratégico
        if not self.warrior.strategy_attack:
            self.button_strategic.disable()

        # Condiciones para la presentación de botón de ataque poderoso
        if not self.warrior.power_strike:
            self.button_powerful.disable()

        # Condiciones para la presentación de botones de consumibles
        if self.warrior.heal == 0:
            self.button_heal.disable()
        if self.warrior.bomb == 0:
            self.button_bomb.disable()
        if self.warrior.stance_recovery == 0:
            self.button_r_stance.disable()
        if self.warrior.roll_recovery == 0:
            self.button_r_roll.disable()

        # Actualiza la barra de salud del guerrero seleccionado
        self.warrior_health_bar.update(delta_time)

        if self.warrior.hp_current > 0 and self.last_enemy.hp_current > 0:
            # Mientras los puntos de guerrero seleccionado y el último enemigo sean superiores a 0.
            if self.ends_enemy == True and self.ends_player == False and self.space_key == False:
                self.enable_buttons()  # Habilitamos los botones para el jugador.
                self.i_message = ''
                self.text_box.hide()  # Escondemos la caja de texto
                self.player_turn() # Llamamos a la función que inicia el turno del jugador.

                self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})

                if self.space_key:
                    self.i_message = ''
                    self.text_box.hide()  # Escondemos la caja de texto

            elif self.ends_player == True and self.ends_enemy == False and self.space_key == True:
                self.i_message = ''
                self.text_box.hide()  # Escondemos la caja de texto
                self.enemy_turn() # Llamamos a la función que inicia el turno del enemigo.

                self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})

        elif self.warrior.hp_current <= 0 and self.space_key == True:
            self.i_message = ''
            self.text_box.hide()  # Escondemos la caja de texto
            db.session.commit()
            new_state = Over(self.game)  # Creamos un objeto de la clase estado de recompensa.
            new_state.enter_state()  # El nuevo estado se añade a la pila de estados.


        elif self.last_enemy.hp_current <= 0 and self.space_key == True:
            self.i_message = ''
            self.text_box.hide()  # Escondemos la caja de texto
            db.session.commit()
            new_state = Reward(self.game)  # Creamos un objeto de la clase estado de recompensa.
            new_state.enter_state()  # El nuevo estado se añade a la pila de estados.

    def player_turn(self):
        if self.warrior.attack_roll == 20 and self.button_attack_1d20.check_pressed():
            self.roll_attack(20)
            self.receive_attack(self.last_enemy, self.roll)
            self.roll_damage(self.warrior)
            self.get_damage(self.warrior, self.last_enemy, self.judgment, self.list_dices)
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.ends_player, self.ends_enemy = True, False
            self.message(self.i_message)

        elif self.warrior.attack_roll == 12 and self.button_attack_1d12.check_pressed():
            self.roll_attack(12)
            self.receive_attack(self.last_enemy, self.roll)
            self.roll_damage(self.warrior)
            self.get_damage(self.warrior, self.last_enemy, self.judgment, self.list_dices)
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.ends_player, self.ends_enemy = True, False
            self.message(self.i_message)

        elif self.button_strategic.check_pressed() and self.warrior.strategy_attack:
            self.str_attack(self.warrior)
            self.warrior.strategy_attack = False # El guerrero pierde la capacidad de ataque estratégico
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.ends_player, self.ends_enemy = True, False
            self.message(self.i_message)

        elif self.button_powerful.check_pressed() and self.warrior.power_strike:
            self.pwr_attack(self.warrior)
            self.warrior.power_strike = False  # El guerrero pierde la capacidad de ataque poderoso
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.ends_player, self.ends_enemy = True, False
            self.message(self.i_message)

        elif self.warrior.heal >= 1 and self.button_heal.check_pressed():
            self.warrior.hp_current = self.warrior.hp_max  # Curamos la salud del guerrero seleccionado al completo.
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.warrior.heal -= 1
            self.ends_player, self.ends_enemy = True, False
            self.i_message = '{} healed<br>[SPACE] to continue'.format(self.warrior.name)
            self.message(self.i_message)

        elif self.warrior.bomb >= 1 and self.button_bomb.check_pressed():
            self.bomb_ani.animate()  # Animación de bomba
            self.last_enemy.hp_current -= random.randint(30, 50)  # El enemigo pierde mucha vida.
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.warrior.bomb -= 1
            self.ends_player, self.ends_enemy = True, False
            self.i_message = '{} trowed a bomb<br>[SPACE] to continue'.format(self.warrior.name)
            self.message(self.i_message)

        elif self.warrior.stance_recovery >= 1 and self.warrior.stance_weak and self.button_r_stance.check_pressed():
            self.warrior.stance_weak = False
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.warrior.stance_recovery -= 1
            self.ends_player, self.ends_enemy = True, False
            self.i_message = '{} recovered the stance<br>[SPACE] to continue'.format(self.warrior.name)
            self.message(self.i_message)

        elif self.warrior.roll_recovery >= 1 and self.warrior.attack_roll != 20 and self.button_r_roll.check_pressed():
            self.warrior.attack_roll = 20
            self.disable_buttons()  # Deshabilitamos botones para el jugador.
            self.warrior.roll_recovery -= 1
            self.ends_player, self.ends_enemy = True, False
            self.i_message = '{} recovered the roll attack<br>[SPACE] to continue'.format(self.warrior.name)
            self.message(self.i_message)

        # Opción para salir del combate sacrificando al guerrero seleccionado para escoger otro
        elif self.button_sacrifice.check_pressed():
            from states.choose import Choose
            Choose.first_time = True  # Volvemos a considerar la pantalla de Choose como nueva
            self.exit_state(-1) # Salimos del combate y lo borramos del stack de estados.

    def disable_buttons(self):
        # Deshabilitamos los botones para el jugador
        self.button_attack_1d20.disable()
        self.button_attack_1d12.disable()
        self.button_strategic.disable()
        self.button_powerful.disable()
        self.button_heal.disable()
        self.button_bomb.disable()
        self.button_r_stance.disable()
        self.button_r_roll.disable()
        self.button_sacrifice.disable()

    def enemy_turn(self):
        odds = random.randint(1, 100)
        if 1 <= odds <= 10:
            self.str_attack(self.last_enemy)
        elif 10 < odds <= 20:
            self.pwr_attack(self.last_enemy)
        else:
            if self.last_enemy.attack_roll == 20:
                self.roll_attack(20)
            elif self.last_enemy.attack_roll == 12:
                self.roll_attack(12)
            self.receive_attack(self.warrior, self.roll)
            self.roll_damage(self.last_enemy)
            self.get_damage(self.last_enemy, self.warrior, self.judgment, self.list_dices)



        self.ends_player, self.ends_enemy = False, True

        self.message(self.i_message)

    def enable_buttons(self):
        # Habilitamos los botones para el jugador si se cumplen las condiciones
        if self.warrior.attack_roll == 20:
            self.button_attack_1d20.enable()
        if self.warrior.attack_roll == 12:
            self.button_attack_1d12.enable()
        if self.warrior.strategy_attack:
            self.button_strategic.enable()
        if self.warrior.power_strike:
            self.button_powerful.enable()
        if self.warrior.heal >= 1:
            self.button_heal.enable()
        if self.warrior.bomb >= 1:
            self.button_bomb.enable()
        if self.warrior.stance_recovery >= 1:
            self.button_r_stance.enable()
        if self.warrior.roll_recovery >= 1:
            self.button_r_roll.enable()
        # Siempre que sea el turno del jugador podrá descartar a su guerrero
        self.button_sacrifice.enable()

    def process_gui_events(self, event):
        self.manager_combat.process_events(event)  # Revisión de eventos propios de los elementos de pygame_gui.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.space_key == False:
                print("Space key pressed")
                self.space_key = True
                print(self.space_key)
            elif event.key == pygame.K_SPACE and self.space_key == True:
                print("Space key pressed")
                self.space_key = False
                print(self.space_key)

    #  -- FUNCIONES PROPIAS DEL INICIO Y DESARROLLO DEL COMBATE --
    def roll_attack(self, dice):
        # Función para realizar una tirada de dados para realizar ataques normales.
        if dice == 20:
            self.roll = random.randint(1, 20)
            return self.roll
        elif dice == 12:
            self.roll = random.randint(1, 12)
            return self.roll
        else:
            pass

    def receive_attack(self, target, roll):
        """Función para determinar como recibirá el ataque (el guerrero seleccionado o el enemigo),
        en función de su barra de postura"""
        self.judgment = ""
        if target.stance == 1 and target.stance_weak is False:
            if roll == 1:
                self.judgment = "Critical Miss"
            elif 2 <= roll <= 6:
                self.judgment = "Miss"
            elif 7 <= roll <= 9:
                self.judgment = "Parry"
            elif roll == 20:
                self.judgment = "Critical Hit"
            else:
                self.judgment = "Hit"
        elif target.stance == 2 and target.stance_weak is False:
            if roll <= 2:
                self.judgment = "Critical Miss"
            elif 3 <= roll <= 6:
                self.judgment = "Miss"
            elif 7 <= roll <= 8:
                self.judgment = "Parry"
            elif roll == 20:
                self.judgment = "Critical Hit"
            else:
                self.judgment = "Hit"
        elif target.stance == 3 and target.stance_weak is False:
            if roll == 1:
                self.judgment = "Critical Miss"
            elif 2 <= roll <= 5:
                self.judgment = "Miss"
            elif 6 <= roll <= 9:
                self.judgment = "Parry"
            elif roll == 20:
                self.judgment = "Critical Hit"
            else:
                self.judgment = "Hit"
        elif target.stance == 4 and target.stance_weak is False:
            if roll == 1:
                self.judgment = "Critical Miss"
            elif 2 <= roll <= 6:
                self.judgment = "Miss"
            elif roll == 20:
                self.judgment = "Critical Hit"
            else:
                self.judgment = "Hit"
        elif target.stance_weak:
            if 1 <= roll <= 5:
                self.judgment = "Miss"
            elif roll == 6:
                self.judgment = "Parry"
            elif 18 <= roll <= 20:
                self.judgment = "Critical Hit"
            else:
                self.judgment = "Hit"

        return self.judgment

    def roll_damage(self, attacker):
        # Función para realizar múltiples tiradas de dados de daño en función del tipo de guerrero/enemigo.
        self.list_dices = []  # Lista de resultados de las tiradas. Inicialmente vacía.
        dict_dices = {
            "Samurai": (2, 6),
            "Kunoichi": (3, 4),
            "Ashigaru": (1, 12),
            "Inugami": (2, 4),
            "Guardian Miko": (1, 10),
            "Swordsman of Ministry": (2, 6),
            "Lone Shinobi": (3, 4),
            "Gang of Kappas": (3, 4)
        }
        for i in range(dict_dices[attacker.name][0]):
            number = random.randint(1, dict_dices[attacker.name][1]) + attacker.dmg_base
            self.list_dices.append(number)  # añadimos cada tirada daño y el modificador a una lista de resultados.

        return self.list_dices

    def get_damage(self, attacker, target, judgment, dices):
        """Función para calcular y ejecutar los daños sobre el personaje objetivo en dependiendo de:
        - Atacante
        - Resultado de la tirada de ataque contra la postura del objetivo
        - Lista de resultados de las tiradas de dados de daño"""
        d = 0 # daño individual recibido
        amount = 0 # daño acumulado
        if judgment == "Critical Miss":
            for i in dices:
                i += attacker.dmg_base
                i -= attacker.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                d = i // 2
                if attacker.type == 'player':
                    damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                        str(d), (152, 31, 48))
                    self.damage_text_group.add(damage_text)
                elif attacker.type == 'enemy':
                    damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                        str(d), (152, 31, 48))
                    self.damage_text_group.add(damage_text)
                amount += d # Acumulamos el daño
            if attacker.type == 'player':
                self.warrior.hp_current -= amount
                if amount > 0:
                    self.warrior_ani_dmg.animate() # Animación de daño
            elif attacker.type == 'enemy':
                self.last_enemy.hp_current -= amount
                if amount > 0:
                    self.last_enemy_ani_dmg.animate() # Animación de daño
            print('Critical Miss! {} failed attack and lost {} HP'.format(attacker.name, amount))
            self.i_message = '<b>Critical Miss</b><br>{} failed attack ' \
                                      'and lost {} HP<br>[SPACE] to continue'.format(attacker.name, amount)

        elif judgment == "Miss":
            if target.type == 'player':
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    "MISS", (152, 31, 48))
                self.damage_text_group.add(damage_text)
            elif target.type == 'enemy':
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    "MISS", (152, 31, 48))
                self.damage_text_group.add(damage_text)
            print('Miss! {} failed attack'.format(attacker.name))
            self.i_message = '<b>Miss</b><br>{} failed attack<br>' \
                                      '[SPACE] to continue'.format(attacker.name)

        elif judgment == "Parry":
            for i in dices:
                i += attacker.dmg_base
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                d = i // 2 # Con el parry recibimos la mitad del daño.
                if target.type == 'player':
                    damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                        str(d), (255, 190, 44))
                    self.damage_text_group.add(damage_text)
                elif target.type == 'enemy':
                    damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                        str(d), (255, 190, 44))
                    self.damage_text_group.add(damage_text)
                amount += d  # Acumulamos el daño
            if target.type == 'player':
                self.warrior.hp_current -= amount
                if amount > 0:
                    self.warrior_ani_dmg.animate()  # Animación de daño
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
                if amount > 0:
                    self.last_enemy_ani_dmg.animate()  # Animación de daño
            print('Parry! {} lost only {} HP'.format(target.name, amount))
            self.i_message = '<b>Parry</b><br>{} lost only {} HP<br>' \
                                      '[SPACE] to continue'.format(target.name, amount)

        elif judgment == "Hit":
            for i in dices:
                i += attacker.dmg_base
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                d = i
                if target.type == 'player':
                    damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                        str(d), (251, 107, 29))
                    self.damage_text_group.add(damage_text)
                elif target.type == 'enemy':
                    damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                        str(d), (251, 107, 29))
                    self.damage_text_group.add(damage_text)
                amount += d # Acumulamos el daño
            if target.type == 'player':
                self.warrior.hp_current -= amount
                if amount > 0:
                    self.warrior_ani_dmg.animate()  # Animación de daño
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
                if amount > 0:
                    self.last_enemy_ani_dmg.animate()  # Animación de daño
            print('Hit! {} lost {} HP'.format(target.name, amount))
            self.i_message = '<b>Hit</b><br>{} lost {} HP<br>[SPACE] ' \
                                      'to continue'.format(target.name, amount)

        elif judgment == "Critical Hit":
            for i in dices:
                i += attacker.dmg_base
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                d = i * 2 # Con critical hit se recibe el doble del daño.
                if target.type == 'player':
                    damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                        str(d), (152, 31, 48))
                    self.damage_text_group.add(damage_text)
                elif target.type == 'enemy':
                    damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                        str(d), (152, 31, 48))
                    self.damage_text_group.add(damage_text)
                amount += d # Acumulamos el daño
            if target.type == 'player':
                self.warrior.hp_current -= amount
                if amount > 0:
                    self.warrior_ani_dmg.animate()  # Animación de daño
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
                if amount > 0:
                    self.last_enemy_ani_dmg.animate()  # Animación de daño
            print('Hit! {} lost {} HP'.format(target.name, amount))
            self.i_message = '<b>Critical Hit</b><br>{} lost {} HP<br>' \
                                      '[SPACE]to continue'.format(target.name, amount)

    def str_attack(self, attacker):
        """Función para ejecutar el ataque estratégico que conlleva distintos efectos en el atacante y en el objetivo,
        sin depender de la tirada de ataque del atacante y la postura del objetivo."""

        if attacker.name == "Samurai":
            amount = 0
            for i in range(1):
                number = random.randint(1, 8) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                recovery_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                      str(d), (93, 167, 93))
                self.damage_text_group.add(recovery_text)
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d  # Acumulamos daño
            self.last_enemy.hp_current -= amount
            self.warrior.hp_current += amount
            if self.warrior.hp_current > self.warrior.hp_max:
                self.warrior.hp_current = self.warrior.hp_max
            print("{} used Vampire Slash and recovered {} HP".format(attacker.name, amount))
            self.i_message = '{} used Vampire Slash and recovered {} HP<br>' \
                             '[SPACE] to continue'.format(attacker.name, amount)

        elif attacker.name == "Kunoichi":
            amount = 0
            for i in range(1):
                number = random.randint(1, 4) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d # Acumulamos daño
            self.last_enemy.hp_current -= amount
            self.last_enemy.stance_weak = True # Debilita la postura del enemigo
            print("{} used Fatal Flaw and weakened the enemy's stance".format(attacker.name))
            self.i_message = '{} used Fatal Flaw and weakened the enemy\'s stance<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Ashigaru":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d # Acumulamos daño
            self.last_enemy.hp_current -= amount
            self.warrior.stance_weak = True  # Debilita la postura del guerrero seleccionado
            print("{} used Direct Shot and weakened its own stance".format(attacker.name))
            self.i_message = '{} used Direct Shot and weakened its own stance<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Inugami":
            amount = 0
            for i in range(1):
                number = random.randint(1, 10) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.last_enemy.hp_current -= amount
            self.last_enemy.attack_roll = 12 # Reduce el dado de tirada de ataque del enemigo.
            print("{} used Curse of Revenge and weakened enemy's roll attack".format(attacker.name))
            self.i_message = '{} used Curse of Revenge and weakened enemy\'s roll attack<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Guardian Miko":
            amount = 0
            for i in range(1):
                number = random.randint(1, 8) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                recovery_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                      str(d), (93, 167, 93))
                self.damage_text_group.add(recovery_text)
                amount += d #Acumulamos daño
            self.warrior.hp_current -= amount
            self.last_enemy.hp_current += amount
            if self.last_enemy.hp_current > self.last_enemy.hp_max:
                self.last_enemy.hp_current = self.last_enemy.hp_max
            print("{} used Stream of Light and recovered {} HP".format(attacker.name, amount))
            self.i_message = '{} used Stream of Light and recovered {} HP<br>' \
                             '[SPACE] to continue'.format(attacker.name, amount)

        elif attacker.name == "Swordsman of Ministry":
            amount = 0
            for i in range(5):
                number = random.randint(1, 4) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d #Acumulamos daño
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Stunner Cut and weakened warrior's stance".format(attacker.name))
            self.i_message = '{} used Stunner Cut and weakened warrior\'s stance<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Lone Shinobi":
            amount = 0
            for i in range(5):
                number = random.randint(1, 2) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d  # Acumulamos daño
            self.warrior.hp_current -= amount
            self.warrior.attack_roll = 12
            print("{} used Caltrops and weakened warrior's roll attack".format(attacker.name))
            self.i_message = '{} used Caltrops and weakened warrior\'s roll attack<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Gang of Kappas":
            amount = 0
            for i in range(3):
                number = random.randint(1, 4) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                number_necrotic = attacker.dmg_necrotic - self.warrior.res_necrotic
                if number_necrotic < 0:
                    number_necrotic = 0
                d = number
                d_necrotic = number_necrotic
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d),(152, 31, 48))
                self.damage_text_group.add(damage_text)
                damage_text_necrotic = animations.DamageText(random.randint(240, 300),
                                                             random.randint(400, 500),
                                                             str(d_necrotic), (105, 79, 98))
                self.damage_text_group.add(damage_text_necrotic)
                amount += d + d_necrotic # Acumulamos daño
            self.warrior.hp_current -= amount
            print("{} used Terrible Jaws".format(attacker.name))
            self.i_message = '{} used Terrible Jaws<br>' \
                             '[SPACE] to continue'.format(attacker.name)

    def pwr_attack(self, attacker):
        """Función para ejecutar el ataque poderoso que conlleva distintos efectos en el atacante y en el objetivo,
        sin depender de la tirada de ataque del atacante y la postura del objetivo."""

        if attacker.name == "Samurai":
            amount = 0
            self.warrior_ani_pwr.animate() #Animación del ataque poderoso
            for i in range(3):
                number = random.randint(1, 10) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.last_enemy.hp_current -= amount
            print("{} used Triple Death".format(attacker.name))
            self.i_message = '{} used Triple Death<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Kunoichi":
            amount = 0
            self.warrior_ani_pwr.animate()  # Animación del ataque poderoso
            for i in range(10):
                number = random.randint(1, 4) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.last_enemy.hp_current -= amount
            print("{} used Wasp Rain".format(attacker.name))
            self.i_message = '{} used Wasp Rain<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Ashigaru":
            amount = 0
            self.warrior_ani_pwr.animate()  # Animación del ataque poderoso
            for i in range(5):
                number = random.randint(1, 10) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.last_enemy.hp_current -= amount
            colateral_dmg = random.randint(1, 6) - self.warrior.armor  # Daño colateral sobre Ashigaru
            damage_text_colateral = animations.DamageText(random.randint(240, 300),
                                                          random.randint(400, 500),
                                                          str(colateral_dmg), (152, 31, 48))
            self.damage_text_group.add(damage_text_colateral)
            self.warrior.hp_current -= colateral_dmg
            print("{} used Force and Fire".format(attacker.name))
            self.i_message = '{} used Force and Fire<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Inugami":
            amount = 0
            self.warrior_ani_pwr.animate()  # Animación del ataque poderoso
            for i in range(4):
                number = random.randint(1, 8) + attacker.dmg_base - self.last_enemy.armor
                if number < 0:
                    number = 0
                number_necrotic = attacker.dmg_necrotic - self.last_enemy.res_necrotic
                if number_necrotic < 0:
                    number_necrotic = 0
                d = number
                d_necrotic = number_necrotic
                damage_text = animations.DamageText(random.randint(300, 400), random.randint(50, 100),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                damage_text_necrotic = animations.DamageText(random.randint(300, 400),
                                                             random.randint(50, 100),
                                                             str(d_necrotic), (105, 79, 98))
                self.damage_text_group.add(damage_text_necrotic)
                amount += d + d_necrotic
            self.last_enemy.hp_current -= amount
            print("{} used Putrid Bite".format(attacker.name))
            self.i_message = '{} used Putrid Bite<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Guardian Miko":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                number_randiant = attacker.dmg_radiant - self.warrior.res_radiant
                if number_randiant < 0:
                    number_randiant = 0
                d = number
                d_radiant = number_randiant
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                damage_text_radiant = animations.DamageText(random.randint(240, 300),
                                                            random.randint(400, 500),
                                                             str(d_radiant), (255, 196, 47))
                self.damage_text_group.add(damage_text_radiant)
                amount += d + d_radiant #Acumulamos daño
            self.warrior.hp_current -= amount
            self.last_enemy.armor += 3
            print("{} used Radiant Double Arrow".format(attacker.name))
            self.i_message = '{} used Radiant Double Arrow<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Swordsman of Ministry":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Crossed Strikes".format(attacker.name))
            self.i_message = '{} used Crossed Strikes<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Lone Shinobi":
            amount = 0
            for i in range(3):
                number = random.randint(1, 6) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Weakener Stab".format(attacker.name))
            self.i_message = '{} used Weakener Stab<br>' \
                             '[SPACE] to continue'.format(attacker.name)

        elif attacker.name == "Gang of Kappas":
            amount = 0
            for i in range(3):
                number = random.randint(1, 8) + attacker.dmg_base - self.warrior.armor
                if number < 0:
                    number = 0
                d = number
                damage_text = animations.DamageText(random.randint(240, 300), random.randint(400, 500),
                                                    str(d), (152, 31, 48))
                self.damage_text_group.add(damage_text)
                amount += d
            self.warrior.hp_current -= amount
            print("{} used Shell Hits".format(attacker.name))
            self.i_message = '{} used Shell Hits<br>' \
                             '[SPACE] to continue'.format(attacker.name)

    def message(self, message):
        self.text_box.set_text(message)
        self.text_box.show()

    def render(self, display):
        # Color de fondo
        display.fill((197, 178, 189))

        # ESCENARIO
        display.blit(self.scenario, (0, 0))

        # Dibujo de las animaciones
        self.moving_sprites.draw(display) #personajes
        self.moving_sprites_att.draw(display) #ataques
        self.damage_text_group.draw(display) #daños

        # -- GUERRERO SELECCIONADO --
        # Mostramos la vida actual y máxima del guerrero seleccionado
        self.game.draw_text_right(display, (str(self.warrior.hp_current))+" / "+(str(self.warrior.hp_max)),
                                  (57, 44, 49), self.game.W - 15, self.game.H // 2 + 80)
        # Símbolo que indica el nivel de armadura y texto del valor de este atributo.
        display.blit(self.warrior_armor_img, (self.game.W - 180, self.game.H // 2 + 120))
        self.game.draw_text(display, str(self.warrior.armor), (57, 44, 49), self.game.W - 162, self.game.H // 2 + 135)
        # Barra de postura del personaje
        if self.warrior.stance_weak is True:
            display.blit(self.stance_weak_img, (self.game.W - 140, self.game.H // 2 + 128))
        else:
            display.blit(self.warrior_stancebar_img, (self.game.W - 140, self.game.H // 2 + 128))

        # Contadores de inventario:
        self.game.draw_text_right(display, "x"+(str(self.warrior.heal)), (57, 44, 49),
                                  self.game.W - 139, self.game.H // 2 + 280)
        self.game.draw_text_right(display, "x"+(str(self.warrior.bomb)), (57, 44, 49),
                                  self.game.W - 97, self.game.H // 2 + 280)
        self.game.draw_text_right(display, "x"+(str(self.warrior.stance_recovery)), (57, 44, 49),
                                  self.game.W - 55, self.game.H // 2 + 280)
        self.game.draw_text_right(display, "x"+(str(self.warrior.roll_recovery)), (57, 44, 49),
                                  self.game.W - 13, self.game.H // 2 + 280)
        # Nombre del guerrero seleccionado y nivel.
        self.game.draw_text_right(display, (str(self.warrior.name)), (57, 44, 49),
                                  self.game.W - 15, self.game.H // 2 + 310)
        self.game.draw_text_right(display, "lvl. " + (str(self.warrior.level)), (57, 44, 49),
                                  self.game.W - 15, self.game.H // 2 + 328)

        # -- ÚLTIMO ENEMIGO --
        # Nombre del enemigo y nivel.
        self.game.draw_text_left(display, (str(self.last_enemy.name)), (57, 44, 49), 30, 30)
        self.game.draw_text_left(display, "lvl. " + (str(self.last_enemy.level)), (57, 44, 49), 30, 48)

        # Mostramos la vida actual y máxima del último enemigo
        self.game.draw_text_left(display, (str(self.last_enemy.hp_current)) + " / " + (str(self.last_enemy.hp_max)),
                                 (57, 44, 49), 32, 80)

        # Mostramos el tipo de roll attack del enemigo
        if self.last_enemy.attack_roll == 20:
            self.game.draw_text_right(display, "1d20", (57, 44, 49), 195, 80)
        elif self.last_enemy.attack_roll == 12:
            self.game.draw_text_right(display, "1d12", (152, 31, 48), 195, 80)

        # Símbolo que indica el nivel de armadura y texto del valor de este atributo.
        display.blit(self.last_enemy_armor_img, (30, 120))
        self.game.draw_text(display, str(self.last_enemy.armor), (57, 44, 49), 48, 135)

        # Mostramos la barra de postura del último enemigo
        if self.last_enemy.stance_weak is True:
            display.blit(self.stance_weak_img, (70, 128))
        else:
            if self.last_enemy.stance == 1:
                display.blit(self.enemy_stancebar_img_1, (70, 128))
            elif self.last_enemy.stance == 2:
                display.blit(self.enemy_stancebar_img_2, (70, 128))
            elif self.last_enemy.stance == 3:
                display.blit(self.enemy_stancebar_img_3, (70, 128))
            elif self.last_enemy.stance == 4:
                display.blit(self.enemy_stancebar_img_4, (70, 128))


        # Función para dibujar todos los elementos de la librería pygame_gui iniciados en __init__
        self.manager_combat.draw_ui(display)
