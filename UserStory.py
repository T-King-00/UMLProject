from pprint import pprint

from spacy import matcher
from spacy.matcher import Matcher

import helperFunctions
from UseCase.Actor import Actor


class UserStory ():
    def extractActor(sentence):
        actorObj = None
        sentenceNlp = helperFunctions.nlp ( sentence )
        for chunk in sentenceNlp.noun_chunks:

            actorObj = Actor ( chunk.text )
            # remove an or a .
            identifier = actorObj.name.find ( "a " )
            identifier2 = actorObj.name.find ( "an " )
            if identifier >= 0:
                actorObj.name = actorObj.name.replace ( "a ", "" )
            elif identifier2 >= 0:
                actorObj.name = actorObj.name.replace ( "an ", "" )
            # checks in list if there is an actor with same name .
            break
        return actorObj

    # recieves not processed sentences .
    def extractActors(sentences):
        actors = [ ]
        for sentence in sentences:
            sentenceNlp = helperFunctions.nlp ( sentence )
            actorObj = UserStory.extractActor ( sentence )
            if not any ( obj.name == actorObj.name for obj in actors ):
                actors.append ( actorObj )

        return actors

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

    def extractUseCase(sentence):

        matcher = Matcher ( helperFunctions.nlp.vocab )
        compoundVerbs = [ ]
        v = sentence.find ( "so that" )
        sentence = sentence [ 0:v ]
        actor = UserStory.extractActor ( sentence )
        x = helperFunctions.nlp ( sentence )
        # verb det noun ,, verb the noun
        pattern0 = [ [ {"POS": "VERB"}, {"POS": "DET"}, {"POS": "NOUN"} ],
                     [ {"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "VERB"}, {"POS": "NOUN"} ]
                     ]

        pattern1 = [ {"POS": "VERB"}, {"POS": "NOUN"} ]

        pattern2 = [ {"POS": "VERB"}, {"POS": "NOUN"}, {"POS": "PART"}, {"POS": "AUX"}, {"POS": "VERB"} ]
        pattern3 = [ {"LOWER": "want"}, {"LOWER": "to"}, {"POS": "VERB"}, {"POS": "DET", "OP": "*"}, {"POS": "NOUN"} ]
        pattern4 = [ {"POS": "VERB"}, {"POS": "ADP"}, {"POS": "NOUN"} ]
        matcher.add ( "verbPhrase2", [ pattern2 ] )
        matcher.add ( "verbPhrase3", [ pattern3 ] )
        matcher.add ( "verbPhrase", pattern0 )
        matcher.add ( "verbPhrase4", [ pattern4 ] )

        matcher.add ( "verb-want-noun", [ pattern1 ] )

        matches = matcher ( x )
        for match_id, start, end in matches:
            string_id = helperFunctions.nlp.vocab.strings [ match_id ]  # Get string representation
            span = x [ start:end ]  # The matched span
            if string_id == "verb-want-noun":
                if span [ 0 ].text == "want" and span [ 1 ].pos_ == "NOUN":
                    continue
            if string_id == "verbPhrase2":
                verb4 = span [ 4 ].lemma_
                nounx = span [ 1 ].text
                newSentence = verb4 + " " + nounx
                span = newSentence
            compoundVerbs.append ( span )
            if span is not None:  # to get only the fist part of use case .
                break
        pprint ( compoundVerbs )
        return compoundVerbs, actor
