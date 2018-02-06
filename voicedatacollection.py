#usr/bin/python2
from sys import byteorder
from array import array
from struct import pack
import pygame
import time
import pyaudio
import wave
import os
import sys


if len(sys.argv[:]) != 2:
    print " Usage : python2 voicedata.py [firstname in lowercase]"
    sys.exit()

dirc = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73','74','75','76','77','78','79','80','81','82','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','house','house_number','makan','makan_number','appartment','appartment_number','flat','flat_number','ghar','ghar_number','building','building_number','home','home_number','residence','residence_number','gate','gate_number','plot','plot_number']

stats = '.' + sys.argv[1] + '.stats'
stats_data = list()

try:
    file = open(stats, 'r')
    stats_data = [line[:-1] for line in file]
except IOError:
    file = open(stats, 'w')
    stats_data = ["0", "1"]

ind = dirc.index(stats_data[0])
ind -= 1
pygame.init()
pygame.font.init()
WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
myfont = pygame.font.SysFont('Comic Sans MS', 50)
pygame.display.set_caption('Audio Recording for NLP Data Collection by Dileep Sankhla')

GREY = (128,18,128)

SCREEN.fill(GREY)
pygame.display.flip()

THRESHOLD = 2000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def play_sound(sound):
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def is_silent(snd_data):
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    r = array('h', [0 for i in xrange(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds*RATE))])
    return r

def trim_with_delta(snd_data, seconds = None):
    size = len(snd_data)
    start, end = 0, size
    for i in range(size):
        if abs(snd_data[i])>THRESHOLD : 
            start = i  
            break
    for i in range(size-1, -1, -1):
        if abs(snd_data[i])>THRESHOLD : 
            end = i +1          # open end ... 'end' index doesn't have above threshod voice 
            break

    if seconds is not None: 
        start = start - int(seconds*RATE)
        if start < 0 : 
            print "start short by seconds: ", -start/float(RATE)
            start =0
        end = end + int(seconds*RATE)
        if end > size : 
            print "end short by seconds: ",(end-size)/float(RATE)
            end = size 

    print start, end
    return snd_data[int(start): int(end)] 

def record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while True:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)                   #kp-edit
    r = add_silence(r, 0.5)       #kp-edit
    #r = trim_with_delta(r, 0.5)       #kp-edit

    return sample_width, r

def record_to_file(path):
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


if __name__ == '__main__':
    counter = int(stats_data[1])
    while ind < 120:  # len(dirc)
        ind += 1
        direct = 'classes/' + dirc[ind] + '/' + sys.argv[1] + '/split'
        if not os.path.exists(direct):
            os.makedirs(direct)
        SCREEN.fill(GREY)	
        text1 = myfont.render(sys.argv[1], False, (255,255,255))
        SCREEN.blit(text1, (420, 50))
        speak = 'Speak : ' + dirc[ind]
        text2 = myfont.render(speak, False, (255,255,255))
        SCREEN.blit(text2, (420, 300))
        pygame.display.update()
        if counter == 100 or counter == 50 or counter == 30:
            counter = 1
        level = 0
        if ind >= 0 and ind <= 9:
            level = 100
        elif ind >= 10 and ind <= 100:
            level = 50
        else:
            level = 30

        time.sleep(5)

        while counter <= level:
            listen = True
            ctr = 'Counter : ' + str(counter)
            t1 = "RECORDING..."
            t2 = "USER MODE..."
            t3 = "PAUSED..."
            SCREEN.fill(GREY)
            SCREEN.blit(text1, (420,50))
            SCREEN.blit(text2, (420, 300))
            text3 = myfont.render(ctr, False, (255,255,255))
            SCREEN.blit(text3, (420, 500))
            textR = myfont.render(t1, False, (255,255,255))
            SCREEN.blit(textR, (370, 600))
            pygame.display.flip()
            record_to_file('.demo.wav')
	    SCREEN.fill(GREY)
            SCREEN.blit(text1, (420, 50))
            SCREEN.blit(text2, (420, 300))
            SCREEN.blit(text3, (420, 500))
            textU = myfont.render(t2, False, (255,255,255))
            SCREEN.blit(textU, (370, 600))
            pygame.display.flip()
            play_sound('.demo.wav')
            time.sleep(2)
            while listen:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                         listen = False
                         break
                        elif event.key == pygame.K_DOWN:
                            play_sound('.demo.wav')
                            time.sleep(2)
                            break
                        elif event.key == pygame.K_RIGHT:
                            counter += 1
                            directory = direct + '/Rec_' + str(counter-1) + '.wav'
                            os.rename('.demo.wav', directory)
                            listen = False
                            f = open(stats, 'w')
                            stats_data[0] = dirc[ind]
			    stats_data[1] = str(counter)
                            f.write(stats_data[0])
                            f.write('\n')
                            f.write(stats_data[1])
			    f.write('\n')
                            break
                        elif event.key == pygame.K_SPACE:
                            textP = myfont.render(t3, False, (255,255,255))
                            SCREEN.fill(GREY)
                            SCREEN.blit(textP, (370, 600))
			    SCREEN.blit(text1, (420, 50))
                            SCREEN.blit(text2, (420, 300))
                            SCREEN.blit(text3, (420, 500))
                            pygame.display.flip()
                            time.sleep(1)
                            continue
                
                        elif event.key == pygame.K_ESCAPE:
                            pugame.quit()
                    elif event.type == pygame.QUIT:
                        os.remove('.demo.wav')
                        pygame.quit()
        counter -= 1

os.remove('.demo.wav')
pygame.quit()

