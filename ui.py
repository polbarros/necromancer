import pygame, sys

class Button():
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
        if self.hovered == True:
            surface.blit(self.image_h, (self.rect.x, self.rect.y))  # Posiciona la imagen.
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y)) # Posiciona la imagen.


class Health_bar():
    '''Esta clase nos permite crear varios objetos tipo barra de salud animada'''
    def __init__(self, x, y, current_health, target_health, max_health,
                 health_bar_length, health_bar_height, health_change_speed):
        self.x = x
        self.y = y
        self.current_health = current_health # La vida actual del personaje
        self.target_health = target_health
        self.max_health = max_health # La vida máxima que puede adquirir el personaje
        self.health_bar_length = health_bar_length # La longitud en pixels de la barra de salud
        self.health_bar_height = health_bar_height
        # Relación de la vida máxima con la longitud de la barra. Convierte los puntos de vida en distancia.
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = health_change_speed

        # Ancho de la barra animada que se ajustará al valor de los puntos de vida. Será 0 por defecto.
        self.transition_width = 0
        self.transition_color = (255, 0, 0)  # Color de la barra animada.

        self.health_bar_width = int(self.current_health / self.health_ratio)
        self.health_bar_rect = pygame.Rect(self.x, self.y, self.health_bar_width, self.health_bar_height)
        self.transition_bar_rect = pygame.Rect(self.health_bar_rect.right, self.y, self.transition_width,
                                               self.health_bar_height)


    def get_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def get_health(self, amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def animate_bar(self):
        # Condición de ganar puntos de vida.
        if self.current_health < self.target_health:
            '''Si la vida actual es menor a la vida a la que nos dirigimos.
            Añadimos puntos de vida hasta alcanzar el objetivo'''
            self.current_health += self.health_change_speed
            '''La barra de transición será la diferencia entre la vida actual y la vida objetivo.
            Y se dividirá por el ratio para jamás superar los límites de la longitud de la barra.'''
            self.transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            self.transition_color = (131, 145, 139)

        # Condición de perder puntos de vida.
        elif self.current_health > self.target_health:
            self.current_health -= self.health_change_speed
            self.transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            self.transition_color = (198, 102, 104)

        # Actualizar las propiedades de la barra de salud y transición
        self.health_bar_width = int(self.current_health / self.health_ratio)
        self.health_bar_rect.width = self.health_bar_width
        self.transition_bar_rect.width = self.transition_width


    def draw(self, display):
        # Dibujamos la barra de puntos de vida, la barra de transición y un rectángulo para el borde.
        pygame.draw.rect(display, (98, 105, 106), self.health_bar_rect)
        pygame.draw.rect(display, self.transition_color, self.transition_bar_rect)
        pygame.draw.rect(display, (57, 44, 49), (self.x, self.y, self.health_bar_length, self.health_bar_height), 2)



