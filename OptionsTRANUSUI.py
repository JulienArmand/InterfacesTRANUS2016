# -*- coding: utf-8 -*-

# Author : Julien Armand
# Created by: PyQt4 UI code generator 4.11.4, heavily modified afterward
#

from PyQt4 import QtCore, QtGui
import extractionScenarios
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralWidget = QtGui.QWidget(MainWindow)
        layout = QtGui.QVBoxLayout(self.centralWidget)
        self.scrollArea = QtGui.QScrollArea(self.centralWidget)
        layout.addWidget(self.scrollArea)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1000, 1400))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout = QtGui.QHBoxLayout(self.scrollAreaWidgetContents)  
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)     
        #Zone for the buttons run TRANUS
        self.label_1 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_1.setEnabled(True)
        self.label_1.setGeometry(QtCore.QRect(0,0,360,100))
        self.label_1.setFont(font)
        self.label_1.setObjectName(_fromUtf8("label_1")) 
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QtCore.QRect(0,0,360,120))
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(0,0,360,140))
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))     
        self.line_2 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(-10, 100, 10000, 16))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_4"))
        #Imploc section
        self.positionYImploc = 100
        self.label_6 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setEnabled(True)
        self.label_6.setGeometry(QtCore.QRect(10, self.positionYImploc+10, 41, 21))
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_21 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_21.setGeometry(QtCore.QRect(50, self.positionYImploc+30, 46, 13))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_22 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_22.setGeometry(QtCore.QRect(60, self.positionYImploc+50, 171, 16))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_23.setGeometry(QtCore.QRect(60, self.positionYImploc+70, 171, 16))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_24.setGeometry(QtCore.QRect(60, self.positionYImploc+90, 171, 16))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.label_25 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_25.setGeometry(QtCore.QRect(60, self.positionYImploc+110, 171, 16))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.label_26 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_26.setGeometry(QtCore.QRect(60, self.positionYImploc+130, 201, 16))
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.label_27 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_27.setGeometry(QtCore.QRect(60, self.positionYImploc+150, 201, 16))
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.label_28 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_28.setGeometry(QtCore.QRect(60, self.positionYImploc+170, 201, 16))
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.line_6 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line_6.setGeometry(QtCore.QRect(0, self.positionYImploc + 190, 10000, 16))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
        #Imptra section
        self.positionYImptra = self.positionYImploc + 190
        self.label_7 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setEnabled(True)
        self.label_7.setGeometry(QtCore.QRect(10, self.positionYImptra+10, 41, 21))
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_29 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_29.setGeometry(QtCore.QRect(60, self.positionYImptra+30, 46, 13))
        self.label_29.setObjectName(_fromUtf8("label_29"))
        self.label_30 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_30.setGeometry(QtCore.QRect(70, self.positionYImptra+50, 91, 16))
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.label_31 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_31.setGeometry(QtCore.QRect(70, self.positionYImptra+70, 161, 16))
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.label_32 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_32.setGeometry(QtCore.QRect(70, self.positionYImptra+90, 181, 16))
        self.label_32.setObjectName(_fromUtf8("label_32"))
        self.label_33 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_33.setGeometry(QtCore.QRect(70, self.positionYImptra+110, 181, 16))
        self.label_33.setObjectName(_fromUtf8("label_33"))
        self.label_34 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_34.setGeometry(QtCore.QRect(70, self.positionYImptra+130, 191, 16))
        self.label_34.setObjectName(_fromUtf8("label_34"))
        self.label_35 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_35.setGeometry(QtCore.QRect(70, self.positionYImptra+150, 191, 16))
        self.label_35.setObjectName(_fromUtf8("label_35"))
        self.label_36 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_36.setGeometry(QtCore.QRect(70, self.positionYImptra+170, 191, 16))
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.label_37 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_37.setGeometry(QtCore.QRect(70, self.positionYImptra+190, 191, 16))
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.label_38 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_38.setGeometry(QtCore.QRect(70, self.positionYImptra+210, 191, 16))
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.label_39 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_39.setGeometry(QtCore.QRect(70, self.positionYImptra+230, 191, 16))
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.line_7 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line_7.setGeometry(QtCore.QRect(-120, self.positionYImptra + 250, 10000, 16))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        #Mats section
        self.positionYMats = self.positionYImptra + 250
        self.label_12 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_12.setEnabled(True)
        self.label_12.setGeometry(QtCore.QRect(10, self.positionYMats+10, 51, 21))
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_58 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_58.setGeometry(QtCore.QRect(90, self.positionYMats+30, 141, 16))
        self.label_58.setObjectName(_fromUtf8("label_58"))
        self.label_59 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_59.setGeometry(QtCore.QRect(90, self.positionYMats+50, 191, 16))
        self.label_59.setObjectName(_fromUtf8("label_59"))
        self.label_60 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_60.setGeometry(QtCore.QRect(90, self.positionYMats+70, 191, 16))
        self.label_60.setObjectName(_fromUtf8("label_60"))
        self.label_61 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_61.setGeometry(QtCore.QRect(90, self.positionYMats+90, 191, 16))
        self.label_61.setObjectName(_fromUtf8("label_61"))
        self.label_62 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_62.setGeometry(QtCore.QRect(90, self.positionYMats+110, 191, 16))
        self.label_62.setObjectName(_fromUtf8("label_62"))
        self.label_63 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_63.setGeometry(QtCore.QRect(90, self.positionYMats+130, 191, 16))
        self.label_63.setObjectName(_fromUtf8("label_63"))
        self.label_64 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_64.setGeometry(QtCore.QRect(90, self.positionYMats+150, 191, 16))
        self.label_64.setObjectName(_fromUtf8("label_64"))
        self.label_65 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_65.setGeometry(QtCore.QRect(90, self.positionYMats+170, 191, 16))
        self.label_65.setObjectName(_fromUtf8("label_65"))
        self.label_66 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_66.setGeometry(QtCore.QRect(90, self.positionYMats+190, 191, 16))
        self.label_66.setObjectName(_fromUtf8("label_66"))
        self.label_67 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_67.setGeometry(QtCore.QRect(90, self.positionYMats+210, 191, 16))
        self.label_67.setObjectName(_fromUtf8("label_67"))
        self.label_68 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_68.setGeometry(QtCore.QRect(90, self.positionYMats+230, 191, 16))
        self.label_68.setObjectName(_fromUtf8("label_68"))
        self.label_69 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_69.setGeometry(QtCore.QRect(90, self.positionYMats+250, 191, 16))
        self.label_69.setObjectName(_fromUtf8("label_69"))
        self.label_70 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_70.setGeometry(QtCore.QRect(90, self.positionYMats+270, 191, 16))
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.label_71 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_71.setGeometry(QtCore.QRect(90, self.positionYMats+290, 191, 16))
        self.label_71.setObjectName(_fromUtf8("label_71"))
        self.line_11 = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line_11.setGeometry(QtCore.QRect(0, self.positionYMats+310, 30000, 16))
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        #Generate Button section   
        self.Generate_Button = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.Generate_Button.setGeometry(QtCore.QRect(80, self.positionYMats + 320, 75, 23))
        self.Generate_Button.setObjectName(_fromUtf8("Generate_Button"))
        #Finalization
        MainWindow.setCentralWidget(self.centralWidget)
        MainWindow.setWindowTitle(_translate("MainWindow", "Options TRANUS", None))
        self.console = QtGui.QTextBrowser(self.scrollAreaWidgetContents)
        self.console.setGeometry(QtCore.QRect(200, self.positionYMats + 350, 500, 150))
        self.console.setObjectName(_fromUtf8("console"))
        self.retranslateUi(MainWindow)
        
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Options TRANUS", None))
        #Label TRANUS run
        self.label_1.setText(_translate("MainWindow", "Use this button to generate the basic files needed for", None))
        self.label_2.setText(_translate("MainWindow", "the other TRANUS operations. This doesn't replace the", None))
        self.label_3.setText(_translate("MainWindow", "need to use the interface TUS on the scenario.", None))
        #Labels imploc
        self.label_6.setText(_translate("MainWindow", "imploc", None))
        self.label_21.setText(_translate("MainWindow", "Run", None))
        self.label_22.setText(_translate("MainWindow", "All information by sector and zone", None))
        self.label_23.setText(_translate("MainWindow", "All information, comma-delimited", None))
        self.label_24.setText(_translate("MainWindow", "Total production by sector and zone", None))
        self.label_25.setText(_translate("MainWindow", "Total production by year/policy", None))
        self.label_26.setText(_translate("MainWindow", "Internal information by sector and zone", None))
        self.label_27.setText(_translate("MainWindow", "Consumption coeficients by sector", None))
        self.label_28.setText(_translate("MainWindow", "Total consumption by sector and zone", None))
        #Labels imptra
        self.label_7.setText(_translate("MainWindow", "imptra", None))
        self.label_29.setText(_translate("MainWindow", "Run", None))
        self.label_30.setText(_translate("MainWindow", " Report all links", None))
        self.label_31.setText(_translate("MainWindow", "Cordons (only with IMPTRA.DAT)", None))
        self.label_32.setText(_translate("MainWindow", "Filter links by Demand/Capacity range", None))
        self.label_33.setText(_translate("MainWindow", "Table of indicators", None))
        self.label_34.setText(_translate("MainWindow", "Indicators in comma delimited format", None))
        self.label_35.setText(_translate("MainWindow", "Report specified links", None))
        self.label_36.setText(_translate("MainWindow", "Link-Route & Category profile", None))
        self.label_37.setText(_translate("MainWindow", "Transit Routes profiles", None))
        self.label_38.setText(_translate("MainWindow", "Route profile in comma delimited format", None))
        self.label_39.setText(_translate("MainWindow", "Report specified link types", None))
        #Labels mats
        self.label_12.setText(_translate("MainWindow", "mats", None))
        self.label_58.setText(_translate("MainWindow", "Disut. by transport category", None))
        self.label_59.setText(_translate("MainWindow", "Disut. by mode and transport category", None))
        self.label_60.setText(_translate("MainWindow", "Disut. by socio-economic sector", None))
        self.label_61.setText(_translate("MainWindow", "Trips by mode", None))
        self.label_62.setText(_translate("MainWindow", "Trips by transport category", None))
        self.label_63.setText(_translate("MainWindow", "Trips by mode and transport category", None))
        self.label_64.setText(_translate("MainWindow", "Total trips (sum of categories)", None))
        self.label_65.setText(_translate("MainWindow", "Frequency distribution of trips by mode", None))
        self.label_66.setText(_translate("MainWindow", "Flows by socio-economic sector", None))
        self.label_67.setText(_translate("MainWindow", "Flows by transport category", None))
        self.label_68.setText(_translate("MainWindow", "Costs by transport category", None))
        self.label_69.setText(_translate("MainWindow", "Costs by socio-economic sector", None))
        self.label_70.setText(_translate("MainWindow", "Exogenus trips by transport category", None))        
        self.label_71.setText(_translate("MainWindow", "Exogenous trips by category and mode", None))        
        #Generate Button
        self.Generate_Button.setText(_translate("MainWindow", "Generate", None))
    