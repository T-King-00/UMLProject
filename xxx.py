import helperFunctions


def run(sent):
    doc = helperFunctions.nlp ( sent )
    for token in doc:
        print ( f"Token: {token.text}" )
        print ( f"  - Class: {token.ent_type_}" )
        print ( f"  - Lemma: {token.lemma_}" )
        print ( f"  - POS: {token.pos_}" )
        print ( f"  - Dependency: {token.dep_}" )
        print ( f"  - Is Stop Word: {token.is_stop}" )
