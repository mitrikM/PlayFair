#UI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHeaderView, QTableWidgetItem,QVBoxLayout
from PyQt5 import QtGui, uic, QtCore



from unidecode import unidecode
import re
from collections import OrderedDict
from num2words import num2words

qtCreatorFile = "kryptoUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # return string  
    return (str1.join(s))
def index_2d(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i, x.index(v)

 

Abeceda=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

class MyApp(QMainWindow, Ui_MainWindow):

    def encrypt(self):
        Klucove_slovo=str(self.plainTextEdit_A.toPlainText())
        if Klucove_slovo.isdigit():
            self.labelVysledek.setText("zadajte platne klucove slovo")
            exit()

        Klucove_slovo=unidecode(Klucove_slovo)
        for k in Klucove_slovo.split("\n"):
            Klucove_slovo =(re.sub(r"[^a-zA-Z0-9]+", '', k))
        
        Klucove_slovo=Klucove_slovo.upper()        
    
    
        vstup=str(self.plainTextEdit_Input.toPlainText())
        i=0
        while i<len(vstup):
            if vstup[i].isdigit():
                if self.CheckBox_JazykCZ.isChecked():
                    x=num2words(vstup[i],lang="cz")
                elif self.CheckBox_JazykEN.isChecked():
                    x=num2words(vstup[i],lang="en")
                else:
                    self.labelVysledek.setText("Vyberte možnosť jazyka")
                    exit(1)
    
                vstup=vstup.replace(vstup[i],x)
            i+=1
        vstup=unidecode(vstup)
        vstup=vstup.replace(" ", "XmezeraX")
        for k in vstup.split("\n"):
            vstup=(re.sub(r"[^a-zA-Z0-9]+",'', k))
           
        vstup=vstup.upper()
        sifrovanyVstup=[]
    
    
        
        if self.CheckBox_JazykCZ.isChecked():
            Klucove_slovo=Klucove_slovo.replace("J","I")
            Klucove_slovo=''.join(OrderedDict.fromkeys(Klucove_slovo).keys())
            Special_abeceda="".join(Klucove_slovo)
            for i in range(len(Abeceda)):
                if(Abeceda[i] not in Special_abeceda and Abeceda[i] != "J"):
                    Special_abeceda+=Abeceda[i]
            vstup=vstup.replace("J","I")
        elif self.CheckBox_JazykEN.isChecked():
            Klucove_slovo=Klucove_slovo.replace("Q","O")
            Klucove_slovo=''.join(OrderedDict.fromkeys(Klucove_slovo).keys())
            Special_abeceda="".join(Klucove_slovo)
            for i in range(len(Abeceda)):
                if(Abeceda[i] not in Special_abeceda and Abeceda[i] != "Q"):
                    Special_abeceda+=Abeceda[i]
            vstup= vstup.replace("Q","O")
        else:
            self.labelVysledek.setText("Vyberte možnosť jazyka")

            
        matica_abeceda=[[0, 0, 0, 0, 0],[0,0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
        
        k=0 
        for i in range(5):
            for j in range(5):        
                matica_abeceda[i][j]=Special_abeceda[k]
                k+=1

        

        for i,row in enumerate(matica_abeceda):
            for j,val in enumerate(row):
                self.tableWidget.setItem(i,j,QTableWidgetItem(matica_abeceda[i][j]))
        i=0
        while(i<len(vstup)):
            if(i+1==len(vstup)):
                vstup=list(vstup)
                if(vstup[i]=="X"):
                    vstup.append("Z")
                    continue
                else:
                    vstup.append("X")
                    continue
            
            if(vstup[i]==vstup[i+1]):
                vstup=list(vstup)
        
                if(vstup[i]=="X"):
                    vstup.insert(i+1,"Z")
                else:
                    
                    vstup.insert(i+1, "X")
                listToString(vstup)
        
            index1=index_2d(matica_abeceda,vstup[i])    
            index2=index_2d(matica_abeceda,vstup[i+1])
            j=index1[0]
            k=index1[1]
            l=index2[0]
            m=index2[1]
            if(j==l):
                sifrovanyVstup.append(matica_abeceda[j][(k+1)%5])
                sifrovanyVstup.append(matica_abeceda[l][(m+1)%5])
            elif(k==m):
                sifrovanyVstup.append(matica_abeceda[(j+1)%5][k])
                sifrovanyVstup.append(matica_abeceda[(l+1)%5][m])
            else:
                sifrovanyVstup.append(matica_abeceda[j][m])
                sifrovanyVstup.append(matica_abeceda[l][k])
            
            i+=2
        
        sifrovanyVstup=listToString(sifrovanyVstup)
        sifrovanyVstup=' '.join([sifrovanyVstup[i:i+5] for i in range(0, len(sifrovanyVstup), 5)])                    

        self.labelVysledek.setText(sifrovanyVstup)

    
    def decrypt(self):
        Klucove_slovo=str(self.plainTextEdit_A.toPlainText())
        Klucove_slovo=unidecode(Klucove_slovo)
        for k in Klucove_slovo.split("\n"):
            Klucove_slovo =(re.sub(r"[^a-zA-Z0-9]+", '', k))
        
        Klucove_slovo=Klucove_slovo.upper()
    
        vstup=str(self.plainTextEdit_Input.toPlainText())
     
        vstup=vstup.replace(" ", "")
        vstup=vstup.upper()
        desifrovanyVstup=[]
        
        if self.CheckBox_JazykCZ.isChecked():
            Klucove_slovo=Klucove_slovo.replace("J","I")        
            Klucove_slovo=''.join(OrderedDict.fromkeys(Klucove_slovo).keys())
            Special_abeceda="".join(Klucove_slovo)
            for i in range(len(Abeceda)):
                if(Abeceda[i] not in Special_abeceda and Abeceda[i] != "J"):
                    Special_abeceda+=Abeceda[i]
            vstup=vstup.replace("J","I")
        elif self.CheckBox_JazykEN.isChecked():
            Klucove_slovo=Klucove_slovo.replace("Q","O") 
            Klucove_slovo=''.join(OrderedDict.fromkeys(Klucove_slovo).keys())
            Special_abeceda="".join(Klucove_slovo)
            for i in range(len(Abeceda)):
                if(Abeceda[i] not in Special_abeceda and Abeceda[i] != "Q"):
                    Special_abeceda+=Abeceda[i]
            vstup= vstup.replace("Q","O")
        else: 
            self.labelVysledek.setText("Vyberte možnosť jazyka")

            
        matica_abeceda=[[0, 0, 0, 0, 0],[0,0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
        
        k=0 
        for i in range(5):
            for j in range(5):        
                matica_abeceda[i][j]=Special_abeceda[k]
                k+=1
        
        for i,row in enumerate(matica_abeceda):
            for j,val in enumerate(row):
                self.tableWidget.setItem(i,j,QTableWidgetItem(matica_abeceda[i][j]))
        
        i=0
        
        while(i<len(vstup)):
            index1=index_2d(matica_abeceda,vstup[i])    
            index2=index_2d(matica_abeceda,vstup[i+1])
            j=index1[0]
            k=index1[1]
            l=index2[0]
            m=index2[1]
            if(j==l):
                desifrovanyVstup.append(matica_abeceda[j][(k-1)%5])
                desifrovanyVstup.append(matica_abeceda[l][(m-1)%5])
            elif(k==m):
                desifrovanyVstup.append(matica_abeceda[(j-1)%5][k])
                desifrovanyVstup.append(matica_abeceda[(l-1)%5][m])
            else:
                desifrovanyVstup.append(matica_abeceda[j][m])
                desifrovanyVstup.append(matica_abeceda[l][k])
            
            i+=2
        
        desifrovanyVstup=listToString(desifrovanyVstup)
        if self.CheckBox_JazykCZ.isChecked():
            desifrovanyVstup=desifrovanyVstup.replace("IEDNA","1").replace("DVA","2").replace("TRI","3").replace("CTYRI","4").replace("PET","5").replace("SEST","6").replace("SEDM","7").replace("OSM","8").replace("DEVET","9").replace("NULA","0")
        elif self.CheckBox_JazykEN.isChecked():
            desifrovanyVstup=desifrovanyVstup.replace("ONE","1").replace("TWO","2").replace("THREE","3").replace("FOUR","4").replace("FIVE","5").replace("SIX","6").replace("SEVEN","7").replace("EIGHT","8").replace("NINE","9").replace("ZERO","0")
        else:
            self.labelVysledek.setText("Vyberte možnosť jazyka")
         
        desifrovanyVstup=desifrovanyVstup.replace("XMEZERAX"," ")
        self.labelVysledek.setText(desifrovanyVstup)

    def execute(self):
        if self.CheckBox_Desifrovat.isChecked():
            self.decrypt()
        elif self.CheckBox_Sifrovat.isChecked():
            self.encrypt()
        else:
            self.labelVysledek.setText("Vyberte možnosť sifrovat alebo desifrovat")

        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Button_Execute.clicked.connect(self.execute)  
        self.tableWidget.setColumnWidth(0,50)
        self.tableWidget.setColumnWidth(1,50)
        self.tableWidget.setColumnWidth(2,50)
        self.tableWidget.setColumnWidth(3,50)
        self.tableWidget.setColumnWidth(4,50)
                


                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())        
 

