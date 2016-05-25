#!/usr/bin/python
# Author : Julien Armand
import os
from PyQt4 import QtGui, QtCore
import sys
from TranusConfig import *
from LcalInterface import *
from LCALparam import *
import InterfaceVariationTRANUSUI
import extractionScenarios
import tkMessageBox
import Tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
       return s     
       
        
class InterfaceVariationTRANUS(QtGui.QMainWindow, InterfaceVariationTRANUSUI.Ui_MainWindow):
    '''InterfaceVariationTRANUS class :
    This class is used to run Imploc multiple times on a scenarion with minute variations to a single variable, 
    so that the user might analyze the impact these variations cause on the price and shadow price. 
    It allows the tracing of graphes with these two values for each zone in the model.
    Due to the presence of four tabs (2.1; 2.2; 2.3 and 3.2) corresponding to the four sections of the L1E file, 
    the methods updateVariable, launch, displayResult and plot each require four methods.
    '''
    def __init__(self, filepath):
        '''InterfaceVariationTRANUS(LCALparam, TranusConfig)
        Constructor of the class, this object has a local variable for each scrolling list and spin box in the interface.
        It also has multiple booleans, used to keep track of the interface's current state.
        Parameters
        ----------
        filepath : string
            the location of the config file (cf README for details about the structure of the file)
        Class attributes
        ----------------
        stockParam : LCALparam object
            stores the LCALparam object created from the file passed in parameter
        stockTranusConfig : TranusConfig object
            stores the TranusConfig object created from the file passed in parameter
        generate2_1 : boolean
            indicates whether there has already been a use of TRANUS in the 2.1 tab
        generate2_2 : boolean
            indicates whether there has already been a use of TRANUS in the 2.2 tab
        generate2_3 : boolean
            indicates whether there has already been a use of TRANUS in the 2.3 tab
        generate3_2 : boolean
            indicates whether there has already been a use of TRANUS in the 3.2 tab
        savedOldValue : double
            used to store the original value of the variable in the L1E file being modified by the current use of the interface in order to restore it afterwards
        windowAvailable : boolean
            indicates whether or not a window of information for the results is currently shown, since only one at a time is possible
        '''
        super(InterfaceVariationTRANUS, self).__init__()
        f = open(filepath,"r")
        path = (f.next()[:-1])
        directory = (f.next()[:-1])
        IDproject = (f.next()[:-1])
        scenarios = extractionScenarios.extractionScenarios(os.path.join(directory, "W_TRANUS.CTL"))
        self.stockTranusConfig = TranusConfig(path,directory,IDproject,scenarios.listCodes[0])
        self.stockParam = LCALparam(self.stockTranusConfig)
        self.generate2_1 = False
        self.generate2_2 = False
        self.generate2_3 = False
        self.generate3_2 = False
        self.savedOldValue = 0
        self.setupUi(self)
        for n in range(len(self.stockParam.list_sectors)):
            self.DropDownListSector2_1.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListSector_22.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListInput2_2.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListSector2_3.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListSubstitution.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListSector3_2.addItem(self.stockParam.list_names_sectors[n])
            self.DropDownListInput3_2.addItem(self.stockParam.list_names_sectors[n])
        
        self.DropDownListInput2_2.setCurrentIndex(1)
        self.DropDownListSubstitution.setCurrentIndex(1)
        self.NbIterations2_1.setValue(1)
        self.NbIterations_22.setValue(1)
        self.NbIterations2_3.setValue(1)
        self.NbIterations3_2.setValue(1)
        self.DropDownListVariable2_1.addItems(["Utility Level 1","Utility Level 2","Price Level 1", "Price Level 2", "Logit Scale", "Attraction Factor", "Price-Cost Ratio", "Sector Type"])
        self.DropDownListVariable_22.addItems(["MinCons", "MaxCons", "Elasticity"])
        self.DropDownListVariable2_3.addItems(["SustElast","LogitSc","Penal"])
        self.DropDownListVariable3_2.addItems(["Level 1"])
        
        nbi = int(self.stockParam.nbIterations)
        self.NbIterLcal2_1.setValue(nbi)
        self.NbIterLcal2_2.setValue(nbi)
        self.NbIterLcal2_3.setValue(nbi)
        self.NbIterLcal3_2.setValue(nbi)
        
        #Conversion from the float value of the convergence factor to the 1E-X format
        cf = 0
        t = float(self.stockParam.convergenceFactor)
        while(t < 1):
            cf = cf + 1
            t = t*10
        
        self.ConvFactor2_1.setValue(cf)
        self.ConvFactor2_2.setValue(cf)
        self.ConvFactor2_3.setValue(cf)
        self.ConvFactor3_2.setValue(cf)
        sf = float(self.stockParam.smoothingFactor)
        self.SmoothingFactor2_1.setValue(sf)
        self.SmoothingFactor2_2.setValue(sf)
        self.SmoothingFactor2_3.setValue(sf)
        self.SmoothingFactor3_2.setValue(sf)
        
        #Connection of lists to updating functions
        self.DropDownListVariable2_1.currentIndexChanged.connect(self.updateVariable21)
        self.DropDownListSector2_1.currentIndexChanged.connect(self.updateVariable21)
        self.DropDownListSector_22.currentIndexChanged.connect(self.updateVariable22)
        self.DropDownListInput2_2.currentIndexChanged.connect(self.updateVariable22)
        self.DropDownListVariable_22.currentIndexChanged.connect(self.updateVariable22)
        self.DropDownListSector2_3.currentIndexChanged.connect(self.updateVariable23)
        self.DropDownListSubstitution.currentIndexChanged.connect(self.updateVariable23)
        self.DropDownListVariable2_3.currentIndexChanged.connect(self.updateVariable23)
        self.DropDownListSector3_2.currentIndexChanged.connect(self.updateVariable32)
        self.DropDownListInput3_2.currentIndexChanged.connect(self.updateVariable32)
        self.DropDownListVariable3_2.currentIndexChanged.connect(self.updateVariable32)
        
        #Connection of buttons to functions launching TRANUS
        self.windowAvailable = True
        self.ButtonLaunchTranus2_1.clicked.connect(self.launch21)
        self.ButtonLaunchTranus2_2.clicked.connect(self.launch22)
        self.ButtonLaunchTranus2_3.clicked.connect(self.launch23)
        self.ButtonLaunchTranus3_2.clicked.connect(self.launch32)
        self.ButtonPlot2_1.clicked.connect(self.plot21)
        self.ButtonPlot2_2.clicked.connect(self.plot22)
        self.ButtonPlot2_3.clicked.connect(self.plot23)
        self.ButtonPlot3_2.clicked.connect(self.plot32)
        
        #Connection of buttons for displaying the results (mean and variance) to the relevant functions
        self.buttonResults2_1.clicked.connect(self.displayResults2_1)
        self.buttonResults2_2.clicked.connect(self.displayResults2_2)
        self.buttonResults2_3.clicked.connect(self.displayResults2_3)
        self.buttonResults3_2.clicked.connect(self.displayResults3_2)
        
        #Initialization of all automatically selected values at launch
        self.updateVariable21()
        self.updateVariable22()
        self.updateVariable23()
        self.updateVariable32()
        self.check22 = True
        self.check23 = True
        self.numFiguresPlot2_1 = -1
        self.numFiguresPlot2_2 = -1
        self.numFiguresPlot2_3 = -1
        self.numFiguresPlot3_2 = -1
        self.currentSectorPlot2_1 = -1
        self.currentSectorPlot2_2 = -1
        self.currentSectorPlot2_3 = -1
        self.currentSectorPlot3_2 = -1
    
    def updateVariable21(self):
        '''updateVariable21()
        This methods is automatically called when the user changes the selected value on one of the selection bars in tab 2.1.
        It takes the value corresponding to the new configuration (sector selected + variable selected) and shows it in LabelDislayCurrentValue2_1.
        '''
        print("Updating variable selected for 2.1 ...")
        sector = self.DropDownListSector2_1.currentIndex()
        variable = self.DropDownListVariable2_1.currentIndex()
        if(variable == 0):
            print ("Updating Utility Level 1")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.beta[sector]))
        if(variable == 1):
            print ("Updating Utility Level 2")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.list_utility_lvl2[sector]))
        if(variable == 2):
            print ("Updating Price Level 1")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.lamda[sector]))
        if(variable == 3):
            print ("Updating Price Level 2")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.list_price_lvl2[sector]))
        if(variable == 4):
            print ("Updating Logit Scale")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.thetaLoc[sector]))
        if(variable == 5):
            print ("Updating Attraction Factor")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.alfa[sector]))
        if(variable == 6):
            print("Updating Price-Cost Ratio")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.list_price_cost_ratio[sector]))
        if(variable == 7):
            print ("Updating Sector Type")
            self.LabelDislayCurrentValue2_1.setText(str(self.stockParam.list_sector_type[sector]))
    
    def updateVariable22(self):
        '''updateVariable22()
        This methods is automatically called when the user changes the selected value on one of the selection bars in tab 2.2.
        It takes the value corresponding to the new configuration (sector selected + input selected + variable selected) and shows it in LabelDislayCurrentValue2_2.
        '''
        print("Updating variable selected for 2.2 ...")
        sector = self.DropDownListSector_22.currentIndex()
        input = self.DropDownListInput2_2.currentIndex()
        variable = self.DropDownListVariable_22.currentIndex()
        root = tk.Tk()
        root.withdraw()
        if(sector == input):
            tkMessageBox.showerror("Error", "Sector and input are identical")
            self.check22 = False
        else :
            self.check22 = True
            if(variable == 0):
                print("Updating MinCons")
                self.LabelDislayCurrentValue2_2.setText(str(self.stockParam.demin[sector, input]))
            if(variable == 1):
                print("Updating MaxCons")
                self.LabelDislayCurrentValue2_2.setText(str(self.stockParam.demax[sector, input]))
            if(variable == 2):
                print("Updating Elasticity")
                self.LabelDislayCurrentValue2_2.setText(str(self.stockParam.delta[sector, input]))

    def updateVariable23(self):
        '''updateVariable23()
        This methods is automatically called when the user changes the selected value on one of the selection bars in tab 2.3.
        It takes the value corresponding to the new configuration (sector selected + sector of substitution selected + variable selected) and shows it in LabelDislayCurrentValue2_3.
        '''
        print("Updating variable selected for 2.3 ...")
        sector = self.DropDownListSector2_3.currentIndex()
        substitution = self.DropDownListSubstitution.currentIndex()
        variable = self.DropDownListVariable2_3.currentIndex()
        root = tk.Tk()
        root.withdraw()
        if(sector == substitution):
            self.check23 = False
            tkMessageBox.showerror("Error", "Sector and substitution are identical")
            
        else :
            self.check23 = True
            if(variable == 0):
                self.LabelDislayCurrentValue2_3.setText(str(self.stockParam.sigma[sector]))
            if(variable == 1):
                self.LabelDislayCurrentValue2_3.setText(str(self.stockParam.thetaSub[sector]))
            if(variable == 2):
                self.LabelDislayCurrentValue2_3.setText(str(self.stockParam.omega[sector, substitution]))
    
    def updateVariable32(self):
        '''updateVariable32()
        This methods is automatically called when the user changes the selected value on one of the selection bars in tab 2.2.
        It takes the value corresponding to the new configuration (first sector selected + second sector selected + variable selected) and shows it in LabelDislayCurrentValue2_3.
        '''
        print("Updating variable selected for 3.2 ...")
        sector = self.DropDownListSector3_2.currentIndex()
        input = self.DropDownListInput3_2.currentIndex()
        variable = self.DropDownListVariable3_2.currentIndex()
        self.LabelDislayCurrentValue3_2.setText(str(self.stockParam.bkn[sector][input]))
    
    def launch21(self):
        '''launch21()
        This methods launches the TRANUS calculation for the selected input in tab 2.1.
        It only works if there are correct values selected for the input fields.
        For each iteration (based on the number of iterations, min and max selected by the user),
        it modifies the L1E file, launches imploc, puts the created files in a new directory.
        The L1E file is restored to its original state at the end of the process.
        '''
        root = tk.Tk()
        root.withdraw()
        if(self.MinValue2_1.value() > self.MaxValue2_1.value()):
            tkMessageBox.showerror("Error 2.1", "Minimal value is greater than maximal value")
        else :
            print("Beginning of execution for section 2.1 ...")
            '''We re-initialize the drop down lists used for the selection of which graph to plot.'''
            self.DropDownListDisplaySector2_1.clear()
            self.DropDownListDisplayIter2_1.clear()
            for n in range(len(self.stockParam.list_sectors)):
                self.DropDownListDisplaySector2_1.addItem(self.stockParam.list_names_sectors[n])
            
            sector = self.DropDownListSector2_1.currentIndex()
            variable = self.DropDownListVariable2_1.currentIndex()
            nbIterations = self.NbIterations2_1.value()
            self.selectedVar2_1 = self.DropDownListVariable2_1.currentIndex()
            self.selectedVar2_1Text = self.DropDownListVariable2_1.currentText()
            '''Save of current value in order to restore the L1E file at the end of the method'''
            if(variable == 0):
                self.savedOldValue = (self.stockParam.beta[sector])
            if(variable == 1):
                self.savedOldValue = (self.stockParam.list_utility_lvl2[sector])
            if(variable == 2):
                self.savedOldValue =(self.stockParam.lamda[sector])
            if(variable == 3):
                self.savedOldValue = (self.stockParam.list_price_lvl2[sector])
            if(variable == 4):
                self.savedOldValue = (self.stockParam.thetaLoc[sector])
            if(variable == 5):
                self.savedOldValue = (self.stockParam.alfa[sector])
            if(variable == 6):
                self.savedOldValue = (self.stockParam.list_price_cost_ratio[sector])
            if(variable == 7):
                self.savedOldValue = (self.stockParam.list_sector_type[sector])
            
            min = self.MinValue2_1.value()
            max = self.MaxValue2_1.value()
            
            self.initialNbIterations = self.stockParam.nbIterations
            self.initialConvergenceFactor = self.stockParam.convergenceFactor
            self.initialSmoothingFactor = self.stockParam.smoothingFactor
            self.stockParam.nbIterations = self.NbIterLcal2_1.value()
            self.stockParam.convergenceFactor = 10**(-self.ConvFactor2_1.value())
            self.stockParam.smoothingFactor = self.SmoothingFactor2_1.value()
            
            for i in range(nbIterations):  
                #Calcul of value for this iteration
                if(nbIterations == 1):
                    currentValue = min
                else :
                    currentValue = min + ((max-min)/(nbIterations-1))*i
                #We need to round up the current value, because if there are too many decimals there will be collision in the L1E file.
                currentValue = round(currentValue, 6)
                print(currentValue)
                self.DropDownListDisplayIter2_1.addItem(str(currentValue))
                '''
                Depending on which variable is selected, the appropriate value in the LCALparam object is modified, and what will be used for 
                the base of the new directory's name is selected.
                '''
                if(variable == 0):
                    self.stockParam.beta[sector] = currentValue
                    name = "utility_lvl1_"
                if(variable == 1):
                    self.stockParam.list_utility_lvl2[sector] = currentValue
                    name = "utility_lvl2_"
                if(variable == 2):
                    self.stockParam.lamda[sector] = currentValue
                    name = "price_lvl1_"
                if(variable == 3):
                    self.stockParam.list_price_lvl2[sector] = currentValue
                    name = "price_lvl2_"
                if(variable == 4):
                    self.stockParam.thetaLoc[sector] = currentValue
                    name = "logit_scale_"
                if(variable == 5):
                    self.stockParam.alfa[sector] = currentValue
                    name = "atrac_factor_"
                if(variable == 6):
                    self.stockParam.list_price_cost_ratio[sector] = currentValue
                    name = "price_cost_ratio_"
                if(variable == 7):
                    self.stockParam.list_sector_type[sector] = currentValue
                    name = "sector_type_"
                '''Execution of TRANUS with this iteration's LCALparam'''
                self.nameDirectory2_1 = name
                name = name + str(i)
                self.stockParam.write_L1E(self.stockTranusConfig)
                pathScenarioResultDirectory = os.path.join(self.stockTranusConfig.workingDirectory, name)
                print pathScenarioResultDirectory
                if not os.path.exists(pathScenarioResultDirectory):
                    os.makedirs(pathScenarioResultDirectory)
                interface = LcalInterface(self.stockTranusConfig,pathScenarioResultDirectory)
                interface.runLcal(True)
                interface.runImplocVariation("J")
            
            '''Restoration of old value'''
            if(variable == 0):
                self.stockParam.beta[sector] = self.savedOldValue
            if(variable == 1):
                self.stockParam.list_utility_lvl2[sector] = self.savedOldValue
            if(variable == 2):
                self.stockParam.lamda[sector] = self.savedOldValue
            if(variable == 3):
                self.stockParam.list_price_lvl2[sector] = self.savedOldValue
            if(variable == 4):
                self.stockParam.thetaLoc[sector] = self.savedOldValue
            if(variable == 5):
                self.stockParam.alfa[sector] = self.savedOldValue
            if(variable == 6):
                self.stockParam.list_price_cost_ratio[sector] = self.savedOldValue
            if(variable == 7):
                self.stockParam.list_sector_type[sector] = self.savedOldValue
            
            '''Restoration of the initial configuration of the L1E file (number of iterations, convergence factor, smoothing factor)'''
            self.stockParam.nbIterations = self.initialNbIterations
            self.stockParam.convergenceFactor = self.initialConvergenceFactor
            self.stockParam.smoothingFactor = self.initialSmoothingFactor
            '''Restoration of the L1E file'''
            self.stockParam.write_L1E(self.stockTranusConfig)
            self.labelVariable2_1.setText(self.selectedVar2_1Text)
            self.generate2_1 = True
    
    def launch22(self):
        '''launch22()
        This methods launches the TRANUS calculation for the selected input in tab 2.2.
        It only works if there are correct values selected for the input fields.
        For each iteration (based on the number of iterations, min and max selected by the user),
        it modifies the L1E file, launches imploc, puts the created files in a new directory.
        The L1E file is restored to its original state at the end of the process.
        '''
        if(not self.check22) :
            root = tk.Tk()
            root.withdraw()
            tkMessageBox.showerror("Error 2.2", "Incorrect values selected")
        else :
            print("Beginning of execution for section 2.2 ...")
            '''We re-initialize the drop down lists used for the selection of which graph to plot.'''
            self.DropDownListDisplaySector2_2.clear()
            self.DropDownListDisplayIter2_2.clear()
            for n in range(len(self.stockParam.list_sectors)):
                self.DropDownListDisplaySector2_2.addItem(self.stockParam.list_names_sectors[n])
            sector = self.DropDownListSector_22.currentIndex()
            input = self.DropDownListInput2_2.currentIndex()
            variable = self.DropDownListVariable_22.currentIndex()
            self.selectedVar2_2 = self.DropDownListVariable_22.currentIndex()
            nbIterations = self.NbIterations_22.value()
            min = self.MinValue_22.value()
            max = self.MaxValue_22.value()
            self.selectedVar2_2Text = self.DropDownListVariable_22.currentText()
            #Save of current value
            if(variable == 0):
                self.savedOldValue = (self.stockParam.demin[sector][input])
            if(variable == 1):
                self.savedOldValue = (self.stockParam.demax[sector][input])
            if(variable == 2):
                self.savedOldValue = (self.stockParam.delta[sector, input])
            
            self.initialNbIterations = self.stockParam.nbIterations
            self.initialConvergenceFactor = self.stockParam.convergenceFactor
            self.initialSmoothingFactor = self.stockParam.smoothingFactor
            self.stockParam.nbIterations = self.NbIterLcal2_2.value()
            self.stockParam.convergenceFactor = 10**(-self.ConvFactor2_2.value())
            self.stockParam.smoothingFactor = self.SmoothingFactor2_2.value()
            
            for i in range(nbIterations):  
                #Calcul of value for this iteration
                if(nbIterations == 1):
                    currentValue = min
                else :
                    currentValue = min + ((max-min)/(nbIterations-1))*i
                #We need to round up the current value, because if there are too many decimals there will be collision in the L1E file.
                currentValue = round(currentValue, 6)
                print(currentValue)
                self.DropDownListDisplayIter2_2.addItem(str(currentValue))
                '''
                Depending on which variable is selected, the appropriate value in the LCALparam object is modified, and what will be used for 
                the base of the new directory's name is selected.
                '''
                if(variable == 0):
                    self.stockParam.demin[sector][input] = currentValue
                    name = "minCons_"
                if(variable == 1):
                    self.stockParam.demax[sector][input] = currentValue
                    name = "maxCons_"
                if(variable == 2):
                    self.stockParam.delta[sector][input] = currentValue
                    name = "elasticity_"
                '''Execution of TRANUS with this iteration's LCALparam'''
                self.nameDirectory2_2 = name
                name = name + str(i)
                self.stockParam.write_L1E(self.stockTranusConfig)
                pathScenarioResultDirectory = os.path.join(self.stockTranusConfig.workingDirectory, name)
                print pathScenarioResultDirectory
                if not os.path.exists(pathScenarioResultDirectory):
                    os.makedirs(pathScenarioResultDirectory)
                interface = LcalInterface(self.stockTranusConfig,pathScenarioResultDirectory)
                interface.runLcal(True)
                interface.runImplocVariation("J")
            
            '''Restoration of old value'''
            if(variable == 0):
                self.stockParam.demin[sector][input] = self.savedOldValue
            if(variable == 1):
                self.stockParam.demax[sector][input] = self.savedOldValue
            if(variable == 2):
                self.stockParam.delta[sector][input] = self.savedOldValue
            
            '''Restoration of the initial configuration of the L1E file (number of iterations, convergence factor, smoothing factor)'''
            self.stockParam.nbIterations = self.initialNbIterations
            self.stockParam.convergenceFactor = self.initialConvergenceFactor
            self.stockParam.smoothingFactor = self.initialSmoothingFactor
            '''Restoration of the L1E file'''
            self.stockParam.write_L1E(self.stockTranusConfig)
            self.labelVariable2_2.setText(self.selectedVar2_2Text)
            self.generate2_2 = True
        
    def launch23(self):
        '''launch23()
        This methods launches the TRANUS calculation for the selected input in tab 2.3.
        It only works if there are correct values selected for the input fields.
        For each iteration (based on the number of iterations, min and max selected by the user),
        it modifies the L1E file, launches imploc, puts the created files in a new directory.
        The L1E file is restored to its original state at the end of the process.
        '''
        if(not self.check23) :
            root = tk.Tk()
            root.withdraw()
            tkMessageBox.showerror("Error 2.3", "Incorrect values selected")
        else :
            print("Beginning of execution for section 2.3") 
            '''We re-initialize the drop down lists used for the selection of which graph to plot.'''
            self.DropDownListDisplaySector2_3.clear()
            self.DropDownListDisplayIter2_3.clear()
            for n in range(len(self.stockParam.list_sectors)):
                self.DropDownListDisplaySector2_3.addItem(self.stockParam.list_names_sectors[n])
            sector = self.DropDownListSector2_3.currentIndex()
            input = self.DropDownListSubstitution.currentIndex()
            variable = self.DropDownListVariable2_3.currentIndex()
            self.selectedVar2_3 = self.DropDownListVariable2_3.currentIndex()
            nbIterations = self.NbIterations2_3.value()
            min = self.MinValue2_3.value()
            max = self.MaxValue2_3.value()
            self.selectedVar2_3Text = self.DropDownListVariable2_3.currentText()
            #Save of current value
            if(variable == 0):
                self.savedOldValue = (self.stockParam.sigma[sector])
            if(variable == 1):
                self.savedOldValue = (self.stockParam.thetaSub[sector])
            if(variable == 2):
                self.savedOldValue = (self.stockParam.omega[sector, input])
            
            self.initialNbIterations = self.stockParam.nbIterations
            self.initialConvergenceFactor = self.stockParam.convergenceFactor
            self.initialSmoothingFactor = self.stockParam.smoothingFactor
            self.stockParam.nbIterations = self.NbIterLcal2_3.value()
            self.stockParam.convergenceFactor = 10**(-self.ConvFactor2_3.value())
            self.stockParam.smoothingFactor = self.SmoothingFactor2_3.value()
            
            for i in range(nbIterations):  
                #Calcul of value for this iteration
                if(nbIterations == 1):
                    currentValue = min
                else :
                    currentValue = min + ((max-min)/(nbIterations-1))*i
                #We need to round up the current value, because if there are too many decimals there will be collision in the L1E file.
                currentValue = round(currentValue, 6)
                print(currentValue)
                self.DropDownListDisplayIter2_3.addItem(str(currentValue))
                '''
                Depending on which variable is selected, the appropriate value in the LCALparam object is modified, and what will be used for 
                the base of the new directory's name is selected.
                '''
                if(variable == 0):
                    self.stockParam.sigma[sector] = currentValue
                    name = "sustElast_"
                if(variable == 1):
                    self.stockParam.thetaSub[sector] = currentValue
                    name = "logitSc_"
                if(variable == 2):
                    self.stockParam.omega[sector, input] = currentValue
                    name = "penal_"
                    
                '''Execution of TRANUS with this iteration's LCALparam'''
                self.nameDirectory2_3 = name
                name = name + str(i)
                self.stockParam.write_L1E(self.stockTranusConfig)
                pathScenarioResultDirectory = os.path.join(self.stockTranusConfig.workingDirectory, name)
                print pathScenarioResultDirectory
                if not os.path.exists(pathScenarioResultDirectory):
                    os.makedirs(pathScenarioResultDirectory)
                interface = LcalInterface(self.stockTranusConfig,pathScenarioResultDirectory)
                interface.runLcal(True)
                interface.runImplocVariation("J")     
            
            '''Restoration of old value'''
            if(variable == 0):
                self.stockParam.sigma[sector] = self.savedOldValue
            if(variable == 1):
                self.stockParam.thetaSub[sector] = self.savedOldValue
            if(variable == 2):
                self.stockParam.omega[sector, input] = self.savedOldValue
            
            '''Restoration of the initial configuration of the L1E file (number of iterations, convergence factor, smoothing factor)'''
            self.stockParam.nbIterations = self.initialNbIterations
            self.stockParam.convergenceFactor = self.initialConvergenceFactor
            self.stockParam.smoothingFactor = self.initialSmoothingFactor
            
            '''Restoration of the L1E file'''
            self.stockParam.write_L1E(self.stockTranusConfig)
            self.labelVariable2_3.setText(self.selectedVar2_3Text)
            self.generate2_3 = True
            
    def launch32(self):
        '''launch32()
        This methods launches the TRANUS calculation for the selected input in tab 3.2.
        For each iteration (based on the number of iterations, min and max selected by the user),
        it modifies the L1E file, launches imploc, puts the created files in a new directory.
        The L1E file is restored to its original state at the end of the process.
        '''
        print("Beginning of execution for section 3.2 ...")
        '''We re-initialize the drop down lists used for the selection of which graph to plot.'''
        self.DropDownListDisplaySector3_2.clear()
        self.DropDownListDisplayIter3_2.clear()
        for n in range(len(self.stockParam.list_sectors)):
                self.DropDownListDisplaySector3_2.addItem(self.stockParam.list_names_sectors[n])
        sector = self.DropDownListSector3_2.currentIndex()
        input = self.DropDownListInput3_2.currentIndex()
        variable = self.DropDownListVariable3_2.currentIndex()
        self.selectedVar3_2 = self.DropDownListVariable3_2.currentIndex()
        nbIterations = self.NbIterations3_2.value()
        min = self.MinValue3_2.value()
        max = self.MaxValue3_2.value()
        '''Save of current value in order to restore the L1E file at the end of the method'''
        #For now, there is only one variable possible : Level 1
        self.savedOldValue = (self.stockParam.bkn[sector, input])
        self.selectedVar3_2Text = self.DropDownListVariable3_2.currentText()
        
        self.initialNbIterations = self.stockParam.nbIterations
        self.initialConvergenceFactor = self.stockParam.convergenceFactor
        self.initialSmoothingFactor = self.stockParam.smoothingFactor
        self.stockParam.nbIterations = self.NbIterLcal3_2.value()
        self.stockParam.convergenceFactor = 10**(-self.ConvFactor3_2.value())
        self.stockParam.smoothingFactor = self.SmoothingFactor3_2.value()
        
        for i in range(nbIterations):  
                #Calcul of value for this iteration
                if(nbIterations == 1):
                    currentValue = min
                else :
                    currentValue = min + ((max-min)/(nbIterations-1))*i
                #We need to round up the current value, because if there are too many decimals there will be collision in the L1E file.
                currentValue = round(currentValue, 6)
                print(currentValue)
                self.DropDownListDisplayIter3_2.addItem(str(currentValue))
                self.stockParam.bkn[sector,input] = currentValue
                name = "lvl1_"
                '''Execution of TRANUS with this iteration's LCALparam'''
                self.nameDirectory3_2 = name
                name = name + str(i)
                self.stockParam.write_L1E(self.stockTranusConfig)
                pathScenarioResultDirectory = os.path.join(self.stockTranusConfig.workingDirectory, name)
                print pathScenarioResultDirectory
                if not os.path.exists(pathScenarioResultDirectory):
                    os.makedirs(pathScenarioResultDirectory)
                interface = LcalInterface(self.stockTranusConfig,pathScenarioResultDirectory)
                interface.runLcal(True)
                interface.runImplocVariation("J")     
        
        '''Restoration of the initial configuration of the L1E file (number of iterations, convergence factor, smoothing factor)'''
        self.stockParam.nbIterations = self.initialNbIterations
        self.stockParam.convergenceFactor = self.initialConvergenceFactor
        self.stockParam.smoothingFactor = self.initialSmoothingFactor
        '''Restoration of the L1E file'''
        self.stockParam.bkn[sector, input] = self.savedOldValue
        self.stockParam.write_L1E(self.stockTranusConfig)
        self.labelVariable3_2.setText(self.selectedVar3_2Text)
        self.generate3_2 = True
    
    def on_closing(self):
        '''on_closing()
        This method is called when the tkMessageBox generated by the display methods are closed, and puts the local boolean windowAvailable to True.
        The boolean windowAvailable, acting as a lock through this method and the check at the beginning of each display method below, is necessary 
        to prevent the apparition of more than one window from a displayResults function at the same time.
        This is required because trying to display more than one causes the program to freeze.
        '''
        self.windowAvailable = True
        
    
    #This function is used to display the mean and variance of each iteration for the currently selected sector
    def displayResults2_1(self):
        '''displayResults2_1()
            This method displays the average and variance of the prices in the zones of the model for each iteration
            in a tkMessageBox. Each line on the tkMessageBox contains one value, with the rest of the line explaining what it is.
            It only works if there has already been an use of launch21(), and there can only be one tkMessageBox
            displayed at the same time (between all displayResults methods).
        '''
        #Check if there has been an execution of TRANUS with the 2.1 tab
        if(self.generate2_1):
            #Check if there is no other window open
            if(self.windowAvailable):
                #Prevent other windows from being opened
                self.windowAvailable = False
                root = tk.Tk()
                root.withdraw()
                sector = self.DropDownListDisplaySector2_1.currentIndex()
                nbIter = self.DropDownListDisplayIter2_1.count()
                stringTitle = "Results for {0}".format(self.stockParam.list_names_sectors[sector])
                #Initialization of the contents of the message box.
                stringData = ""
                #For each iteration, two lines are added to the text : the mean and the variance
                for i in range(nbIter):
                    #Access to the imploc file for the current iteration
                    nameDirectory = self.nameDirectory2_1 + str(i)
                    pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
                    filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
                    #Conversion of file into pandas matrix
                    matrix = pd.read_csv(filepath)
                    matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
                    #Removal of the noise (production equal to zero => adjust equal to zero)
                    matrix.Adjust[matrix.TotProd == 0] = 0
                    matrix.Adjust[matrix.Price == 0] = 0
                    #Change of null price to None, to avoid anomalies perturbing the result
                    matrix.Price[matrix.Price == 0] = None
                    matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
                    #Isolation of the data for the sector selected
                    nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
                    matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
                    matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
                    y = matrix4["Price"].convert_objects(convert_numeric=True)
                    #Calcul of mean and variance and addition to stringData
                    average ="Mean for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_1.itemText(i), y.mean(0))
                    stringData = stringData + average
                    variance = "Variance for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_1.itemText(i), y.var(0))
                    stringData = stringData + variance

                tkMessageBox.showinfo(stringTitle, stringData)
                root.protocol("WM_DELETE_WINDOW", self.on_closing())
               
    def displayResults2_2(self):
        '''displayResults2_2()
            This method displays the average and variance of the prices in the zones of the model for each iteration
            in a tkMessageBox.
            It only works if there has already been an use of launch22(), and there can only be one tkMessageBox
            displayed at the same time (between all displayResults methods).
        '''
        #Check if there has been an execution of TRANUS with the 2.1 tab
        if(self.generate2_2):
            #Check if there is no other window open
            if(self.windowAvailable):
                #Prevent other windows from being opened
                self.windowAvailable = False
                root = tk.Tk()
                root.withdraw()
                sector = self.DropDownListDisplaySector2_2.currentIndex()
                nbIter = self.DropDownListDisplayIter2_2.count()
                stringTitle = "Results for {0}".format(self.stockParam.list_names_sectors[sector])
                #Initialization of the contents of the message box.
                stringData = ""
                #For each iteration, two lines are added to the text : the mean and the variance
                for i in range(nbIter):
                    #Access to the imploc file for the current iteration
                    nameDirectory = self.nameDirectory2_2 + str(i)
                    pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
                    filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
                    #Conversion of file into pandas matrix
                    matrix = pd.read_csv(filepath)
                    matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
                    #Removal of the noise (production equal to zero => adjust equal to zero)
                    matrix.Adjust[matrix.TotProd == 0] = 0
                    matrix.Adjust[matrix.Price == 0] = 0
                    #Change of null price to None, to avoid anomalies perturbing the result
                    matrix.Price[matrix.Price == 0] = None
                    matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
                    #Isolation of the data for the sector selected
                    nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
                    matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
                    matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
                    y = matrix4["Price"].convert_objects(convert_numeric=True)
                    #Calcul of mean and variance and addition to stringData
                    average ="Mean for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_2.itemText(i), y.mean(0))
                    stringData = stringData + average
                    variance = "Variance for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_2.itemText(i), y.var(0))
                    stringData = stringData + variance

                tkMessageBox.showinfo(stringTitle, stringData)
                root.protocol("WM_DELETE_WINDOW", self.on_closing())
                
    def displayResults2_3(self):
        '''displayResults2_3()
            This method displays the average and variance of the prices in the zones of the model for each iteration
            in a tkMessageBox.
            It only works if there has already been an use of launch23(), and there can only be one tkMessageBox
            displayed at the same time (between all displayResults methods).
        '''
        if(self.generate2_3):
            #Check if there is no other window open
            if(self.windowAvailable):
                #Prevent other windows from being opened
                self.windowAvailable = False
                root = tk.Tk()
                root.withdraw()
                sector = self.DropDownListDisplaySector2_3.currentIndex()
                nbIter = self.DropDownListDisplayIter2_3.count()
                stringTitle = "Results for {0}".format(self.stockParam.list_names_sectors[sector])
                #Initialization of the contents of the message box.
                stringData = ""
                #For each iteration, two lines are added to the text : the mean and the variance
                for i in range(nbIter):
                    #Access to the imploc file for the current iteration
                    nameDirectory = self.nameDirectory2_3 + str(i)
                    pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
                    filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
                    #Conversion of file into pandas matrix
                    matrix = pd.read_csv(filepath)
                    matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
                    #Removal of the noise (production equal to zero => adjust equal to zero)
                    matrix.Adjust[matrix.TotProd == 0] = 0
                    matrix.Adjust[matrix.Price == 0] = 0
                    #Change of null price to None, to avoid anomalies perturbing the result
                    matrix.Price[matrix.Price == 0] = None
                    matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
                    #Isolation of the data for the sector selected
                    nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
                    matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
                    matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
                    y = matrix4["Price"].convert_objects(convert_numeric=True)
                    #Calcul of mean and variance and addition to stringData
                    average ="Mean for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_3.itemText(i), y.mean(0))
                    stringData = stringData + average
                    variance = "Variance for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter2_3.itemText(i), y.var(0))
                    stringData = stringData + variance

                tkMessageBox.showinfo(stringTitle, stringData)
                root.protocol("WM_DELETE_WINDOW", self.on_closing())
                
    def displayResults3_2(self):
        '''displayResults3_2()
            This method displays the average and variance of the prices in the zones of the model for each iteration
            in a tkMessageBox.
            It only works if there has already been an use of launch32(), and there can only be one tkMessageBox
            displayed at the same time (between all displayResults methods).
        '''
        if(self.generate3_2):
            #Check if there is no other window open
            if(self.windowAvailable):
                #Prevent other windows from being opened
                self.windowAvailable = False
                root = tk.Tk()
                root.withdraw()
                sector = self.DropDownListDisplaySector3_2.currentIndex()
                nbIter = self.DropDownListDisplayIter3_2.count()
                stringTitle = "Results for {0}".format(self.stockParam.list_names_sectors[sector])
                #Initialization of the contents of the message box.
                stringData = ""
                #For each iteration, two lines are added to the text : the mean and the variance
                for i in range(nbIter):
                    #Access to the imploc file for the current iteration
                    nameDirectory = self.nameDirectory3_2 + str(i)
                    pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
                    filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
                    #Conversion of file into pandas matrix
                    matrix = pd.read_csv(filepath)
                    matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
                    #Removal of the noise (production equal to zero => adjust equal to zero)
                    matrix.Adjust[matrix.TotProd == 0] = 0
                    matrix.Adjust[matrix.Price == 0] = 0
                    #Change of null price to None, to avoid anomalies perturbing the result
                    matrix.Price[matrix.Price == 0] = None
                    matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
                    #Isolation of the data for the sector selected
                    nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
                    matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
                    matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
                    y = matrix4["Price"].convert_objects(convert_numeric=True)
                    #Calcul of mean and variance and addition to stringData
                    average ="Mean for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter3_2.itemText(i), y.mean(0))
                    stringData = stringData + average
                    variance = "Variance for iteration {0} = {1}\n" .format(self.DropDownListDisplayIter3_2.itemText(i), y.var(0))
                    stringData = stringData + variance

                tkMessageBox.showinfo(stringTitle, stringData)
                root.protocol("WM_DELETE_WINDOW", self.on_closing())
        
    def plot21(self):
        '''plot21()
        This methods uses matplotlib.pyplot to draw a graph corresponding to the data selected by the user in the tab 2.1.
        It displays the price for each zone in the selected sector, then the shadow price for the selected iteration on the same graph.
        If there are sections of the graph that appear to be missing, it's because the price for these zones is equa to zero, and has
        been removed to facilitate comprehension.
        '''
        if(self.generate2_1):
            print("Beginning plot for section 2.1 ...")
            #Get the selected iteration and sector
            iter = self.DropDownListDisplayIter2_1.currentIndex()
            sector = self.DropDownListDisplaySector2_1.currentIndex()
            #Access the corresponding IMPLOC file and extract the data for the selected sector
            nameDirectory = self.nameDirectory2_1 + str(iter)
            pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
            filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
            matrix = pd.read_csv(filepath)
            matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
            #Removal of the noise (production equal to zero => adjust equal to zero)
            matrix.Adjust[matrix.TotProd == 0] = 0
            matrix.Adjust[matrix.Price == 0] = 0
            matrix.Price[matrix.Price == 0] = None
            matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
            #Isolation of the data for the sector selected
            nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
            matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
            matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
            #This boolean is used to allow for multiple graphes to be shown on the same panel.
            firstPlot = False
            #Plot graph and display it
            if(self.DropDownListDisplaySector2_1.currentIndex() != self.currentSectorPlot2_1):
                self.numFiguresPlot2_1 = self.numFiguresPlot2_1 + 1
                self.currentSectorPlot2_1 = self.DropDownListDisplaySector2_1.currentIndex()
                firstPlot = True
            fig = plt.figure(self.numFiguresPlot2_1)
            
            fig.canvas.set_window_title(self.DropDownListDisplaySector2_1.currentText())
            x = np.arange(0, self.stockParam.nZones, 1);
            y = matrix4["Price"].convert_objects(convert_numeric=True)
            print("Moyenne = ")
            print(y.mean(0))
            z = (matrix4["Adjust"].convert_objects(convert_numeric=True)*y)/100 + y
            if(firstPlot):
                price = plt.plot(x, y, label = ("Price"))
            shadowPrice = plt.plot(x, z, label = ("Price + adjust for iteration "+self.DropDownListDisplayIter2_1.currentText()))
            plt.legend()
            plt.draw()
            plt.show()
        
    def plot22(self):
        '''plot22()
        This methods uses matplotlib.pyplot to draw a graph corresponding to the data selected by the user in the tab 2.2.
        It displays the price for each zone in the selected sector, then the shadow price for the selected iteration on the same graph.
        If there are sections of the graph that appear to be missing, it's because the price for these zones is equa to zero, and has
        been removed to facilitate comprehension.
        '''
        if(self.generate2_2):
            print("Beginning plot for section 2.2 ...")
            #Get the selected iteration and sector
            iter = self.DropDownListDisplayIter2_2.currentIndex()
            sector = self.DropDownListDisplaySector2_2.currentIndex()
            #Access the corresponding IMPLOC file and extract the data for the selected sector
            nameDirectory = self.nameDirectory2_2 + str(iter)
            pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
            filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
            matrix = pd.read_csv(filepath)
            matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
            #Removal of the noise (production equal to zero => adjust equal to zero)
            matrix.Adjust[matrix.TotProd == 0] = 0
            matrix.Adjust[matrix.Price == 0] = 0
            matrix.Price[matrix.Price == 0] = None
            matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
            nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
            matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
            matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
            firstPlot = False
            #Plot graph and display it
            if(self.DropDownListDisplaySector2_2.currentIndex() != self.currentSectorPlot2_2):
                self.numFiguresPlot2_2 = self.numFiguresPlot2_2 + 1
                self.currentSectorPlot2_2 = self.DropDownListDisplaySector2_2.currentIndex()
                firstPlot = True
            fig = plt.figure(self.numFiguresPlot2_2)
            
            fig.canvas.set_window_title(self.DropDownListDisplaySector2_2.currentText())
            x = np.arange(0, self.stockParam.nZones, 1);
            y = matrix4["Price"].convert_objects(convert_numeric=True)
            z = (matrix4["Adjust"].convert_objects(convert_numeric=True)*y)/100 + y
            if(firstPlot):
                price = plt.plot(x, y, label = ("Price"))
            shadowPrice = plt.plot(x, z, label = ("Price + adjust for iteration "+self.DropDownListDisplayIter2_2.currentText()))
            plt.legend()
            plt.draw()
            plt.show()
    
    def plot23(self):
        '''plot23()
        This methods uses matplotlib.pyplot to draw a graph corresponding to the data selected by the user in the tab 2.3.
        It displays the price for each zone in the selected sector, then the shadow price for the selected iteration on the same graph.
        If there are sections of the graph that appear to be missing, it's because the price for these zones is equa to zero, and has
        been removed to facilitate comprehension.
        '''
        if(self.generate2_3):
            print("Beginning plot for section 2.3 ...")
            #Get the selected iteration and sector
            iter = self.DropDownListDisplayIter2_3.currentIndex()
            sector = self.DropDownListDisplaySector2_3.currentIndex()
            #Access the corresponding IMPLOC file and extract the data for the selected sector
            nameDirectory = self.nameDirectory2_3 + str(iter)
            pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
            filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
            matrix = pd.read_csv(filepath)
            matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
            #Removal of the noise (production equal to zero => adjust equal to zero)
            matrix.Adjust[matrix.TotProd == 0] = 0
            matrix.Adjust[matrix.Price == 0] = 0
            matrix.Price[matrix.Price == 0] = None
            matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
            nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
            matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
            matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
            firstPlot = False
            #Plot graph and display it
            if(self.DropDownListDisplaySector2_3.currentIndex() != self.currentSectorPlot2_3):
                self.numFiguresPlot2_3 = self.numFiguresPlot2_3 + 1
                self.currentSectorPlot2_3 = self.DropDownListDisplaySector2_3.currentIndex()
                firstPlot = True
            fig = plt.figure(self.numFiguresPlot2_3)
            
            fig.canvas.set_window_title(self.DropDownListDisplaySector2_3.currentText())
            x = np.arange(0, self.stockParam.nZones, 1);
            y = matrix4["Price"].convert_objects(convert_numeric=True)
            z = (matrix4["Adjust"].convert_objects(convert_numeric=True)*y)/100 + y
            if(firstPlot):
                price = plt.plot(x, y, label = ("Price"))
            shadowPrice = plt.plot(x, z, label = ("Price + adjust for iteration "+self.DropDownListDisplayIter2_3.currentText()))
            plt.legend()
            plt.draw()
            plt.show()
    
    def plot32(self):
        '''plot32()
        This methods uses matplotlib.pyplot to draw a graph corresponding to the data selected by the user in the tab 3.2.
        It displays the price for each zone in the selected sector, then the shadow price for the selected iteration on the same graph.
        If there are sections of the graph that appear to be missing, it's because the price for these zones is equa to zero, and has
        been removed to facilitate comprehension.
        '''
        if(self.generate3_2):
            print("Beginning plot for section 3.2 ...")
            #Get the selected iteration and sector
            iter = self.DropDownListDisplayIter3_2.currentIndex()
            sector = self.DropDownListDisplaySector3_2.currentIndex()
            #Access the corresponding IMPLOC file and extract the data for the selected sector
            nameDirectory = self.nameDirectory3_2 + str(iter)
            pathToDirectory = os.path.join(self.stockTranusConfig.workingDirectory, nameDirectory)
            filepath = os.path.join(pathToDirectory, "IMPLOC_J.MTX")
            matrix = pd.read_csv(filepath)
            matrix.columns = ["Scen", "Sector", "Zone", "TotProd", "TotDem", "ProdCost", "Price", "MinRes", "MaxRes", "Adjust"]
            #Removal of the noise (production equal to zero => adjust equal to zero)
            matrix.Adjust[matrix.TotProd == 0] = 0
            matrix.Adjust[matrix.Price == 0] = 0
            matrix.Price[matrix.Price == 0] = None
            matrix2 = matrix[["Sector","Zone", "Price", "Adjust"]]
            nameSector = str(self.stockParam.list_sectors[sector])+" "+(self.stockParam.list_names_sectors[sector])
            matrix3 = matrix2[matrix2["Sector"].str.contains(nameSector) == True]
            matrix4 = matrix3[matrix3["Zone"].str.contains("ext_") == False]
            firstPlot = False
            #Plot graph and display it
            if(self.DropDownListDisplaySector3_2.currentIndex() != self.currentSectorPlot3_2):
                self.numFiguresPlot3_2 = self.numFiguresPlot3_2 + 1
                self.currentSectorPlot3_2 = self.DropDownListDisplaySector3_2.currentIndex()
                firstPlot = True
            fig = plt.figure(self.numFiguresPlot3_2)

            fig.canvas.set_window_title(self.DropDownListDisplaySector3_2.currentText())
            x = np.arange(0, self.stockParam.nZones, 1);
            y = matrix4["Price"].convert_objects(convert_numeric=True)
            z = matrix4["Adjust"].convert_objects(convert_numeric=True)*y/100 + y
            if(firstPlot):
                price = plt.plot(x, y, label = ("Price for iteration "+self.DropDownListDisplayIter3_2.currentText()))
            shadowPrice = plt.plot(x, z, label = ("Price"))
            plt.legend()
            plt.draw()
            plt.show()
    
    def main(self):
		self.show()
        
 
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    interfaceVariation = InterfaceVariationTRANUS("config")
    interfaceVariation.main()
    app.exec_()