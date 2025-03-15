import os, sys
import numpy 
from PIL import Image


gscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~i!lI;:,\"^`"
#grayscale 70 livelli

ilpath="img.jpg"
#il path dell'immagine

#questa funzione ritorna la media di 'luminosità' per ogni pixel
#in sostanza la funzione rende l'immagine un array numpy
#diventa un array bidimensionale dove in ogni cella è contenuta la luminosità del pixel rappresentato
def avgLuminosita(img):
    immagine=numpy.array(img)
    w,h= immagine.shape
    
    #in questo momento con reshape trasformo l'array bidimensionale in uno monodimensionale
    #dove la lunghezza è la larghezza moltiplicata per l'altezza in questo modo mantengo lo stesso numero di celle
    #con average calcolo l'avg della luminosità dell'array
    return numpy.average(immagine.reshape(w*h))
    

def processimage():
    immagine = Image.open(ilpath).convert('L')
    #questo apre l'immagine (con open) e converte in una scala 8-bit dove:'L=8-bit greyscale. 0 means black, 255 means white.'
    
    La, Al = immagine.size[0], immagine.size[1]
    #size per salvare il formato dell'immagine

    #con cols scegliamo la definizione che la nostra immagine dovrebbe avere
    #con scale dobbiamo mettere un valore che mantega l'aspect ratio in 16:9 nel mio caso e quindi 2    

    cols=300
    scale=1
    
    la=La/cols
    al=la/scale
    
    #qui invece trovo il numero di righe che è proporzionale alla scala scelta
    righe=int(Al/al)
    
    
    #creo la lista di ascii che conterrà l'immagine convertita in ascii
    
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
            newimg = immagine.crop((x1,y1,x2,y2))
            
            #qui usiamo finalmente la funzione preparata in precedenza per la luminosità
            #il cast quà serve perchè i nostri ascii sono salvati in una stringa e (ovviamente) ogni carattere occupa uno spazio
            #questo valore andrà proprio a stabilire il carattere da inserire
            avg = int(avgLuminosita(newimg))
            
            #infine inseriamo nella cella del array il valore ASCII, il cast qui è necessario perchè come detto prima ogni carattere occupa uno spazio
            #avg*69 ci serve per spalmare il nostro valore di gradient sulla stringa di caratteri e poi dividendo per 255(ovvero il gradient)
            #otteniamo il vero e proprio ascii per la nostra immagine
            imgarr[j] += gscale[int((avg*63)/255)]
            
    
    f = open("outFile.txt", 'w')
    for righe in imgarr:
        f.write(righe+"\n")
    
    f.close()
    print("finito")
        
    
    
    
    
    
processimage()