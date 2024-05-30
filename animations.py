import pygame, sys
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
                             pygame.image.load(os.path.join(self.anim_dir, 's_dmg10.png'))]
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



# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_with = 400
screen_height = 400
screen = pygame.display.set_mode((screen_with, screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
animation = Animation(100, 100)
moving_sprites.add(animation)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            animation.animate()


    # Drawing

    screen.fill((0, 0 , 0))
    moving_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
