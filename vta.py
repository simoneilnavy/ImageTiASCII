import numpy 
import cv2
import time
import sys
from colorama import Cursor
from PIL import Image


gscale = "$@@%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~i!lI;:,\"^`    "[::-1]
#grayscale 66 livelli

#questa funzione ritorna la media di 'luminosità' per ogni pixel o piu pixel che vengono presi in considerazione
#in sostanza la funzione rende l'immagine un array numpy
#diventa un array bidimensionale dove in ogni cella è contenuta la luminosità del pixel rappresentato

def avgLuminosita(img):
    immagine=numpy.array(img)
    w,h= immagine.shape
    
    #in questo momento con reshape trasformo l'array bidimensionale in uno monodimensionale
    #dove la lunghezza è la larghezza moltiplicata per l'altezza in questo modo mantengo lo stesso numero di celle
    #con average calcolo l'avg della luminosità dell'array
    
    return numpy.average(immagine.reshape(w*h))
    

def processimage(valoreImmagine):
    
    #per rendere possibile l'acquisizione di un immagine da un video devo convertire l'immagine da
    #un oggetto di tipo "Videocapture" di OpenCV in una immagine comprensibile da PIL (Pillow),lo faccio passando per un array numpy
    #e converte in una scala 8-bit dove:'L=8-bit greyscale. 0 means black, 255 means white.'
   
    immagine=Image.fromarray(valoreImmagine)
    
    
    #size per salvare il formato dell'immagine
    
    La, Al = immagine.size[0], immagine.size[1]
    

    #con cols scegliamo la definizione che la nostra immagine deve avere
    #con scale dobbiamo mettere un valore che mantega l'aspect ratio corretto    

    cols=300
    scale=0.43
    
    la=La/cols
    al=la/scale
    
    #qui invece trovo il numero di righe che è proporzionale alla scala scelta
    
    righe=int(Al/al)
    
    
    #creo la lista di stringhe che conterrà l'immagine convertita in ascii riga per riga
    
    imgarr = []
    
    #con questo for riempio la lista con le stringhe che conterranno i caratteri
    #e successivamente la riempio con i valori
    
    for j in range(righe):
        
        #con questo primo step calcolo l'effettiva dimensione che avrà l'immagine
        #per rendere possibile la conversione in ASCII abbiamo bisogno che le dimensioni siano intere
        #così da poter creare una lista con un numero definito di celle in cui inserire il testo
        #questi numeri rappresentano le coordinate di inizio e di fine di una cella da cui ricavare la luminosotà
        #infatti grazie alla funzione di crop dopo prenderemo solamente alcune celle di immagine e non tutta l'immagine
        
        y1 = int(j*al)
        y2 = int((j+1)*al)
        
        #se siamo all'ultima iterazione allora prendo tutta l'immagine rimanente
        
        if j == righe-1:
            y2 = Al
            
        imgarr.append("")
        
        #e ora faccio lo stesso per le colonne ovviamente dentro all'altro for in modo da poter scorrere tutta l'immagine
        
        for i in range(cols):
            x1 = int(i*la)
            x2 = int((i+1)*la)
            
            if i == cols-1:
                x2 = La
            
            
            #.crop prende in input delle vere e proprie coordinate per sapere dove croppare l'immagine
            #queste coordinate sono le porzioni di immagine pezzo per pezzo
            
            newimg = immagine.crop((x1,y1,x2,y2))
            
            #qui usiamo finalmente la funzione preparata in precedenza per la luminosità
            #il cast quà serve perchè i nostri ascii sono salvati in una stringa e (ovviamente) ogni carattere occupa uno spazio
            #questo valore andrà proprio a stabilire il carattere da inserire
            
            avg = int(avgLuminosita(newimg))
            
            #infine inseriamo nella cella del array il valore ASCII, il cast qui è necessario perchè come detto prima ogni carattere occupa uno spazio
            #avg*69 ci serve per spalmare il nostro valore di gradient sulla stringa di caratteri e poi dividendo per 255(ovvero il gradient di grigi)
            #otteniamo il vero e proprio ascii per la nostra immagine
            
            imgarr[j] += gscale[int((avg*66)/255)]
            
    
    
    #una acquisita tutta l'immagine salviamo il fram in ascii in un file
    
    f = open("outFile.txt", 'a')
    
    for righe in imgarr:
        f.write(righe+"\n")
        
    f.close()

#questa funzione sfrutta delle funzioni di OpenCV che ci permettono di estrapolare frame per frame uno stream video

def videoslicing():
    
    #apro il video
    video=cv2.VideoCapture("video.mp4")
    
    #valore per capire se è stato possibile estrarre un frame
    success=1
    
    #scorro tutto il video frame per frame, ogni frame viene processato (per la trasformazione in ascii) e salvato su un file
    #dal quale successivamente prenderemo le informazioni per stampare su cmd
    
    while success:
        
    #catturo il frame
    
        success, immagine = video.read()
    
    
    #invio il frame video a convertire
    
        processimage(cv2.cvtColor(immagine,cv2.COLOR_BGR2GRAY))
        
        
        
#questa funzione è impiegata per la riproduzione del video in ascii     
def riproduttore():
    
    #qui definisco:il file,un contatore nel quale viene inserito il numero di colonne di un frame ed il frame effettivo
    #ovvero una stringa di testo che contiene i caratteri di tutto un frame
    
    f=open("outFile.txt",'r')
    counter=0
    frame=""
    
    #questo for scorre il file riga per riga fino a che nella stringa non viene salvato un frame intero
    #in quel momento il frame viene stampato e reinizializzato vuoto e il counter di nuovo azzerato
    for line in f:
        if(counter == 72):
            
            #per la stampa delle informazione è stato utilizzato stdout.write che è usato per stampare le informazioni
            #direttamente sul cmd e non inserisce \n a fine riga, inoltre grazie alla libreria colorama
            #posso portare il cursore di nuovo in cima al cmd e non cancellare tutto il terminale
            #con clear che farebbe flickerare non rendendo meno fruibile il video
            
            sys.stdout.write(Cursor.POS(0,0)+frame)
            sys.stdout.flush()
            
            frame=""
            counter=0
            
            #con questo si imposta il framerate in questo caso 30fps
            time.sleep(1/30)
            
            
        frame+=line
        counter+=1

    
#videoslicing()
riproduttore()
