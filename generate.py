#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms ranging from pure "random"
    selections (see PRNG info), to more strict instructions. 

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
from random import randint
from midi import midiStuff as mid
from decisions import decide as choice
from containers.melody import melody

#Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms ranging from pure "random"
    selections (see PRNG info), to more strict instructions.  
    '''

    # Constructor
    def __init__(self):


        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#

        #--------Notes and Scales--------#

        # Enharmonically spelled note names starting on A. Indicies: 0-16. 
        self.noteNames = ["A", "A#", "Bb", "B", 
                          "C", "C#", "Db", "D", 
                          "D#", "Eb", "E", "F", 
                          "F#", "Gb", "G", "G#",
                          "Ab"]

        # Major Scales
        '''
        NOTE:
            We won't need to create extra scales if we want to create 
            some kind of "mood" feature (happy/sad) since those "moods" 
            are usually elicited from chord progressions. If we want that, 
            then I'll just add a function to generate some minor chords based
            off the scale chosen from the dicitonary below.
        '''
        # Use indicies 0 - 6
        self.scales = {1: ['C', 'D', 'E', 'F', 'G', 'A', 'B'], 
                       2: ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
                       3: ['D', 'E', 'F#', 'G', 'A', 'B', 'C#' ],
                       4: ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
                       5: ['E', 'F#', 'G#', 'A', 'B', 'C#', "D#"],
                       6: ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
                       7: ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
                       8: ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                       9: ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
                       10:['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                       11:['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
                       12:['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']}

     
        #-------------Rhythm--------------#
        '''
        Notes:

            Durations in seconds (1 = quarter note (60bpm))
            Whole note to 32nd note
            
                [0] 4 = whole note                                                          
                [1] 3 = dotted half
                [2] 2 = half note           
                [3] 1.5 = dotted quarter    
                [4] 1 = quarter             
                [5] 0.75 = dotted eighth
                [6] 0.5 = eighth
                [7] 0.375 = dotted sixteenth
                [8] 0.25 = sixteenth 
                [9] 0.125 = thirty-second

        '''
        # Rhythms (0-9)
        self.rhythms = [4.0, 3.0, 2.0, 1.5, 1.0, 0.75, 0.5, 
                        0.375, 0.25, 0.125]

        # Fast rhythms (0-8)
        self.rhythmsFast = [0.375, 0.28125, 0.25, 0.1875, 0.125, 0.09375, 
                            0.0625, 0.046875, 0.03125]

        # Slow rhythms (0-7) - [n2 = n1 + (n1/2)]
        self.rhythmsSlow = [8.0, 12.0, 18.0, 27.0, 
                            40.5, 60.75, 91.125, 136.6875]
        

        #------------Chords-------------#

        # Major, minor, augmented, and diminished triads
        self.triads = {1: [0,4,7], 2: [0,3,7], 
                       3: [0,4,8], 4: [0,3,6]}
        
  
        #------------Tempo-------------#

        # Tempos (indices: 0-38)
        self.tempo = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0, #1-9 (0-8)
                      60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, #10-18 (9-17)
                      92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
                      126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, #28-36 (27-35)
                      184.0, 200.0, 208.0] #37-39 (36-38)


        #-----------Dynamics------------#
        '''
        Note: MIDI velocity/dynamics range: 0 - 127
        '''

        # Dynamics (0-26)
        self.dynamics = [20, 24, 28, 32, 36, 40, 44, 48, 52,
                         56, 60, 64, 68, 72, 76, 80, 84, 88,
                         92, 96, 100, 104, 108, 112, 116, 120, 124]

        # Soft dynamics (0-8)
        self.dynamicsSoft = [20, 24, 28, 32, 36, 40, 44, 48, 52]

        # Medium dynamics (0-8)
        self.dynamicsMed = [56, 60, 64, 68, 72, 76, 80, 84, 88]

        # Loud dynamics (0-8)
        self.dynamicsLoud = [92, 96, 100, 104, 108, 112, 116, 120, 124]



    #--------------------------------------------------------------------------------#
    #-----------------------------Misc. Utility Functions----------------------------#
    #--------------------------------------------------------------------------------#


    # Convert base rhythms to values in a specified tempo
    def convert(self, newMelody):
        '''
        A rhythm converter function to translate durations in self.rhythms
        to actual value in seconds for that rhythm in a specified tempo. 
        
        ex: [base] q = 60, quarterNote = 1 sec, [new tempo] q = 72, quarterNote = 0.8333(...) sec

        60/72 = .83 - The result becomes the converter value to multiply all supplied
        durations against to get the new tempo-accurate durations.

        '''
        if(not newMelody):
            return -1
        diff = 60/newMelody.tempo
        for i in range(len(newMelody.rhythms) - 1):
            newMelody.rhythms[i] *= diff
        return newMelody


    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#

    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo between 40-208bpm.
        Returns a float upon success, 60.0 if fail.
        '''
        tempo = 0.0
        tempo = self.tempo[randint(0, len(self.tempo) - 1)]
        if (not tempo):
            return 60.0
        return tempo


    #-------------------------------------------------------------------------------#
    #-------------------------------------Pitch-------------------------------------#
    #-------------------------------------------------------------------------------#

    # Converts a given integer to a pitch class in a specified octave (ex C#6)
    def newNote(self, num, octave):
        '''
        Converts a given integer to a pitch class in a specified octave (ex C#6)
        '''
        if(num > len(self.noteNames) - 1):
            return -1
        if(octave < 1 or octave > 8):
            return -1
        newNote = self.noteNames[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote


    #-----------------------------------------------------------------------------------#
    #--------------------------------------Rhythm---------------------------------------#
    #-----------------------------------------------------------------------------------#

    #Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        return rhythm

    #Pick a fast duration
    def newRhythmFast(self):
        '''
        Generate a single new fast rhythm
        '''
        rhythm = self.rhythmsFast[randint(0, len(self.rhythmsFast) - 1)]
        return rhythm
    
    #Pick a slow duration
    def newRhythmSlow(self):
        '''
        Generate a single new slow rhythm
        '''
        rhythm = self.rhythmsSlow[randint(0, len(self.rhythmsSlow) - 1)]
        return rhythm

    #Generate a list containing a rhythmic pattern
    def newRhythms(self, total):
        '''
        Generate lists of 2-20 rhythms to be used as a 
        melody/ostinato/riff/whatever. Uses infrequent repetition.

        Algorithm:
            1. Pick pattern length (l) 
            2. Pick duration.
            3. Repeat duration or pick another?
                3.1. If repeat, how many times (r < l)?
                3.2. If not, repeat steps 2-3 while duration total < l.
        '''
        rhythms = []
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            #Pick rhythm + add to list    
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            #Repeat this rhythm or not? 1 = yes, 2 = no
            repChoice = randint(1, 2) 
            if(repChoice == 1):
                #Limit reps to no more than 1/3 of the total no. of rhythms
                limit = math.floor(len(rhythms)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 1
                reps = randint(1, limit) 
                for i in range(reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == total):
                        break
            else:
                if(rhythm not in rhythms):
                    rhythms.append(rhythm)

            print("Total:", len(rhythms))

        if(not rhythms):
            print("...Unable to generate pattern!")
            return -1
        return rhythms


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    #Generate a single dynamic (to be used such that a passage doesn't have consistenly
    #changing dynamics)
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        dynamic = self.dynamics[randint(0, len(self.dynamics) - 1)]
        return dynamic

    #Generate a soft dynamic
    def newDynamicSoft(self):
        '''
        Generates a single soft dynamic
        '''
        dynamic = self.dynamicsSoft[randint(0, len(self.dynamicsSoft) - 1)]
        return dynamic

    #Generate a medium dynamic
    def newDynamicMed(self):
        '''
        Generates a single medium dynamic
        '''
        dynamic = self.dynamicsMed[randint(0, len(self.dynamicsMed) - 1)]
        return dynamic

    #Generate a loud dynamic.
    def newDynamicLoud(self):
        '''
        Generates a single loud dynamic
        '''
        dynamic = self.dynamicsLoud[randint(0, len(self.dynamicsLoud) - 1)]
        return dynamic

    #Generate a list of dynamics. 
    def newDynamics(self, total):
        '''
        Generates a list of dynamics (MIDI velocites). Total supplied from elsewhere.
        Uses infrequent repetition. Returns -1 if unable to generate a list.
        '''
        dynamics = []
        print("\nGenerating", total, "semi-reapeating dynamics...")
        while(len(dynamics) < total):
            #Pick dynamic    
            dynamic = self.dynamics[randint(0, 9)]
            #Repeat this dynamic or not? 1 = yes, 2 = no
            repChoice = randint(1, 2) 
            if(repChoice == 1):
                #Limit reps to no more than 1/3 of the supplied total
                limit = math.floor(total/3)
                '''Note: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 1
                reps = randint(1, limit) 
                for i in range(reps):
                    dynamics.append(dynamic)
                    if(len(dynamics) == total):
                        break
            else:
                if(dynamic not in dynamics):
                    dynamics.append(dynamic)
        if(not dynamics):
            print("...Unable to generate pattern!")
            return -1
        return dynamics


    #-----------------------------------------------------------------------------------#
    #-------------------------------------Scales----------------------------------------#
    #-----------------------------------------------------------------------------------#


    #Generate a new scale with pitch classes.
    def newScale(self, data):
        '''
        Generate a new scale with pitch classes with enharmonic spellings
        in the middle octave (4)
        '''
        if(data is None):
            return -1
        # How many notes do we need?
        total = len(data) - 1
        # What key are we in?
        pc = self.scales(randint(1, 12))

        # i = 0
        # scale = []
        # octave = 4
        # pcScale = self.newScale()
        # print("\nGenerating scale with pitch classes...")
        # while(len(scale) < len(pcScale)):
        #     note = self.chromaticScaleSharps[pcScale[i]]
        #     note = "{}{}".format(note, octave)
        #     scale.append(note)
        #     i += 1
        # #Test output
        # if(not scale):
        #     print("...Unable to generate scale!")
        #     return -1
        # print("New scale:", scale)
        # return scale



    #--------------------------------------------------------------------------------#
    #--------------------------------------Chords------------------------------------#
    #--------------------------------------------------------------------------------#


    #Generate a pitch class triad set
    def newPCTriad(self):
        '''
        Generate a pitch class triad set in prime form.
        '''
        print("\nGenerating new PC triad...")
        triad = []
        while(len(triad) < 3):
            note = randint(0, 11)
            if(note not in triad):
                triad.append(note)
        triad.sort()
        if(not triad):
            print("...No PC triad generated!")
            return -1
        print("New PC triad:", triad)
        return triad

    #Generates a series of pitch class sets
    def newPCChords(self):
        '''
        Generates a series of pitch class sets
    
        Note:
            Select from structures class - decide on what chord to use. 
            add ability to select chord, and when translating the integers to
            note names, randomly assign octChoice to each note name. Adds possibility
            of unusual voicings.
        '''
        print("\nGenerating chord progression...")
        i = 0
        newChords = []
        #3-10 chords
        totalChords = randint(3, 10)
        if(not totalChords):
            print("...No amount decided!")
        print("Total new PC chords:", totalChords)
        #Are we generating tertian(1), symmetrical(2), or mixed chord3?
        chordChoice = randint(1, 3)
        if(not chordChoice):
            print("...No chord type decision!")
        #If we're using triads
        if(chordChoice == 1):
            while(i < totalChords):
                newChords.append(self.triads[randint(1, 4)])
                i += 1
        #If we're using symmetrical chords
        elif(chordChoice == 2):
            while(i < totalChords):
                newChords.append(self.symChords[randint(1, 4)])
                i += 1
        #If we're using both
        elif(chordChoice == 3):
            thisChoice = 0
            while(i < totalChords):
                thisChoice = randint(1, 2)
                if(thisChoice == 1):
                    newChords.append(self.triads[randint(1, 4)])
                newChords.append(self.symChords[randint(1, 4)])
                i += 1
        if(not newChords):
            print("...No progression generated!")
            return -1
        print("New progression:", newChords)
        return newChords      

    #Generate 3 random pitches in random octaves to form a triad
    def newPitchTriad(self):
        '''
        Generate 3 random pitches in random octaves to form a triad (i.e. C3, Ab7, Db2, etc.)
        '''
        print("\nGenerating new pitch triad...")
        triad = []
        while(len(triad) < 3):
            note = self.note()
            if(note not in triad):
                triad.append(note)
        if(not triad):
            print("...Unable to generate pitch triad!")
            return -1
        print("New pitch triad:", triad)
        return triad


    #Generates a chromatic chord with 2-9 notes in random octaves
    def newChord(self):
        '''
        Generates a chromatic chord with 2-9 notes in 
        random octaves. Returns -1 if new chord is None/null.
        '''
        chord = []
        totalNotes = randint(2, 9)
        while(len(chord) < totalNotes):
            note = self.note()
            if(note not in chord):
                chord.append(note)
        if(not chord):
            return -1
        return chord

    '''
    Note:
        Create function that generates chords and repeats each one individually
        n number of times.

        ALGORITHM: 
            1. Generate chord.
            2. Repeat this chord?
                2.1. If so, how many times in a row?
                2.2. If not, go back to 1. 
    '''

    #Generates a series of random chromatic chords 
    def newChords(self):
        '''
        Generates 3-10 non-repeating chromatic chords in
        various octaves and spellings. Returns -1 if newChords
        is None/null.
        '''
        print("\nGenerating random chord progression...")
        chord = []
        newChords = []
        #3-10 chords
        totalChords = randint(3, 10)
        while(len(newChords) < totalChords): 
            chord = self.newChord()
            if(chord not in newChords):
                newChords.append(chord)
        if(not newChords):
            print("...No progression generated!")
            return -1
        print("Total chords:", totalChords)
        print("New progression:", newChords)
        return newChords

    #Generates a progression from the notes of a given scale
    def newChordsFromScale(self, scale):
        '''
        Generates a progression from the notes of a given scale.
        Returns 0 if recieving bad input, and -1 if generation was unsuccessfull. 
        '''
        if(scale is None):
            return 0
        print("\nGenerating chords from a given scale...")
        print("Given scale:", scale)
        #How many chords?
        chords = []
        total = randint(3, 10)
        print("\nGenerating", total, "chords...")
        #Pick notes
        while(len(chords) < total):
            chord = []
            #How many notes in this chord?
            totalNotes = randint(2, 9)
            while(len(chord) < totalNotes):
                note = scale[randint(0, len(scale) - 1)]
                if(note not in chord):
                    chord.append(note)
                elif(note in chord and len(chord) > 2):
                    break
            chords.append(chord)
        if(not chords):
            print("...Unable to generate chords!")
            return -1
        print("\nTotal chords:", len(chords))
        print("Chords:", chords)
        return chords





    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    #Generate a melody. 
    def newMelody(self, data):
        '''
        Picks a new tempo, rhythmic pattern, set of dynamics (or single dynamic), and
        notes. Notes are picked using the array generated by newScale(). Rhythms and
        dynamics are picked randomly; the total for both is determined by the number of 
        notes generated

        Appends to pretty_midi object and returns new MIDI object. Also exports a MIDI file.
        '''

        #Melody container object
        newMelody = melody()

        print("\nGenerating melody...")

        #---------------------Initial choices---------------------#

        #Pick tempo
        newMelody.tempo = self.newTempo()

    
            
        #----------------------Generate--------------------------#

        #Pick the notes
        print("\nPicking notes...")
        while(len(newMelody.notes) < len(newMelody.rhythms)):

            #Using single octave
            if(choices[3] == 1):
                note = self.aNote(choices[4])
            #Using limited range of octaves
            elif(choices[3] == 2):
                note = self.aNote(octaves[randint(0, len(octaves) - 1)])
            #Use random alteration between fixed range/random octaves
            elif(choices[3] == 3):
                #Random octave(1) or select from fixed range (2)?
                if(randint(1, 2) == 1):
                    note = self.note()
                else:
                    note = self.aNote(octaves[randint(0, len(octaves) - 1)])
            #Use random octaves
            elif(choices[3] == 4):
                note = self.note()

            #Repeat this note (1) or not (2)?
            repeat = randint(1, 2)

            #Repeat
            if(repeat == 1):
                #Repeat this note r times(reps)
                r = 0
                reps = 0
                #If 1 < notes < 5, repeat between 1 and 3 times 
                if(len(newMelody.notes) < 6 and len(newMelody.notes) > 0):
                    reps = randint(1, 3)
                #Otherwise scale repetitions
                else:
                    reps = choice.howManyRepetitions(self, newMelody.notes)
                while(r < reps):
                    newMelody.notes.append(note)
                    r += 1
                    if(len(newMelody.notes) == choices[0]):
                        break
            #Dont repeat
            elif(repeat == 2):
                if(note not in newMelody.notes):
                    newMelody.notes.append(note)

        #Add data to MIDI object and write out file.
        if(mid.saveMelody(self, newMelody) == -1):
            return -1

        #Display results
        print("\nRESULTS:")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

        return 0