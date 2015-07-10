__author__ = 'Bonte'

import thread
import time
from VideoCapture import Device
from datetime import datetime
import os
import sys

from PIL import ImageGrab
from PIL import Image
import pygame
import cv2

waitTime = 5
choice = 0

pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h


def timestamp():
    adesso = datetime.now()
    datestring = ""
    datestring = datestring + str(adesso.year) + "_" + str(adesso.month) + "_" + str(adesso.day) + "-" + str(
        adesso.hour) + "-" + str(adesso.minute) + "-" + str(adesso.second)
    return datestring


def input_thread(L):
    raw_input()
    L.append(None)


def do_screen():
    L = []
    i = 0
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(waitTime)
        i = i + 1
        istr = str(i)
        ImageGrab.grab().save("imgs/" + istr + ".png", "PNG")
        print "saved" + istr
        if L:
            main()
            break


def do_cam():
    L = []
    i = 0
    cam = Device()
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(waitTime)
        i = i + 1
        istr = str(i)

        cam.saveSnapshot("imgs/" + istr + ".png")
        print "saved" + istr
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
        time.sleep(waitTime)
        i = i + 1
        istr = str(i)

        combinedImage.paste(ImageGrab.grab(), (0, 0))
        photo = cam.getImage(3, 1, "tl")
        combinedImage.paste(photo, (width, 0))
        combinedImage.save("imgs/" + istr + ".png")
        # combinedImage.save("imgs/" + timestamp() + ".png")
        print "saved" + istr
        if L:
            main()
            break


def update_progress(progress):
    sys.stdout.write("\r%d%%" % progress)
    sys.stdout.flush()

def do_movie():
    fileName = ""
    fps = 10
    immagini = []
    for immagine in os.listdir("imgs"):
        if immagine.endswith(".png"):
            fileName = immagine
            immagini.append(int(fileName[:-4]))
    immagini.sort()
    nfoto = immagini[-1]  # l'ultimo elemento della lista
    tempoStimato = nfoto / fps
    print "Il video durera' circa" + str(tempoStimato) + " secondi"

    scelta = int(
        raw_input("Segli 0 per continuare con l'elaborazione, 1 per inserire una durata custom \n -> "))
    if scelta == 1:
        # TODO: inserire la durata minima consigliata (almeno 5 fps)
        tempoScelto = int(raw_input("Inserisci la durata desiderata in SECONDI \n -> "))
        fps = nfoto / tempoScelto

    att = "imgs/" + str(immagini[0]) + ".png"
    img1 = cv2.imread(att)

    alt, larg, layers = img1.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('video.avi', fourcc, fps, (larg, alt))

    for foto in immagini:
        att = "imgs/" + str(foto) + ".png"
        perc = (100 * foto) / nfoto
        fotoImg = cv2.imread(att)
        video.write(fotoImg)
        update_progress(perc)

    cv2.destroyAllWindows()
    video.release()


def main():
    choice = int(
        raw_input("Scegli cosa vuoi fare: \n 1 per fare solo screen\n 2 per fare foto \n 3 screen e foto combinati "
                  "\n 4 per sttare l'intervallo di acquisizione \n 5 per generare il timelapse \n 0 per uscire\n -> "))
    if choice == 1:
        do_screen()
    elif choice == 2:
        do_cam()
    elif choice == 3:
        do_both()
    elif choice == 4:
        global waitTime
        waitTime = int(raw_input("Ogni quanto salvare la foto (default 10) \n -> "))
        main()
    elif choice == 5:
        do_movie()
    elif choice == 0:
        print "Ciao! :D"
    else:
        print "Opzione non valida"


main()
