import pygame
import os

class Animation(pygame.sprite.Sprite):
    """Esta clase nos permite crear varios objetos de tipo animación con ciertos parámetros que permitirán a cada
        instancia un cierto nivel de versatilidad y reutilización."""
    def __init__(self, pos_x, pos_y, code):
        super().__init__()
        self.is_animating = False
        self.anim_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sprites', 'anim')
        self.ani_dict = {
            "samurai_dmg" : [pygame.image.load(os.path.join(self.anim_dir, 's_dmg1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg10.png'))],
            "kunoichi_dmg" : [pygame.image.load(os.path.join(self.anim_dir, 'k_dmg1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'k_dmg10.png'))],
            "ashigaru_dmg" : [pygame.image.load(os.path.join(self.anim_dir, 'a_dmg1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_dmg10.png'))],
            "inugami_dmg" : [pygame.image.load(os.path.join(self.anim_dir, 'i_dmg1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg10.png'))],
            "miko_dmg": [pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg1.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg2.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg3.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg4.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg5.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg6.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg7.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg8.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg9.png')),
                         pygame.image.load(os.path.join(self.anim_dir, 'mi_dmg10.png'))],
            "ministry_dmg": [pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'sw_dmg10.png'))],
            "shinobi_dmg": [pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg1.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg2.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg3.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg4.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg5.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg6.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg7.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg8.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg9.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'sh_dmg10.png'))],
            "kappas_dmg" : [pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg1.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg2.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg3.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg4.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg5.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg6.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg7.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg8.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg9.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'ka_dmg10.png'))],
            "samurai_pwr": [pygame.image.load(os.path.join(self.anim_dir, 's_pwr1.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr2.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr3.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr4.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr5.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr6.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr7.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr8.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr9.png')),
                           pygame.image.load(os.path.join(self.anim_dir, 's_pwr10.png'))],
            "kunoichi_pwr": [pygame.image.load(os.path.join(self.anim_dir, 'k_pwr1.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr2.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr3.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr4.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr5.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr6.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr7.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr8.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr9.png')),
                            pygame.image.load(os.path.join(self.anim_dir, 'k_pwr10.png'))],
            "ashigaru_pwr": [pygame.image.load(os.path.join(self.anim_dir, 'a_pwr1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'a_pwr10.png'))],
            "inugami_pwr": [pygame.image.load(os.path.join(self.anim_dir, 'i_pwr1.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr2.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr3.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr4.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr5.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr6.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr7.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr8.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr9.png')),
                             pygame.image.load(os.path.join(self.anim_dir, 'i_pwr10.png'))],
            "bomb": [pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani1.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani2.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani3.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani4.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani5.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani6.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani7.png')),
                     pygame.image.load(os.path.join(self.anim_dir, 'bomb_ani8.png'))]
        }

        # Usamos el parámetro "code" como la clave que nos permite encontrar la lista de frames de la animación.
        self.sprites = self.ani_dict[code]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating:
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]

class DamageText(pygame.sprite.Sprite):
    """Esta clase nos permite crear varios objetos temporales para mostrar textos animados en pantalla que representen
    el daño infligido al personaje."""
    def __init__(self, pos_x, pos_y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        # Creamos punteros a carpetas y subcarpetas con los archivos de assets para la fuente.
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "font")
        # Cargamos un objeto font con tamaño de letra de 12
        self.font = pygame.font.Font(os.path.join(self.font_dir, "Retro Gaming.ttf"), 20)
        # Creamos la imagen del texto y la situamos en base los parámetros
        self.image = self.font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.counter = 0

    def update(self):
        #Mover el texto hacia arriba
        self.rect.y -= 1
        #Borrar el texto tras unos segundos
        self.counter += 1
        if self.counter > 30:
            self.kill()
