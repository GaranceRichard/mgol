import pygame
import numpy as np
from pygame.locals import *
from interface import *

couleur=1
matrice = np.zeros((cases,cases))
unit = screen_size/cases
continuer = 1
repeat = 0
etat_du_jeu = "Lancer"

def colors(couleur):
	global white, black, red, green
	if couleur == 1:
		white = (255,255,255)
		black = (0,0,0)
		red = (255,0,0)
		green = (0,255,0)
	if couleur == 2:
		black = (255,255,255)
		white = (0,0,0)
		red = (255,0,0)
		green = (0,255,0)

def maj(screen):
	#mise à jour de l'écran
	colors(couleur)
	fenetre.fill(white)
	myfont = pygame.font.SysFont("monospace", 25,bold=True)
	label0 = myfont.render("Génération :", 1, red)
	label = myfont.render(str(repeat), 1, red)
	label2 = myfont.render(str(etat_du_jeu), 1, black)
	label2b = myfont.render("taille :", 1, green)
	label3 = myfont.render(str(matrice.shape[0])+"x"+str(matrice.shape[0]), 1, green)
	fenetre.blit(label0, (screen_size+10, 10))
	fenetre.blit(label, (screen_size+10, 30))
	fenetre.blit(label2, (screen_size+10, screen_size/2))
	fenetre.blit(label2b, (screen_size+10, 70))
	fenetre.blit(label3, (screen_size+10, 90))
	for x in range(matrice.shape[0]):
		if matrice.shape[0]>100 and matrice[x].max()==0:
			pass
		else:
			for y in range(matrice.shape[1]):
				if matrice.item((x,y)) == 0 and matrice.shape[0]<=100:
					pygame.draw.rect(screen, black,(x*unit,y*unit,unit,unit),1)
				elif matrice.item((x,y)) == 1:
					pygame.draw.rect(screen, red,(x*unit,y*unit,unit,unit),0)
	pygame.draw.line(screen,black,(screen_size,0),(screen_size,screen_size))
	pygame.display.update()


def control(x,y):
	#fonction de contrôle qui permet de compter l'entourage d'une cellule
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
	except IndexError:
		pass
	return sum(control_array)

def click(button):
	global matrice, cases, unit, continuer,couleur, etat_du_jeu
	if button == 4 and matrice.shape[0]>2:
		matrice = matrice[1:-1,1:-1]
		cases = matrice.shape[0]
	if button == 5:
		matrice = np.pad(matrice,1,'constant')
		cases = matrice.shape[0]
	if button == 3:
		transitoire = ((matrice*8)+np.random.randint(11,size=matrice.shape))>7
		matrice = transitoire+0
	if button == 2:
		if couleur == 1:
			couleur = 2
		else:
			couleur = 1
	if button == 1:
		pos = pygame.mouse.get_pos()
		pos = (np.asarray(pos)/(screen_size/matrice.shape[0])).astype(int)
		try:
			if matrice.item(tuple(pos)) == 0:
				matrice[tuple(pos)] = 1
			else:
				matrice[tuple(pos)] = 0
		except IndexError:
			pygame.draw.rect(fenetre, green, (matrice.shape[0]*unit,0,(int(screen_size+200)-matrice.shape[0]),screen_size),0)
			pygame.display.update()
			if continuer == 1:
				continuer = 2
			else:
				etat_du_jeu = "Lancer"
				continuer = 1

	unit = screen_size/cases
	maj(fenetre)
	pygame.display.update()

pygame.init()
colors(couleur)
fenetre = pygame.display.set_mode((int(screen_size+200),screen_size))
pygame.display.set_caption('Jeu de la vie')
maj(fenetre)

test = 1
while test == 1:
	while continuer == 1: # boucle d'initialisation du panel
		etat_du_jeu = "Lancer"
		for event in pygame.event.get():
			if event.type == QUIT:
				test = 0
				continuer = 0
			if event.type == pygame.MOUSEBUTTONDOWN:
				click(event.button)



	while continuer == 2: # lancement du game of life
		etat_du_jeu = "Arrêter"
		repeat += 1
		control_matrice = np.pad(matrice,1,'constant') 	#on crée une matrice copie entourée de zéros
		future_matrice = np.zeros((cases+2,cases+2))	#la matrice de retour des entourage
		next_matrice = np.zeros((cases,cases))			#matrice générée

		for x in range(1,control_matrice.shape[0]-1):
			if (control_matrice[x-1].max() == 0) and (control_matrice[x].max() == 0) and (control_matrice[x+1].max() == 0):
				pass
			else:
				for y in range(1,control_matrice.shape[1]-1):
					future_matrice[(x,y)] = control(x,y)

		future_matrice = future_matrice[1:-1,1:-1]

		for x in range(future_matrice.shape[0]):
			for y in range(future_matrice.shape[1]):
				if (future_matrice.item((x,y)) == 3) or (matrice.item((x,y)) ==  1 and (future_matrice.item((x,y)) == 2)):
					next_matrice[(x,y)] = 1

		if (matrice == next_matrice).all():
			etat_du_jeu = "Arrêté"
			maj(fenetre)
			continuer = 1

		else:
			matrice = next_matrice
			maj(fenetre)
			pygame.display.update()

		for event in pygame.event.get():
				if event.type == QUIT:
					test = 0
					continuer = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					click(event.button)
