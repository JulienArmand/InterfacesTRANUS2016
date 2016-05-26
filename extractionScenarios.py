#This is a program for the extraction of the scenarios in a W_TRANUS.CTL file.
#author : Julien Armand
import os
class Scenarios:
    '''
    The Scenarios class is used to store the codes and names of a list of scenarios on different lists of the same length.
    listCodes : list of the codes of the scenarios
    listNames : list of the names of the scenarios
    '''
    def __init__(self, code, nom):
        self.listCodes = code
        self.listNames = nom
        
def extractionScenarios(filePath):
    '''
    This methods takes the path to a W_TRANUS.CTL file and returns an object Scenarios containing the scenarios described in that file.
    Parameters
    ----------
    filepath : Strings
        the location of the W_TRANUS.CTL file
    Example
    -------    
    >>> filepath = (""ExampleC\W_TRANUS.CTL")
    >>> r = extractionScenarios(filepath)
    >>> r.listCodes
    ['03A', '08A','08B','13A','13B']
    '''
    f = open(filePath,"r")
    #Advance until the 2.0 line
    while not f.next()[0] is '2':
        pass
    f.next()
    #The code and name go to two arrays of Strings named 'codeScenario' and 'nameScenario' respectively
    codeScenario = []
    nameScenario = []
    #Repeat the extraction of the code and name until reaching the *---- line
    currentLine = f.next()
    while not currentLine[0] is '*':
        currentSplit = str.split(currentLine, "'")
        codeScenario.append(currentSplit[1])
        nameScenario.append(currentSplit[3])
        currentLine = f.next()
    #Creation of the object Scenarios for return
    result = Scenarios(codeScenario,nameScenario)
    return result

if __name__=='__main__':
    f = open("config","r")
    lines = f.readlines()
    tranusBinPath = lines[0].rstrip('\n')
    workingDirectory = lines[1].rstrip('\n')
    projectID = lines[2].rstrip('\n')
    r = extractionScenarios(os.path.join(workingDirectory, "W_TRANUS.CTL"))
    print r.listCodes
    print r.listNames
