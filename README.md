# InterfacesTRANUS2016
Julien Armand

The goal of this project is to create various interfaces making the use of the program TRANUS easier and more practical.

There are two interfaces in this project : OptionsTRANUS and InterfaceVariationTRANUS.

The files InterfaceVariationTRANUSUI.py and OptionsTRANUSUI.py only contain the structure of the interfaces, with no proper function in them. All the other files
(LCALparam.py, extractionScenarios.py, Tools.py, LcalInterface.py and TranusConfig.py) are necessary to their proper execution.

To use the interfaces, simply run the corresponding Python program. However, these programs both use the config file to know the location of the necessary programs and files. The config file
must therefore be modified prior to running the OptionsTRANUS.py or InterfaceVariationTRANUS.py programs. 
You can also use these classes directly. An exemple on how to do that can be found in their main section, which use the config file in the same directory as the python files.

The config file must be written in accordance to the following model :
Location of TRANUS bin directory
Location of the directory of the TRANUS project
Code of which scenario of the TRANUS project you want to use
One more line at the end, necessary for proper reading of the file, which can contain anything.
