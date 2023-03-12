# dont forget to run pip install -r requirements.txt
import os
from pprint import pprint

import spacy.tokens

import UseCase.Actor
import helperFunctions
import plantUML
from UserStory import UserStory

###pipeline
"""
format of user story . As a ..... , i want to , so that   ...... .
0-getting file
1-file preproccessing (detection of line rules . starting of 
    sentence is as and middle word i want to ,so that and full stop .((not done yet))
2-sentence separation . (done)
3-actor detection       (done)
4-use case extraction for each actor. (done)
5-drawing. (done)



"""
# get sentences
file = helperFunctions.getFile ()
sentences = helperFunctions.getSentencesFromFile ( file )
pprint ( sentences )
# reduce sentences
# removes determinants , aux verbs and adjectives.
sentences = helperFunctions.reduceSentences ( sentences )

# get actors .
actorsList = UserStory.extractActors ( sentences )
for actor in actorsList:
    pprint ( actor.name )


# for each actor get his use cases :

# for each actor get his use cases :
def printtags(sent):
    sent = helperFunctions.nlp ( sent )
    for token in sent:
        print ( "token:", token.text, "  token pos", token.pos_ )


actors = [ ]
for i, sent in enumerate ( sentences ):
    # printtags ( sent )
    print ( i, "new sentence @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" )
    x, actor = UserStory.extractUseCase ( sent )
    print ( type ( x ) )
    print ( actor.name )

    for c in x:
        if isinstance ( c, spacy.tokens.Span ):
            print ( "c type : ", type ( c ) )
            textvar = c [ 0: ].text
            actor.addUseCase ( textvar )
            print ( actor.usecases )
        elif isinstance ( c, str ):
            print ( "c type : ", type ( c ) )
            textvar = c
            actor.addUseCase ( textvar )
            print ( actor.usecases )
    if not any ( obj.name == actor.name for obj in actors ):
        actors.append ( actor )

filename = "other/usecasediagram1111.txt"
filename2 = "usecasediagram1111.png"
if os.path.exists ( filename ) and os.path.exists ( filename2 ):
    os.remove ( filename )
    os.remove ( filename2 )
else:
    print ( "The file does not exist" )

os.system ( "pip install plantuml" )
usecasemodel = plantUML.UseCaseModel ( filename )
usecasemodel.addCustomMessage ( "left to right direction" )
for a in actors:
    print ( a.name )

for actor in actors:
    for usecaseobj in actor.usecases:
        usecasemodel.addUseCasetoActor ( actor.name, usecaseobj )

usecasemodel.closeFile ()

os.system ( "python -m plantuml " + filename )
