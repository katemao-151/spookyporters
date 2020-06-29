import pygame
import time
import random
import math

import qkd
import pygame_textinput


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
purple = (128,0,128)
light_red = (255, 102, 102)

computers = {}
repeaters = {}

connections = {}

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
	textRect.center = ( int(x+(w/2)), int(y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)


def quitgame():
	pygame.quit()
	quit()

def clearUI():
  gameDisplay.fill(pygame.Color("white"), (0, display_height*2/3, display_width, display_height))

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

def draw_grid(top_left=(0,0), width=display_width, height=int(display_height * 2/3)): # 0 gamewidth 2/3 gamewidth 
	#print(top_left, width, height)
	#print(repeaters)
	blockSize = 50 #Set the size of the grid block
	for x in range(height):
		for y in range(width):
			if x*blockSize <= width and y * blockSize <= height:
				rect = pygame.Rect(top_left[0] + x*blockSize, top_left[1] + y*blockSize,
								   blockSize, blockSize)
				if rect.topleft in repeaters and rect.topleft not in computers:
					#print(rect.topleft , "in repeaters")
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
    a_c = pygame.Rect((50, int(display_height/3-h/2)), (w,h))
    pygame.draw.rect( gameDisplay, blue, a_c)
    for d1 in [0,50]:
      for d2 in [0,50]:
        computers[a_c.left + d1, a_c.top + d2] = blue

    smallText = pygame.font.Font("freesansbold.ttf", 12)
    textSurf, textRect = text_objects("Your computer", smallText, colour=blue)
    textRect.center = (100, 0)
    textRect.top = a_c.bottom + 10
    gameDisplay.blit(textSurf, textRect)

    b_c = pygame.Rect((display_width-w-50, int(display_height/3-h/2)), (w,h))
    pygame.draw.rect( gameDisplay, purple, b_c)
    for d1 in [0,h]:
      for d2 in [0,w]:
        computers[b_c.left + d1, b_c.top + d2] = purple

    textSurf, textRect = text_objects("Bob's computer", smallText, colour=purple)
    textRect.center = (display_width - 100, 0)
    textRect.top = b_c.bottom + 10
    gameDisplay.blit(textSurf, textRect)


    add_button = button("add repeater", 50, display_height * 2.1/3 + 60, 150, 50, green, dark_green, action=add)



    pygame.display.update()
    clock.tick(15)

def add():

  pygame.mouse.set_cursor(*pygame.cursors.tri_left)
  from_grid = choice_selection("Where do you want the connection to come from", (display_width*2/3, display_height*5/6))


  pygame.mouse.set_cursor(*pygame.cursors.broken_x)
  nearest_grid = choice_selection("Choose a grid to place your new repeater", (display_width*2/3, display_height*5/6), measure_distance_from=from_grid)


	#smallText = pygame.font.Font("freesansbold.ttf", 12)
	#textSurf, textRect = text_objects("Choose a grid to place your new repeater", smallText)
	#textRect.center = (display_width*2/3, display_height*5/6)
	#gameDisplay.blit(textSurf, textRect)


	

  pygame.mouse.set_cursor(*pygame.cursors.arrow)
  pygame.display.update()

  create_key(from_grid, nearest_grid)

  #main_loop()


def choice_selection(message, position, is_repeater=True, measure_distance_from=None):
  clearUI()
  smallText = pygame.font.Font("freesansbold.ttf", 12)
  textSurf, textRect = text_objects(message, smallText)
  textRect.center = position
  gameDisplay.blit(textSurf, textRect)

  remove_next = None

  while True:
    for event in pygame.event.get():
      #print(event)
      if event.type == pygame.QUIT:
        quitgame()
      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        if pos[1] < display_height * 2/3:
          grid_block = (pos[0] - (pos[0]% 50), pos[1] - (pos[1] % 50))
          if is_repeater:
            if grid_block in repeaters:
              del repeaters[grid_block]
              print("TODO: implement deletion")
            else:
              repeaters[grid_block] = red
              draw_grid((0,0), display_width, int(display_height * 2/3))
          else:
            if grid_block not in computers: print("choice must be in a computer", 1/0)
          return grid_block

    if measure_distance_from:
      gameDisplay.fill(pygame.Color("white"), (position[0]-100, position[1] + 25, 200, 50))
      pos = pygame.mouse.get_pos()
      nearest = (pos[0] - (pos[0]% 50), pos[1] - (pos[1] % 50))
      dist =  math.sqrt( ((measure_distance_from[0] - nearest[0])/50)**2 +((measure_distance_from[1] - nearest[1])/50)**2)
      loss = qkd.calc_loss(0.1, dist)
      label = "Distance: " + str(round(dist, 3)) + "=> loss: " + str(round(loss,3))
      colour = [(1-loss) * green[j] + loss * red[j] for j in range(3)]
      textSurf, textRect = text_objects(label, smallText, colour=colour)
      textRect.center = (position[0], position[1] + 50)
      gameDisplay.blit(textSurf, textRect)

      if remove_next and nearest != remove_next:
        print("here", remove_next)
        rect = pygame.Rect(remove_next[0], remove_next[1], 50, 50)
        pygame.draw.rect(gameDisplay, white, rect, 0)
        pygame.draw.rect(gameDisplay, grey, rect, 1)
        remove_next = None


      if nearest not in computers or nearest not in repeaters:
        rect = pygame.Rect(nearest[0], nearest[1], 50, 50)
        pygame.draw.rect(gameDisplay, light_red, rect, 0)
        remove_next = nearest

    pygame.display.update()
    clock.tick(30)
    
      




def create_key(a, b):
  global n

  while True:
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        quitgame()

    clearUI()
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
      print("great success")
      dist = distance(a,b)/50
      clearUI()
      q.run_protocol(dist)
      draw_lines(q.n_sent-q.n_received, q.n_received, (a[0] + 50, a[1]), b)
      repeaters[b] = green
      #time.sleep(5)
      draw_grid()
      connections[q.get_key()] = (a, b)
      textSurf, textRect = text_objects("Keys : \n" + q.get_key(), smallText)
      textRect.center = (display_width*3/4, display_height*5/6)
      gameDisplay.blit(textSurf, textRect)

      print("added the text ting", textRect.center)
      main_loop()
    except:
      if len(n) > 0:
        textSurf, textRect = text_objects("Invalid input", smallText, colour=red)
        textRect.center = (textRect.left+100, display_height*5.5/6)
        gameDisplay.blit(textSurf, textRect)

    pygame.display.update()
    clock.tick(30)

def update_n():
  global n
  n = textinput.get_text()
  print("n now", n, len(n))

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def draw_lines(red_lines, green_lines, a, b):
  red_remaining = red_lines
  green_remaining = green_lines

  n_drawn = 0

  drawn_lines = {"red": [((0,0),(0,0))]*(red_lines + green_lines), "green":[]}

  while red_remaining + green_remaining > 0 or max(drawn_lines["red"]) != ((0,0),(0,0)):
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        quitgame()


    gameDisplay.fill(pygame.Color("white"), (a[0], a[1], b[0]-a[0], b[1]-a[1] + 50))
    if green_remaining > 0 and random.random() > red_remaining/green_remaining:
      #draw a green line
      sep = n_drawn/green_lines * 50
      coords = ((a[0], a[1] + sep), (b[0], b[1] + sep))
      #pygame.draw.line(gameDisplay, green, (a[0], a[1] + sep), (b[0], b[1] + sep)))
      drawn_lines["green"].append(coords)
      n_drawn += 1
      green_remaining -= 1
    elif red_remaining > 0:
      sep1 = random.random() * 50
      sep2 = random.random() * 50
      coords = ((a[0], a[1] + sep1), (b[0], b[1] + sep2))
      drawn_lines["red"].insert(0, coords)
      red_remaining -= 1
    
    drawn_lines["red"].insert(0, ((0,0),(0,0)))
    
    drawn_lines["red"] = drawn_lines["red"][:red_lines + green_lines]
    
    #print("drawing ", len(drawn_lines["green"]), " green lines")
    for fr, to in drawn_lines["green"]:
      pygame.draw.line(gameDisplay, green, fr, to, 2)
    for i, (fr, to) in enumerate(drawn_lines["red"]):
      if (fr, to) != (0,0): 
        c = (i+1)/len(drawn_lines["red"]) * 255
        new_col = [min(j + c, 255) for j in red]
        #print("drawing red with colour", new_col)
        pygame.draw.line(gameDisplay, red + (i/len(drawn_lines["red"]), ), fr, to)
      
    pygame.display.update()
    clock.tick(30)
    #print(drawn_lines["red"])
    
#show_tutorial()
main_loop()
