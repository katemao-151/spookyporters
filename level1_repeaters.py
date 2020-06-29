import pygame
import pygame_textinput
import time
import random

import qkd

pygame.init()
textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
dark_green = (0,255,0)
dark_red = (255,0,0)
grey = (220,220,220)

repeaters = {}

n = ""


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Level 1')
clock = pygame.time.Clock()


def text_objects(text, font, colour=black):
	textSurface = font.render(text, True, colour)
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


def quitgame():
	pygame.quit()
	quit()

def show_tutorial():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()


		gameDisplay.fill(white)

		close = button("X", display_width-40, 20, 20, 20, dark_red, red, action=main_loop)
		

		smallText = pygame.font.Font("freesansbold.ttf", 12)
		textSurf, textRect = text_objects("In this level you will learn about chaining quantum repeaters to create a secure connection between any user", smallText)
		textRect.center = ((display_width / 2), (display_height / 3))
		gameDisplay.blit(textSurf, textRect)

		pygame.display.update()
		clock.tick(15)

def draw_grid(top_left, width, height): # 0 gamewidth 2/3 gamewidth
	print(top_left, width, height)
	print(repeaters)
	blockSize = 50 #Set the size of the grid block
	for x in range(height):
		for y in range(width):
			if x*blockSize <= width and y * blockSize <= height:
				rect = pygame.Rect(top_left[0] + x*blockSize, top_left[1] + y*blockSize,
								   blockSize, blockSize)
				if rect.topleft in repeaters:
					print(rect.topleft , "in repeaters")
					pygame.draw.rect(gameDisplay, repeaters[rect.topleft], rect, 0) #0 fill
				else:
					pygame.draw.rect(gameDisplay, grey, rect, 1)#1 dont fill


def main_loop():
	qubits = 0
	intro = True

	

	while intro:
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				quitgame()
		gameDisplay.fill(white)

		draw_grid((0,0), display_width, int(display_height * 2/3))

		h, w = (100,100)
		a_c = pygame.Rect((50, display_height/3-h/2), (w,h))
		#srf = gameDisplay.subsurface( x )
		pygame.draw.rect( gameDisplay, blue, a_c)

		smallText = pygame.font.Font("freesansbold.ttf", 12)
		textSurf, textRect = text_objects("Your computer", smallText, colour=blue)
		textRect.center = (100, 0)
		textRect.top = a_c.bottom + 10
		gameDisplay.blit(textSurf, textRect)

		b_c = pygame.Rect((display_width-w-50, display_height/3-h/2), (w,h))
		pygame.draw.rect( gameDisplay, green, b_c)

		textSurf, textRect = text_objects("Bob's computer", smallText, colour=green)
		textRect.center = (display_width - 100, 0)
		textRect.top = b_c.bottom + 10
		gameDisplay.blit(textSurf, textRect)


		add_button = button("add repeater", 50, display_height * 2/3 + 60, 100, 75, green, dark_green, action=add)



		pygame.display.update()
		clock.tick(15)

def add():

	smallText = pygame.font.Font("freesansbold.ttf", 12)
	textSurf, textRect = text_objects("Choose a grid to place your new repeater", smallText)
	textRect.center = (display_width*2/3, display_height*5/6)
	gameDisplay.blit(textSurf, textRect)


	pygame.mouse.set_cursor(*pygame.cursors.broken_x)
	while True:
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				quitgame()
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				if pos[1] < display_height * 2/3:
					nearest_grid = (pos[0] - (pos[0]% 50), pos[1]- (pos[1] % 50))
					if nearest_grid in repeaters:
						del repeaters[nearest_grid]
					else:
						repeaters[nearest_grid] = red
						draw_grid((0,0), display_width, int(display_height * 2/3))
					pygame.mouse.set_cursor(*pygame.cursors.arrow)
					pygame.display.update()

					create_key("a", nearest_grid)

					#do the protocol
					#main_loop()
		pygame.display.update()
		clock.tick(15)


def create_key(a, b):

	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				quitgame()

		gameDisplay.fill(pygame.Color("white"), (0, display_height*2/3, display_width, display_height))
		smallText = pygame.font.Font("freesansbold.ttf", 16)
		textSurf, textRect = text_objects("How many qubits do you want to send to the repeater to create the key?", smallText)
		textRect.center = (display_width*1/2, display_height*4.5/6)
		gameDisplay.blit(textSurf, textRect)

		textinput.update(events)
		#gameDisplay.blit(textinput.get_surface(), (display_width*1/2, display_width * 10/12))
		gameDisplay.blit(textinput.get_surface(), (textRect.left,500))

		add_button = button("OK", textRect.left + 50, 500, 50, 50, green, dark_green, action=update_n)

		try:
			n = int(n)
			q = qkd.bb84(n)
		except:
			if len(n) > 0:
				textSurf, textRect = text_objects("Invalid input", smallText, colour=red)
				textRect.center = (textRect.left, display_height*5/6)
				gameDisplay.blit(textSurf, textRect)



		pygame.display.update()
		clock.tick(30)

def update_n():
	n = textinput.get_text()



#show_tutorial()
main_loop()
