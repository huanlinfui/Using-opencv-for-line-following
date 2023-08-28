import cv2
import numpy as np

cam = cv2.VideoCapture(1)

while True:
    ret, frame = cam.read()
    
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
      #print("CX :"+ str(cx)+"CY :" + str(cy))  //Print para ter os valores de onde esta o centro da linha
#Fim centro linha
      
#Detectar as bordas da linha
    for c in contours:
        x=600
        if cv2.contourArea(c)>x :
            x,y,w,h = cv2.boundingRect(c) #x a borda da esquerda o w a borda da direita
            cv2.circle(frame,(x,30),5,(0,0,255),-1)
            print("x:"+str(x))
            print("w:"+str(w))
#Fim bordas linhas
    
#Imagem do que o robô está vendo
    
    cv2.drawContours(frame, contours, -1, (255,0,0),4)
    cv2.imshow('video', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Color', linha)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()


