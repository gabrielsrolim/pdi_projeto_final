import os,cv,cv2
from Iris import Iris,pegarIris,gerarDct,inicializarListaIris,procurarIris,\
                 inicializarListaIrisBoas 

if __name__ == "__main__":
    listIris = inicializarListaIrisBoas()    
    
    while(True):
        caminho = raw_input('Digite o caminho da iris a identificar: ')
        procurarIris(listIris,caminho)

                
    """
    orig = cv.LoadImage("bryanr1.bmp")
    pegarIris(orig,"bryanr12.bmp")
    orig = cv.LoadImage("bryanr2.bmp")
    pegarIris(orig,"bryanr22.bmp")
    orig = cv.LoadImage("bryanr3.bmp")
    pegarIris(orig,"bryanr32.bmp")
    orig = cv.LoadImage("bryanr4.bmp")
    pegarIris(orig,"bryanr42.bmp")
    orig = cv.LoadImage("bryanr5.bmp")
    pegarIris(orig,"bryanr52.bmp")
    """