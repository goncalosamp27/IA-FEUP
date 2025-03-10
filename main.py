import pygame
import time
import random

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jelly Field")

PURPLEBG = SCREEN.fill((203, 195, 227)) 
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                #return  # Exit the program 
                run= False
                break
            #SCREEN.fill((203, 195, 227))  # Fill the screen with cyan
            pygame.display.flip()  # Update the screen
    pygame.quit()

        


        
main()
