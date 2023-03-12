from helperFunctions import nlp


class Actor ():

    def __init__(self, actorName):
        self.name = actorName
        self.usecases = [ ]

    def checkSimilarityB2UseCases(self, t1):

        t1tokens = nlp ( t1 )
        print ( "token -> ", t1 )
        for i, x in enumerate ( self.usecases ):
            v = x.find ( t1tokens [ 0 ].text )
            if v > -1:
                self.usecases [ i ] = x.replace ( x, t1 )
                print ( self.usecases [ i ] )
                return False

        return True

    def addUseCase(self, useCase):
        if self.checkSimilarityB2UseCases ( useCase ):
            self.usecases.append ( useCase )

###############################
