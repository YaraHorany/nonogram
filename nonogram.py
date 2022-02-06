import pygame  # Import the pygame library
import numpy as np
import random

pygame.init() # initialize the pygame

# ---------
# CONSTANTS
# ---------
BOARD_ROWS = 10
BOARD_COLS = 10
WIDTH = 500
HEIGHT = 650
# rgb: red green blue
WHITE = (255,255,255)
BLACK = (0, 0, 0)
LIGHT_GREY = (169,169,169)
GREY = (100,100,100)

# Load images
icon = pygame.image.load('icon.png')
xImg = pygame.image.load('x.png')
black_square = pygame.image.load('black_square.png')
redHeartImg = pygame.image.load('red_heart.png')
whiteHeartImg = pygame.image.load('white_heart.png')
fire_work = pygame.image.load('fire_work.png')
sad_emoji = pygame.image.load('sad_emoji.jpg')
  
# Create the screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Caption and Icon
pygame.display.set_caption("Nonogram")
pygame.display.set_icon(icon)

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros((BOARD_ROWS,BOARD_COLS))

# Fonts
font = pygame.font.Font('freesansbold.ttf', 50)
level_completed_text = font.render('Level completed!', True, WHITE, None)
textRect = level_completed_text.get_rect()	 
textRect.center = (WIDTH // 2, 300) # set the center of the rectangular object.

smallfont = pygame.font.SysFont('Corbel',30)  
Next_level = smallfont.render('Next Level' , True , WHITE)
restart_level = smallfont.render('Restart' , True , WHITE)

font2 = pygame.font.Font('freesansbold.ttf', 50)
game_over_text = font2.render('Out Of Lives', True, BLACK, WHITE)
textRect2 = game_over_text.get_rect()	 
textRect2.center = (WIDTH // 2, 300) # set the center of the rectangular object.

# ---------
# FUNCTIONS
# ---------
def create_board():
	i=0
	resultBoard = np.zeros((BOARD_ROWS,BOARD_COLS))
	while i < BOARD_ROWS:
		count = 0
		for j in range(BOARD_COLS):
			resultBoard[i][j] = random.randint(1, 2)
			if resultBoard[i][j] == 1 :
				count+=1

		if count != 0: # Making sure each row contains at least a '1'
			i += 1
	j=0
	while j < BOARD_COLS: # Making sure each column contains at least a '1'
		count = 0
		for i in range(BOARD_ROWS):
			if resultBoard[i][j] == 1:
				count+=1
		if count == 0:
			for i in range(BOARD_ROWS):
				resultBoard[i][j] = random.randint(1, 2)
		else:
			j += 1

	return resultBoard 

def makeRules(resultBoard, rows): # It works also for the columns and rows

	length = BOARD_ROWS if rows == 1 else BOARD_COLS
	rules = []* length

	for j in range(length):
		info = list()
		count = 0
		tempArr = resultBoard[j,:] if rows == 1 else resultBoard[:,j]
		for i in range(len(tempArr)):
			if tempArr[i] == 1:
				count +=1
			else: # if it's equal to 2
				if count!=0:
					info.append(count)
					count=0
		if count!=0:
			info.append(count)
		rules.append(info)
		
	return rules

def draw_lines():
	x=145
	y=240
	for i in range(BOARD_ROWS+1):
		thickness = 3 if i%5==0 else 1
		pygame.draw.line(screen, BLACK, (55,y),(445,y), thickness)
		y+=30

	for j in range(BOARD_COLS+1):
		thickness = 3 if j%5==0 else 1
		pygame.draw.line(screen, BLACK, (x,150),(x,540), thickness)
		x+=30

	pygame.draw.line(screen, BLACK, (145,150),(445,150), 3)
	pygame.draw.line(screen, BLACK, (55,240),(55,540), 3)

def fill_Rules(rowsInfo, colsInfo):
	y = 255
	for lst in rowsInfo:
		font = pygame.font.SysFont(None, 20)
		img = font.render(' '.join(map(str, lst)), True, BLACK)
		screen.blit(img, (65, y))
		y += 30

	x = 155
	for i in colsInfo:
		y = 160
		for j in i:
			font = pygame.font.SysFont(None, 20)
			img = font.render(str(j), True, BLACK)
			screen.blit(img, (x, y))
			y += 15
		x += 30

def change_choice(choice):	
	if choice == 1:
		choice = 2
		pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(257, 582, 42, 35))
		pygame.draw.rect(screen, WHITE, pygame.Rect(212, 582, 42, 35))
	else:
		choice = 1
		pygame.draw.rect(screen, WHITE, pygame.Rect(257, 582, 42, 35))
		pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(212, 582, 42, 35))
	screen.blit(xImg, (220, 587))
	screen.blit(black_square, (265, 587))

	return choice

def convertRowCol(mouseX, mouseY): 
	checked_row = int((mouseY - 240) / 30)
	checked_col = int((mouseX - 145) / 30)
	return checked_row, checked_col

def available_square(row, col):
	return board[row][col] == 0

def check_correctness(row, col, choice):
	return resultBoard[row][col] == choice

def mark_square(row, col): # choice is equal to 1 OR 2
	board[row][col] = resultBoard[row][col]

def check_win():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if resultBoard[row][col] == 1:
				if board[row][col] != 1:
					return False
	return True

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):			
			if board[row][col] == 1: # draw a black rectangle
				pygame.draw.rect(screen, BLACK, pygame.Rect(145+(col*30), 240+(row*30), 30, 30))
			elif board[row][col] == 2: # draw an X
				screen.blit(xImg, (148+(col*30), 243+(row*30)))

def update_lives(heartX, heartY, lives):
	i=-1
	if(lives!=0):
		for i in range(lives):
			pygame.draw.rect(screen, WHITE, pygame.Rect(heartX, heartY, 30, 30))
			screen.blit(redHeartImg, (heartX, heartY))
			heartX = heartX + 30
	for j in range(i+1,3):
		pygame.draw.rect(screen, WHITE, pygame.Rect(heartX, heartY, 30, 30))
		screen.blit(whiteHeartImg, (heartX, heartY))
		heartX = heartX + 30

def fill_xes(row, col):
	bol = True
	for j in range(BOARD_COLS):
		if resultBoard[row][j] == 1:
			if board[row][j] != 1:
				bol = False
	if bol == True:
		for j in range(BOARD_COLS):
			if board[row][j] != 1:
				board[row][j] = 2

	bol = True
	for i in range(BOARD_ROWS):
		if resultBoard[i][col] == 1:
			if board[i][col] != 1:
				bol = False
	if bol == True:
		for i in range(BOARD_COLS):
			if board[i][col] != 1:
				board[i][col] = 2

def create_game():
	screen.fill(WHITE)
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0
	resultBoard = create_board()
	rowsInfo = makeRules(resultBoard, 1)
	colsInfo = makeRules(resultBoard, 0)
	fill_Rules(rowsInfo, colsInfo)
	pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(210, 580, 90, 40))
	pygame.draw.rect(screen, WHITE, pygame.Rect(257, 582, 42, 35))
	screen.blit(xImg, (220, 587))
	screen.blit(black_square, (265, 587))

	print(resultBoard)
	print(board)
	print('rows rules')
	print(rowsInfo)
	print('columns rules')
	print(colsInfo)

	return resultBoard

resultBoard = create_game()

# ---------
# VARIABLES
# ---------
lives = 3 # in each round a player can have 3 lives
choice = 1
gameOver = False

# Run until the user asks to quit
running = True
# --------
# MAINLOOP
# --------
while running:
# Did the user click the window close button?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			if not gameOver and not check_win():
				if(210 <= mouseX <= 300 and 580 <= mouseY <= 620):	# Changing the choice
					choice = change_choice(choice) # choice is equal to 1 OR 2

				elif 145 <= mouseX <= 444 and 240 <= mouseY <= 539:
					(checked_row, checked_col) = convertRowCol(mouseX, mouseY)

					if available_square(checked_row, checked_col):
						if check_correctness(checked_row, checked_col, choice) == True:
							mark_square(checked_row, checked_col)
						else: # Wrong choice
							mark_square(checked_row, checked_col)
							lives -=1				
						fill_xes(checked_row, checked_col)

			# Clicked the restart button in case of winning or losing
			elif WIDTH/2 - 75 <= mouseX <= WIDTH/2 + 65 and  395 <= mouseY <= 435:
				lives = 3
				choice = 1
				gameOver = False
				resultBoard =  create_game()

	draw_figures()
	update_lives(210, 50, lives)
	mouse = pygame.mouse.get_pos()
	if lives == 0: # Game over
		gameOver = True
		screen.fill(WHITE)
		screen.blit(pygame.transform.scale(sad_emoji,(WIDTH,HEIGHT)),(0,0))
		screen.blit(game_over_text , textRect2)

		# if mouse is hovered on a button it changes to lighter shade
		if  WIDTH/2 - 75 <= mouse[0] <= WIDTH/2 + 65 and  395 <= mouse[1] <= 435:
			pygame.draw.rect(screen, LIGHT_GREY,[WIDTH/2 - 75, 395 ,140,40])
		else:
			pygame.draw.rect(screen, GREY,[WIDTH/2 - 75, 395 ,140,40])

		screen.blit(restart_level , (WIDTH/2 - 50, 400))

	if check_win(): # Level completed
		screen.fill(WHITE)
		screen.blit(pygame.transform.scale(fire_work,(WIDTH,HEIGHT)),(0,0))
		screen.blit(level_completed_text, textRect)
	
		# if mouse is hovered on a button it changes to lighter shade
		if  WIDTH/2 - 75 <= mouse[0] <= WIDTH/2 + 65 and  395 <= mouse[1] <= 435:
			pygame.draw.rect(screen, LIGHT_GREY,[WIDTH/2 - 75, 395 ,140,40])
		else:
			pygame.draw.rect(screen, GREY,[WIDTH/2 - 75, 395 ,140,40])

		screen.blit(Next_level , (WIDTH/2 - 70, 400))

	pygame.display.update()

# Done! Time to quit.
pygame.quit()