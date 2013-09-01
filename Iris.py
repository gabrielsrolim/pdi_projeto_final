import cv,cv2
import numpy as np
import os


class Iris():
	def __init__(self,nomeIris,dct,imgProcessada):
		self.nomeIris = nomeIris
		self.dct = dct
		self.imgProcessada = imgProcessada

class ErroDct():
    def __init__(self,errodct,indiceLista,nomeArquivo):
        self.errodct = errodct
        self.indiceLista = indiceLista
        self.nomeArquivo = nomeArquivo

def inicializarListaIris():
    listIris = []
    dirbase = 'iris/'
    list1 = os.listdir(dirbase)
    print("Inicializando iris, Aguarde...")
    for l in list1:
        try:
            list2 = os.listdir(dirbase+l+"/")
        except:
            print('Erro1')
        for laus in list2:
            try:
                list3 = os.listdir(dirbase+l+"/"+laus+"/")
            
                for laux in list3:
                    string = dirbase+l+"/"+laus+"/"+laux
                    #print "caminho: %s" % string
                    nome = laux.split('.')[0]
                    extensao = laux.split('.')[1]
                    #print 'extensao %s' %extensao
                    if extensao == "bmp":
                        try:
                            nomeImage = "iris/"+nome+"_2.bmp"
                            iris = pegarIris(string,nomeImage)
                            dct = gerarDct(nomeImage)
                            irisNew = Iris(nomeImage,dct,iris)
                            listIris.append(irisNew)     
                        except:
                            print 'Caminho invalido %s' %string
                    else:
                        print 'Img Invalida %s' %string
            except:
                print 'Diretorio invalido %s' % dirbase+l+"/"+laus+"/"
    return listIris

def inicializarListaIrisBoas():
    listIris = []
    dirbase = '/home/gabriel/Documentos/pdi_projeto_final/iris/bons/'
    list1 = os.listdir(dirbase)
    print("Inicializando iris, Aguarde...")
    for laux in list1:
        string = dirbase+laux
        #print "caminho: %s" % string
        nome = laux.split('.')[0]
        extensao = laux.split('.')[1]
        #print 'extensao %s' %extensao
        if extensao == "bmp":
            try:
                nomeImage = "iris/novo/"+nome+"_2.bmp"
                iris = pegarIris(string,nomeImage)
                dct = gerarDct(nomeImage)
                irisNew = Iris(nomeImage,dct,iris)
                listIris.append(irisNew)     
            except:
                print 'Caminho invalido %s' %string
        else:
            print 'Img Invalida %s' %string
    return listIris    

def pegarIris(caminho,nameFoto="teste.bmp",salvarImage=True):
    orig = cv2.cv.LoadImage(caminho)

    orig2 = cv2.cv.CloneImage(orig)

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
    cv2.cv.SaveImage("Processamento_final_pupila.jpg",processedPupila)
    #cv.ShowImage("pupila_processada", processedPupila)


    cv.Smooth(grey_scale, processedIris, cv.CV_GAUSSIAN, 15, 15)
    cv.Canny(processedIris, processedIris, 5, 70, 3)
    cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)
    cv.Smooth(processedIris, processedIris, cv.CV_GAUSSIAN, 15, 15)
    cv2.cv.SaveImage("Processamento_final_iris.jpg",processedPupila)
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
    cv2.cv.SaveImage("macaraPupila.jpg",imagemMaskPupila)
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
    cv2.cv.SaveImage("macaraIris.jpg",imagemMaskIris)
    cv.Circle(orig, centerIris, 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
    cv.Circle(orig, centerIris, RadiusIris, cv.CV_RGB(255, 0, 0), 3, 8, 0)
    #cv.ShowImage("Iris"+str(0), orig)
    orig = cv.CloneImage(orig2)

    #cv.WaitKey(0)

    #except:
    #    print "nothing found"
    #    pass
    #criando imagem final
    finalAux = cv2.cv.CreateImage(cv.GetSize(orig), 8, 3)
    final = cv2.cv.CreateImage(cv.GetSize(orig), 8, 3)

    #pegando a iris toda
    cv2.cv.And(orig,imagemMaskPupila,finalAux)
    cv2.cv.SaveImage("pupila_cortada.jpg",finalAux)
    cv2.cv.And(finalAux,imagemMaskIris,final)
    cv2.cv.SaveImage("iris_pupila_cortada.jpg",final)

    if salvarImage:
    	cv2.cv.SaveImage(nameFoto,final)
    #cv.ShowImage("original with circles", final)
    #cv.WaitKey(0)
    return final

def gerarDct(caminnhoimg):

    img1 = cv2.imread(caminnhoimg, cv2.CV_LOAD_IMAGE_GRAYSCALE)
     
    h, w = img1.shape[:2]
    vis0 = np.zeros((h,w), np.float32)
    vis0[:h, :w] = img1
    vis1 = cv2.dct(vis0)
    img2 = cv.CreateMat(vis1.shape[0], vis1.shape[1], cv.CV_32FC3)
    cv.CvtColor(cv.fromarray(vis1), img2, cv.CV_GRAY2BGR)
     
    #cv.ShowImage('1',img2)
    #cv2.waitKey()
    #cv.SaveImage('saved.jpg', img2)
           
    #cv2.imshow("before_save", vis1)
    #vis1[vis1>255] = 255
    #vis1[vis1<0] = 0
    #cv2.imshow("saved", vis1.astype(np.uint8))

    return img2

def igualDct(dct1,dct2):
    for row in range(0,dct1.rows):
        for col in range(0,dct1.cols):
            if dct1[row,col][0] != dct2[row,col][0]:
                return False
            if dct1[row,col][1] != dct2[row,col][1]:
                return False
            if dct1[row,col][2] != dct2[row,col][2]:
                return False
    return True

def por_erroQuadratico(item):
    return item.errodct

def procurarIris(listIris,caminnhoimg):
    achou = False
    listErroDct = []
    pegarIris(caminnhoimg,"dct.bmp")
    dct = gerarDct("dct.bmp");
    predictions = np.asarray( dct[:,:] )
    N=len(predictions)
    index = 0
    for l in listIris:
        targets = np.asarray( l.dct[:,:] )
        rmse=np.linalg.norm(predictions-targets)/np.sqrt(N)
        erroDct = ErroDct(rmse,index,l.nomeIris)
        listErroDct.append(erroDct) 
        index = index + 1

    lista =sorted(listErroDct, key=por_erroQuadratico)
    listErroDct.sort()

    for a in lista:
        print "Erro %f nome: %s" %(a.errodct,a.nomeArquivo)
    """
    for l in listIris:
        if igualDct(l.dct,dct):
            print 'Achou: %s %s' %(caminnhoimg, l.nomeIris)
            return
        else:
            print 'Errado: %s %s' %(caminnhoimg, l.nomeIris)
        #cv2.waitKey()
    """

            

