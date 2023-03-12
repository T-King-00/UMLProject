import helperFunctions


def svoExtraction(text):
    doc = text
    root = None
    rightChildren = [ ]
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ == 'VERB':
            root = token
            print ( "Root is :", root )
            for child in root.children:
                if child.i > root.i:
                    print ( "child :", child.text )
                    rightChildren.append ( child.text )
                    for child2 in child.children:
                        if child2.i () < child.i:
                            print ( "child2 :", child2.text, child2.dep_ )
                            index = rightChildren.index ( child.text )
                            rightChildren.insert ( index - 1, child2.text )
                            break
                        if child2.i > child.i:
                            print ( "child2 :", child2.text, child2.dep_ )
                            index = rightChildren.index ( child.text )
                            rightChildren.insert ( index + 1, child2.text )

                    if child.dep_ != "dobj" or child.dep_ != "pobj" or child.dep_ != "iobj":
                        break

    if rightChildren:
        print ( rightChildren )
    goal = root.text + ' '.join ( rightChildren )
    return goal


def extract_object_phrase(sentence):
    doc = helperFunctions.nlp ( sentence )
    object_phrase = ''
    for token in doc:
        if token.dep_ == 'dobj':  # find the direct object
            # Traverse the subtree of the direct object to get the entire object phrase
            object_tokens = [ t for t in token.subtree ]
            object_phrase = ' '.join ( [ t.text for t in object_tokens ] )
            break
    print ( "object phrase 2 : ", object_phrase )
    return object_phrase
