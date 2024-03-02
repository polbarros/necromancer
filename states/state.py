class State():
    '''Se trata de una clase "abstracta" que servirá de base para todas las clases del juego que funcionen
    como estados de este. Basicamente funciona a modo de plantilla de la cual heredaran las clases de estado una
    serie de características comunes.'''
    def __init__(self, game):
        self.game = game # Referencia al objeto game de la clase Game, que encapsula lo esencial.
        self.prev_state = None # Apuntamos al estado inmediatamente previo al actual y le asignamos None.

    def update(self, delta_time):
        # Función vacía que llenaremos en las clases que hereden de esta.
        pass

    def render(self, surface):
        # Función vacía que llenaremos en las clases que hereden de esta.
        pass

    def enter_state(self):
        # Función para incorporar un estado a la pila.
        if len(self.game.state_stack) > 1:
            # Asignamos el último estado de la pila (lista) a la variable de estado previo.
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self) # Añadimos el estado del objeto game a la pila como estado actual (último).

    def exit_state(self, index):
        # Función para descartar los estados del final de la pila desde el índice indicado.
        # self.game.state_stack.pop(index)
        del self.game.state_stack[index:]
