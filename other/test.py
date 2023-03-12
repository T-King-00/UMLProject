# Copyright 2017 Peter de Vocht
from other.pipelineTextPartsExtraction import findSVOs, printDeps
#dont forget to run pip install -r requirements.txt
import helperFunctions
import requests
response = requests.get('https://raw.githubusercontent.com/T-King-00/Gp-AutomationOfBaTasks/tony/university.txt')
file = response.text
#%%

x=helperFunctions.getSentencesFromFile(file)

# testthe subject/verb/object_extraction
class SubjectVerbOjectExtractTest():


    def test_svo_1(self):
        tok = helperFunctions.nlp(x[0])
        print(tok)
        svos = findSVOs(tok)
        printDeps(tok)  # just show what printDeps() does
        #self.assertTrue(set(svos) == {('the annoying person', 'was', 'my boyfriend'), ('the annoying person', 'hit', 'me')})