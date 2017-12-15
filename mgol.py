import pygame
import numpy as np
from pygame.locals import *


screen_size=500
cases = 10
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
matrice = np.zeros((cases,cases))
unit = screen_size/cases

def maj(screen):
	fenetre.fill(white)
	for x in range(matrice.shape[0]):
			for y in range(matrice.shape[1]):
				if matrice.item((x,y)) == 0:
					pygame.draw.rect(screen, black,(x*unit,y*unit,unit,unit),1)
				elif matrice.item((x,y)) == 1:
					pygame.draw.rect(screen, red,(x*unit,y*unit,unit,unit),0)
	pygame.display.update()

pygame.init()
fenetre = pygame.display.set_mode((int(screen_size*1.1),screen_size), RESIZABLE)
maj(fenetre)



continuer = 1

while continuer:
	for event in pygame.event.get():
		if event.type == QUIT:
			continuer = 0
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			pos = (np.asarray(pos)/(screen_size/cases)).astype(int)
			try:
				if matrice.item(tuple(pos)) == 0:
					matrice[tuple(pos)] = 1
				else:
					matrice[tuple(pos)] = 0
				maj(fenetre)
				pygame.display.update()
			except:
				print('launch')

