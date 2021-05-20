#*******************************************************************************************#
#-------------------------------This class composition data---------------------------------#
#*******************************************************************************************#

class music(self):
    '''
    This is a container for all things related to a stand-alone music composition.

    music.melodies is an array of pretty_midi instruments with a single melody
    music.chords is an array of pretty_midi instruments with chords
    '''

    # Constructor
    def __init__(self):

        # Global tempo
        self.tempo = 0.0
        # Title
        self.title = ""
        # Array of melody() instruments
        self.melodies = []
        # Array of chord() objects (copied from newChordsFromScale())
        self.chords = []
    
    # Check if there's data in this instance
    def hasData(self):
        if(len(self.melodies) != 0 and 
           len(self.chords) != 0 and 
           self.tempo != 0.0):
            return True
        else:
            return False