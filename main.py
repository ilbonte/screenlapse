__author__ = 'Bonte'

import thread
import time
from VideoCapture import Device

from PIL import ImageGrab
from PIL import Image
import pygame

choice = 0
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h

def input_thread(L):
    raw_input()
    L.append(None)


def do_screen():
    L = []
    i = 0
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(.5)
        i = i + 1
        istr = str(i)
        ImageGrab.grab().save("imgs/" + istr + ".png", "PNG")
        print "saved"
        if L:
            main()
            break


def do_cam():
    L = []
    i = 0
    cam = Device()
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(1)
        i = i + 1
        istr = str(i)

        cam.saveSnapshot("imgs/" + istr + ".png")

        print "saved"
        if L:
            main()
            break


def do_both():
    L = []
    i = 0
    cam = Device()
    thread.start_new_thread(input_thread, (L,))
    photo = cam.getImage(3, 1, "tl")
    photoWidth, phoroHeight = photo.size
    combinedImage = Image.new("RGB", (width + photoWidth, height), color=0)
    while 1:
        time.sleep(1)
        i = i + 1
        istr = str(i)

        combinedImage.paste(ImageGrab.grab(), (0, 0))
        photo = cam.getImage(3, 1, "tl")
        combinedImage.paste(photo, (width, 0))
        # ImageGrab.grab().save("imgs/screen" + istr + ".png", "PNG")
        # cam.saveSnapshot("imgs/" + istr + ".png")
        combinedImage.save("imgs/" + istr + ".png")
        print "saved"
        if L:
            main()
            break



def main():
    choice = int(raw_input("Scegli cosa vuoi fare: \n 1 per printare\n 2 per camera \n 3 combined \n 0 per uscire"))
    if choice == 1:
        do_screen()
    elif choice == 2:
        do_cam()
    elif choice == 3:
        do_both()
    elif choice == 0:
        print "Ciao! :D"
    else:
        print "Opzione non valida"

main()
