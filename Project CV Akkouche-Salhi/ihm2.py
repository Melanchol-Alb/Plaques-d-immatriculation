from PyQt5 import QtCore, QtGui, QtWidgets
import os
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np

from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter as tk

def mouseHandler(event,x,y,flags,param):
    global im_temp, pts_src
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(im_temp,(x,y),3,(0,255,255),5,cv2.LINE_AA)
        cv2.imshow("Image", im_temp)
        if len(pts_src) < 4:
            pts_src = np.append(pts_src,[(x,y)],axis=0)
            
def extractMat(image):
    global im_temp, pts_src
    im_src = cv2.imread(image)
    
    cv2.namedWindow("Image", 1)

    im_temp = im_src.copy()
    pts_src = np.empty((0,2))

    cv2.setMouseCallback("Image",mouseHandler)
    
    cv2.imshow("Image", im_temp)
    cv2.waitKey(0)
    
    return im_src[int(pts_src[:,1].min()):int(pts_src[:,1].max()),int(pts_src[:,0].min()):int(pts_src[:,0].max())]
    
def getTrain():
    sift = cv2.SIFT_create()
    train = []
    trainNames = []
    for file in os.listdir("train/"):
        if file.endswith(".jpg"):
            kp, des = sift.detectAndCompute(cv2.cvtColor(cv2.imread("train/"+file),cv2.COLOR_BGR2GRAY), None)
            train = train + [tuple(des)]
            trainNames = trainNames + [file]
    return train,trainNames
    
def afficher(image,des):
    sift = cv2.SIFT_create()
    mat = cv2.imread("train/"+image)
    bf = ""
    best = 0
    for file2 in os.listdir("Done/"):
        if file2.endswith(".jpg"):
            img = cv2.imread("Done/"+file2,0)
            kpp,dess = sift.detectAndCompute(img, None)
            match = cv2.BFMatcher()
            matches = match.knnMatch(dess,des,k=2)
                
            good = []
            for m,n in matches:
                if m.distance < 0.6*n.distance:
                    good.append(m)
            
            if(len(good)>best):
                bf = str(file2)
                best = len(good)
    cv2.imshow("Matricule",mat)
    cv2.imshow("Image d'origine",cv2.imread("Done/"+bf))
    cv2.waitKey(0)
def fonction(train,tn):
    sift = cv2.SIFT_create()
    file = fd.askopenfilename()
    if file.endswith(".jpg") or file.endswith(".png") :
        kp,dess = sift.detectAndCompute(cv2.cvtColor(cv2.imread(file),cv2.COLOR_BGR2GRAY), None)
        match = cv2.BFMatcher()
        
        best = 0
        bf = 0
        for i in range(len(train)):
            des = np.array(list(train[i]))
            matches = match.knnMatch(des,dess,k=2)
                
            good = []
            for m,n in matches:
                if m.distance < 0.6*n.distance:
                    good.append(m)
            if(len(good)>best):
                bf = i
                best = len(good)
                
    if(len(train[bf])<2*best):
        messagebox.showinfo("Match found", str(best)+"/"+str(len(train[bf]))+" correspondances de points sift trouvées !")
        afficher(tn[bf],np.array(list(train[bf])))
    else:
        messagebox.showinfo("Match not found", str(best)+"/"+str(len(train[bf]))+" correspondances de points sift trouvées !")
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Gestion des matricules")
        MainWindow.resize(580, 386)
        
        self.TRAIN,self.tn = getTrain()
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 591, 411))
        self.label.setPixmap(QtGui.QPixmap("Simple.jpg"))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 60, 281, 41))
        self.pushButton.setStyleSheet("font: bold 14px;\n"
"border-width: 5px;\n"
"border-color: white;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnTrain)
        
        self.pushButtonTest = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonTest.setGeometry(QtCore.QRect(20, 240, 281, 41))
        self.pushButtonTest.setStyleSheet("font: bold 14px;\n"
"border-width: 5px;\n"
"border-color: white;")
        self.pushButtonTest.setObjectName("pushButtonTest")
        self.pushButtonTest.clicked.connect(self.btnTest)
        
        self.pushButtonAJT = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAJT.setGeometry(QtCore.QRect(170, 120, 281, 41))
        self.pushButtonAJT.setStyleSheet("font: bold 14px;\n"
"border-width: 5px;\n"
"border-color: white;")
        self.pushButtonAJT.setObjectName("pushButtonAJT")
        self.pushButtonAJT.clicked.connect(self.btnAJT)
        
        self.pushButtonDEL = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDEL.setGeometry(QtCore.QRect(100, 180, 281, 41))
        self.pushButtonDEL.setStyleSheet("font: bold 14px;\n"
"border-width: 5px;\n"
"border-color: white;")
        self.pushButtonDEL.setObjectName("pushButtonDEL")
        self.pushButtonDEL.clicked.connect(self.btnDEL)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 580, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Configurer le TRAIN set"))
        self.pushButtonTest.setText(_translate("MainWindow", "Tester"))
        self.pushButtonAJT.setText(_translate("MainWindow", "Ajouter au TRAIN set"))
        self.pushButtonDEL.setText(_translate("MainWindow", "Enlever du TRAIN set"))

    def btnTrain(self):
        train = []
        ROOT = tk.Tk()
        ROOT.withdraw()
        i = 0
        for file in os.listdir("License Plates/"):
            if file.endswith(".jpg"):
                e = extractMat("License Plates/"+file)
                MAT = simpledialog.askstring(title="Test",prompt="Inserer le matricule:")
                if(MAT==""):
                    cv2.imwrite('train/'+str(i)+'.jpg',e)
                    i = i + 1
                else:
                    cv2.imwrite('train/'+MAT+'.jpg',e)
                
                os.rename("License Plates/"+file, "Done/"+file)
              
        self.TRAIN,self.tn = getTrain()
        ROOT.destroy()
    
    def btnTest(self):
        ROOT = tk.Tk()
        ROOT.withdraw()
        fonction(self.TRAIN,self.tn)
        ROOT.destroy()
        
    def btnAJT(self):
        ROOT = tk.Tk()
        ROOT.withdraw()
        file = fd.askopenfilename()
        if file.endswith(".jpg"):
            e = extractMat(file)
            MAT = simpledialog.askstring(title="Ajouter a train",prompt="Inserer le matricule:")
            cv2.imwrite('train/'+MAT+'.jpg',e)
            self.TRAIN,self.tn = getTrain()
        ROOT.destroy()
                
    def btnDEL(self):
        ROOT = tk.Tk()
        ROOT.withdraw()
        MAT = simpledialog.askstring(title="Matricule du vehicule a enlever",prompt="Inserer le matricule:")
        if os.path.isfile("train/"+str(MAT)+".jpg"):
            os.remove("train/"+str(MAT)+".jpg")
            messagebox.showinfo("Succes: ","%s retiré du train set" % str(MAT))
        else:    ## Show an error ##
            messagebox.showinfo("Erreur: ","%s non existante" % str(MAT))
        ROOT.destroy()
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
