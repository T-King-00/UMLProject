#dont forget to run pip install -r requirements.txt
import plantUML,helperFunctions
import spacy
import requests
response = requests.get('https://raw.githubusercontent.com/T-King-00/Gp-AutomationOfBaTasks/tony/atmUserStories.txt')
file = response.text


x=helperFunctions.getSentencesFromFile(file)

print(x[0])

#from spacy import displacy
doc5 = helperFunctions.nlp(x[0])
#displacy.serve(doc5, style="dep",)

# Find the main verb of the sentence
mainVerb=None
subject=None
object=None
action=None

for token in doc5:
    print(token , token.dep_  )
    # Find the subject of the sentence (a noun or pronoun)
    if token.dep_ == 'nsubj' and token.pos_ in ['NOUN', 'PRON']:
        subject = token.text
    # Find the main verb of the sentence
    elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
        mainVerb = token.text
    elif token.dep_ == "dobj" and token.head.text == action:
        object =  token.text
    if token.dep_ == "xcomp":
        action=token.text

print(subject)
print (mainVerb)
print("action is : " ,action)
print("object is :" , object)
