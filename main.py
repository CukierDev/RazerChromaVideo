from PIL import Image
import os
from os.path import isfile, join
import subprocess

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import argparse

import time
import pygame

from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants

parser = argparse.ArgumentParser()
#parser.add_argument("--help", help="Show this help message and exit.")
parser.add_argument("--no-audio", action="store_true", help="don't play audio")
parser.add_argument("-k", "--keyboard-mode", action="store_true", help="play the video only on the keyboard")
parser.add_argument("-l", "--loop", action="store_true", help="loop video")
args = parser.parse_args()

device_manager = DeviceManager()

fps = (1 / 30)

if not os.path.isfile("vid.mp4"):
    print("No video file exists (no vid.mp4 in the script location)")

os.system("rm -fr tmp")
os.mkdir("tmp")
print("Extracting frames...")
subprocess.run(["ffmpeg", "-i", "vid.mp4", "tmp/frame-%03d.png"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#os.system('ffmpeg -i "vid.mp4" "tmp/frame-%03d.png"')
print("Extracting audio...")
subprocess.run(["ffmpeg", "-i", "vid.mp4", "-vn", "tmp/audio.ogg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#os.system('ffmpeg -i "vid.mp4" -vn tmp/audio.ogg')

frames = [f for f in os.listdir("tmp") if isfile(join("tmp", f))]

print("Found {} Razer devices".format(len(device_manager.devices)))

devices = device_manager.devices
for device in list(devices):
    if not device.fx.advanced:
        print("Skipping device " + device.name + " (" + device.serial + ")")
        devices.remove(device)

print()
device_manager.sync_effects = False

def resize(x,y, image):
    if not image.endswith(".png"):
        return

    if os.path.isfile("tmp/last.png"):
        os.remove("tmp/last.png")
    size = x,y

    im = Image.open("tmp/"+image)
    im_resized = im.resize(size, Image.Resampling.NEAREST)
    im_resized.save("tmp/last.png", "PNG")

fps = 1/int(input("Enter frames per second: "))
input("Press enter when you are ready.")
print("Enjoy the show ;)")

def playAudio():
    pygame.mixer.init()
    pygame.mixer.music.load('tmp/audio.ogg')
    pygame.mixer.music.play()

def draw():
    for image in frames:
        start = time.time()
        for device in devices:
                if args.keyboard_mode and not device.type == "keyboard":
                    break
                #print("Drawing to device " + device.name + " (" + device.serial + ")")
                rows, cols = device.fx.advanced.rows, device.fx.advanced.cols
                resize(cols, rows, image)

                im = Image.open('tmp/last.png')
                pix = im.load()
                #print("Keyboard size:", cols, rows)
                #print("Image size:", im.size)

                for row in range(rows):
                    for col in range(cols):
                        rgb = pix[col,row]
                        device.fx.advanced.matrix[row, col] = rgb

                device.fx.advanced.draw()

        end = time.time()
        length = end - start
        #print(length)
        if length < fps:
            time.sleep(fps-length)
        else:
            print(f"I can't keep up with drawing! ({image})")

def loop():
    if not args.no_audio:
        playAudio()
    draw()
    loop()

if args.loop:
    loop()
else:
    if not args.no_audio:
        playAudio()
    draw()