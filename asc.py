import numpy as np
import cv2
import sys
import cv2
import time
import os
import pafy
import random
import urllib
import requests
import io
from PIL import Image
import colorama
import time
from tqdm import tqdm
import threading

def RGBmemory():
    files = os.listdir('./')
    if 'color.npy' in files:
        RGB = np.load('color.npy',)
        return RGB
    else:
        from sty import fg, bg, ef, rs, RgbFg
        print("\x1b[38;2;0;255;250m Need to create RGB memory file. Expected size: 300mb \x1b[39m")
        RGB = np.chararray(shape=[256,256,256],itemsize = 19)
        RGB = RGB.astype('|S19')
        from sty import fg, bg, ef, rs, RgbFg
        for x in tqdm(range(256)):
            for y in range(256):
                for z in range(256):
                    fg.set_style('colorr', RgbFg(z, y, x))
                    RGB[x,y,z] = fg.colorr.replace('38','48')
        np.save('color.npy',RGB)
        return RGB
print('--- Loading RGB memory ---')
RGB = RGBmemory().astype("<U19")
try:
    os.system('cls')
except:
    os.system('clear')

try:
    os.system('clear')
except:
    os.system('cls')
colorama.init()

colored = int(sys.argv[5])

def move_cursor(x,y):
    print ("\x1b[{};{}H".format(y+1,x+1))
 
def clear():
    print ("\x1b[2J")


class Decide(object):
    def __init__(self,url):
        self.url = url
        self.video = ['mp4','wmv','avi','mkv']
        self.stream = ['youtube.com']
        self.image = ['jpg','png','bmp']
        self.is_url = ['http','.com']

    def decide(self):
        method = 'local'
        data_type = ''
        for i in self.is_url:
            if i in self.url and 'youtube.com' in self.url:
                print(i)
                method = 'net'
                data_type = 'video'
                break
            if i in self.url and 'youtube.com' not in self.url:
                print(i,self.url)
                method ='net'
                data_type = 'image'
                break

        if data_type == '':
            if self.url.split('.')[-1] in self.image:
                data_type = 'image'
                
            if self.url.split('.')[-1] in self.video:
                data_type = 'video'

        return method,data_type

                
    
url = sys.argv[1]
size = (int(sys.argv[2]),int(sys.argv[3]))
image_mask = np.zeros(shape=size)

Guess = Decide(url)
method,data_type = Guess.decide()

# Color to letters table 
table = u'■■■■■■  . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ'
table = u'■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■ '
#table = '■■■■■■    . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ''
#3-dimensional body - fill with table
table = ' '
d3 = np.chararray(shape=[image_mask.shape[0],image_mask.shape[1],len(table)],unicode=True)


indexes = np.where(image_mask==0)
for i in range(d3.shape[-1]):
    d3[:,:,i]=table[i]
    #print(type(table[i]))
    #sys.stdout.buffer.write(RGB[0,0,0]+bytes(d3[0,0,0].encode()))
    #sys.stdout.buffer.write(d3[0,0,0:5].encode())


#print(RGB[0,0,0].tostring()+d3[0,0,0])
#exit()

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    imageRGB = image.copy()
    image = image.mean(axis=2)/((256./len(table)))
    return image,imageRGB
def view(img):
    return np.int64(img.reshape(img.shape[0]*img.shape[1]))

def ixs(indexes,view):
    return (indexes[0],indexes[1],view)

def ixsRGB(img):
    shap = img.shape[0]*img.shape[1]
    x1 = img[:,:,0].reshape(shap)
    x2 = img[:,:,1].reshape(shap)
    x3 = img[:,:,2].reshape(shap)
    return (x1,x2,x3)
def renderUnicode(screen):
    screen[:,-1]='\n'
    #screen=screen.reshape(screen.shape[0]*screen.shape[1])
    #data = screen.encode()
    #print(data.shape)
    #print(screen.tostring())
    sys.stdout.buffer.write(screen)
    #sys.stdout.flush()
    #for i in screen.decode():
    ##data = ''.join([a for a in i])
    ##sys.stdout.write(data+'\n')
    #    data = ''.join([a for a in i])
    #print(data)
    #    sys.stdout.buffer.write(data)
    
def render(screen):
    screen[:,-1]='\n'
    #screen=screen.reshape(screen.shape[0]*screen.shape[1])
    #data = screen.decode(encoding='utf-8')
    #print(data.shape)
    #print(''.join(data))
    sys.stdout.buffer.write(screen.encode())
    sys.stdout.flush()
    #for i in screen.decode():
    ##data = ''.join([a for a in i])
    ##sys.stdout.write(data+'\n')
    #    data = ''.join([a for a in i])
    #print(data)
    #    sys.stdout.buffer.write(data)
    
def image(path):
    if method == 'net':
        image,imageRGB = url_to_image(url)
    if method == 'local':
        image = cv2.imread(path,0)/((256./len(table)))
        imageRGB = cv2.imread(path,1)
    
    image = cv2.resize(image,(int(sys.argv[2]),int(sys.argv[3])))
    image = np.uint8(image)

    imageRGB = cv2.resize(imageRGB,(int(sys.argv[2]),int(sys.argv[3])))
    imageRGB = np.uint8(imageRGB)
    if colored == 1:
        screenRGB = RGB[ixsRGB(imageRGB)]
    
    screen = d3[ixs(indexes,view(image))]
    if colored == 1:
        screen = (screenRGB+screen).reshape(image.shape)
        threading.Thread(target=render,args=(screen,)).start()
    else:
        screen = screen.reshape(image.shape)
        render(screen)
        #renderUnicode(screen)
    

def stream(url):
    print(method,data_type)
    if method == 'net':
        vPafy = pafy.new(url)
        play = vPafy.getbest(preftype="webm")
        streams = vPafy.streams
        for s in streams:
            print(s)
        print(play.url)
        capture = cv2.VideoCapture(play.url)
    if method == 'local':
        capture = cv2.VideoCapture(url)
    try:
    	FPS = int(sys.argv[4])
    except:
        FPS = 25
    while capture.isOpened():       
        ret,image = capture.read() 
        if ret:
            start = time.time()
            

            image = cv2.resize(image,(int(sys.argv[2]),int(sys.argv[3])))
            if colored == 1:
                screenRGB = RGB[ixsRGB(image)]
            image = image.mean(axis=2)/((256/len(table)))
            image = np.uint8(image)
     
            screen = d3[ixs(indexes,view(image))]
            if colored == 0:
                screen = screen.reshape(image.shape)
            else:
                screen = (screenRGB+screen).reshape(image.shape)
            
            move_cursor(0,0)
            x = time.time()
            xxx = x-start
            #threading.Thread(target=render,args=(screen,)).start()
            render(screen)
            xx = time.time()-x
            
            dt=time.time()-start
            if 1./dt>FPS:
                time.sleep(np.abs((1./FPS)-dt))
            print(RGB[0,0,0]+"FPS: {}, RENDERING FPS: {}, CALCULATION FPS: {} \x1b[39m".format(1./(time.time()-start),1./xx,1./xxx))
            

if data_type == 'video':
    stream(url)
if data_type == 'image':
    image(url)

