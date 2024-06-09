import db
import models
import pygame, os
from states.state import State

import ui

class Over(State):
    """Clase heredera de la clase State que define el estado del juego correspondiente a la pantalla de derrota."""
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

        # Establecemos el fondo del menú
        self.menu_bg = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "game_over.png"))
        self.menu_rect = self.menu_bg.get_rect()
        self.menu_rect.center = (self.game.W // 2, self.game.H // 2)

        # Posibles acciones tras la derrota o el sacrificio.
        # Botón de Seppuku
        self.seppuku_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "seppuku.png"))
        self.seppuku_img.set_colorkey([0, 0, 0]) # Quitar el fondo negro que ocupa el espacio de la transparencia.
        self.seppuku_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "seppuku_h.png"))
        self.seppuku_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro que ocupa el espacio de la transparencia.
        self.seppuku_button = ui.Button((self.game.W // 2) - 45, self.game.H - 425,
                                          self.seppuku_img, self.seppuku_img_h, .7)
        # Botón de invocación de un nuevo guerrero (nueva run).
        self.retry_img = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "summon_retry.png"))
        self.retry_img.set_colorkey([0, 0, 0])  # Quitar el fondo negro que ocupa el espacio de la transparencia.
        self.retry_img_h = pygame.image.load(os.path.join(self.game.assets_dir, "sprites", "summon_retry_h.png"))
        self.retry_img_h.set_colorkey([0, 0, 0])  # Quitar el fondo negro de la transparencia.
        self.retry_button = ui.Button((self.game.W // 2) - 45, self.game.H - 320,
                                          self.retry_img, self.retry_img_h, .7)

        # Recordamos que jugador está jugando para tomar sus datos de puntuación
        self.necromancer = db.session.query(models.Login).filter_by(selection=True).first()

        # Llamamos a la función count_enemies para conocer el nivel de avance
        self.enemies_counted = self.count_enemies()

        # Llamamos a la función que registra la máxima puntuación en la base de datos.

        self.best_score = self.max_score()

        # Textos básicos
        self.count_text = "You have defeated {} enemies".format(self.enemies_counted)
        self.best_text = "Your best: {} enemies".format(self.best_score)

    def count_enemies(self):
        # Función que cuenta los enemigos derrotados = todos los registros salvo el guerrero y el último enemigo.
        number = db.session.query(models.Warrior).count() - 2
        return number

    def max_score(self):
        # Función que registra la última puntuación y la compara con la mejor registrada. Siempre retorna la mejor.
        if self.necromancer.max_score <= self.enemies_counted:
            self.necromancer.max_score = self.enemies_counted
        else:
            pass
        return self.necromancer.max_score


    def update(self, delta_time):
        if self.seppuku_button.action():
            db.session.query(models.Warrior).delete()  # Borramos los datos en la BD
            self.necromancer.selection = False # Deseleccionamos al jugador
            db.session.commit()
            from states.choose import Choose
            Choose.first_time = True  # Volvemos a considerar la pantalla de Choose como nueva
            self.exit_state(-3)  # Salimos del estado over y lo borramos "over", "combat" y "choose".
        elif self.retry_button.action():
            db.session.query(models.Warrior).delete()  # Borramos los datos en la BD
            db.session.commit()
            from states.choose import Choose
            Choose.first_time = True # Volvemos a considerar la pantalla de Choose como nueva
            self.exit_state(-2)  # Salimos del estado over y lo borramos "over" y "combat".

    def render(self, display):
        # Renderizamos la pantalla de combate detrás del menu de recompensa
        self.prev_state.render(display)

        # Renderizamos el fondo del menu
        display.blit(self.menu_bg, self.menu_rect)

        # Renderizamos textos
        self.game.draw_text(display, self.count_text, (57, 44, 49), self.game.W // 2,
                            self.game.H - 465)
        self.game.draw_text(display, self.best_text, (57, 44, 49), self.game.W // 2,
                            self.game.H - 445)

        # Renderizamos botones de selección de opciones
        self.seppuku_button.draw(display)
        self.retry_button.draw(display)

        # Renderizamos texto explicativo de opciones
        if self.seppuku_button.hovered:
            self.game.draw_text(display, "Defeat", (57, 44, 49), self.game.W // 2,
                                self.game.H - 380)
        elif self.retry_button.hovered:
            self.game.draw_text(display, "Retry", (57, 44, 49), self.game.W // 2,
                                self.game.H - 275)