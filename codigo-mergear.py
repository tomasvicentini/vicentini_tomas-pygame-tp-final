import pygame
import pygame.mixer
from player import Player

# INCIAR PYGAME
pygame.init()

# PANTALLA - VENTANA
ANCHO_VENTANA = 1480
ALTO_VENTANA = 900
ventana_juego = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
imagen = pygame.image.load(r"E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\fondo_alien_isolation.jpg")

# ICONO
pygame.display.set_caption("Alien Shooter")
icono = pygame.image.load(r"E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\Xeno 00.png")
pygame.display.set_icon(icono)

# SONIDOS
ambiente_sound = pygame.mixer.Sound(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\sounds\The Medbay.mp3')
ambiente_sound.play() #MUSICA AMBIENTE
click_sound = pygame.mixer.Sound(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\sounds\M41A Rifle Alien-corto.mp3')
pygame.mouse.set_visible(False)

# TITULO
font_titulo = pygame.font.Font(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\fonts\Alien_Resurrection.ttf', 100)
txt_titulo = font_titulo.render("ALiEN SHOOTER", True, "white")
pos_txt_titulo = ((ANCHO_VENTANA - txt_titulo.get_width()) // 2, 35)

# FUENTE PARA EL MENÚ
font_menu = pygame.font.Font(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\fonts\Roboto-Regular.ttf', 36)  # Puedes ajustar el tamaño y el estilo según tus preferencias

opciones_menu = ["Iniciar", "Opciones", "Salir"]
textos_menu = [font_menu.render(opcion, True, "white") for opcion in opciones_menu]

# Posición inicial para el menú
pos_x_menu = (ANCHO_VENTANA - textos_menu[0].get_width()) // 2
pos_y_menu = 200

# Espacio vertical entre las opciones del menú
espacio_entre_opciones = 50

# PLAYER
quieto = [pygame.image.load(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\players\ripley_1.png'),
          pygame.image.load(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\players\ripley_2.png')]

caminaDerecha = [pygame.image.load(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\players\ripley_rifle_1.png'),
                 pygame.image.load(r'E:\Python\Programacion_I\UTN 2023\5-Pygame\Alien game\img\players\ripley_rifle_2.png')]





clock = pygame.time.Clock()
juego_on = True

while juego_on:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    lista_eventos = pygame.event.get()
    for event in lista_eventos:

        

        #Se verifica si el usuario cerro la ventana
        if event.type == pygame.QUIT:
            juego_on = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play() # Reproducir el sonido al hacer clic

    # fill the screen with a color to wipe away anything from last frame
    #ventana_juego.fill("blue")
    ventana_juego.blit(imagen,(0,0))
    
    
    
    ventana_juego.blit(txt_titulo, pos_txt_titulo)
    # Dibuja las opciones del menú en la pantalla
    for i, texto_opcion in enumerate(textos_menu):
        ventana_juego.blit(texto_opcion, (pos_x_menu, pos_y_menu + i * espacio_entre_opciones))

    # RENDER YOUR GAME HERE

    # Muestra los cambios en la pantalla
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()