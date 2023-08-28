import cv2
import numpy as np
import time
import serial

cam = cv2.VideoCapture(1)

#ard = serial.Serial('/dev/ttyUSB0',9600)

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
            if len(cnts) > 0:
             c=max(cnts,key=cv2.contourArea)
             M=cv2.moments(c)
             if M ["m00"]!= 0:
              gx = int(M["m10"]/M["m00"])
              gy = int(M["m01"]/M["m00"]) 
              cv2.circle(frame,(gx,gy),5,(0,255,0),-1)
              #print("CX :"+ str(cx)+"CY :" + str(cy))
              return gx
      
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
def intersection():
    if wl == 640:
        return True
    else:
        return False
#Fim funções

while True:
    ret, frame = cam.read()
    
#Código para identificação do verde
    kernel2 = np.ones((10,10),np.uint8)
    kernel3 = np.ones((18,18),np.uint8)
    lower = np.array([68,82,40])
    upper = np.array([95,255,255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower, upper)
    mask3 = cv2.erode(mask1,kernel2,iterations =1)
    dilate = cv2.dilate(mask3,kernel3,iterations =3)
    _, mask2 = cv2.threshold(dilate,254,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    a=[]
#Fim codigo identificação verde
    
#Máscara para saber onde está a linha
    low_b = np.uint8([150,150,150])
    high_b = np.uint8([0,0,0 ])
    mask = cv2.inRange(frame, high_b,low_b)
#Fim da máscara

#Tirar ruídos da imagem
    kernel = np.ones((10,10),np.uint8) #kernel e uma varíavel usada para determinar os ruidos que se deve tirar(dependendo do valor pode-se tirar parte da linha)
    linha = cv2.erode(mask,kernel,iterations =1)#Erode é o comando para tirar os ruidos, o contrário dessa varíavel é o dilate, ela aumenta tudo o que a câmera vê

    
#Comandos para saber o centro da linha
    contours, hierarchy = cv2.findContours(linha, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
     c=max(contours,key=cv2.contourArea)
     M=cv2.moments(c)
     if M ["m00"]!= 0:
      cx = int(M["m10"]/M["m00"])
      cy = int(M["m01"]/M["m00"]) 
      cv2.circle(frame,(cx,cy),5,(255,0,0),-1)
      #print("CX :"+ str(cx)+"CY :" + str(cy))  #//Print para ter os valores de onde esta o centro da linha
#Fim centro linha
      
#Detectar as bordas da linha
    for c in contours:
        x=600
        if cv2.contourArea(c)>x :
            xl,yl,wl,hl = cv2.boundingRect(c) #x a borda da esquerda o w a borda da direita
            cv2.circle(frame,(x,30),5,(0,0,255),-1)
       #     print("yl:"+str(y))
      #      print("xl:"+str(x))
            #print("wl:"+str(w))
#Fim bordas linhas
            
#Detectar valores verde   
    quantidade = many(frame) #Quantos verdes
    localx = coord(frame) #Posição X do verde
    localy = coordy(frame) #Posição Y do verde
    green(frame)#Detectar verde
#Fim valores verde
    
#Imagem do que o robô está vendo
    
    cv2.drawContours(frame, contours, -1, (255,0,0),4)
    cv2.imshow('video', frame)
    cv2.imshow('Mask', mask2)
    #cv2.imshow('Color', linha)
    
    
    if localx == None:
        localx = 0
    if intersection() == True:
        print('interseção')
        #time.sleep(1)
   #if w == 640 and y != 0:
    #    print(' 90° a direita')
        #time.sleep(1)
   # if x ==0 and w != 640 and y != 0:
   #     print(' 90° a esquerda')
   # if x ==0 and w != 640 and y == 0:
   #     print(' Falso 90° a esquerda, seguir reto')
   # if x != 0 and w == 640 and y == 0:
   #     print(' Falso 90° a direita, seguir reto')
    print("x:" + str(xl))
    #print("w:" + str(w))
    #print("y:" + str(y))
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()

