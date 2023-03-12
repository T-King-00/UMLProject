import helperFunctions


class classDiagram:

    def get_classes(sent, actorslist):
        global classes
        classes = set ()
        if not sent.endswith ( "." ):
            sent += "."
            business_env = [ "database", "record", "system", "information", "organization", "detail", "website",
                             "computer" ]
            doc = helperFunctions.nlp ( sent )
            skip_next = False

            for i, token in enumerate ( doc ):
                # Check if we need to skip the token
                if skip_next:
                    skip_next = False
                    continue

                # Check if the token is a noun and do not appear in business_env
                if token.pos_ == "NOUN" and token.text not in business_env:
                    # Check if the next token is a noun (compound)
                    if token.dep_ == "compound":
                        element = token.lemma_ + ' ' + doc [ i + 1 ].lemma_
                        if any ( obj.name == element for obj in actorslist ):
                            skip_next = True  # Skip the next token
                            continue
                        classes.add ( token.lemma_ + '_' + doc [ i + 1 ].lemma_ )
                        skip_next = True  # Skip the next token

                    # Check if the next token is a gerund
                    elif doc [ i + 1 ].tag_ == "VBG":
                        classes.add ( token.lemma_ + '_' + doc [ i + 1 ].text )
                        skip_next = True  # Skip the next token

                    # if the next token is nor a noun nor a gerund, add the token as a class
                    else:
                        classes.add ( token.lemma_ )

                # Check if the token is a gerund
                elif token.tag_ == "VBG":
                    # Check if the next token is a noun
                    if doc [ i + 1 ].pos_ == "NOUN":
                        classes.add ( token.text + '_' + doc [ i + 1 ].lemma_ )
                        skip_next = True  # Skip the next token

            return classes

    deps_attr = [ "pobj", "dobj", "conj" ]
    deps_class = [ "nsubj", "nsubjpass", "conj", "attr" ]

    def add_to_attributes(classes_attr, sent, token):
        if token not in classes_attr.keys ():
            try:
                classes_attr [ list ( sent.root.children ) [ 0 ].lemma_ ].add ( token )
            except KeyError:
                pass
        return classes_attr

    def discard_attr_from_classes(classes_attr, attribute):
        for cls in classes_attr.keys ():
            if attribute in classes_attr [ cls ]:
                classes_attr [ cls ].discard ( attribute )
        return classes_attr

    def add_to_classes(classes_attr, sent, token):
        if token not in classes_attr.keys ():
            classes_attr [ token ] = set ()
        else:
            classes_attr [ token ].add ( token )
        classes_attr = classDiagram.discard_attr_from_classes ( classes_attr, token )
        return classes_attr

    def get_classes_attributes(text):
        classes_attr = {}
        doc = helperFunctions.nlp ( text )
        for sent in doc.sents:
            for token in sent:
                if token.pos_ == "NOUN":
                    # attribute
                    if token.dep_ in classDiagram.deps_attr:
                        classes_attr = classDiagram.add_to_attributes ( classes_attr, sent, token.lemma_ )
                    # class
                    elif token.dep_ in classDiagram.deps_class:
                        classes_attr = classDiagram.add_to_classes ( classes_attr, sent, token.lemma_ )
        return classes_attr

    def getClasses1(sent, actorslist):
        classes = set ()

        if not sent.endswith ( "." ):
            sent += "."

        doc = helperFunctions.nlp ( sent )
        skip_next = False

        for i, token in enumerate ( doc ):
            # Check if we need to skip the token
            if skip_next:
                skip_next = False
                continue
            # case 1
            if token.dep_ == "subj" and token.pos_ == "NOUN":
                classes.add ( token.lemma_ )
            if token.dep_ == "dobj":
                classes.add ( token.lemma_ )

            prepositions = [ "to", "of", "for" ]
            if token.dep_ == "case" and token.text in prepositions:
                classes.add ( doc [ i + 1 ].lemma_ )

        return classes

    def test_next_attr(doc, i):
        list__ = set ()
        br = 0
        while (br != 1):
            if doc [ i + 1 ].text == "," or ";":
                if doc [ i + 2 ].text == "and" and doc [ i + 3 ].pos_ == "PRON":
                    list__.add ( doc [ i + 4 ].lemma_ )
                if doc [ i + 2 ].pos_ == "PRON":
                    list__.add ( doc [ i + 3 ].lemma_ )
                else:
                    list__.add ( doc [ i + 2 ].lemma_ )
                # if doc[i+2].pos_ != "PRON" and (doc[i+2].tag_ != "NN" or "NNS"):
                #     br = 1
            elif doc [ i + 1 ].text == "and":
                if doc [ i + 2 ].pos_ == "PRON":
                    list__.add ( doc [ i + 3 ].lemma_ )
                else:
                    list__.add ( doc [ i + 2 ].lemma_ )
            elif doc [ i + 1 ].pos_ == "PRON":
                list__.add ( doc [ i + 2 ].lemma_ )
            if doc [ i + 1 ].text == ".":
                br = 1
            i = i + 1
        return list__

    def get_attributes(text):
        global classes
        doc = helperFunctions.nlp ( text )
        # attributes_noun_phrase_main = set()
        # relationship_attributes = set()
        concept_attributes = set ()
        specific_indicators = {"type", "number", "date", "reference", "no", "code", "volume", "birth", "id", "address",
                               "name"}
        for i, token in enumerate ( doc ):
            # #A1
            # if token.tag_== "JJ":
            #     attributes_noun_phrase_main.add(token.lemma_)
            # #A2
            # if token.tag_ == "RB":
            #     if doc[i+1].pos_ == "VERB" and doc[i+1].pos_ != "ADJECTIVE":
            #         relationship_attributes.add(token.lemma_)
            # A3
            if token.tag_ == "POS":
                concept_attributes.add ( doc [ i + 1 ].lemma_ )
                classes.discard ( doc [ i + 1 ].lemma_ )
                if doc [ i - 2 ].text == "and":
                    concept_attributes.add ( doc [ i - 3 ].lemma_ )
                    classes.discard ( doc [ i - 3 ].lemma_ )
            # #A4
            # if token.text == "of":
            #     concept_attributes.add(doc[i-1].lemma_)
            #     classes.discard(doc[i-1].lemma_)
            if token.tag_ == "NN" or token.tag_ == "NNS":
                if doc [ i - 1 ].tag_ == "IN":
                    if doc [ i - 2 ].pos_ == "VERB":
                        concept_attributes.add ( token.lemma_ )
                        classes.discard ( token.lemma_ )
                        if i < len ( doc ):
                            if doc [ i + 1 ].text == "and":
                                concept_attributes.add ( doc [ i + 2 ].lemma_ )
                                classes.discard ( doc [ i + 2 ].lemma_ )
            # A+
            if token.text == "by":
                if doc [ i + 1 ].pos_ == "PRON":
                    concept_attributes.add ( doc [ i + 2 ].lemma_ )
                    classes.discard ( doc [ i + 2 ].lemma_ )
                    list__ = classDiagram.test_next_attr ( doc, i + 2 )
                    for l in list__:
                        concept_attributes.add ( l )
                        classes.discard ( l )
                else:
                    concept_attributes.add ( doc [ i + 1 ].lemma_ )
                    classes.discard ( doc [ i + 1 ].lemma_ )
                    # list__ = test_next_attr(doc, i+2)
                    # for l in list__:
                    #     concept_attributes.add(l)
                    #     classes.discard(l)
            # A5
            if token.text == "have" and doc [ i - 1 ].text == "to":
                concept_attributes.add ( doc [ i + 1 ].lemma_ )
                classes.discard ( doc [ i + 1 ].lemma_ )
            # A6
            if token.text in specific_indicators:
                concept_attributes.add ( token.lemma_ )
                classes.discard ( token.lemma_ )
                if i < len ( doc ):
                    if doc [ i + 1 ].text == "," and (doc [ i + 2 ].tag_ == "NN" or "NNS"):
                        concept_attributes.add ( doc [ i + 2 ].lemma_ )
                        classes.discard ( doc [ i + 2 ].lemma_ )
                    elif doc [ i + 1 ].tag_ == "NN" or "NNS":
                        concept_attributes.add ( doc [ i + 1 ].lemma_ )
                        classes.discard ( doc [ i + 1 ].lemma_ )
            ############################################################################
            # if token.text in concept_attributes:
            #     list__ = test_next_attr(doc, i+2)
            #     for l in list__:
            #         concept_attributes.add(l)
            #         classes.discard(l)
        return concept_attributes  # , relationship_attributes,attributes_noun_phrase_main

    def text_to_uml(text):
        uml = {}
        entities = classDiagram.get_classes ( text )
        attributes = classDiagram.get_attributes ( text )
        for entity in entities:
            uml [ entity ] = [ ]
        for attribute in attributes:
            entity = classDiagram.get_entity ( text, attribute, entities )
            if entity:
                uml [ entity ].append ( (attribute, classDiagram.get_attribute_type ( attribute )) )

        inheritance, relationship, object, object_inh = classDiagram.get_relations ( text )
        return uml, inheritance, relationship, object, object_inh
