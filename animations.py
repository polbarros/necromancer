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
                             pygame.image.load(os.path.join(self.anim_dir, 'i_dmg10.png'))]
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
        if self.is_animating == True:
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]
