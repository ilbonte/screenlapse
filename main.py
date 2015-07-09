__author__ = 'Bonte'

import thread
import time

from PIL import ImageGrab

choice = 0


def input_thread(L):
    raw_input()
    L.append(None)


def do_print():
    L = []
    i = 0
    thread.start_new_thread(input_thread, (L,))
    while 1:
        time.sleep(1)
        i = i + 1
        istr = str(i)
        ImageGrab.grab().save("imgs/" + istr + ".png", "PNG")

        print "saved"
        if L:
            main()
            break
        print "Hi Mom!"


def main():
    choice = int(raw_input("Cosa vuoi? 0 per printare"))
    if choice == 0:
        do_print()
    else:
        print "nada"


main()
