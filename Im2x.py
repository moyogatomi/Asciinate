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

try:
    os.system('cls')
except:
    os.system('clear')

colorama.init()


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

                
        

            


#print('\033[31m' + 'some red text')
#print('\033[30m')
#sys.argv = [30,30,30]
#path = sys.argv[1]
    
url = sys.argv[1]
size = (int(sys.argv[2]),int(sys.argv[3]))
image_mask = np.zeros(shape=size)

Guess = Decide(url)
method,data_type = Guess.decide()

# Color to letters table
table = '   . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ'

#table = '.............:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ'
#table = 'asdjqwklej'*10
#3-dimensional body - fill with table
d3 = np.chararray(shape=[image_mask.shape[0],image_mask.shape[1],len(table)])
d3 = d3.astype('|S10')
#d3 = d3.astype('|S30')
indexes = np.where(image_mask==0)
for i in range(d3.shape[-1]):
    d3[:,:,i]=table[i]

#RGB = np.load('colorWin.npy')



def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    image = image.mean(axis=2)/(int(256/len(table)))
    return image
def view(img):
    return np.int64(img.reshape(img.shape[0]*img.shape[1]))

def ixs(indexes,view):
    return (indexes[0],indexes[1],view)

def ixsRGB(img):
    shap = img.shape[0]*img.shape[1]
    x1 = np.int64(img[:,:,0].reshape(shap))
    x2 = np.int64(img[:,:,1].reshape(shap))
    x3 = np.int64(img[:,:,2].reshape(shap))
    return (x1,x2,x3)
def render(screen):
    screen[:,-1]='\n'
    #for i in screen:
    #    print(i)
    sys.stdout.buffer.write(screen)
    
    #for i in screen.decode():
    ##data = ''.join([a for a in i])
    ##sys.stdout.write(data+'\n')
    #    data = ''.join([a for a in i])
    #print(data)
    #    sys.stdout.buffer.write(data)
    
def image(path):
    if method == 'net':
        image = url_to_image(url)
    if method == 'local':
        image = cv2.imread(path,0)/2
        imageRGB = cv2.imread(path,1)
    
    image = cv2.resize(image,(int(sys.argv[2]),int(sys.argv[3])))
    image = np.uint8(image)

    #imageRGB = cv2.resize(imageRGB,(int(sys.argv[2]),int(sys.argv[3])))
    #imageRGB = np.uint8(imageRGB)
    #screenRGB = RGB[ixsRGB(imageRGB)]
    
    screen = d3[ixs(indexes,view(image))]
    screen = (screen).reshape(image.shape)
    #screen[0,0]=b'\033[1m'+screen[0,0]
    render(screen)
                    

#url = "https://www.youtube.com/watch?v=S0_qSemZZSs"
#url = "https://www.youtube.com/watch?v=2DIl3Hfh9tY"

def stream(url):
    
    if method == 'net':
        vPafy = pafy.new(url)
        play = vPafy.getbest(preftype="webm")
        capture = cv2.VideoCapture(play.url)
    if method == 'local':
        capture = cv2.VideoCapture(url)
    FPS = 30
    while capture.isOpened():       
        ret,image = capture.read() 
        if ret:
            start = time.time()
            

            image = cv2.resize(image,(int(sys.argv[2]),int(sys.argv[3])))
            screenRGB = RGB[ixsRGB(image)]
            image = image.mean(axis=2)/(int(256/len(table)))
            image = np.uint8(image)
     
            screen = d3[ixs(indexes,view(image))]
            screen = (screenRGB+screen).reshape(image.shape)
            
            move_cursor(0,0)
            render(screen)
            dt=time.time()-start
            #if dt<0:
            #    dt = 1
            if 1./dt>FPS:
                time.sleep(np.abs((1./FPS)-dt))
            print("FPS: {}".format(1./(time.time()-start)))
            

if data_type == 'video':
    stream(url)
if data_type == 'image':
    image(url)

