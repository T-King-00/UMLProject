# dont forget to run pip install -r requirements.txt
import os
from pprint import pprint
import spacy.tokens
import UseCase.Actor
import helperFunctions
import plantUML
import xxx
from UserStory import UserStory
import fn
from models.classDiagram import classDiagram
from transformers import pipeline

#
# pipe = pipeline ( model="facebook/bart-large-mnli" )
# result = pipe ( "I have a problem with my iphone that needs to be resolved asap!",
#                 candidate_labels=[ "urgent", "not urgent", "phone", "tablet", "computer" ],
#                 )
# print ( result [ "scores" ] )

###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of 
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . ()
3-class entities        ()
4-class atributes ()
5-class relation ()
5-drawing. (done)
"""
# get sentences
file = helperFunctions.getFile ()
sentences = helperFunctions.getSentencesFromFile ( file )

# reduce sentences
# removes determinants , aux verbs and adjectives.
sentences1 = helperFunctions.reduceSentences ( sentences )
actorsList = UserStory.extractActors ( sentences1 )
# for x in actorsList:
# print ( x.name )
# print ( "#######################" )

"""
1-get all classes and attributes
2-get_inheritance
3-get relations
"""

for i, sent in enumerate ( sentences1 ):
    classes = classDiagram.extract_classes ( sent )
    if classes != None:
        print ( "classes_attr: ", [ x for x in classes ] )
    print ( "#########################################" )
# graph = fn.graph_from_uml ( classes_attr, relations, inheritances )

# for i, sent in enumerate ( sentences1 ):
#
#     if i == 2:
#         x = classDiagram.getClasses1 ( sent, actorsList )
#
#         if x is not None:
#             print ( sent )
#             x = [ element for element in x if not any ( obj.name == element for obj in actorsList ) ]
#
#        print ( x )

# for i, sent in enumerate ( sentences1 ):
#     if i == 6:
#         sentence = sent.lower ()
#         x = helperFunctions.getAllNouns ( sentence )
#
#         if x is not None:
#             print ( sentence )
#             x = [ element for element in x if not any ( obj.name == element for obj in actorsList ) ]
#
#         print ( x )
