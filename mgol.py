import pygame
import numpy as np
from pygame.locals import *


screen_size=700
cases = 100
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
matrice = np.zeros((cases,cases))
unit = screen_size/cases
continuer = 1

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




while continuer == 1: # boucle d'initialisation du panel
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
				pygame.draw.rect(fenetre, green, (matrice.shape[0]*unit,0,(int(screen_size*1.1)-matrice.shape[0]),screen_size),0)
				pygame.display.update()
				continuer = 2

while continuer == 2: # lancement du game of life
	control_matrice = np.pad(matrice,1,'constant')
	future_matrice = np.zeros((cases+2,cases+2))
	next_matrice = np.zeros((cases,cases))
	

	def control(x,y):
		try:
			control_array = [0]*8	
			control_array[0] = control_matrice.item((x-1,y+1))
			control_array[1] = control_matrice.item((x,y+1))
			control_array[2] = control_matrice.item((x+1,y+1))
			control_array[3] = control_matrice.item((x-1,y))
			control_array[4] = control_matrice.item((x+1,y))
			control_array[5] = control_matrice.item((x-1,y-1))
			control_array[6] = control_matrice.item((x,y-1))
			control_array[7] = control_matrice.item((x+1,y-1))
		except:
			pass
		return sum(control_array)

	for x in range(control_matrice.shape[0]):
			for y in range(control_matrice.shape[1]):
				a=control(x,y)
				future_matrice[(x,y)] = a

	future_matrice = future_matrice[1:-1,1:-1]

	for x in range(future_matrice.shape[0]):
		for y in range(future_matrice.shape[1]):
			if matrice.item((x,y)) ==  0 and future_matrice.item((x,y)) == 3:
				next_matrice[(x,y)] = 1
			if matrice.item((x,y)) ==  1 and (future_matrice.item((x,y)) == 3):
				next_matrice[(x,y)] = 1
			if matrice.item((x,y)) ==  1 and (future_matrice.item((x,y)) == 2):
				next_matrice[(x,y)] = 1

	matrice = next_matrice
	maj(fenetre)
	pygame.display.update()

	for event in pygame.event.get():
			if event.type == QUIT:
				continuer = 0

