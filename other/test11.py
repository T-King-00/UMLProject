# Copyright 2017 Peter de Vocht
#dont forget to run pip install -r requirements.txt
import helperFunctions
import requests
response = requests.get('https://raw.githubusercontent.com/T-King-00/Gp-AutomationOfBaTasks/tony/university.txt')
file = response.text
x=helperFunctions.getSentencesFromFile(file)

for sent in x :
    print("sentence:" , sent)
from other.pipelineTextPartsExtraction import findSVOs, printDeps

print(x[6])
tok=helperFunctions.nlp(x[6])
svos = findSVOs(tok)
printDeps(tok)
print(svos)