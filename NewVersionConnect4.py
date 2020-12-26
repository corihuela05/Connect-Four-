import pygame
import sys
import math
from pygame import mixer
import random
import numpy as np

mixer.init()

BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BROWN=(101,67,33)
BLUE=(135,206,235)
ROW_COUNT = 6
COLUMN_COUNT = 7

 #Background Music
SongList= ['NoSleep.ogg', 'RainOnMe.ogg', 'NoSleep.ogg', 'happiness.ogg', 'LoseSomebody.ogg',"playlist.ogg" ]

#pygame.mixer.music.load('NoSleep.ogg')
#pygame.mixer.music.play(0)
for song in SongList :
        RandomSong= random.choice(SongList)
        pygame.mixer.music.load(RandomSong)
        pygame.mixer.music.play()
        NextSong=random.choice(SongList)
        pygame.mixer.music.queue(NextSong)

'''
def play_a_different_song():
    global _currently_playing_song, _songs
    next_song = random.choice(_songs)
    while next_song == _currently_playing_song:
            _currently_playing_song = next_song
            pygame.mixer.music.load(_currently_playing_song)
            pygame.mixer.music.play(1)
            next_song = random.choice(_songs)
            pygame.mixer.music.queue(next_song)

play_a_different_song()
'''
winner_sound=mixer.Sound("WinnerSound.ogg")
game_ended=mixer.Sound("GameOver.ogg")

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_checker(board, row, col, piece):
	board[row][col] = piece

def is_empty_spot(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_line(board, col):
	for row in range(ROW_COUNT):
		if board[row][col] == 0:
			return row

def print_board(board):
	print(np.flip(board, 0))
'''
def full_board(board, row, col):
	for col in board[ROW_COUNT-1][col]:
		if board[ROW_COUNT-1][col] !=0:
			return True
'''
def winner_move(board, piece):
	# Check horizontal locations for win
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True

	# Check vertical locations for win
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][cow] == piece:
				return True

	# Check positively sloped diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True

	# Check negatively sloped diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(3, ROW_COUNT):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True

def draw_board(board):
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			pygame.draw.rect(screen, BROWN, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, YELLOW, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			if board[row][col] == 1:
				pygame.draw.circle(screen, RED, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[row][col] == 2:
				pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLUE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BROWN, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_empty_spot(board, col):
					row = get_next_open_line(board, col)
					drop_checker(board, row, col, 1)

					if winner_move(board, 1):
						pygame.mixer.music.pause()
						label = myfont.render("Player 1 wins!!", 1, RED)
						winner_sound.play()
						screen.blit(label, (40,10))
						game_over = True


			# # Ask for Player 2 Input
			else:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_empty_spot(board, col):
					row = get_next_open_line(board, col)
					drop_checker(board, row, col, 2)

					if winner_move(board, 2):
						pygame.mixer.music.pause()								
						label = myfont.render("Player 2 wins!!", 1, BLACK)
						winner_sound.play()
						screen.blit(label, (40,10))
						game_over = True


			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2
			

			if game_over:
				pygame.time.wait(3000)
