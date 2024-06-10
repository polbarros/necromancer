class State():
    """Se trata de una clase "abstracta" que servirá de base para todas las clases del juego que funcionen
    como estados de este. Básicamente, funciona a modo de plantilla de la cual heredarán las clases de estado una
    serie de características comunes."""
    def __init__(self, game):
        self.game = game # Referencia al objeto game de la clase Game, que encapsula lo esencial.
        self.prev_state = None # Apuntamos al estado inmediatamente previo al actual y le asignamos None.

    def update(self, delta_time):
        # Método vacío que llenaremos en las clases que hereden de esta. Se sobreescribirá.
        pass

    def render(self, surface):
        # Método vacío que llenaremos en las clases que hereden de esta. Se sobreescribirá.
        pass

    def enter_state(self):
        # Método para incorporar un estado a la pila de estados.
        if len(self.game.state_stack) > 1:
            # Asignamos el último estado de la pila (lista) a la variable de estado previo.
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self) # Añadimos el objeto del estado de la pila como estado actual (y último).

    def exit_state(self, index):
        # Método para descartar los estados del final de la pila desde el índice indicado.
        del self.game.state_stack[index:]
