#*******************************************************************************************#
#---------------------------This class handles single chord data----------------------------#
#*******************************************************************************************#

class chord():
    '''
    A class/container for managing all data relevant to a single chord. This contains the tempo (float: BPM), 
    a list for notes (strings: i.e. "C#2:"), a rhythm (float: duration in seconds), 
    and list for dynamics (int: MIDI velocity numbers).
    '''

    # Constructor
    def __init__(self):

        # Data
        self.tempo = 0.0
        self.notes = []
        self.rhythm = 0.0
        self.dynamics = []

    # Check if there's any data
    def hasData(self):
        '''
        Is there complete chord data? 
        If True, then all fields have been used.
        '''
        if(self.tempo != 0.0 and
            len(self.notes) != 0 and
            self.rhythm != 0.0 and
            len(self.dynamics) != 0):
            return True
        return False