

#!/usr/bin/env python

#===============================================================================
# This is the class that interfaces the lcal.o file with python. Here we run 
# lcal providing it with the required inputs from python.
#===============================================================================
import subprocess
import os
import time
import logging
import platform

class LcalInterface:
    "LcalInterface models an interface to communicate with LCAL Tranus Module"
    
    # Messages
    LCAL_RUN_ERROR = "ERROR: LCAL has not been run yet"
    
    # Initialize lcal interface
    def __init__(self, t, dirResult, numSample=None):
        "LcalInterface constructor. It initializes the needed values."
        self.nSamp = numSample
        self.resultDirectory = dirResult
        self.outFile = "outlcal.txt"       #output of lcal stored here                 
        self.tranusConf = t  #Configure tranus using TranusConfiguration class
        self.TranusHasBeenRun = 0
        operating_system = platform.system()
        if operating_system.startswith('Windows'):
            self.extension = '.exe'
            can_use_fds = False
        else:
            self.extension = ''
            can_use_fds = True
                   #flag that lcal.o has been executed

         
    
    # Checks if lcal module has converged or not. May change it as required.
    # Nothing important going on here  
    def __checkConvergenceValues(self, convFactor, valuesDict):
        "It checks if the values in the Dict are all lower than the 'convFactor'"
        converge = 1 #Initial value of converge 

        # For each convergence indicator, check if it doesn't converges
        
        for key in valuesDict:
            if abs( float( valuesDict[key][0]) ) > float(convFactor) or abs( float( valuesDict[key][1]) ) > float(convFactor):
                converge = 0 # if any of the values are greater than conv factor the flag is 0 hence lcal hasn't converged
                break
        
        return converge
    
    #Returns the maximum deviation variable in lcal
    def __maxConvergenceValues(self, valuesDict,N):
      "returns the maximum of convergence values to check how far we are from the convergence"
      res1 = 0
      res2 = 0
      # For each convergence indicator, check if it doesn't converges
      for key in valuesDict:

          res1 = max([abs(float(valuesDict[key][0])),res1])
          res2 = max([abs(float(valuesDict[key][1])),res2])
      return [res1, res2, N]

     #==========================================================================
     # Reads file .L1E in tranus project directory and returns the convergence factor written on it.
     # Nothing important going on here       
     #==========================================================================
    def getConvergenceFactor(self):
       """ It reads the file with extension L1E and returns the convergence factor """
       if ( os.path.exists(self.tranusConf.workingDirectory + "/" + self.tranusConf.scenarioId + "/" + "W_" + self.tranusConf.projectId + self.tranusConf.scenarioId + ".L1E") ):
           # Open the output file for reading
           file = open( self.tranusConf.workingDirectory + "/" + self.tranusConf.scenarioId + "/" + "W_" + self.tranusConf.projectId + self.tranusConf.scenarioId + ".L1E", 'r')
          
           convFactor = file.readlines()[5].split()[1]
           
           file.close()            
           return convFactor
       else:
           print "ERROR: File " + self.tranusConf.workingDirectory + "/" + self.tranusConf.scenarioId + "/" + "W_" + self.tranusConf.projectId + self.tranusConf.scenarioId + ".L1E" + " does not exist."
           return ""
     #==========================================================================
     # Checks if output of Lcal has some errors by inspecting the output file and 
     # returns the message that lcal has not been run properly 
     #==========================================================================
    def errorRunningLcal(self):
        "Checks the output file generated by LCAL for errors. If the file has an error, the method returns it. otherwise, it returns an empty string" 
    #if self.lcalHasBeenRunned:
        # Open the output file for reading
        file = open(self.tranusConf.workingDirectory + "/" +self.outFile, 'r')
        # Read the last line
        lastLine = file.readlines()[-1]
        
        file.close()
        # Check for the error
        if lastLine.split()[0] == "ERROR#":
            return lastLine
        else:
            return ""
    #else:
        print self.LCAL_RUN_ERROR
        return self.LCAL_RUN_ERROR  
    
    
     #==========================================================================
     # Inspecting convergence of lcal module  
     # The convergence of .lcal can be construed to be similar to the convergence 
     # via iterations achieved by Newton-Raphson's method.
     # Point to note:- .lcal performs iterative convergence itself. We just check 
     # here if it actually converges or not. 
     #==========================================================================
          
    def converges(self, blocksToCheck = 2,maxConv='False'):
        """Checks if the model achieves or not the convergence. To do that, it inspects the last iterations to know if it converges or not. The amount of blocks
            to inspect is "blocksToCheck" (it 2 by default).
        """
        convFactor = self.getConvergenceFactor() # gets convergence factor from L1E file. See functions above
        
        if convFactor: # if convergence factor not equal to zero
            if not self.errorRunningLcal(): # if lcal has run properly. See functions above for more info 
                # Open the output file for reading
                file = open( self.tranusConf.workingDirectory + "/"+self.outFile, 'r')

                # Read the lines of the file
                lines = file.readlines() 
                file.close()
                scratch = 1
                
                if lines[-6].split(' ')[1]=='WARNING':
                    lineNumber = len(lines) - 1
                    Niter = 250
                else:
                    i=0
                    while scratch:                        
                        if lines[-i][0]=='\n':
                            i = i+1 
                        if(lines[-i].split()[0])=='Iter':
                            scratch = 0                                  
                            lineNumber =  len(lines) - i 
                            Niter = float(lines[-i].split()[1])
                           
                        i= i+1     
                                    

                        
            
                # The list structure is: valuesList[("Iter","Sector")] = ("ConvPric", "ConvProd"). It takes a file
                valuesDict = {} # valuesDict variable stores the fraction difference between output values of two iterations
  
            
                readBlocks = 0
                
##                lineNumber = len(lines) - 1
            
                # Iterating backward in the file
                # Read the lines from last to first 
                
                while lineNumber >= 0 and readBlocks < blocksToCheck:
                    # Split the line into a List of strings
                    lineRead = lines[lineNumber].split()
            
                    # If I find a block of convergence information for an iteration
                    # searches for the word Iter in the line. that is where fraction difference is stored. 
                    # Recall- valuesDict
                    # To understand this append the output of .lcal to a .csv/.txt file and try to read it.
                    # REMEMBER- lcal generates files which only makes sense if you read it after running imploc.                
                    
                    if lineRead[0] == "Iter":
                        # Save the Iter number
                        iter = lineRead[1]
                        # Increment the amount of blocks read
                        readBlocks = readBlocks + 1
                        # Read a line to discard garbage (blank spaces)                        
                        lineNumber = lineNumber - 1
                        # Read the next useful line
                        lineNumber = lineNumber - 1
                        lineRead = lines[lineNumber].split()
                    
                        # While reading sectors from the file...
                        while lineRead[0].isdigit():
                            # Add to the dictionary the new values
                            while len(lineRead)>8:
                                lineRead[1]=lineRead[1]+lineRead[2]
                                lineRead.pop(2)
                                
                            valuesDict[(iter,lineRead[0])] = (lineRead[2], lineRead[4])
                             
                            # Read the next line
                            lineNumber = lineNumber - 1
                            lineRead = lines[lineNumber].split()

                        
                        # Once the sectors have been read, we check if it sector converges
                        if maxConv:

                            return self.__maxConvergenceValues(valuesDict,Niter)
                            
                            
                        else:
                            # Once the sectors have been read, we check if it sector converges
                            if self.__checkConvergenceValues(convFactor, valuesDict):
                                return 1
                            else:
                                # Clear the map in order to look for convergence in the previous iteration 
                                valuesDict.clear()
                
                    
                
                    lineNumber = lineNumber - 1
                    
        # If convergence not achieved 
        return 0
           
    def CreateImploc(self):
        '''Creates the Imploc report from lcal'''
        program = os.path.join(self.tranusConf.tranusBinPath,'imploc'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <imploc> program was not found in %s'%self.tranusBinPath )
            return 0
        outimploc = os.path.join(self.tranusConf.workingDirectory, "outimploc.txt")
        outimplocerr = os.path.join(self.tranusConf.workingDirectory, "outimplocerr.txt")
        args = [program, self.tranusConf.scenarioId,'-S',' ']
        proc = subprocess.Popen(args, stdout=open(outimploc, 'w'), stderr=open(outimplocerr,'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1            
                
    def runLcal(self, freeze=False):
        '''Runs LCAL module and write its output in the file indicated by 'self.outFile'''
        program = os.path.join(self.tranusConf.tranusBinPath,'lcal'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <lcal> program was not found in %s'%self.tranusBinPath )
            return 0
        outlcal = os.path.join(self.resultDirectory, "outlcal.txt")
        outlcalerr = os.path.join(self.resultDirectory, "outlcalerr.txt")
        if(freeze):
            print("Running lcal with freeze option activated")
            args = [program, self.tranusConf.scenarioId, "-f"]
            print("argument")
            print(args)
        else :
            args = [program, self.tranusConf.scenarioId]
            print("argument")
            print(args)
        result = subprocess.Popen(args, stdout=open(outlcal, "w"), stderr=open(outlcalerr, 'w'), cwd=self.tranusConf.workingDirectory).communicate() # Success!
        return 1
        
    def runLoc(self):
        '''Runs loc module and write its output in the file indicated by 'self.outFile'''
        program = os.path.join(self.tranusConf.tranusBinPath,'loc'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <loc> program was not found in %s'%self.tranusBinPath )
            return 0
        outloc = os.path.join(self.resultDirectory, "outloc.txt")
        outlocerr = os.path.join(self.resultDirectory, "outlocerr.txt")
        args = [program, self.tranusConf.scenarioId]
        result = subprocess.Popen(args, stdout=open(outloc, "w"), stderr=open(outlocerr, 'w'), cwd=self.tranusConf.workingDirectory).communicate() # Success!
        return 1
   
    #Running the transport Module
    def runTrans(self,loopn):
        '''Runs Trans module and write its output in a file'''
        
        program = os.path.join(self.tranusConf.tranusBinPath,'trans'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <trans> program was not found in %s'%self.tranusBinPath )
            return 0
        outtrans = os.path.join(self.resultDirectory, "outtrans.txt")
        outtranserr = os.path.join(self.resultDirectory, "outtranserr.txt")
        if loopn == 0:
            args = [program, self.tranusConf.scenarioId,'-I', " "]
        else: 
            args = [program, self.tranusConf.scenarioId, '-N'," "]
        result = subprocess.Popen(args, stdout = open(outtrans, "w"), stderr = open(outtranserr,'w'), cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1
    
    #Runs Fluj module which transforms the lcal matrices into flows for the transport sector    
    def runFluj(self):
        '''Runs Fluj module and write its output in a file'''
        program = os.path.join(self.tranusConf.tranusBinPath,'fluj' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <fluj> program was not found in %s'%self.tranusBinPath )
            return 0
        outfluj = os.path.join(self.resultDirectory, "outfluj.txt")
        outflujerr = os.path.join(self.resultDirectory, "outflujerr.txt")
        args = [program,self.tranusConf.scenarioId]
        result = subprocess.Popen(args, stdout=open(outfluj, "w"), stderr = open(outflujerr, 'w'), close_fds = False, cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1
        
    def runFlujI(self):
        '''Runs Fluj module with option -I and write its output in a file'''
        program = os.path.join(self.tranusConf.tranusBinPath,'fluj' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <fluj> program was not found in %s'%self.tranusBinPath )
            return 0
        outflujI = os.path.join(self.resultDirectory, "outflujI.txt")
        outflujIerr = os.path.join(self.resultDirectory, "outflujIerr.txt")
        args = [program,self.tranusConf.scenarioId, "-I", " "]
        result = subprocess.Popen(args, stdout=open(outflujI, "w"), stderr = open(outflujIerr, 'w'), close_fds = False, cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1

    def runPasos(self):
        '''Runs PASOS module and write its output in a file'''
        program = os.path.join(self.tranusConf.tranusBinPath,'pasos' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <pasos> program was not found in %s'%self.tranusBinPath )
            return 0
        outpasos = os.path.join(self.resultDirectory, "outpasos.txt")
        outpasoserr = os.path.join(self.resultDirectory, "outpasoserr.txt")
        args = [program, self.tranusConf.scenarioId, " "]
        result = subprocess.Popen(args, stdout=open(outpasos, "w"), stderr = open(outpasoserr, 'w'), close_fds = False, cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1
        
    def runImpas(self):
        '''Runs Impas module and write its output in a file'''
        program = os.path.join(self.tranusConf.tranusBinPath,'impas' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <impas> program was not found in %s'%self.tranusBinPath )
            return 0
        outimpas = os.path.join(self.resultDirectory, "outimpas.txt")
        outimpaserr = os.path.join(self.resultDirectory, "outimpaserr.txt")
        args = [program,self.tranusConf.scenarioId,"-o", self.tranusConf.scenarioId+"/IMPAS.MTX", " "]
        result = subprocess.Popen(args, stdout=open(outimpas, "w"), stderr = open(outimpaserr, 'w'), close_fds = False, cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1    
            
    def runMats(self):
        '''Runs MATS to generate the transport cost and disutilities matrix COST_T.MTX and DISU_T.MTX
        Needs L1S file!'''
        logging.debug('Creating Disutility matrix')
        program = os.path.join(self.tranusConf.tranusBinPath, 'mats' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <mats> program was not found in %s'%self.tranusBinPath )
            return 0
        
        outmats = os.path.join(self.resultDirectory, "outmats.txt")
        outmatserr = os.path.join(self.resultDirectory, "outmatserr.txt")

        args = [program, self.tranusConf.scenarioId, "-S", "[k]", "-o", "DISU_T.MTX", " "]
        proc = subprocess.Popen(args, stdout=open(outmats, 'w'), stderr=open(outmatserr, 'w'), cwd=self.tranusConf.workingDirectory).communicate()

        args = [program, self.tranusConf.scenarioId, "-K", "[k]", "-o", "COST_T.MTX", " "]
        proc = subprocess.Popen(args, stdout=open(outmats, 'w'), stderr=open(outmatserr, 'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1   
        
    def runMatsOption(self, option):
        '''Runs MATS to generate the matrixes passed in option'''
        logging.debug('Creating indicated matrix')
        program = os.path.join(self.tranusConf.tranusBinPath, 'mats' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <mats> program was not found in %s'%self.tranusBinPath )
            return 0
        
        outmats = os.path.join(self.resultDirectory, "outmats"+option+".txt")
        outmatserr = os.path.join(self.resultDirectory, "outmats"+option+"err.txt")
        args = [program, self.tranusConf.scenarioId, "-"+option, "-o", self.tranusConf.scenarioId+"/MATS_"+option+".CSV", " "]
        proc = subprocess.Popen(args, stdout=open(outmats, 'w'), stderr=open(outmatserr, 'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1
        
    #Running the cost module that will convert the matrices/flows from the transport to costs
    def runCost(self):
        '''Runs Cost module and write its output in a file'''
        program = os.path.join(self.tranusConf.tranusBinPath,'cost' + self.extension)
        if not os.path.isfile(program):
            logging.error('The <cost> program was not found in %s'%self.tranusBinPath )
            return 0
        outcost = os.path.join(self.resultDirectory, "outcost.txt")
        outcosterr = os.path.join(self.resultDirectory, "outcosterr.txt")
        args = [program,self.tranusConf.scenarioId, " "]
        result = subprocess.Popen(args, stdout=open(outcost, "w"), stderr = open(outcosterr, 'w'), close_fds = False, cwd = self.tranusConf.workingDirectory).communicate() # Success!
        return 1
        
    def runImplocOption(self, option):
        '''Creates the Imploc report with the indicated option from lcal'''
        program = os.path.join(self.tranusConf.tranusBinPath,'imploc'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <imploc> program was not found in %s'%self.tranusBinPath )
            return 0
        outimploc = os.path.join(self.resultDirectory, "outimploc"+option+".txt")
        outimplocerr = os.path.join(self.resultDirectory, "outimploc"+option+"err.txt")
        args = [program, self.tranusConf.scenarioId, "-"+option, "-o", self.tranusConf.scenarioId+"/IMPLOC_"+option+".MTX", " "]
        proc = subprocess.Popen(args, stdout=open(outimploc, 'w'), stderr=open(outimplocerr,'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1
        
    
    def runImplocVariationSubDir(self, option, nameFile):
        program = os.path.join(self.tranusConf.tranusBinPath,'imploc'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <imploc> program was not found in %s'%self.tranusBinPath )
            return 0
        print(self.resultDirectory)
        outimploc = os.path.join(self.resultDirectory, "outimploc"+option+".txt")
        outimplocerr = os.path.join(self.resultDirectory, "outimploc"+option+"err.txt")
        args = [program, self.tranusConf.scenarioId, "-"+option, "-o", nameFile, " "]
        print(args)
        proc = subprocess.Popen(args, stdout=open(outimploc, 'w'), stderr=open(outimplocerr,'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1
    
    def runImplocVariation(self, option):
        program = os.path.join(self.tranusConf.tranusBinPath,'imploc'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <imploc> program was not found in %s'%self.tranusBinPath )
            return 0
        outimploc = os.path.join(self.resultDirectory, "outimploc"+option+".txt")
        outimplocerr = os.path.join(self.resultDirectory, "outimploc"+option+"err.txt")
        dir = os.path.basename(os.path.normpath(self.resultDirectory))
        print("Check interface result directory "+ self.resultDirectory)
        args = [program, self.tranusConf.scenarioId, "-"+option, "-o", dir+"/IMPLOC_"+option+".MTX", " "]
        proc = subprocess.Popen(args, stdout=open(outimploc, 'w'), stderr=open(outimplocerr,'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1
    
    def runImptraOption(self, option):
        '''Creates the Imptra report with the indicated option from lcal'''
        program = os.path.join(self.tranusConf.tranusBinPath,'imptra'+self.extension)
        if not os.path.isfile(program):
            logging.error('The <imptra> program was not found in %s'%self.tranusBinPath )
            return 0
        outimptra = os.path.join(self.resultDirectory, "outimptra"+option+".txt")
        outimptraerr = os.path.join(self.resultDirectory, "outimptra"+option+"err.txt")
        args = [program, self.tranusConf.scenarioId, "-"+option, "-o", self.tranusConf.scenarioId+"/IMPTRA_"+option+".MTX", " "]
        proc = subprocess.Popen(args, stdout=open(outimptra, 'w'), stderr=open(outimptraerr,'w'), cwd=self.tranusConf.workingDirectory).communicate()
        return 1
        
        
    '''YOU HAVE TO RUN TRANUS IN A LOOP TO ACHIEVE PROPER CONVERGENCE IN THE SAME SEQUENCE GIVEN HERE IN THE PROGRAM.'''
    def runTranus(self,loopn):
        self.runPasos()
        self.runTrans(loopn)
        self.runCost()
        self.runLcal()
        self.runFluj()
        self.runTrans(1)
        self.TranusHasBeenRun = 1
        return self.TranusHasBeenRun

        
    ''' RUN THE LCAL MODULE ONLY.'''
    def runOnlyLcal(self):
        self.runLcal()  
        self.CreateImploc()
        self.TranusHasBeenRun = 1      
        print "TRANUS Convergence %s"%self.converges()     
        return self.TranusHasBeenRun                     
      
if __name__ == '__main__':
    pass

    
