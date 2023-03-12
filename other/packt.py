from spacy import matcher

import plantUML, helperFunctions, extractSVO
import spacy
import requests


##############################################################
###functions
##############################################################
def get_prepostionalPhrase(doc):
    pps = [ ]
    for token in doc:

        # Try this with other parts of speech for different subtrees.
        if token.pos_ == "ADP":
            pp = ' '.join ( [ tok.orth_ for tok in token.subtree ] )
            pps.append ( pp )
    print ( "pp:", pps )
    return pp


def get_subject_phrase(doc):
    for token in doc:
        if "subj" == token.dep_:
            subtree = list ( token.subtree )
            start = subtree [ 0 ].i
            end = subtree [ -1 ].i * 1
            return doc [ start:end ]


def get_object_phrase(doc):
    for token in doc:
        if "dobj" == token.dep_:
            subtree = list ( token.subtree )
            start = subtree [ 0 ].i
            end = subtree [ -1 ].i + 1
            return doc [ start:end ]


def get_prepositional_phrase_objs(doc):
    prep_spans = [ ]
    for token in doc:
        if "pobj" == token.dep_:
            subtree = list ( token.subtree )
            start = subtree [ 0 ].i
            end = subtree [ -1 ].i + 1
            prep_spans.append ( doc [ start:end ] )
    return prep_spans


def getRootVerb(doc):
    root = None
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            root = token
    print ( "ROOT VERB:", root )
    return root


def childofrootverb(doc):
    objs = [ ]
    OBJECTS = {"dobj", "dative", "attr", "oprd"}
    pps = [ ]
    for token in doc:
        # Try this with other parts of speech for different subtrees.
        if token.dep_ == "ROOT":
            for child in token.children:
                if child.dep_ in OBJECTS:
                    objs.append ( child.text )
                if child.pos_ == "ADP":
                    pp = ' '.join ( [ c.orth_ for c in child.subtree ] )
                    pps.append ( pp )
                    print ( "cccc:", pps )

    objs = "".join ( objs )
    print ( "childofrootverb:", objs )
    return objs


def extract_object_and_verb(doc):
    object_phrase = ''
    root_verb = ''
    for token in doc:
        if token.dep_ == 'dobj':  # find the direct object
            # Traverse the subtree of the direct object to get the entire object phrase
            object_tokens = [ t for t in token.subtree ]
            object_phrase = ' '.join ( [ t.text for t in object_tokens ] )
        if token.dep_ == 'ROOT':  # find the root verb
            root_verb = token.text
    return root_verb, object_phrase


def extract_verb_and_prep_phrase(doc):
    root_verb = ''
    prep_phrase = ''
    first_pp = ""
    second_pp = ""
    for i, token in enumerate ( doc ):
        if token.dep_ == 'ROOT':  # find the root verb
            root_verb = token.text
            for k, tok in enumerate ( doc ):
                if tok.i >= token.i:
                    """
                    if tok.dep_ == 'prep':  # find the preposition
                        # Traverse the subtree of the preposition to get the entire prepositional phrase
                        prep_tokens = [ t for t in tok.subtree ]
                        prep_phrase = ' '.join ( [ t.text for t in prep_tokens ] )
                        break
                    """
                    if tok.dep_ == "prep" and tok.head.pos_ == "VERB":
                        first_pp = tok.text
                        for child in tok.children:
                            if child.dep_ == "pobj":
                                first_pp += " " + child.text

                    if tok.dep_ == "prep" and tok.head.pos_ != "VERB":
                        prep2_tokens = [ t for t in tok.subtree ]
                        second_pp = ' '.join ( [ t.text for t in prep2_tokens ] )

    return root_verb, prep_phrase, first_pp, second_pp


response = requests.get ( 'https://raw.githubusercontent.com/T-King-00/Gp-AutomationOfBaTasks/tony/university.txt' )
file = response.text

sentences = helperFunctions.getSentencesFromFile ( file )
v = sentences [ 0 ].find ( "so that" )
sentVar = sentences [ 0 ] [ 0:v ]
doc = helperFunctions.reduceSentence ( sentVar )
subject_phrase = get_subject_phrase ( doc )
object_phrase = get_object_phrase ( doc )
get_prepositional_phrase_objsx = get_prepositional_phrase_objs ( doc )

print ( getRootVerb ( doc ) )

### get prepostional phrase after root verb and main object
root_verb, prep_phrase, first_pp, second_pp = extract_verb_and_prep_phrase ( doc )
print ( "Root verb:", root_verb )
print ( "Prepositional phrase:", prep_phrase )
print ( "1st Prepositional phrase:", first_pp )
print ( "2nd  Prepositional phrase:", second_pp )
print ( "verb ,obj : ", extract_object_and_verb ( doc ) )


def extractUseCase(sentence):
    compoundVerb = None
    v = sentence.find ( "so that" )
    sentence = sentence [ 0:v ]
    x = helperFunctions.nlp ( sentence )
    # verb det noun ,, verb the noun
    pattern1 = [ {"POS": "VERB"}, {"POS": "DET"}, {"POS": "NOUN"} ]
    matcher.add ( "verbPhrase", pattern1 )
    matches = matcher ( x )
    for match_id, start, end in matches:
        string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
        span = x [ start:end ]  # The matched span
        if span.text.find ( "want the" ) > -1:
            continue
        compoundVerb = span

    return compoundVerb
