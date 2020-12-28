import numpy
import time
from ppadb.client import Client
from PIL import Image


#Fonctions utilitaires

def capture():
	image = device.screencap()

	with open('screen.png', 'wb') as f:
		f.write(image)

	image = Image.open('screen.png')
	image = numpy.array(image, dtype=numpy.uint8)

	return image
	
#Fonctions d'interaction
def avance():
	device.shell('input touchscreen swipe 750 3000 750 50 3500')

def avanceUnPeut():
	device.shell('input touchscreen swipe 750 3000 750 50 500')

def decale():
	device.shell('input touchscreen swipe 1050 3000 750 3000 250')

def reDecale(nbDecale):
	while(nbDecale!=0):
		device.shell('input touchscreen swipe 750 3000 1050 3000 250')
		print(nbDecale)
		nbDecale+=-1

def retourMilieu():
	milieu = False
	while(not milieu):
		capture

def roue():
	device.shell('input touchscreen swipe 500 2300 500 2300')
	time.sleep(6)

def diable():
	device.shell('input touchscreen swipe 420 2400 420 2400')
	time.sleep(1)

def marchand():
	device.shell('input touchscreen swipe 120 3000 120 3000')
	time.sleep(1)

#Fonctions de détection
def bloque():
	image = capture()

	image = image[0][0]

	if(image[0]>230 and image[1]>230 and image[2]>230):
		return False
	return True

def demandeChoixComp():
	image = capture()

	image = image[800][1330]

	if(image[0]==255 and image[1]==181 and image[2]==0):
		return True
	return False

def choixComp():
	device.shell('input touchscreen swipe 300 2150 300 2150')

def bossAlive():
	image = capture()

	image = image[200][240]

	if(image[0]>245 and image[1]>125 and image[1]<145 and image[2]>25 and image[2]<60):
		return True
	return False

def porteOuverte():
	image = capture()

	image = image[1103][659]

	if(image[0]>250 and image[1]>250 and image[2]>200):
		return True
	return False

def marchandEstLa():
	image = capture()
	image = image[2995][120]

	print(image[0], image[1], image[2])

	if(image[0]==255 and image[1]==255 and image[2]==255):
		return True
	return False


#Fonctions d'action
def ange():
	avance()
	time.sleep(1)
	choixComp()
	avanceUnPeut()
	marchand()
	avanceUnPeut()

def norm():
	nbDecale=0

	avance()

	while bloque():
		decale()
		nbDecale+=1
		avance()

	while not porteOuverte() and not demandeChoixComp():
		time.sleep(1)

	while demandeChoixComp():
		choixComp()
		time.sleep(2)
		if marchandEstLa():
			marchand()

	reDecale(nbDecale)

	time.sleep(1)
	if marchandEstLa():
		marchand()

	avanceUnPeut()

def boss():
	time.sleep(3)
	while bossAlive():
		time.sleep(1)

	while demandeChoixComp():
		time.sleep(3)
		choixComp()

	avance()

	roue()
	if marchandEstLa():
		marchand()

	diable()

	avanceUnPeut()

def debut():
	choixComp()

	avance()

	roue()

	avance()

##MAIN
#Prérequis
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices)==0:
    print("Pas d'appareil connecté")
    quit()

device = devices[0]

#Jeu
choixComp()

lvl = ['d','a','n','a','b','n','a','n','a','b','n','a','n','a','b','n','a','n','a','b']

for lvlCourant in lvl:
	if lvlCourant=='a':
		ange()
	elif lvlCourant=='n':
		norm()
	elif lvlCourant=='b':
		boss()
	else:
		debut()
