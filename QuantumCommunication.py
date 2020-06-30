import pygame
import pygame_textinput
import time
import random
from microqiskit import QuantumCircuit, simulate
import numpy as np
import math

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
dark_green = (0, 255, 0)
dark_red = (255, 0, 0)

n = 0
qlist = []
aliceBases = []
bobBases = []
bobBits = []
aliceBits = []
key = []


pygame.init()
textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Quantum Communication')
clock = pygame.time.Clock()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button(text, x, y, w, h, dark, light, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, light, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, dark, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    global n,qlist,aliceBits,aliceBases,bobBits,bobBases,key

    #reset to default for play again
    n = 0
    qlist = []
    aliceBases = []
    bobBases = []
    bobBits = []
    aliceBits = []
    key = []
    textinput.clear_text()

    #start
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
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
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        createTextCenter((display_width / 2), (display_height / 20), "Message Sender", 40)

        createTextLeft(20, 120, "Number of Qubits you want to send:", 20)

        textinput.update(events)
        gameDisplay.blit(textinput.get_surface(), (450, 110))

        button("OK", 600, 110, 30, 30, green, dark_green, Qubit)

        createTextLeft(20, 220, "Random qubits in Random bases are:", 20)
        createTextCenter((display_width / 2), 250, str(qlist), 20)
        createTextLeft(20, 320, "Bases", 20)
        createTextCenter((display_width / 2), 350, str(aliceBases), 20)
        createTextLeft(20, 420, "Your Bit Sequence is:",20)
        createTextCenter((display_width / 2), 450, str(aliceBits), 20)

        if qlist != []:
            button("Send", 600, 500, 100, 50, dark_green, green, receiver)

        pygame.display.update()
        clock.tick(15)


def createTextLeft(x, y, text, fontsize):
    smallText = pygame.font.Font("freesansbold.ttf", fontsize)
    textSurf, textRect = text_objects(text, smallText)
    textRect.midleft = (x, y)
    gameDisplay.blit(textSurf, textRect)

def createTextCenter(x, y, text, fontsize):
    smallText = pygame.font.Font("freesansbold.ttf", fontsize)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def Qubit():
    global qlist, aliceBases, aliceBits
    qlist = []
    aliceBases = []
    aliceBits = []


    if textinput.get_text() != "":
        n = int(textinput.get_text())

        for i in range(n):
            qc = QuantumCircuit(1, 1)
            bit = random.choice("01")
            base = random.choice("zx")
            qlist.append(bit + base)
            aliceBases.append(base)
            aliceBits.append(bit)

def randomBase():
    global bobBases, bobBits, aliceBases, aliceBits
    bobBases = []
    bobBits = []

    if textinput.get_text() != "":
        n = int(textinput.get_text())

        for i in range(n):
            base = random.choice("zx")
            bobBases.append(base)
            if base == aliceBases[i]:

                bobBits.append(aliceBits[i])
            else:
                bobBits.append("-")


def receiver():
    receiver = False

    while not receiver:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        createTextCenter((display_width / 2), (display_height / 20), "Message Receiver", 40)

        createTextLeft(20, 120, "The qubits received are:", 20)
        createTextCenter((display_width / 2), 150, str(qlist), 20)
        createTextLeft(20, 220, "The randomly selected Bases are:", 20)
        button("Random!", 650, 210, 100, 30, dark_green, green, randomBase)
        createTextCenter((display_width / 2), 250, str(bobBases), 20)
        createTextLeft(20, 320, "Your Bit Sequence is:",20)
        createTextCenter((display_width / 2), 350, str(bobBits), 20)

        button("Generate Private Key!", 250, 480, 300, 50, dark_green, green, generate)

        pygame.display.update()
        clock.tick(15)

def generate():
    generate = False

    while not generate:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)

        createTextCenter((display_width / 2), (display_height / 20), "Message Receiver", 40)

        createTextLeft(20, 120, "The Bit Sequence of Sender is:", 20)
        createTextCenter((display_width / 2), 150, str(aliceBits), 20)
        createTextLeft(20, 270, "The Bit Sequence of Receiver is:",20)
        createTextCenter((display_width / 2), 300, str(bobBits), 20)

        if key != []:
            createTextLeft(20, 370, "Bingo! The private key for this message is:", 20)
            createTextCenter((display_width / 2), 400, str(key), 20)
            button("Play Again!", 250, 480, 300, 50, dark_green, green, game_intro)


        button("Compare!", 650, 220, 100, 30, dark_green, green, compare)

        pygame.display.update()
        clock.tick(15)

def compare():
    global key
    key = []
    for i,x in zip(aliceBits,bobBits):
        if i == x:
            key.append(i)

game_intro()
