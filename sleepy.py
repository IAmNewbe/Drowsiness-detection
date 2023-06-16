# import pyglet.media
from cvzone.FaceMeshModule import FaceMeshDetector
import cv2
import csv
from datetime import datetime

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = FaceMeshDetector(maxFaces=1)
state=""
lambe=""
x=10
breakcount_s, breakcount_y = 0, 0
counter_s, counter_y = 0, 0
state_s, state_y = False, False
# sound = pyglet.media.load("alarm.wav", streaming=False)
def alert():
    cv2.rectangle(img, (590, 40),(1190, 140), (0, 0, 255),cv2.FILLED)
    cv2.putText(img, "Tangi WOII!!! ", (600, 120), cv2.FONT_HERSHEY_PLAIN, 6,(255, 255, 255), 5)

def recordData(condition):
    file = open("database.csv", "a", newline="")
    now = datetime.now()
    dtString = now.strftime("%d-%m-%Y %H:%M:%S")
    tuple = (dtString, condition)
    writer = csv.writer(file)
    writer.writerow(tuple)
    file.close()


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, faces = detector.findFaceMesh(img, draw=False)
    # print(len(faces[0]))
    
    if faces:
        face = faces[0]
        matakiri = [27, 23, 130, 243]  # up, down, left, right
        matakanan = [257, 253, 463, 359]  # up, down, left, right
        mulut = [11, 16, 57, 287]  # up, down, left, right
        idwajah = [ 11, 16, 57, 287]
        idmata = [27, 23, 130, 243,257, 253, 463, 359]

        matakiri_ver,_ = detector.findDistance(face[matakiri[0]], face[matakiri[1]])
        matakiri_hor,_ = detector.findDistance(face[matakiri[2]], face[matakiri[3]])
        matakiri_ratio = int((matakiri_ver/matakiri_hor)*100)
        matakanan_ver,_ = detector.findDistance(face[matakanan[0]], face[matakanan[1]])
        matakanan_hor,_ = detector.findDistance(face[matakanan[2]], face[matakanan[3]])
        matakanan_ratio = int((matakanan_ver/matakanan_hor)*100)
        mulut_ver,_ = detector.findDistance(face[mulut[0]], face[mulut[1]])
        mulut_hor,_ = detector.findDistance(face[mulut[2]], face[mulut[3]])
        mulut_ratio = int((mulut_ver/mulut_hor)*100)

        if matakiri_ratio <= 50 and matakanan_ratio:
            breakcount_s += 1
            state = "Kedip"
            if breakcount_s >= 30:
                alert()
                if state_s == False:
                    counter_s += 1
                    # sound.play()
                    # board.digital[pin].write(0)
                    recordData("Turu")
                    state_s = not state_s
                    state = "Keturon"
            # cv2.rectangle(img, (590, 40),(1190, 140), (0, 0, 255),cv2.FILLED)
            # cv2.putText(img, "Tangi WOII!!! ", (600, 120), cv2.FONT_HERSHEY_PLAIN, 6,(255, 255, 255), 5)
        else:
            breakcount_s = 0
            state = "Melek"
            if state_s:
                # board.digital[pin].write(1)
                state_s = not state_s
                
        if mulut_ratio > 60:
            breakcount_y += 1
            lambe = "Ngantuk"
            if breakcount_y >= 30:
                alert()
                if state_y == False:
                    counter_y += 1
                    # sound.play()
                    # board.digital[pin].write(0)
                    recordData("Menguap")
                    state_y = not state_y
                    
        else:
            breakcount_y = 0
            lambe = "Seger"
            if state_y:
                # board.digital[pin].write(1)
                state_y = not state_y
                
        
        for id in idwajah:
            cv2.circle(img,face[id], 2, (0,0,255), cv2.FILLED)
        for id in idmata:
            cv2.circle(img,face[id], 2, (0,255,0), cv2.FILLED)    
    # length, info = detector.findDistance(1, 2, img)
    cv2.rectangle(img, (30, 20+80),(400+30, 140+80), (0, 255, 255),cv2.FILLED)
    cv2.rectangle(img, (30, 20),(400+30, 80), (0, 255, 0),cv2.FILLED)
    cv2.putText(img, "Deteksi Turu" , (10+30, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.putText(img, "Mata: " + state, (10+30, 70+80), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    cv2.putText(img, "Mulut: " + lambe, (10+30, 120+80), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 0), 3)
    
    cv2.rectangle(img, (30, 200+30), (350, 300+30), (255,0,0), cv2.FILLED)
    cv2.putText(img, f'Keturon Count: {counter_s}', (40, 240+30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
    cv2.putText(img, f'Ngantuk Count: {counter_y}', (40, 280+30),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
                    
    cv2.imshow("Deteksi Turu", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

