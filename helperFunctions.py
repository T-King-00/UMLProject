from spacy.language import Language
import spacy

@Language.component("custom_sentencizer")
def custom_sentencizer(doc):
    for i, token in enumerate(doc[:-1]):
    
        if token.text == "."  :
          doc[i + 1].is_sent_start = True
        elif  token.text == "As":
          doc[i].is_sent_start = True
        else:
            # Explicitly set sentence start to False otherwise, to tell
            # the parser to leave those tokens alone
            doc[i + 1].is_sent_start = False
    return doc

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("custom_sentencizer", before="parser")  # Insert before the parser

def getSentencesFromFile(file):
    doc = nlp(file)
    sentences=[]
    for sent in doc.sents:
        sentences.append(sent.text)
    return sentences


