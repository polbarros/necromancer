import pygame

class Button:
    """Esta clase nos permite crear varios objetos de tipo botón con ciertos parámetros que permitirán a cada
    instancia un cierto nivel de versatilidad y reutilización."""
    def __init__(self, x, y, image, image_h, scale):
        width = image.get_width() #Tomamos las medidas de la imagen (ancho)
        heigh = image.get_height() #Tomamos las medidas de la imagen (alto)
        # Transformamos las medidas de la imagen en función de la escala en caso de ser necesario.
        self.image = pygame.transform.scale(image, (int(width * scale), int(heigh * scale)))
        self.image_h = pygame.transform.scale(image_h, (int(width * scale), int(heigh * scale)))
        self.rect = self.image.get_rect() # Asigna las dimensiones de la imagen como rectangulo "hitbox" (su cuerpo).
        self.rect.topleft = (x, y) # Asigna x e y como posición de la esquina superior izquierda del rectangulo.
        self.hovered = False
        self.clicked = False

    def action(self):
        action = False # Establecemos que la acción que produce el botón está inactiva por defecto.

        # Tomamos la posición del ratón
        pos = pygame.mouse.get_pos()

        # Comprobamos el ratón sobre el botón y las condiciones de click para habilitar el click izquierdo.
        if self.rect.collidepoint(pos):
            self.hovered = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                print("Click")
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.hovered = False

        return action  # Retornamos si la acción del botón está activa o no.

    def draw(self, surface):
        # Dibuja el botón en la pantalla
        if self.hovered:
            surface.blit(self.image_h, (self.rect.x, self.rect.y))  # Posiciona la imagen.
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y)) # Posiciona la imagen.
