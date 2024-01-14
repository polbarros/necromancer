import db
import models
from sqlalchemy import desc
from states.state import State
import pygame_gui
import os
import pygame
import random


class Combat(State):
    """Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de combate."""

    def __init__(self, game):
        State.__init__(self, game)
        # El manager de pygame_gui para el estado de combate
        # Debemos crear un nuevo manager porque de lo contrario cargaría los elementos de otros archivos de estado.
        self.manager_combat = pygame_gui.UIManager((self.game.W, self.game.H), "theme.json")

        # -- GUERRERO ESCOGIDO --
        # Toma de la información de la BD sobre el guerrero escogido
        self.warrior = db.session.query(models.Warrior).filter_by(type="player").first()

        # Imágen del guerrero escogido
        if self.warrior.name == "Samurai":
            self.warrior_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "samurai.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_1.png"))
        elif self.warrior.name == "Kunoichi":
            self.warrior_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "kunoichi.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_2.png"))
        elif self.warrior.name == "Ashigaru":
            self.warrior_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "ashigaru.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_3.png"))
        elif self.warrior.name == "Inugami":
            self.warrior_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "inugami.png"))
            self.warrior_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
            self.warrior_stancebar_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_4.png"))

        # -- GUERRERO ENEMIGO --
            # Datos aleatorios para los enemigos: nivel y puntos de salud.
        level_enemy = random.randint(self.warrior.level, self.warrior.level + 1)
        health_enemy = random.randint(30, 35) + (self.warrior.level * 2)
        # Valores posibles de los enemigos. Tuplas con los datos para crear objetos.
        tuple_miko = ("Guardian Miko", level_enemy, 0, health_enemy, health_enemy, 1, 0, 3, 0, 0,
                          True, True, 0, 2, 1, 4, False, 0, 20, 0, "enemy")
        tuple_ministry = ("Swordsman of Ministry", level_enemy, 0, health_enemy, health_enemy, 1, 0, 0, 0, 0,
                              True, True, 0, 1, 2, 1, False, 0, 20, 0, "enemy")
        tuple_shinobi = ("Lone Shinobi", level_enemy, 0, health_enemy, health_enemy, 1, 0, 3, 0, 0,
                             True, True, 0, 2, 1, 2, False, 0, 20, 0, "enemy")
        tuple_kappas = ("Gang of Kappas", level_enemy, 0, health_enemy, health_enemy, 1, 3, 0, 0, 0,
                            True, True, 0, 2, 3, 3, False, 0, 20, 0, "enemy")
        # Diccionario de enemigos
        self.dict_enemies = {1: tuple_miko,
                             2: tuple_ministry,
                             3: tuple_shinobi,
                             4: tuple_kappas}
        # Iniciamos el objeto de la clase combate con la creación de un enemigo
        self.enemy_generator()

        # Toma de la información de la BD sobre el último enemigo generado
        self.last_enemy = db.session.query(models.Warrior).filter_by(type="enemy").order_by(desc(models.Warrior.id)).first()

        # Cargamos las imágenes de los enemigos y de las barras de postura de los enemigos
        self.miko_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "miko.png"))
        self.miko_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.ministry_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "ministry.png"))
        self.ministry_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.shinobi_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "shinobi.png"))
        self.shinobi_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.kappas_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "kappas.png"))
        self.kappas_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro.
        self.enemy_stancebar_img_1 = pygame.image.load(
            os.path.join(self.game.assets_dir, "sprites", "stance_1_enemy.png"))
        self.enemy_stancebar_img_2 = pygame.image.load(
            os.path.join(self.game.assets_dir, "sprites", "stance_2_enemy.png"))
        self.enemy_stancebar_img_3 = pygame.image.load(
            os.path.join(self.game.assets_dir, "sprites", "stance_3_enemy.png"))
        self.enemy_stancebar_img_4 = pygame.image.load(
            os.path.join(self.game.assets_dir, "sprites", "stance_4_enemy.png"))

        # -- OTROS ELEMENTOS --
        # El símbolo para indicar la armadura del guerrero seleccionado y el enemigo
        self.warrior_armor_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "armor.png"))
        self.last_enemy_armor_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "armor_enemy.png"))
        # Imagen de la barra de postura debilitada
        self.stance_weak_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "stance_weak.png"))

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

        # UI BOTONES DE COMBATE
        self.button_attack_1d20 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 180,
                                                                                     self.game.H // 2 + 150),
                                                                                    (167, 40)),
                                                               text="ATTACK ROLL 1d20",
                                                               manager=self.manager_combat,
                                                               tool_tip_text="Roll a dice of <b>20 sides</b> to attack",
                                                               object_id='#button_attack_1d20')

        self.button_attack_1d12 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.game.W - 180,
                                                                                          self.game.H // 2 + 150),
                                                                                         (167, 40)),
                                                               text="ATTACK ROLL 1d12",
                                                               manager=self.manager_combat,
                                                               tool_tip_text="Roll a dice of <b>12 sides</b> to attack",
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
        self.text_box = pygame_gui.elements.UITextBox(html_text="",
                                                      relative_rect=pygame.Rect((100,
                                                                                 300),
                                                                                (300, 150)),
                                                      manager=self.manager_combat,
                                                      wrap_to_height=True,
                                                      object_id='#text_box_message')
        self.text_box.hide()  # Escondemos la caja de texto para mensajes.

        # Elementos operativos para el combate
        self.roll = None
        self.judgment = None
        self.list_dices = None
        self.space_key = False

    def calculate_health_percent(self):
        # Función para calcular el porcentaje de salud del guerrero seleccionado (para la barra de salud).
        return (self.warrior.hp_current/self.warrior.hp_max)*100

    def calculate_enemy_health_percent(self):
        # Función para calcular el porcentaje de salud del último enemigo (para la barra de salud).
        return (self.last_enemy.hp_current/self.last_enemy.hp_max)*100

    def update(self, delta_time):

        # Actualiza los efectos animados y otros elementos de la caja de texto de mensajes para el jugador
        self.text_box.update(delta_time)
        #self.text_box.update_text_effect(delta_time)

        # Condiciones para la presentación de botones de ataque simple
        if self.warrior.attack_roll == 20:
            self.button_attack_1d12.hide()
            self.button_attack_1d20.show()
        elif self.warrior.attack_roll == 12:
            self.button_attack_1d20.hide()
            self.button_attack_1d12.show()

        # Actualiza la barra de salud del guerrero seleccionado
        self.warrior_health_bar.update(delta_time)

        if self.warrior.hp_current > 0 and self.last_enemy.hp_current > 0:
            # Mientras los puntos de guerrero seleccionado y el último enemigo sean superiores a 0.
            # Llamamos a la función que inicia el turno del jugador.
            self.player_turn()
        elif self.warrior.hp_current <= 0:
            pass
        elif self.last_enemy.hp_current <= 0:
            pass

        # Actualizador del manager de los elementos pygame_gui
        self.manager_combat.update(delta_time)

    def player_turn(self):
        if self.warrior.attack_roll == 20 and self.button_attack_1d20.check_pressed():
            self.roll_attack(20)
            self.receive_attack(self.last_enemy, self.roll)
            self.roll_damage(self.warrior)
            self.get_damage(self.warrior, self.last_enemy, self.judgment, self.list_dices)
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.warrior.attack_roll == 12 and self.button_attack_1d12.check_pressed():
            self.roll_attack(12)
            self.receive_attack(self.last_enemy, self.roll)
            self.roll_damage(self.warrior)
            self.get_damage(self.warrior, self.last_enemy, self.judgment, self.list_dices)
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.button_strategic.check_pressed():
            self.str_attack(self.warrior)
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.button_powerful.check_pressed():
            self.pwr_attack(self.warrior)
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.warrior.heal >= 1 and self.button_heal.check_pressed():
            self.warrior.hp_current = self.warrior.hp_max  # Curamos la salud del guerrero seleccionado al completo.
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.warrior.bomb >= 1 and self.button_bomb.check_pressed():
            self.last_enemy.hp_current -= random.randint(30, 50)  # El enemigo pierde mucha vida.
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.warrior.stance_recovery >= 1 and self.button_r_stance.check_pressed():
            self.warrior.stance_weak = False
            self.end_player_turn()  # Terminamos turno del jugador.
        elif self.warrior.roll_recovery >= 1 and self.button_r_roll.check_pressed():
            self.warrior.attack_roll = 20
            self.end_player_turn()  # Terminamos turno del jugador.

    def end_player_turn(self):
        # Deshabilitamos los botones para el jugador
        self.button_attack_1d20.disable()
        self.button_attack_1d12.disable()
        self.button_strategic.disable()
        self.button_powerful.disable()
        self.button_heal.disable()
        self.button_bomb.disable()
        self.button_r_stance.disable()
        self.button_r_roll.disable()
        print(self.space_key)
        if self.space_key:
            print("Space key is True. Initiating enemy turn.")
            self.enemy_turn()  # Iniciamos el turno del enemigo

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

        self.end_enemy_turn()  # Terminamos el turno del enemigo.

    def end_enemy_turn(self):
        if self.space_key:
            self.player_turn()  # Volvemos al turno del jugador
            # Habilitamos los botones para el jugador
            self.button_attack_1d20.enable()
            self.button_attack_1d12.enable()
            self.button_strategic.enable()
            self.button_powerful.enable()
            self.button_heal.enable()
            self.button_bomb.enable()
            self.button_r_stance.enable()
            self.button_r_roll.enable()

    def process_gui_events(self, event):
        self.manager_combat.process_events(event)  # Revisión de eventos propios de los elementos de pygame_gui.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space key pressed")
                self.space_key = True
                print(self.space_key)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                print("Space key released")
                self.space_key = False
                print(self.space_key)

    #  -- FUNCIONES PROPIAS DEL INICIO Y DESARROLLO DEL COMBATE --
    def enemy_generator(self):
        # Esta función sirve para generar y registrar nuevos enemigos en la base de datos.
        # Mediante este método desempaquetamos las tuplas como parametros para crear el objeto de la clase Warrior.
        new_enemy = models.Warrior(*self.dict_enemies[random.randint(1, 4)])
        db.session.add(new_enemy)
        db.session.commit()

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
        self.list_dices = []  # Lista de resultados de las tiradas. Inicialmente vacia.
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
        amount = 0
        if judgment == "Critical Miss":
            for i in dices:
                i -= attacker.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                amount += i // 2
            if attacker.type == 'player':
                self.warrior.hp_current -= amount
            elif attacker.type == 'enemy':
                self.last_enemy.hp_current -= amount
            print('Critical Miss! {} failed attack and lost {} HP'.format(attacker.name, amount))
            self.text_box.html_text = '<effect id=judgement><b>Critical Miss!</b></effect><br>{} failed attack ' \
                                      'and lost {} HP<br><br>[SPACE] to continue'.format(attacker.name, amount)
            self.text_box.show()
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='judgement')
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})
            self.text_box.stop_finished_effect()

        elif judgment == "Miss":
            print('Miss! {} failed attack'.format(attacker.name))
            self.text_box.html_text = '<effect id=judgement><b>Miss!</b></effect><br>{} failed attack <br><br>' \
                                      '[SPACE] to continue'.format(attacker.name)
            self.text_box.show()
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='judgement')
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})
            self.text_box.stop_finished_effect()

        elif judgment == "Parry":
            for i in dices:
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                amount += i // 2
            if target.type == 'player':
                self.warrior.hp_current -= amount
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
            print('Parry! {} lost only {} HP'.format(target.name, amount))
            self.text_box.html_text = '<effect id=judgement><b>Parry!</b></effect><br>{} lost only {} HP<br><br>' \
                                      '[SPACE] to continue'.format(target.name, amount)
            self.text_box.show()
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='judgement')
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})
            self.text_box.stop_finished_effect()

        elif judgment == "Hit":
            for i in dices:
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                amount += i
            if target.type == 'player':
                self.warrior.hp_current -= amount
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
            print('Hit! {} lost {} HP'.format(target.name, amount))
            self.text_box.html_text = '<effect id=judgement><b>Hit!</b></effect><br>{} lost {} HP<br><br>[SPACE] ' \
                                      'to continue'.format(target.name, amount)
            self.text_box.show()
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='judgement')
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})
            self.text_box.stop_finished_effect()

        elif judgment == "Critical Hit":
            for i in dices:
                i -= target.armor  # Reducimos el valor de las tiradas de daño dependiendo del nivel de armadura.
                if i < 0:
                    i = 0
                amount += (i * 2)
            if target.type == 'player':
                self.warrior.hp_current -= amount
            elif target.type == 'enemy':
                self.last_enemy.hp_current -= amount
            print('Hit! {} lost {} HP'.format(target.name, amount))
            self.text_box.html_text = '<effect id=judgement><b>Critical Hit!</b></effect><br>{} lost {} HP<br><br>' \
                                      '[SPACE]to continue'.format(target.name, amount)
            self.text_box.show()
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='judgement')
            self.text_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.1})
            self.text_box.stop_finished_effect()

    def str_attack(self, attacker):
        """Función para ejecutar el ataque estratégico que conlleva distintos efectos en el atacante y en el objetivo,
        sin depender de la tirada de ataque del atacante y la postura del objetivo."""

        if attacker.name == "Samurai":
            amount = 0
            for i in range(1):
                number = random.randint(1, 8) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            self.warrior.hp_current += amount
            if self.warrior.hp_current > self.warrior.hp_max:
                self.warrior.hp_current = self.warrior.hp_max
            print("{} used Vampire Slash and recovered {} HP".format(attacker.name, amount))

        elif attacker.name == "Kunoichi":
            amount = 0
            for i in range(1):
                number = random.randint(1, 4) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            self.last_enemy.stance_weak = True
            print("{} used Fatal Flaw and weakened the enemy's stance".format(attacker.name))

        elif attacker.name == "Ashigaru":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            self.warrior.stance_weak = True  # Debilita la postura del guerrero seleccionado
            print("{} used Direct Shot and weakened its own stance".format(attacker.name))

        elif attacker.name == "Inugami":
            amount = 0
            for i in range(1):
                number = random.randint(1, 10) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            self.last_enemy.attack_roll = 12
            print("{} used Curse of Revenge and weakened enemy's roll attack".format(attacker.name))

        elif attacker.name == "Guardian Miko":
            amount = 0
            for i in range(1):
                number = random.randint(1, 8) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.last_enemy.hp_current += amount
            if self.last_enemy.hp_current > self.last_enemy.hp_max:
                self.last_enemy.hp_current = self.last_enemy.hp_max
            print("{} used Stream of Light and recovered {} HP".format(attacker.name, amount))

        elif attacker.name == "Swordsman of Ministry":
            amount = 0
            for i in range(5):
                number = random.randint(1, 4) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Stunner Cut and weakened warrior's stance".format(attacker.name))

        elif attacker.name == "Lone Shinobi":
            amount = 0
            for i in range(5):
                number = random.randint(1, 2) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.warrior.attack_roll = 12
            print("{} used Caltrops and weakened warrior's roll attack".format(attacker.name))

        elif attacker.name == "Gang of Kappas":
            amount_necrotic = 0
            for i in range(3):
                number = random.randint(1, 4) - self.warrior.res_necrotic
                if number < 0:
                    number = 0
                amount_necrotic += number
            self.warrior.hp_current -= amount_necrotic
            print("{} used Terrible Jaws".format(attacker.name))

    def pwr_attack(self, attacker):
        """Función para ejecutar el ataque poderoso que conlleva distintos efectos en el atacante y en el objetivo,
        sin depender de la tirada de ataque del atacante y la postura del objetivo."""

        if attacker.name == "Samurai":
            amount = 0
            for i in range(3):
                number = random.randint(1, 10) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            print("{} used Triple Death".format(attacker.name))

        elif attacker.name == "Kunoichi":
            amount = 0
            for i in range(10):
                number = random.randint(1, 4) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            print("{} used Wasp Rain".format(attacker.name))

        elif attacker.name == "Ashigaru":
            amount = 0
            for i in range(5):
                number = random.randint(1, 10) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            self.warrior.hp_current -= random.randint(1, 6) - self.warrior.armor  # Daño colateral sobre Ashigaru
            print("{} used Force and Fire".format(attacker.name))

        elif attacker.name == "Inugami":
            amount = 0
            for i in range(4):
                number = random.randint(1, 8) - self.last_enemy.armor
                if number < 0:
                    number = 0
                amount += number
            self.last_enemy.hp_current -= amount
            amount_necrotic = random.randint(1, 6) - self.last_enemy.res_necrotic
            self.last_enemy.hp_current -= amount_necrotic
            print("{} used Putrid Bite".format(attacker.name))

        elif attacker.name == "Guardian Miko":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.last_enemy.armor += 3
            amount_radiant = random.randint(1, 4) - self.warrior.res_radiant
            self.last_enemy.hp_current -= amount_radiant
            print("{} used Radiant Double Arrow".format(attacker.name))

        elif attacker.name == "Swordsman of Ministry":
            amount = 0
            for i in range(2):
                number = random.randint(1, 10) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Crossed Strikes".format(attacker.name))

        elif attacker.name == "Lone Shinobi":
            amount = 0
            for i in range(3):
                number = random.randint(1, 6) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            self.warrior.stance_weak = True
            print("{} used Weakener Stab".format(attacker.name))

        elif attacker.name == "Gang of Kappas":
            amount = 0
            for i in range(3):
                number = random.randint(1, 8) - self.warrior.armor
                if number < 0:
                    number = 0
                amount += number
            self.warrior.hp_current -= amount
            print("{} used Shell Hits".format(attacker.name))

    def render(self, display):
        # Color de fondo
        display.fill((197, 178, 189))

        # -- GUERRERO SELECCIONADO --
        # Imagen del guerrero seleccionado
        if self.warrior.name == "Samurai":
            display.blit(self.warrior_img, (-30, self.game.H - 500))
        if self.warrior.name == "Kunoichi":
            display.blit(self.warrior_img, (15, self.game.H - 446))
        if self.warrior.name == "Ashigaru":
            display.blit(self.warrior_img, (-85, self.game.H - 524))
        if self.warrior.name == "Inugami":
            display.blit(self.warrior_img, (-30, self.game.H - 476))

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
        # Imagen del último enemigo generado
        if self.last_enemy.name == "Guardian Miko":
            display.blit(self.miko_img, (self.game.W - 256, 0))
        elif self.last_enemy.name == "Swordsman of Ministry":
            display.blit(self.ministry_img, (self.game.W - 256, 0))
        elif self.last_enemy.name == "Lone Shinobi":
            display.blit(self.shinobi_img, (self.game.W - 256, 0))
        elif self.last_enemy.name == "Gang of Kappas":
            display.blit(self.kappas_img, (self.game.W - 256, 0))

        # Nombre del guerrero seleccionado y nivel.
        self.game.draw_text_left(display, (str(self.last_enemy.name)), (57, 44, 49), 30, 30)
        self.game.draw_text_left(display, "lvl. " + (str(self.last_enemy.level)), (57, 44, 49), 30, 48)

        # Mostramos la vida actual y máxima del último enemigo
        self.game.draw_text_left(display, (str(self.last_enemy.hp_current)) + " / " + (str(self.last_enemy.hp_max)),
                                 (57, 44, 49), 32, 80)

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