import pygame
import numpy as np
from pygame.locals import *
from tkinter import *

window = Tk()
window.title("Jeu de la vie")
screen=IntVar()
case = IntVar()

def sel():
	global screen_size, cases
	screen_size = screen.get()
	cases = case.get()
	window.destroy()

text1 = Label(window,text="Paramètres de l'application :")
scale1 = Scale(window, variable = screen, orient='horizontal', from_=500, to=1000,
      resolution=10, tickinterval=100, length=500,
      label='Taille de l\'écran')
scale2 = Scale(window, variable = case, orient='horizontal', from_=10, to=100,
      resolution=1, tickinterval=10, length=500,
      label='Cases par cotés')
button = Button(window, text="Valider", command = sel)
text1.pack()
scale1.pack()
scale2.pack()
button.pack(anchor=CENTER)
window.mainloop()


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
matrice = np.zeros((cases,cases))
unit = screen_size/cases
continuer = 1
repeat = 0
etat_du_jeu = "Lancer"

def maj(screen):
	fenetre.fill(white)
	myfont = pygame.font.SysFont("monospace", 25,bold=True)
	label = myfont.render(str(repeat), 1, (255,0,0))
	label2 = myfont.render(str(etat_du_jeu), 1, (0,0,0))
	fenetre.blit(label, (screen_size+10, 10))
	fenetre.blit(label2, (screen_size+10, screen_size/2))	
	for x in range(matrice.shape[0]):
			for y in range(matrice.shape[1]):
				if matrice.item((x,y)) == 0:
					pygame.draw.rect(screen, black,(x*unit,y*unit,unit,unit),1)
				elif matrice.item((x,y)) == 1:
					pygame.draw.rect(screen, red,(x*unit,y*unit,unit,unit),0)
	pygame.display.update()

pygame.init()
fenetre = pygame.display.set_mode((int(screen_size+150),screen_size))
pygame.display.set_caption('Jeu de la vie')
maj(fenetre)

test = 1
while test == 1:
	while continuer == 1: # boucle d'initialisation du panel
		repeat = 0
		for event in pygame.event.get():
			if event.type == QUIT:
				test = 0
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
				except IndexError:
					pygame.draw.rect(fenetre, green, (matrice.shape[0]*unit,0,(int(screen_size+150)-matrice.shape[0]),screen_size),0)
					pygame.display.update()
					continuer = 2

	while continuer == 2: # lancement du game of life
		etat_du_jeu = "arrêter"
		repeat += 1
		control_matrice = np.pad(matrice,1,'constant') 	#on crée une matrice copie entourée de zéros
		future_matrice = np.zeros((cases+2,cases+2))	#la matrice de retour des entourage
		next_matrice = np.zeros((cases,cases))			#matrice générée
		

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
					test = 0
					continuer = 0
				if event.type == MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					pos = (np.asarray(pos)/(screen_size/cases)).astype(int)
					try:
						if matrice.item(tuple(pos)) == 0:
							matrice[tuple(pos)] = 1
						else:
							matrice[tuple(pos)] = 0
						maj(fenetre)
						pygame.display.update()
					except IndexError:
						etat_du_jeu = "Lancer"
						maj(fenetre)
						continuer = 1


