import cv2
import numpy as np

cam = cv2.VideoCapture(1)

#Funções para detectar verde, o valor de x e y do verde e para detectar quantos verdes tem
def green(img):
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x :
            #a.append(x)
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    #print(len(a))
def coord(img):
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x :
            x,y,w,h = cv2.boundingRect(c)
            return x
def coordy(img):
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x :
            x,y,w,h = cv2.boundingRect(c)
            return y
def many(img):
    for c in cnts:
        x=600
        if cv2.contourArea(c)>x :
            a.append(x)
            x,y,w,h = cv2.boundingRect(c)
    return(len(a))
#Fim funções

while True:
    #Código para identificação do verde
    ret, frame = cam.read()
    lower = np.array([68,82,40])
    upper = np.array([95,255,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    _, mask1 = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    a=[]
    #Fim codigo identificação verde
    
    quantidade = many(frame) #Quantos verdes
    localx = coord(frame) #Posição X do verde
    localy = coordy(frame) #Posição Y do verde
    green(frame)#Detectar verde
    
    cv2.imshow('frame', frame)
    
    print("Y:" + str(localy))
    print("x:" + str(localx))
    print(quantidade)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.release()
cv2.breakAllWindows()
