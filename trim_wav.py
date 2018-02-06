#!/usr/bin/python3
import pygame
import os
import sys
from pydub import AudioSegment

if len(sys.argv) < 4:
    print("Usage : python trim.py [classname] [name of human] [silence_threshold in dB (-32 is the best)]")
    sys.exit(1)

trim_ms = 0
index = 1
silence_threshold = float(sys.argv[3])  ## keep it -32 for the best result; I manually tested it
pygame.init()
pygame.font.init()
WIDTH = 600
HEIGHT = 300
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption('Audio Segmentation by Dileep Sankhla')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)
text1 = myfont.render('# Press [ARROW KEY DOWN] to replay the sound', False, (0,0,0))
text2 = myfont.render('# Press [ARROWN KEY LEFT] to delete the sound', False, (0,0,0))
text3 = myfont.render('# Press [ARROW KEY RIGHT] for save and next sound', False, (0,0,0))

SCREEN.fill(RED)
SCREEN.blit(text1, (10, 220))
SCREEN.blit(text2, (10, 120))
SCREEN.blit(text3, (10, 20))
pygame.display.flip()

def detect_leading_silence(sound,chunk_size=100):
    global trim_ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms * 0.001 < float(sound.duration_seconds):
        trim_ms += chunk_size

    return trim_ms


def detect_preceding_silence(sound,chunk_size=100):
    global trim_ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS > silence_threshold and trim_ms * 0.001 < float(sound.duration_seconds): 
        trim_ms += chunk_size

    return trim_ms

def play_sound(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

file_name = "classes/" + sys.argv[1] + "/" + sys.argv[2] + "/" + sys.argv[2] + ".wav"
direct = "classes/" + sys.argv[1] + "/" + sys.argv[2] + "/split"
if not os.path.exists(direct):
    os.makedirs(direct)
sound = AudioSegment.from_wav(file_name)
while True:
    listen = True
    start_trim = detect_leading_silence(sound)
    end_trim = detect_preceding_silence(sound)
    if trim_ms * 0.001 >= float(sound.duration_seconds):
        break
    trim_sound = sound[start_trim:end_trim]
    export_name = "classes/" + sys.argv[1] + "/" + sys.argv[2] + "/split/Rec_" + str(index) + ".wav"
    trim_sound.export(export_name, format="wav")
    play_sound(export_name)  
    while listen:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    os.remove(export_name)
                    print("Audio segment deleted!\n")
                    listen = False
                    break
                elif event.key == pygame.K_DOWN:
                    play_sound(export_name)
                    break
                elif event.key == pygame.K_RIGHT:
                    index += 1
                    print("Generating " + export_name + " ...\n")
                    listen = False
                    break
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()

pygame.quit()
