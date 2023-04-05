import cv2
import pytesseract
from PIL import Image
import requests as req
import numpy
import time
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def mirar_placa():

  mi = Image.open(req.get("http://192.168.0.6/camera?" + str(int(time.time() * 1000)),stream=True).raw)

  placa = []
  placa2 = []
  placaf = ""
  image = numpy.array(mi)
  image2 = numpy.array(mi)

  image = cv2.flip(image,1)
  image2 = cv2.flip(image2,1)

  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

  suavi = cv2.medianBlur(gray,1)
  suavi2 = cv2.medianBlur(gray2,1)

  kernel = numpy.ones((1,1),numpy.uint8)

  dil = cv2.dilate(suavi, kernel, iterations = 2)
  dil2 = cv2.dilate(suavi2, kernel, iterations = 3)

  placa = pytesseract.image_to_string(dil, config= r'--psm 8')
  placa2 = pytesseract.image_to_string(dil2, config= r'--psm 8')

  #placa = pytesseract.image_to_string(suavi, config= r'--psm 8')
  #placa2 = pytesseract.image_to_string(suavi2, config= r'--psm 11')

  for i in range(7):
    #print(str(i) + " " + placa[i])
    placaf += placa[i]

  print("placa final: " + placaf)

  print("esto es la placa 1: " + placa)
  print("esto es la placa 2: " + placa2)

  salida_dato = {
  "placa": placaf,
  "entrando": True
  } 
  salida_placa = json.dumps(salida_dato)
  print(salida_placa)

  return salida_placa








'''
canny = cv2.Canny(gray,150,200)
canny = cv2.dilate(canny,cv2.getStructuringElement(cv2.MORPH_RECT,(1,2)),iterations=1)
cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image,cnts,-1,(0,255,0),2)

for c in cnts: 
  area = cv2.contourArea(c)
  x,y,w,h = cv2.boundingRect(c)
  epsilon = 0.09*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  
  if len(approx)==4:
    print('area=',area)
    cv2.drawContours(image,[approx],0,(0,255,0),3)
    aspect_ratio = float(w)/h
    if aspect_ratio>1.9:
      placa = gray[y:y+h,x:x+w]
      text = pytesseract.image_to_string(placa,config='--psm 11')
      print('PLACA: ',text)
      cv2.imshow('PLACA',placa)
      cv2.moveWindow('PLACA',780,10)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
      cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3)
  
cv2.imshow('Image',image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)
'''
