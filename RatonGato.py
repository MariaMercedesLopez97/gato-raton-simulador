import pygame  
import random  
import sys  

# Dimensiones del tablero
ancho = 500
alto = 500
num_celdas = 5
tamaño_celdas = ancho // num_celdas

# Colores del tablero
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)

# Clase para representar el tablero y la lógica del juego
class JuegoGatoRaton:
    def __init__(self):
        pygame.init()
        
        # Configuración de la ventana del juego
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Simulador del Gato y Ratón")

        # Posición Inicial
        self.posicion_gato = (0, 0)
        self.posicion_raton = (num_celdas - 1, num_celdas - 1)
        self.posicion_escapatoria = self.generar_escapatoria()
        self.juego_terminado = False

        self.clock = pygame.time.Clock()

        # Cargar imágenes para los personajes y la madriguera
        self.img_gato = pygame.image.load('gato.png')
        self.img_gato = pygame.transform.scale(self.img_gato, (tamaño_celdas, tamaño_celdas))
        self.img_raton = pygame.image.load('raton.png')
        self.img_raton = pygame.transform.scale(self.img_raton, (tamaño_celdas, tamaño_celdas))
        self.img_madriguera = pygame.image.load('madriguera1.png')
        self.img_madriguera = pygame.transform.scale(self.img_madriguera, (tamaño_celdas, tamaño_celdas))

    def generar_escapatoria(self):
        while True:
            escapatoria = (random.randint(0, num_celdas - 1), random.randint(0, num_celdas - 1))
            if escapatoria != self.posicion_gato and escapatoria != self.posicion_raton:
                return escapatoria

    def dibujar_tablero(self):# Dibujamos el tablero
    
        for fila in range(num_celdas):
            for columna in range(num_celdas):
                x0 = columna * tamaño_celdas
                y0 = fila * tamaño_celdas
                if (fila + columna) % 2 == 0:
                    color = color_blanco
                    pygame.draw.rect(self.screen, color, (x0, y0, tamaño_celdas, tamaño_celdas))
                    if (fila, columna) == self.posicion_escapatoria:
                        pygame.draw.rect(self.screen, color, (x0, y0, tamaño_celdas, tamaño_celdas))
                        self.screen.blit(self.img_madriguera, (x0, y0))
                else:
                    color = color_negro
                    pygame.draw.rect(self.screen, color, (x0, y0, tamaño_celdas, tamaño_celdas))
            #Dibujar la imagen la madriguera si es la posicion de la escapatoria
                    if (fila, columna) == self.posicion_escapatoria:
                        pygame.draw.rect(self.screen, color, (x0, y0, tamaño_celdas, tamaño_celdas))
                        self.screen.blit(self.img_madriguera, (x0, y0))
                    
    def dibujar_gato(self):
        x = self.posicion_gato[1] * tamaño_celdas
        y = self.posicion_gato[0] * tamaño_celdas
        self.screen.blit(self.img_gato, (x, y))

    def dibujar_raton(self):
        x = self.posicion_raton[1] * tamaño_celdas
        y = self.posicion_raton[0] * tamaño_celdas
        self.screen.blit(self.img_raton, (x, y))

    def mover_gato(self):
        if self.juego_terminado:
            return
        movimientos = ["Up", "Down", "Left", "Right"]
        mejor_movimiento = None
        menor_distancia = float('inf')

        for movimiento in movimientos:
            nueva_posicion_gato = self.simular_movimiento(self.posicion_gato, movimiento)
            distancia = self.distancia(nueva_posicion_gato, self.posicion_raton)
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_movimiento = movimiento

        self.posicion_gato = self.simular_movimiento(self.posicion_gato, mejor_movimiento)

        if self.posicion_gato == self.posicion_raton:
            self.juego_terminado = True
            self.mostrar_mensaje("¡El gato ha atrapado al ratón!")

        self.dibujar_todo()

    def mover_raton_minimax(self):
        if self.juego_terminado:
            return

        movimientos = ["Up", "Down", "Left", "Right"]
        mejor_movimiento = None
        mejor_valor = -float('inf')

        error = random.random()
        if error < 0.2:
            movimientos_random = movimientos[:]
            random.shuffle(movimientos_random)
            mejor_movimiento = movimientos_random[0]
        else:
            for movimiento in movimientos:
                valor = self.minimax(self.posicion_raton, self.posicion_gato, movimiento, True, 0)
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = movimiento

        self.mover_raton(mejor_movimiento)

    def minimax(self, raton, gato, movimiento, es_raton, profundidad):
        # Limitar la profundidad del algoritmo
        if profundidad == 3:
            return self.distancia(raton, gato)

        # Simular el movimiento 
        nueva_posicion_raton = self.simular_movimiento(raton, movimiento) if es_raton else raton
        nueva_posicion_gato = self.simular_movimiento(gato, movimiento) if not es_raton else gato

        # Verificar condiciones de victoria
        if nueva_posicion_raton == gato:
            return -float('inf')  # El ratón es atrapado
        if nueva_posicion_raton == self.posicion_escapatoria:
            return float('inf')  # El ratón escapa

        if es_raton:
            mejor_valor = -float('inf')
            for mov in ["Up", "Down", "Left", "Right"]:
                valor = self.minimax(nueva_posicion_raton, gato, mov, False, profundidad + 1)
                mejor_valor = max(mejor_valor, valor)
            return mejor_valor
        else:
            mejor_valor = float('inf')
            for mov in ["Up", "Down", "Left", "Right"]:
                valor = self.minimax(raton, nueva_posicion_gato, mov, True, profundidad + 1)
                mejor_valor = min(mejor_valor, valor)
            return mejor_valor

    def simular_movimiento(self, posicion, movimiento):
        if movimiento == "Up" and posicion[0] > 0:
            return (posicion[0] - 1, posicion[1])
        elif movimiento == "Down" and posicion[0] < num_celdas - 1:
            return (posicion[0] + 1, posicion[1])
        elif movimiento == "Left" and posicion[1] > 0:
            return (posicion[0], posicion[1] - 1)
        elif movimiento == "Right" and posicion[1] < num_celdas - 1:
            return (posicion[0], posicion[1] + 1)
        return posicion

    def distancia(self, posicion1, posicion2):
        return abs(posicion1[0] - posicion2[0]) + abs(posicion1[1] - posicion2[1])

    def mover_raton(self, movimiento):
        nueva_posicion_raton = self.simular_movimiento(self.posicion_raton, movimiento)

        if nueva_posicion_raton != self.posicion_gato:
            self.posicion_raton = nueva_posicion_raton

        if self.posicion_raton == self.posicion_escapatoria:
            self.juego_terminado = True
            self.mostrar_mensaje("¡El ratón pudo escapar!")

        self.dibujar_todo()

    def mostrar_mensaje(self, mensaje):
        print(mensaje)

    def dibujar_todo(self):
        self.screen.fill(color_blanco)
        self.dibujar_tablero()
        self.dibujar_gato()
        self.dibujar_raton()
        pygame.display.flip()

    def run(self):
        while not self.juego_terminado:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.mover_gato()
            self.mover_raton_minimax()
            self.clock.tick(1)

# Crear y ejecutar el juego
juego = JuegoGatoRaton()
juego.dibujar_todo()
juego.run()
