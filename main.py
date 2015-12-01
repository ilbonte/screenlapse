__author__ = 'Bonte'

import thread
import time
from VideoCapture import Device  # http://videocapture.sourceforge.net/
from datetime import datetime
import os
import sys

from PIL import ImageGrab  #https://pillow.readthedocs.org/en/3.0.x/
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pygame  # http://pygame.org/
import cv2  #http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_tutorials.html

waitTime = 5
choice = 0

pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h


def timestamp():
    now = datetime.now()
    datestring = ""
    datestring = datestring + str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "-" + str(
        now.hour) + "-" + str(now.minute) + "-" + str(now.second)
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
    photoWidth, photoHeight = photo.size
    combinedImage = Image.new("RGB", (width + photoWidth, height), color=0)
    startTime = time.time()
    print "Press enter to stop."
    while 1:
        time.sleep(waitTime)
        i = i + 1
        istr = str(i)

        combinedImage.paste(ImageGrab.grab(), (0, 0))
        photo = cam.getImage(3, 1, "tl")
        combinedImage.paste(photo, (width, 0))
        draw = ImageDraw.Draw(combinedImage)
        font = ImageFont.truetype("arialbd.ttf", 40)
        draw.rectangle([(width, photoHeight), (width + photoWidth, photoHeight + height - photoHeight)], fill="black",
                       outline="red")
        draw.text((width + 10, photoHeight + 10), datetime.now().strftime("%A, %d. %B %Y %I:%M%p"), (255, 255, 255),
                  font=font)
        elapsed = time.time() - startTime
        m, s = divmod(elapsed, 60)
        h, m = divmod(m, 60)
        formattedElapsed = "%d:%02d:%02d" % (h, m, s)
        draw.text((width + 10, photoHeight + 60), formattedElapsed, (255, 255, 255), font=font)
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
    pictures = []
    for immagine in os.listdir("imgs"):
        if immagine.endswith(".png"):
            fileName = immagine
            pictures.append(int(fileName[:-4]))
    pictures.sort()
    picturesNumber = pictures[-1]  # last element
    estimatedDuration = picturesNumber / fps
    print "Estimated duration:" + str(estimatedDuration) + " seconds"

    scelta = int(
        raw_input("Choose 0 to continue, 1 if you want choose a custom duration \n -> "))
    if scelta == 1:
        # TODO: inserire la durata minima consigliata (almeno 5 fps)
        customTime = int(raw_input("Insert desired duration in seconds \n -> "))
        fps = picturesNumber / customTime

    att = "imgs/" + str(pictures[0]) + ".png"
    img1 = cv2.imread(att)

    alt, larg, layers = img1.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('video.avi', fourcc, fps, (larg, alt))

    for foto in pictures:
        att = "imgs/" + str(foto) + ".png"
        perc = (100 * foto) / picturesNumber
        fotoImg = cv2.imread(att)
        video.write(fotoImg)
        update_progress(perc)

    cv2.destroyAllWindows()
    video.release()


def main():
    choice = int(
        raw_input(
            "Choose what you want ti do: \n 1 screenshot only \n 2 webcam snapshot \n 3 screenshot and snapshot combined"
            "\n 4 set capture interval (seconds) \n 5 generates timelapse (.avi) \n 0 exit\n -> "))
    if choice == 1:
        do_screen()
    elif choice == 2:
        do_cam()
    elif choice == 3:
        do_both()
    elif choice == 4:
        global waitTime
        waitTime = int(raw_input("Capture time in seconds (default: 10):  \n -> "))
        main()
    elif choice == 5:
        do_movie()
    elif choice == 0:
        print "Ciao! :D"
    else:
        print "Invalid option!"


main()
