import pygame
import pygame_textinput
import time
import random

pygame.init()

textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
dark_green = (0,255,0)
dark_red = (255,0,0)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Quantum Communication')
clock = pygame.time.Clock()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(text,x,y,w,h,dark,light, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, light,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, dark,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects("Quantum Communication", smallText)
        textRect.center = ((display_width / 2), (display_height / 3))
        gameDisplay.blit(textSurf, textRect)

        mouse = pygame.mouse.get_pos()
        button("Start", 150, 450, 100, 50, dark_green, green, game_Sender)
        button("Quit", 550, 450, 100, 50, dark_red, red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_Sender():
    sender = False

    while not sender:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        smallText = pygame.font.Font("freesansbold.ttf", 40)
        textSurf, textRect = text_objects("Message Sender", smallText)
        textRect.center = ((display_width / 2), (display_height / 10))
        gameDisplay.blit(textSurf, textRect)

        smallText = pygame.font.Font("freesansbold.ttf", 20)
        textSurf, textRect = text_objects("Number of Qubits", smallText)
        textRect.center = (200, 100)
        gameDisplay.blit(textSurf, textRect)

        button("Quit", 550, 450, 100, 50, dark_red, red, quitgame)

        textinput.update(pygame.event.get())
        gameDisplay.blit(textinput.get_surface(), (400, 90))


        pygame.display.update()
        clock.tick(1500)

def quitgame():
    pygame.quit()
    quit()

game_intro()