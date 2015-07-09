__author__ = 'Bonte'

import thread
import time
from VideoCapture import Device

from PIL import ImageGrab

choice = 0


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


def main():
    choice = int(raw_input("Scegli cosa vuoi fare: \n 0 per printare\n 1 per camera"))
    if choice == 0:
        do_screen()
    elif choice == 1:
        do_cam()
    else:
        print "nada"

main()
