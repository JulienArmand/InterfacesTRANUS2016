#!/usr/bin/python
# Author : Julien Armand
import os
from PyQt4 import QtGui, QtCore
import sys
from TranusConfig import *
from LcalInterface import *
from LCALparam import *
import OptionsTRANUSUI
import tkMessageBox
import extractionScenarios

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
       return s    
 
class OptionsTRANUS(QtGui.QMainWindow, OptionsTRANUSUI.Ui_MainWindow):
    '''OptionsTRANUS class :
    This class is used to create the interface enabling the user to launch the TRANUS programs with various options.
    The programs allowed are imploc, imptra, and mats. It also allows to run TRANUS basic form for the generation of the
    files required by the other programs.
    '''

    def __init__(self,filepath):
        '''OptionsTRANUS(filepath)
        Constructor of the class
        
        Parameters
        ----------
        filepath : string
            the location of the config file (cf README for details about the structure of the file)
            
        Class Attributes
        ----------------
        This class has 33 * number of scenarios in project QCheckBox objects : one for each implemented use of the TRANUS programs for each scenario in the selected project.
        They are sorted by the option they activate and arranged in lists.
        ''' 
        super(OptionsTRANUS, self).__init__()
        self.setupUi(self)
        self.Generate_Button.clicked.connect(self.launch)
        f = open(filepath,"r")
        self.tranusBinPath = (f.next()[:-1])
        self.workingDirectory = (f.next()[:-1])
        self.projectID = (f.next()[:-1])
        scenarios = extractionScenarios.extractionScenarios(os.path.join(self.workingDirectory, "W_TRANUS.CTL"))
        nbScenarios = len(scenarios.listCodes)
        self.resize(400+100*nbScenarios,800)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 360+100*nbScenarios, self.positionYMats + 500))
        #Declaration of variables to store data passed in parameter
        self.listCodesScenarios = []
        self.listNamesScenarios = []
        #Declaration of lists of buttons for checking all fields at once
        self.listButtonsCheckAll = []
        self.listIsAllChecked = []
        #Declaration of lists of checkboxes and entry fields
        self.listSpinBoxesNumIteration = []
        #imploc
        self.listCheckBoxesImplocRun = []
        self.listCheckBoxesImplocI = []
        self.listCheckBoxesImplocJ = []
        self.listCheckBoxesImplocP = []
        self.listCheckBoxesImplocQ = []
        self.listCheckBoxesImplocS = []
        self.listCheckBoxesImplocC = []
        self.listCheckBoxesImplocT = []
        #imptra
        self.listCheckBoxesImptraRun = []
        self.listCheckBoxesImptraA = []
        self.listCheckBoxesImptraC = []
        self.listCheckBoxesImptraD = []
        self.listCheckBoxesImptraI = []
        self.listCheckBoxesImptraJ = []
        self.listCheckBoxesImptraL = []
        self.listCheckBoxesImptraP = []
        self.listCheckBoxesImptraR = []
        self.listCheckBoxesImptraS = []
        self.listCheckBoxesImptraT = []
        #mats
        self.listCheckBoxesMatsD = []
        self.listCheckBoxesMatsM = []
        self.listCheckBoxesMatsS = []
        self.listCheckBoxesMatsP = []
        self.listCheckBoxesMatsQ = []
        self.listCheckBoxesMatsR = []
        self.listCheckBoxesMatsT = []
        self.listCheckBoxesMatsO = []
        self.listCheckBoxesMatsE = []
        self.listCheckBoxesMatsF = []
        self.listCheckBoxesMatsC = []
        self.listCheckBoxesMatsK = []
        self.listCheckBoxesMatsX = []
        self.listCheckBoxesMatsY = []
        self.initLists(nbScenarios)
        
        #Creation of all columns in loop
        for i in range (nbScenarios) :
            self.createCheckBoxes(scenarios,i)
            
        self.line = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line.setGeometry(QtCore.QRect(350+((nbScenarios)*100), 10, 20, self.positionYMats + 307))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)    
        
    
    
    def launch(self):
        '''launch()
        This method is activated when clicking on the button labeled 'Generate' at the bottom of the interface.
        It executes TRANUS with the options checked by the user.
        '''
        self.console.append("Beginning execution TRANUS ...")
        for i in range (len(self.listCodesScenarios)):
            self.console.append("Beginning of execution for scenario "+self.listCodesScenarios[i] )
            t = TranusConfig(self.tranusBinPath,self.workingDirectory, self.projectID,self.listCodesScenarios[i])
            self.console.append("TRANUS binaries directory                    : "+ t.tranusBinPath)
            self.console.append("Directory where is located the .tuz file     : "+ t.workingDirectory)
            self.console.append("ID of the project that we want to simulate   : "+ t.projectId)
            self.console.append("ID of the scenario that we want to simulate  : "+ t.scenarioId)
            self.console.append("Parameters file                              : "+ t.param_file)
            self.console.append("Observations file                            : "+ t.obs_file)
            self.console.append("Zone file                                    : "+ t.zone_file)
            self.console.append("Convergence factor                           : "+ t.convFactor)
            #Creation of directory for results :
            pathScenarioResultDirectory = os.path.join(self.workingDirectory, self.listCodesScenarios[i])
            if not os.path.exists(pathScenarioResultDirectory):
                os.makedirs(pathScenarioResultDirectory)
            interface = LcalInterface(t,pathScenarioResultDirectory)
            #imploc
            if(self.listCheckBoxesImplocI[i].isChecked()):
                self.console.append("Executing Imploc -I for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("I")
                self.console.append("The resulting matrix is written in file IMPLOC_I.MTX")
            if(self.listCheckBoxesImplocJ[i].isChecked()):
                self.console.append("Executing Imploc -J for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("J")
                self.console.append("The resulting matrix is written in file IMPLOC_J.MTX")
            if(self.listCheckBoxesImplocP[i].isChecked()):
                self.console.append("Executing Imploc -P for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("P")
                self.console.append("The resulting matrix is written in file IMPLOC_P.MTX")
            if(self.listCheckBoxesImplocQ[i].isChecked()):
                self.console.append("Executing Imploc -Q for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("Q")
                self.console.append("The resulting matrix is written in file IMPLOC_Q.MTX")
            if(self.listCheckBoxesImplocS[i].isChecked()):
                self.console.append("Executing Imploc -S for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("S")
                self.console.append("The resulting matrix is written in file IMPLOC_S.MTX")
            if(self.listCheckBoxesImplocC[i].isChecked()):
                self.console.append("Executing Imploc -C for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("C")
                self.console.append("The resulting matrix is written in file IMPLOC_C.MTX")
            if(self.listCheckBoxesImplocT[i].isChecked()):
                self.console.append("Executing Imploc -T for scenario " +self.listNamesScenarios[i])
                interface.runImplocOption("T")
                self.console.append("The resulting matrix is written in file IMPLOC_T.MTX")
            #imptra
            if(self.listCheckBoxesImptraA[i].isChecked()):
                self.console.append("Executing Imptra -A for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("A")
                self.console.append("The resulting matrix is written in file IMPTRA_A.MTX")
            if(self.listCheckBoxesImptraC[i].isChecked()):
                self.console.append("Executing Imptra -C for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("C")
                self.console.append("The resulting matrix is written in file IMPTRA_C.MTX")
            if(self.listCheckBoxesImptraD[i].isChecked()):
                self.console.append("Executing Imptra -D for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("D")
                self.console.append("The resulting matrix is written in file IMPTRA_D.MTX")
            if(self.listCheckBoxesImptraI[i].isChecked()):
                self.console.append("Executing Imptra -I for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("I")
                self.console.append("The resulting matrix is written in file IMPTRA_I.MTX")
            if(self.listCheckBoxesImptraJ[i].isChecked()):
                self.console.append("Executing Imptra -J for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("J")
                self.console.append("The resulting matrix is written in file IMPTRA_J.MTX")
            if(self.listCheckBoxesImptraL[i].isChecked()):
                self.console.append("Executing Imptra -L for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("L")
                self.console.append("The resulting matrix is written in file IMPTRA_L.MTX")
            if(self.listCheckBoxesImptraP[i].isChecked()):
                self.console.append("Executing Imptra -P for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("P")
                self.console.append("The resulting matrix is written in file IMPTRA_P.MTX")
            if(self.listCheckBoxesImptraR[i].isChecked()):
                self.console.append("Executing Imptra -R for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("R")
                self.console.append("The resulting matrix is written in file IMPTRA_R.MTX")
            if(self.listCheckBoxesImptraS[i].isChecked()):
                self.console.append("Executing Imptra -S for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("S")
                self.console.append("The resulting matrix is written in file IMPTRA_S.MTX")
            if(self.listCheckBoxesImptraT[i].isChecked()):
                self.console.append("Executing Imptra -T for scenario " +self.listNamesScenarios[i])
                interface.runImptraOption("T")
                self.console.append("The resulting matrix is written in file IMPTRA_T.MTX")
            #mats
            if(self.listCheckBoxesMatsD[i].isChecked()):
                self.console.append("Executing mats -D for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("D")
                self.console.append("The resulting matrix is written in file MATS_D.MTX")
            if(self.listCheckBoxesMatsM[i].isChecked()):
                self.console.append("Executing mats -M for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("M")
                self.console.append("The resulting matrix is written in file MATS_M.MTX")
            if(self.listCheckBoxesMatsS[i].isChecked()):
                self.console.append("Executing mats -S for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("S")
                self.console.append("The resulting matrix is written in file MATS_S.MTX")
            if(self.listCheckBoxesMatsP[i].isChecked()):
                self.console.append("Executing mats -P for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("P")
                self.console.append("The resulting matrix is written in file MATS_P.MTX")
            if(self.listCheckBoxesMatsQ[i].isChecked()):
                self.console.append("Executing mats -Q for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("Q")
                self.console.append("The resulting matrix is written in file MATS_Q.MTX")
            if(self.listCheckBoxesMatsR[i].isChecked()):
                self.console.append("Executing mats -R for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("R")
                self.console.append("The resulting matrix is written in file MATS_R.MTX")
            if(self.listCheckBoxesMatsT[i].isChecked()):
                self.console.append("Executing mats -T for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("T")
                self.console.append("The resulting matrix is written in file MATS_T.MTX")
            if(self.listCheckBoxesMatsO[i].isChecked()):
                self.console.append("Executing mats -O for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("O")
                self.console.append("The resulting matrix is written in file MATS_O.MTX")
            if(self.listCheckBoxesMatsE[i].isChecked()):
                self.console.append("Executing mats -E for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("E")
                self.console.append("The resulting matrix is written in file MATS_E.MTX")
            if(self.listCheckBoxesMatsF[i].isChecked()):
                self.console.append("Executing mats -F for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("F")    
                self.console.append("The resulting matrix is written in file MATS_F.MTX")
            if(self.listCheckBoxesMatsC[i].isChecked()):
                self.console.append("Executing mats -C for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("C")
                self.console.append("The resulting matrix is written in file MATS_C.MTX")
            if(self.listCheckBoxesMatsK[i].isChecked()):
                self.console.append("Executing mats -K for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("K")
                self.console.append("The resulting matrix is written in file MATS_K.MTX")
            if(self.listCheckBoxesMatsX[i].isChecked()):
                self.console.append("Executing mats -X for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("X")
                self.console.append("The resulting matrix is written in file MATS_X.MTX")
            if(self.listCheckBoxesMatsY[i].isChecked()):
                self.console.append("Executing mats -Y for scenario " +self.listNamesScenarios[i])
                interface.runMatsOption("Y")
                self.console.append("The resulting matrix is written in file MATS_Y.MTX")
                
        self.console.append("Calculations complete")
    
    #Creation of lists of Check Boxes    
    def initLists(self,nbScenarios):
        self.listSpinBoxesNumIteration = [QtGui.QSpinBox() for i in range (nbScenarios)]
        self.listButtonsCheckAll = [QtGui.QPushButton() for i in range(nbScenarios)]
        self.listIsAllChecked = [0 for i in range(nbScenarios)]
        self.listCheckBoxesImplocRun = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocI = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocJ = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocP = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocQ = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocS = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocC = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImplocT = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraRun = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraA = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraC = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraD = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraI = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraJ = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraL = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraP = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraR = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraS = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesImptraT = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsD = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsM = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsS = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsP = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsQ = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsR = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsT = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsO = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsE = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsF = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsC = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsK = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsX = [QtGui.QCheckBox() for i in range(nbScenarios)]
        self.listCheckBoxesMatsY = [QtGui.QCheckBox() for i in range(nbScenarios)]
          
    #Create the checkboxes for column i
    def createCheckBoxes(self,scenarios,i):
            self.currentLabel = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.currentLabel.setGeometry(QtCore.QRect(400+(i*100), 20, 100, 13))
            self.currentLabel.setText(scenarios.listCodes[i])
            self.listCodesScenarios.append(scenarios.listCodes[i])
            self.listNamesScenarios.append(scenarios.listNames[i])
            #Button Run TRANUS
            self.currentButtonCheckAll = QtGui.QPushButton(self.scrollAreaWidgetContents)
            self.currentButtonCheckAll.setGeometry(QtCore.QRect(370+(i*100), 50, 82, 17))
            self.currentButtonCheckAll.setText("Run TRANUS")
            self.currentButtonCheckAll.clicked.connect(lambda : self.runTRANUS(i))
            #Spinbox for number of iterations
            self.currentSpinBox = QtGui.QSpinBox(self.scrollAreaWidgetContents)
            self.currentSpinBox.setGeometry(QtCore.QRect(390+(i*100), 70, 42, 22))
            self.listSpinBoxesNumIteration[i] = self.currentSpinBox
            #Trace the vertical line between columns
            self.line = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.line.setGeometry(QtCore.QRect(350+(i*100), 10, 20, self.positionYMats + 307))
            self.line.setFrameShape(QtGui.QFrame.VLine)
            self.line.setFrameShadow(QtGui.QFrame.Sunken)
            #Put the checkboxes into place  
            #imploc
            self.currentCheckBoxImplocRun = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocRun.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+30, 82, 17))
            self.listCheckBoxesImplocRun[i] = self.currentCheckBoxImplocRun
            self.currentCheckBoxImplocI = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocI.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+50, 82, 17))
            self.listCheckBoxesImplocI[i] = self.currentCheckBoxImplocI
            self.currentCheckBoxImplocJ = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocJ.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+70, 82, 17))
            self.listCheckBoxesImplocJ[i] = self.currentCheckBoxImplocJ
            self.currentCheckBoxImplocP = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocP.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+90, 82, 17))
            self.listCheckBoxesImplocP[i] = self.currentCheckBoxImplocP
            self.currentCheckBoxImplocQ = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocQ.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+110, 82, 17))
            self.listCheckBoxesImplocQ[i] = self.currentCheckBoxImplocQ
            self.currentCheckBoxImplocS = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocS.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+130, 82, 17))
            self.listCheckBoxesImplocS[i] = self.currentCheckBoxImplocS
            self.currentCheckBoxImplocC = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocC.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+150, 82, 17))
            self.listCheckBoxesImplocC[i] = self.currentCheckBoxImplocC
            self.currentCheckBoxImplocT = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImplocT.setGeometry(QtCore.QRect(400+(i*100), self.positionYImploc+170, 82, 17))
            self.listCheckBoxesImplocT[i] = self.currentCheckBoxImplocT
            #imptra
            self.currentCheckBoxImptraRun = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraRun.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+30, 82, 17))
            self.listCheckBoxesImptraRun[i] = self.currentCheckBoxImptraRun
            self.currentCheckBoxImptraA = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraA.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+50, 82, 17))
            self.listCheckBoxesImptraA[i] = self.currentCheckBoxImptraA
            self.currentCheckBoxImptraC = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraC.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+70, 82, 17))
            self.listCheckBoxesImptraC[i] = self.currentCheckBoxImptraC
            self.currentCheckBoxImptraD = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraD.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+90, 82, 17))
            self.listCheckBoxesImptraD[i] = self.currentCheckBoxImptraD
            self.currentCheckBoxImptraI = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraI.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+110, 82, 17))
            self.listCheckBoxesImptraI[i] = self.currentCheckBoxImptraI
            self.currentCheckBoxImptraJ = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraJ.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+130, 82, 17))
            self.listCheckBoxesImptraJ[i] = self.currentCheckBoxImptraJ
            self.currentCheckBoxImptraL = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraL.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+150, 82, 17))
            self.listCheckBoxesImptraL[i] = self.currentCheckBoxImptraL
            self.currentCheckBoxImptraP = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraP.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+170, 82, 17))
            self.listCheckBoxesImptraP[i] = self.currentCheckBoxImptraP
            self.currentCheckBoxImptraR = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraR.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+190, 82, 17))
            self.listCheckBoxesImptraR[i] = self.currentCheckBoxImptraR
            self.currentCheckBoxImptraS = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraS.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+210, 82, 17))
            self.listCheckBoxesImptraS[i] = self.currentCheckBoxImptraS
            self.currentCheckBoxImptraT = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxImptraT.setGeometry(QtCore.QRect(400+(i*100), self.positionYImptra+230, 82, 17))
            self.listCheckBoxesImptraT[i] = self.currentCheckBoxImptraT
            #mats
            self.currentCheckBoxMatsD = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsD.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+30, 82, 17))
            self.listCheckBoxesMatsD[i] = self.currentCheckBoxMatsD
            self.currentCheckBoxMatsM = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsM.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+50, 82, 17))
            self.listCheckBoxesMatsM[i] = self.currentCheckBoxMatsM
            self.currentCheckBoxMatsS = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsS.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+70, 82, 17))
            self.listCheckBoxesMatsS[i] = self.currentCheckBoxMatsS
            self.currentCheckBoxMatsP = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsP.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+90, 82, 17))
            self.listCheckBoxesMatsP[i] = self.currentCheckBoxMatsP
            self.currentCheckBoxMatsQ = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsQ.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+110, 82, 17))
            self.listCheckBoxesMatsQ[i] = self.currentCheckBoxMatsQ
            self.currentCheckBoxMatsR = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsR.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+130, 82, 17))
            self.listCheckBoxesMatsR[i] = self.currentCheckBoxMatsR
            self.currentCheckBoxMatsT = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsT.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+150, 82, 17))
            self.listCheckBoxesMatsT[i] = self.currentCheckBoxMatsT
            self.currentCheckBoxMatsO = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsO.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+170, 82, 17))
            self.listCheckBoxesMatsO[i] = self.currentCheckBoxMatsO
            self.currentCheckBoxMatsE = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsE.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+190, 82, 17))
            self.listCheckBoxesMatsE[i] = self.currentCheckBoxMatsE
            self.currentCheckBoxMatsF = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsF.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+210, 82, 17))
            self.listCheckBoxesMatsF[i] = self.currentCheckBoxMatsF
            self.currentCheckBoxMatsC = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsC.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+230, 82, 17))
            self.listCheckBoxesMatsC[i] = self.currentCheckBoxMatsC
            self.currentCheckBoxMatsK = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsK.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+250, 82, 17))
            self.listCheckBoxesMatsK[i] = self.currentCheckBoxMatsK
            self.currentCheckBoxMatsX = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsX.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+270, 82, 17))
            self.listCheckBoxesMatsX[i] = self.currentCheckBoxMatsX
            self.currentCheckBoxMatsY = QtGui.QCheckBox(self.scrollAreaWidgetContents)
            self.currentCheckBoxMatsY.setGeometry(QtCore.QRect(400+(i*100), self.positionYMats+290, 82, 17))
            self.listCheckBoxesMatsY[i] = self.currentCheckBoxMatsY
            #Button CheckAll
            self.currentButtonCheckAll = QtGui.QPushButton(self.scrollAreaWidgetContents)
            self.currentButtonCheckAll.setGeometry(QtCore.QRect(370+(i*100), self.positionYMats + 320, 82, 17))
            self.currentButtonCheckAll.setText("Check All")
            self.currentButtonCheckAll.clicked.connect(lambda : self.checkAll(i))
 
        #Check all the boxes of column i (calling the function again unchecks them)
    def checkAll(self,i):
        newState = 0
        if(self.listIsAllChecked[i] == 0):
            self.listIsAllChecked[i] = 1
            newState = 1
        else :
            self.listIsAllChecked[i] = 0
        #imploc
        self.listCheckBoxesImplocRun[i].setCheckState(newState)
        self.listCheckBoxesImplocI[i].setCheckState(newState)
        self.listCheckBoxesImplocJ[i].setCheckState(newState)
        self.listCheckBoxesImplocP[i].setCheckState(newState)
        self.listCheckBoxesImplocQ[i].setCheckState(newState)
        self.listCheckBoxesImplocS[i].setCheckState(newState)
        self.listCheckBoxesImplocC[i].setCheckState(newState)
        self.listCheckBoxesImplocT[i].setCheckState(newState)
        #imptra
        self.listCheckBoxesImptraRun[i].setCheckState(newState)
        self.listCheckBoxesImptraA[i].setCheckState(newState)
        self.listCheckBoxesImptraC[i].setCheckState(newState)
        self.listCheckBoxesImptraD[i].setCheckState(newState)
        self.listCheckBoxesImptraI[i].setCheckState(newState)
        self.listCheckBoxesImptraJ[i].setCheckState(newState)
        self.listCheckBoxesImptraL[i].setCheckState(newState)
        self.listCheckBoxesImptraP[i].setCheckState(newState)
        self.listCheckBoxesImptraR[i].setCheckState(newState)
        self.listCheckBoxesImptraS[i].setCheckState(newState)
        self.listCheckBoxesImptraT[i].setCheckState(newState)
        #mats
        self.listCheckBoxesMatsD[i].setCheckState(newState)
        self.listCheckBoxesMatsM[i].setCheckState(newState)
        self.listCheckBoxesMatsS[i].setCheckState(newState)
        self.listCheckBoxesMatsP[i].setCheckState(newState)
        self.listCheckBoxesMatsQ[i].setCheckState(newState)
        self.listCheckBoxesMatsR[i].setCheckState(newState)
        self.listCheckBoxesMatsT[i].setCheckState(newState)
        self.listCheckBoxesMatsO[i].setCheckState(newState)
        self.listCheckBoxesMatsE[i].setCheckState(newState)
        self.listCheckBoxesMatsF[i].setCheckState(newState)
        self.listCheckBoxesMatsC[i].setCheckState(newState)
        self.listCheckBoxesMatsK[i].setCheckState(newState)
        self.listCheckBoxesMatsX[i].setCheckState(newState)
        self.listCheckBoxesMatsY[i].setCheckState(newState)
        
    
    def runTRANUS(self, i):
        self.console.append("Beginning of execution of basic TRANUS programs for scenario "+self.listCodesScenarios[i] )
        t = TranusConfig(self.tranusBinPath,self.workingDirectory, self.projectID,self.listCodesScenarios[i])
        self.console.append("TRANUS binaries directory                    : "+ t.tranusBinPath)
        self.console.append("Directory where is located the .tuz file     : "+ t.workingDirectory)
        self.console.append("ID of the project that we want to simulate   : "+ t.projectId)
        self.console.append("ID of the scenario that we want to simulate  : "+ t.scenarioId)
        self.console.append("Parameters file                              : "+ t.param_file)
        self.console.append("Observations file                            : "+ t.obs_file)
        self.console.append("Zone file                                    : "+ t.zone_file)
        self.console.append("Convergence factor                           : "+ t.convFactor)
        #Creation of directory for results :
        pathScenarioResultDirectory = os.path.join(self.workingDirectory, self.listCodesScenarios[i])
        if not os.path.exists(pathScenarioResultDirectory):
            os.makedirs(pathScenarioResultDirectory)
        interface = LcalInterface(t,pathScenarioResultDirectory)
        self.console.append("Executing loop TRANUS for "+ `self.listSpinBoxesNumIteration[i].value()` +" iterations")
        interface.runTranus(self.listSpinBoxesNumIteration[i].value())
     
    def main(self):
		self.show()
 
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    optionsTRANUS = OptionsTRANUS("config")
    optionsTRANUS.main()
    app.exec_()