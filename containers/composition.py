#*******************************************************************************************#
#-------------------------------This class composition data---------------------------------#
#*******************************************************************************************#

class music(self):
    '''
    This is a container for all things related to a stand-alone music composition. Data includes
    a global tempo, the piece's title, an array of melody() objects, and an array of chord() objects.
    '''

    # Constructor
    def __init__(self):

        # Global tempo
        self.tempo = 0.0
        # Title
        self.title = ""
        # Array of melody() objects
        self.melodies = []
        # Array of chord() objects
        self.chords = []
    
    # Check if there's data in this instance
    def hasData(self):
        '''
        Check if this piece has data (does not check for title!)
        '''
        if(len(self.melodies) != 0 and 
           len(self.chords) != 0 and 
           self.tempo != 0.0):
            return True
        else:
            return False