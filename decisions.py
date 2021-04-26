#****************************************************************************************************************#
#-------------------------------------This class handles decision functions------------=-------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------

    This module contains the decide() class which handles decisions for generative and variation functions. 

    Class hierarchy:
        
        decide():
            generate():
                note()
                rhythms()
                ect..
                
                Comp Modes:
                    random()
                    minimalist()
                    tonal()
                    atonal()
                    serialist()
                ect...

            variate()
                mainDecision():
                howManyNotes():
                ect..

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
import pretty_midi as pm
from pretty_midi import constants as inst
from random import randint

#Decision functions
class decide(object):
    '''
    These are the RNG functions that make "decisions" about a variety of creative questions.  
    Basically you roll some dice and see what happens.

    This is the BASE CLASS for all generative functions.
    '''

    # Constructor
    def __init__(self):

        # Used for rhythm modifications
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 
                        0.375, 0.25, 0.125]

    #-----------------------------------------------------------------------------------------------------------#
    #-----------------------------------------MATERIAL GENERATION-----------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------#

    # How many times should we repeat this note?
    def howManyRepetitions(self, notes):
        '''
        Determines how many times to repeat a note, scaled to
        the amount of rhythms generated for this melody.

        Returns 0 if supplied notes is null, and 1 if it
        receives an empty list
        '''
        if(notes is None):
            return 0
        elif(len(notes) == 0):
            return 1
        reps = 0
        '''Note: change to if(len(notes)) % 3 == 0), etc?
                 Use total notes as divisible by n as the decider rather than
                 total notes itself. I dunno.'''
        if(len(notes) > 10):
            #Limit to 1/5
            limit = math.floor(len(notes) / 5)
            reps = randint(1, limit)
        elif(len(notes) > 8):
            #Limit to 1/4
            limit = math.floor(len(notes) / 4)
            reps = randint(1, limit)
        elif(len(notes) > 6):
            #Limit to 1/3
            limit = math.floor(len(notes) / 3)
            reps = randint(1, limit)
        return reps

    # Choose melody parameters
    def melodyChoices(self):
        '''
        Choses parameters for melody generation. 
        Returns a list with each decision at a corresponding
        index.

        0 = rhythm choice (1 - 3)
        1 = dynamics choice (1 - 2)
        2 = tonality choice (1 - 2)
        3 = melodic range choice (1 - 4)
        4 = which single octave to use, if chosen (single int or None)
        5 = total elements (number of notes, rhythms, dynamics)
        '''
        choices = []

        #0 - Total elements (2-20)
        '''Determines total number of notes, rhythms, and dynamics.
           Each will be whatever randint() returns here.'''
        choices.append(randint(2, 20))

        #1 - Rhythm 
        '''Generate list of nonrepeating rhythms (1), a single repeated rhythm (2), 
           or alternate between non-repeat and repeat(3)?'''
        choices.append(randint(1, 3))

        #2 - Dynamics 
        '''Repeating single dynamic (1), non-repeating list(2), semi-repeating(3)?'''
        choices.append(randint(1, 3))

        #3 - Tonality: Tonal(1) or atonal(2)?
        choices.append(randint(1, 2))

        #4 - Melodic range
        '''Place notes in specified octave (1), used fixed range (2), 
           alternate between fixed octave and randomly chosen octaves (3),
           use randomly chosen octaves only (4)'''
        rangeChoice = randint(1, 4)
        choices.append(rangeChoice)

        #5 - Using one single octave (or not)
        if(rangeChoice == 1):
            # Which octave (2-6)?                     
            choices.append(randint(2, 6))
        else:
            choices.append(None)

        return choices

    # Choses a single instrument
    def newInstrument(self, tempo):
        '''
        Choses a MELODIC instrument from pretty_midi's container's module 
        which contains a mapping of integers to available MIDI instruments. 

        Returns a pretty_midi object containing the supplied tempo and the 
        newly chosen instrument. To be used for single instrument pieces.
        '''
        # Create new PrettyMIDI() instance
        newInstrument = pm.PrettyMIDI(initial_tempo = tempo)
        # Returns a string (I think) from the mapping
        # NOTE: Indices 0 - 110 are the MELODIC instruments in INSTRUMENT_MAP!
        instrument = inst.INSTRUMENT_MAP[randint(0, 110)]
        # Append to pm Instrument instance
        instrument = pm.Instrument(program = instrument)
        # Add to PrettyMIDI instance
        newInstrument.instruments.append(instrument)
        return newInstrument

    # Choses how many instruments to create (2 - 13 (for now))
    def howManyInstruments(self):
        return randint(2, 13)

    # Choses the instruments for a non-solo piece
    def newEnsemble(self, tempo):
        '''
        Generates a list of 2 - 13 MELODIC instruments. Does not 
        pick PERCUSSION instruments yet!

        Returns a pretty_midi object containing the supplied tempo and list of
        instruments. To be used for multi-instrument pieces.
        '''
        # Pick total number of instruments
        total = randint(2, 13)
        # Create new PrettyMIDI() instance
        newEnsemble = pm.PrettyMIDI(initial_tempo = tempo)
        # Select instruments
        while(len(newEnsemble.instruments) < total):
            # Returns a string (I think) from the mapping
            # NOTE: Indices 0 - 110 are the MELODIC instruments in INSTRUMENT_MAP!
            instrument = inst.INSTRUMENT_MAP[randint(0, 110)]
            # Append to pm Instrument object
            instrument = pm.Instrument(program = instrument)
            # Add to PrettyMIDI instance
            newEnsemble.instruments.append(instrument)
        return newEnsemble

