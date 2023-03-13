from pprint import pprint

from spacy.training.example import Example

import spacy
import json

import helperFunctions

with open ( 'annotations3.json', encoding="utf8" ) as fp:
    trainingdData = json.load ( fp )

#    print ( trainingdData )

# prepare an empty model to train
nlp = spacy.blank ( "en" )
nlp.vocab.vectors.name = 'demo'

nlp.add_pipe ( 'ner', last=True )

# Add the custome NER Tags as entities into the model
for label in trainingdData [ "classes" ]:
    nlp.get_pipe ( 'ner' ).add_label ( label )

# train model
optimizer = nlp.begin_training ()
# print ( trainingdData [ "annotations" ] )
examples = [ ]
for iter in range ( 2 ):
    for text, annotations in trainingdData [ "annotations" ]:
        if len ( text ) > 0:
            doc = nlp.make_doc ( text )
            # print ( doc )
            examples.append ( Example.from_dict ( doc, annotations ) )
            nlp.update ( examples, sgd=optimizer )

text = open ( "LibraryManagementSystem.txt", encoding='utf8' )
lines = text.readlines ()
for i, x in enumerate ( lines ):
    if i == 3:
        doc = nlp ( x )
        for ent in doc.ents:
            print ( ent.text, "label : ", ent.label_ )
