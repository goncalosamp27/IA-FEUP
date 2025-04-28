import pygame

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jelly Field")

COLORS = ['#e08b8b',  # Darker pastel red
          '#5b97c2',  # Darker pastel blue
          '#9a64c0',  # Darker pastel purple
          '#7fc57b',  # Darker pastel green
          '#5fb5ae',  # Darker pastel cyan
          '#e0c750']  # Darker pastel yellow

TILE_TEXTURE = pygame.image.load("assets/textures/quartz.png").convert_alpha()
HINT_TEXTURE = pygame.image.load("assets/textures/gold.png").convert_alpha()

BG = pygame.image.load("assets/Background7.png")

UNMUTE = pygame.image.load("assets/images/unmute2.png")
MUTE = pygame.image.load("assets/images/mute2.png")

# track sound status (on/off)
sound_on = True

#Background Music
pygame.mixer.music.load("assets/music/background1.mp3")  
pygame.mixer.music.set_volume(0.1)  
pygame.mixer.music.play(-1)  

#Sound Effects
POP_SOUND = pygame.mixer.Sound("assets/music/pop.mp3")
POP_SOUND.set_volume(0.5)

HINT_SOUND = pygame.mixer.Sound("assets/music/hint.mp3")
HINT_SOUND.set_volume(0.7)

JELLY_SOUND = pygame.mixer.Sound("assets/music/jelly.mp3")
JELLY_SOUND.set_volume(0.7)

CLICK_SOUND = pygame.mixer.Sound("assets/music/1.mp3")
CLICK_SOUND.set_volume(0.7) 

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def toggle_sound():
    global sound_on
    if sound_on:
        pygame.mixer.music.pause()  # Pause music
        print("Sound Paused")  
    else:
        pygame.mixer.music.unpause()  # Unpause music
        print("Sound Unpaused")  
    sound_on = not sound_on  # Toggle sound state


def draw_microphone_icon():
    icon_width, icon_height = 50, 50
    icon_x, icon_y = 10, SCREEN.get_height() - icon_height - 10  

    resized_unmute = pygame.transform.scale(UNMUTE, (icon_width, icon_height))
    resized_mute = pygame.transform.scale(MUTE, (icon_width, icon_height))

    if sound_on:
        SCREEN.blit(resized_unmute, (icon_x, icon_y))
    else:
        SCREEN.blit(resized_mute, (icon_x, icon_y))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]: 
        if icon_x <= mouse_x <= icon_x + icon_width and icon_y <= mouse_y <= icon_y + icon_height:
            toggle_sound() 
            pygame.time.delay(200)
