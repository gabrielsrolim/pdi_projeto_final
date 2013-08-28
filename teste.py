import cv,cv2
import numpy as np
import os

def pegarIris(orig,nameFoto="teste.bmp"):
    orig2 = cv.CloneImage(orig)

    # create tmp images
    grey_scale = cv.CreateImage(cv.GetSize(orig), 8, 1)
    processedPupila = cv.CreateImage(cv.GetSize(orig), 8, 1)
    processedIris = cv.CreateImage(cv.GetSize(orig), 8, 1)


    cv.Smooth(orig, orig, cv.CV_GAUSSIAN, 3, 3)

    cv.CvtColor(orig, grey_scale, cv.CV_RGB2GRAY)
    cv.CvtColor(orig, processedIris, cv.CV_RGB2GRAY)

    cv.Smooth(grey_scale, processedPupila, cv.CV_GAUSSIAN, 15, 15)
    cv.Canny(processedPupila, processedPupila, 5, 70, 3)
    cv.Smooth(processedPupila, processedPupila, cv.CV_GAUSSIAN, 15, 15)
    #cv.ShowImage("pupila_processada", processedPupila)


    cv.Smooth(grey_scale, processedIris, cv.CV_GAUSSIAN, 15, 15)
    cv.Canny(processedIris, processedIris, 5, 70, 3)
    cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)
    cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)
    #cv.ShowImage("pupila_processada2", processedIris)

    #cv.Erode(processedIris, processedIris, None, 10)
    #cv.Dilate(processedIris, processedIris, None, 10)
    #cv.Canny(processedIris, processedIris, 5, 70, 3)
    #cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)
    #cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)



    #cv.Smooth(processedPupila, processedIris, cv.CV_GAUSSIAN, 15, 15)
    #cv.ShowImage("Iris_processada", processedIris)
    #cv.Dilate(processedIris, processedIris, None, 10)
    
    storagePupila = cv.CreateMat(orig.width, 1, cv.CV_32FC3)
    storageIris = cv.CreateMat(orig.width, 1, cv.CV_32FC3)

    # these parameters need to be adjusted for every single image
    HIGH = 30
    LOW = 20

    HIGH2 = 120
    LOW2 = 60


    imgBranca = cv.CreateImage(cv.GetSize(orig), 8, 3)
    imgPreta = cv.CreateImage(cv.GetSize(orig), 8, 3)
    cv.Zero(imgPreta)
    cv.Not(imgPreta,imgBranca)

    imagemMaskPupila = cv.CreateImage(cv.GetSize(orig), 8, 3)
    imagemMaskPupila = cv.CloneImage(imgBranca)

    imagemMaskIris = cv.CreateImage(cv.GetSize(orig), 8, 3)
    imagemMaskIris = cv.CloneImage(imgPreta)

    #try: 
    # extract circles
    #cv2.cv.HoughCircles(processedIris, storageIris, cv.CV_HOUGH_GRADIENT, 3, 100.0,LOW,HIGH, LOW2, HIGH2)
    cv2.cv.HoughCircles(processedPupila, storagePupila, cv.CV_HOUGH_GRADIENT, 2, 100.0, LOW, HIGH)
    cv2.cv.HoughCircles(processedIris, storageIris, cv.CV_HOUGH_GRADIENT, 3, 100.0,LOW,HIGH, LOW2, HIGH2)
    
    
    #Circulos da pupila
    #for i in range(0, len(np.asarray(storagePupila))):
    RadiusPupila = int(np.asarray(storagePupila)[0][0][2])
    xPupila = int(np.asarray(storagePupila)[0][0][0])
    yPupila = int(np.asarray(storagePupila)[0][0][1])
    centerPupila = (xPupila, yPupila)
    #print "RadiusPupila %d" %RadiusPupila

    cv.Circle(imagemMaskPupila, centerPupila, RadiusPupila, cv.CV_RGB(0, 0, 0), -1, 8, 0)
    cv.Circle(orig, centerPupila, 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
    cv.Circle(orig, centerPupila, RadiusPupila, cv.CV_RGB(255, 0, 0), 3, 8, 0)
    #cv.ShowImage("pupila"+str(0), orig)
    orig = cv.CloneImage(orig2)

    #cv.WaitKey(0)

#Circulos da Iris
#for i in range(0, len(np.asarray(storageIris))):
    RadiusIris = int(np.asarray(storageIris)[0][0][2])
    xIris = int(np.asarray(storageIris)[0][0][0])
    yIris = int(np.asarray(storageIris)[0][0][1])
    centerIris = (xIris, yIris)
    #print "RadiusIris %d" %RadiusIris

    cv.Circle(imagemMaskIris, centerIris, RadiusIris, cv.CV_RGB(255, 255, 255), -1, 8, 0)

    cv.Circle(orig, centerIris, 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
    cv.Circle(orig, centerIris, RadiusIris, cv.CV_RGB(255, 0, 0), 3, 8, 0)
    #cv.ShowImage("Iris"+str(0), orig)
    orig = cv.CloneImage(orig2)

    #cv.WaitKey(0)

    #except:
    #    print "nothing found"
    #    pass
    #criando imagem final
    finalAux = cv.CreateImage(cv.GetSize(orig), 8, 3)
    final = cv.CreateImage(cv.GetSize(orig), 8, 3)

    #pegando a iris toda
    cv.And(orig,imagemMaskPupila,finalAux)
    cv.And(finalAux,imagemMaskIris,final)

    cv.SaveImage(nameFoto,final)
    #cv.ShowImage("original with circles", final)

    #cv.WaitKey(0)
    

    return final

"""
def GerarMascaraPupila(iplimage orig):
    orig2 = cv.CloneImage(orig)

    # create tmp images
    grey_scale = cv.CreateImage(cv.GetSize(orig), 8, 1)
    processed = cv.CreateImage(cv.GetSize(orig), 8, 1)


    cv.Smooth(orig, orig, cv.CV_GAUSSIAN, 3, 3)

    cv.CvtColor(orig, grey_scale, cv.CV_RGB2GRAY)

    cv.Smooth(grey_scale, processed, cv.CV_GAUSSIAN, 15, 15)
    cv.Canny(processed, processed, 5, 70, 3)
    cv.Smooth(processed, processed, cv.CV_GAUSSIAN, 15, 15)
    storage = cv.CreateMat(orig.width, 1, cv.CV_32FC3)

    # these parameters need to be adjusted for every single image
    HIGH = 50
    LOW = 140

    try: 
        # extract circles
        cv.HoughCircles(processed, storage, cv.CV_HOUGH_GRADIENT, 2, 32.0, HIGH, LOW)

        for i in range(0, len(np.asarray(storage))):
            #print "circle #%d" %i
            Radius = int(np.asarray(storage)[i][0][2])
            x = int(np.asarray(storage)[i][0][0])
            y = int(np.asarray(storage)[i][0][1])
            center = (x, y)

            # green dot on center and red circle around
            cv.Circle(orig, center, 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
            cv.Circle(orig, center, Radius, cv.CV_RGB(255, 0, 0), 3, 8, 0)
            cv.SaveImage('final'+str(i)+'.bmp',orig)
            orig = cv.CloneImage(orig2)

            #Criando mascara
            imagemMask = cv.CreateImage(cv.GetSize(orig), 8, 3)
            cv.Zero(imagemMask)
            cv.Circle(imagemMask, center, Radius, cv.CV_RGB(255, 255, 255), -1, 8, 0)
            
    except:
        print "nothing found"
        pass
    #criando imagem final
    final = cv.CreateImage(cv.GetSize(orig), 8, 3)

    #pegando a iris toda
    cv.And(orig,imagemMask,final)
    #cv.SaveImage('final'+str(10)+'.bmp',final)

    return final
"""

if __name__ == "__main__":
    list1 = os.listdir('.')
    for l in list1:
        try:
            list2 = os.listdir(l+"/")
        except:
            print('Erro1')
        for laus in list2:
            try:
                list3 = os.listdir(l+"/"+laus+"/")
            except:
                print('Erro1')
            for laux in list3:
                string = "/home/gabriel/Downloads/MMU_Iris_Database/"+l+"/"+laus+"/"+laux
                print "caminho: %s" % string
                nome = laux.split('.')[0]
                try:
                    orig = cv.LoadImage(string)
                except:
                    print('Erro')
                nomeImage = "/home/gabriel/Downloads/MMU_Iris_Database/"+l+"/"+laus+"/"+nome+"_2.bmp"
                print "nomefinal: %s" % nomeImage
                try:
                    pegarIris(orig,nomeImage)     
                except:
                    print('ErroU')    
                
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