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
text1.config(font=("monospace",15))
scale1 = Scale(window, variable = screen, orient='horizontal', from_=500, to=1000,
      resolution=50, tickinterval=100, length=500,
      label='Taille de l\'écran :')
scale1.config(font=("monospace",12))
scale2 = Scale(window, variable = case, orient='horizontal', from_=10, to=100,
      resolution=10, tickinterval=10, length=500,
      label='Cases par cotés :')
scale2.config(font=("monospace",12))
button = Button(window, text="Valider", command = sel)
button.config(font=("monospace",12))
text1.pack()
scale1.pack()
scale2.pack()
button.pack(anchor=CENTER)
window.mainloop()