import re

import helperFunctions
from UserStory import UserStory
from spacy.lang.en import stop_words as stop_words

conceptList = [ ]
noun_phrases = [ ]


def preprocess(sentences):
    for i, sentence in enumerate ( sentences ):
        sentences [ i ] = re.sub ( r'[^\w\s]', '', sentence )  # Remove punctuation
        # sentences [ i ] = sentence.replace ( '\r\n', '' )  # Remove newline
        sentences [ i ] = re.sub ( r'\W+', ' ', sentence )
        print ( sentences [ i ] )
    return sentences


def stemmingAlgorithm(words):
    for i, word in enumerate ( words ):
        doc = helperFunctions.nlp ( word )
        for t in doc:
            words [ i ] = t.lemma_
    return words


def parser(sentences):
    global conceptList
    global noun_phrases
    # nouns
    for sentenceObj in sentences:
        objNlp = helperFunctions.nlp ( sentenceObj )
        for doc in objNlp:

            if doc.pos_ == "PROPN" or doc.dep_ == "ROOT":
                conceptList.append ( doc.text )
        ### this part get compound nouns (actors))
        for i, chunk in enumerate ( objNlp.noun_chunks ):
            noun_phrases.append ( chunk.text )
            if i == 0:
                continue;
            if chunk.text not in conceptList:
                conceptList.append ( chunk.text )
            else:
                continue
    # remove dublicates
    conceptList = list ( dict.fromkeys ( conceptList ) )
    noun_phrases = list ( dict.fromkeys ( noun_phrases ) )
    return conceptList


def removestopwords_from_conceptlist():
    global conceptList
    global noun_phrases

    conceptList.append ( [ x for x in noun_phrases ] )
    conceptList = list ( dict.fromkeys ( conceptList ) )


###  main part
file = helperFunctions.getFile ()
sentences = helperFunctions.getSentencesFromFile ( file )

stop_words_found = [ ]
countOfWords = 0
stop_words = stop_words.STOP_WORDS
wordsinDoc = {}
for sentence in sentences:
    sentence = sentence.lower ()
    sentence = helperFunctions.nlp ( sentence )
    for tok in sentence:
        if tok.is_stop or tok.text == "," or tok.text == "." or tok.text == '“':
            stop_words_found.append ( tok.text )
        else:
            countOfWords = countOfWords + 1
            if tok.text not in wordsinDoc:
                wordsinDoc [ tok.text ] = 0
            wordsinDoc [ tok.text ] = wordsinDoc [ tok.text ] + 1
if stop_words_found is None:
    print ( "is nnone" )
stop_words_found = list ( dict.fromkeys ( stop_words_found ) )
print ( stop_words_found )
print ( wordsinDoc )
print ( countOfWords )
frequency = {}
for key in wordsinDoc:
    freq = wordsinDoc [ key ] / countOfWords
    print ( freq )
    frequency [ key ] = freq

print ( frequency )

wordsAfterLemmaization = stemmingAlgorithm ( list ( wordsinDoc.keys () ) )
print ( wordsAfterLemmaization )

conceptListVar = parser ( sentences )
print ( conceptListVar )
