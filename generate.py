#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.  

----------------------------------------------------------------------------------------------------------------
'''

#IMPORTS
import math
from random import randint
from datetime import datetime
from midi import midiStuff as mid
from containers.melody import melody

#Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.

    NOTE:
    
    Consolidate newRhythms() and newDynamics() into single generative loop, with an
    additional 'type' (int) argument. Each type chooses which resource data to draw from.

    '''

    # Constructor
    def __init__(self):


        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#


        # ----------------------------Letters---------------------------------#  

        '''
        NOTE:
            Used to search against and return an integer representing an 
            Array index. The array will be used to generate a scale from
            whos total is the len(alphabet) - 1
        '''

        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u',
                         'v', 'w', 'x', 'y', 'z']

        #-----------------------Notes and Scales------------------------------#

        # Enharmonically spelled note names starting on A. Indicies: 0-16.
        '''
        NOTE: 
            Interval mappings for enhamonicly spelled chromatic scale array starting on A
                0 = unison
                1, 2 = half-step
                3 = whole-step
                4 = minor third
                5, 6 = major third
                7 = perfect 4th
                8, 9 = tritone
                10 = perfect 5th
                11 = minor 6th
                12, 13 = major 6th/dim 7th
                14 = minor 7th
                15, 16 = major 7th
        '''
        self.notes = ["A", "A#", "Bb", "B", 
                      "C", "C#", "Db", "D", 
                      "D#", "Eb", "E", "F", 
                      "F#", "Gb", "G", "G#",
                      "Ab"]

        # Major Scales
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

     
        #---------------------------Rhythm-----------------------------------#

        '''
        NOTE:
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
        
  
        #----------------------------Tempo-----------------------------------#

        # Tempos (indices: 0-38)
        self.tempos = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0, #1-9 (0-8)
                       60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, #10-18 (9-17)
                       92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
                       126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, #28-36 (27-35)
                       184.0, 200.0, 208.0] #37-39 (36-38)


        #--------------------------Dynamics---------------------------------#
        
        '''
        NOTE: MIDI velocity/dynamics range: 0 - 127
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



    #-----------------------------------------------------------------------------------------#
    #-----------------------------Conversion and Utility Functions----------------------------#
    #-----------------------------------------------------------------------------------------#

    # Display newMelody() object data
    def display(self, newMelody):
        '''
        Display newMelody() object data
        '''
        if(newMelody.hasData() == False):
            print("ERROR: no melody data!")
            return -1

        print("\n-----------MELODY Data:------------")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

        return 0

    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''Converts an array of floats to an array of ints'''
        print("\nConverting floats to ints...")
        if(len(data) == 0):
            print("ERROR: no data inputted!")
            return -1
        result = []
        for i in range(len(data)):
            result.append(int(data[i]))
        return result

    # Scale individual data set integers such that i = i < len(dataSet) - 1
    def scaleTheScale(self, data):
        '''
        Returns no. of times data[i] is divisible by the total number of elements 
        in the structure it's in. This will keep the newly inputted data array's 
        values within the bounds of the scale array. These values function as a 
        collection of index numbers to randomly chose from in order to pick note 
        strings from the scale array.

        NOTE: Current method introduces a bias towards the notes in the lower indices
              of the total array (at least the first third). 

        '''
        print("\nScaling input...")
        if(len(data) == 0):
            print("ERROR: no data inputted") 
            return -1
        for i in range(len(data) - 1):
            if(data[i] > len(data) - 1):
                # Which scaling method should we use?
                s = randint(1, 3)
                # Divide data[i] by len(data) - 1
                if(s == 1):
                    print("...dividing by len(data) - 1!")
                    data[i] = math.floor(data[i] / len(data) - 1)
                # Subtract by len(data) - 1    
                elif(s == 2):
                    print("...subtracting by len(data) - 1!")
                    while(data[i] > len(data) - 1):
                        data[i] -= len(data) - 1
                # Subtract by 1                    
                else:
                    print("...subtracting by 1!")
                    while(data[i] > len(data) - 1):
                        data[i] -= 1
        print("\nnew data:", data)
        return data

    # Maps letters to index numbers
    def mapLettersToNumbers(self, letters):
        '''
        Maps letters to index numbers, which will then be 
        translated into notes (strings).
        '''
        print("\nMapping letters to index numbers...")
        if(len(letters) == 0): 
            print("ERROR: no data inputted!")
            return -1
        # Make all uppercase characters lowercase
        for i in range(len(letters) - 1):
            if(letters[i].isupper() == True):
                letters[i] = letters[i].lower()
        numbers = []
        # Pick a letter
        for i in range(len(letters)):
            # Search alphabet letter by letter
            for j in range(len(self.alphabet) - 1):
                # If we get a match, store that index number
                if(letters[i] == self.alphabet[j]):
                    numbers.append(j)
        if(len(numbers) == 0):
            print("ERROR: no index numbers found!")
            return -1
        return numbers
    
    # Convert a hex number representing a color to an array of integers
    def hexToIntArray(self, hex):
        '''
        Converts a prefixed hex number to an array of integers.

        Algorithm:
            1. Convert to integer
            2. Break single integer into array of individual integers (ex 108 to [1, 0, 8])
               using list comprehension
        '''
        if(hex == 0 or hex == None):
            print("ERROR: Invalid input!")
            return -1
        # Convert to int
        hexStr = int(hex, 0)
        # Convert to array of ints (ie. 132 -> [1, 3, 2])
        numArr = [int(x) for x in str(hexStr)]
        # Make sure any ints aren't greater than len(numArr) - 1
        for i in range(len(numArr) - 1):
            if(numArr[i] > len(numArr) - 1):
                while(numArr[i] > len(numArr) - 1):
                    numArr[i] -= 1
        return numArr

    # Auto generate a file name (date:time)
    def newFileName(self, fileType):
        '''
        Takes a string as an argument, returns a string 
        with the format: name - date:time
        
        NOTE: maybe the date module is causing the OS error?
        '''
        # Get date and time.
        date = datetime.now()
        # Convert to str d-m-y (hh:mm:ss)
        dateStr = date.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        # Merge date and file type
        fileName = "{}{}".format(fileType, dateStr)
        return fileName


    #--------------------------------------------------------------------------------#
    #-------------------------------------Tempo--------------------------------------#
    #--------------------------------------------------------------------------------#


    # Picks the tempo
    def newTempo(self):
        '''
        Picks tempo between 40-208bpm.
        Returns a float upon success, 60.0 if fail.
        '''
        print("\nPicking tempo...")
        tempo = 0.0
        tempo = self.tempos[randint(0, len(self.tempos) - 1)]
        if(tempo == 0.0):
            return 60.0
        return tempo


    #-------------------------------------------------------------------------------#
    #-------------------------------------Pitch-------------------------------------#
    #-------------------------------------------------------------------------------#

    # Converts a given integer to a pitch in a specified octave (ex C#6)
    def newNote(self, num, scale, octave):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6).
        Requires an integer, a given scale, and the required octave. 
        Returns a single string.
        '''
        if(num > len(scale) - 1): return -1
        if(octave < 1 or octave > 8): return -1
        newNote = scale[num]
        newNote = "{}{}".format(newNote, octave)
        return newNote

    # Generate a series of notes based off an inputted array of integers
    '''
    NOTE: Should newNotes()'s total output be contingent on the total data elements
          inputted? Is there a way to scale integers to a randomly chosen indicie within
          the bounds of a new array of notes that's already been generated? Probably.
    '''
    def newNotes(self, data, isLetters):
        '''
        Generate a series of notes based on inputted data (an array of integers)
        This randomly picks the key and the starting octave! 

        NOTE:
            Long data sets will have the same note associated with different 
            values elsewhere in the array. 
            
            If we ascend through the available octaves we can pick a new 
            key/scale and cycle through the octaves again. This will allow for 
            some cool chromaticism to emerge rather "organiclly" while minimizing
            the amount of repeated notes associated with different elements in 
            the data array (unless we get the same scale chosen again, or there's
            a lot of common tones between the scales that are picked) .  
        '''
        if(len(data) == 0):
            print("ERROR: no data inputted!")
            return -1

        # Pick starting octave (1 - 3)
        octave = randint(1, 3)

        # Pick initial root/starting scale (major or minor)
        root = self.scales[randint(1, 12)]
        # Will this be a minor scale (0 = no, 1 = yes)?
        isMinor = False
        if(randint(0, 1) == 1):
            isMinor = True
            root = self.convertToMinor(root)

        # Display choices
        if(isMinor == True):
            print("\nGenerating", len(data), "notes starting in the key of", root[0], "minor")
        else:
            print("\nGenerating", len(data), "notes starting in the key of", root[0], "major")
        '''
        Note generation algorithm:

            1. Total notes is equivalent to number of notes in data set.
                1b. Maybe if data-sets exceed a certain length, we can 
                    create a subset of available notes that is divisible
                    by the total number elements in the data set
            2. Generate a starting key/scale, and a starting octave.
            3. Cycle through this scale appending each note to a list
               of available notes until we reach the last note in the scale
               in octave 6.
            4. If we reach this note, reset octave to starting point, and 
               pick a new starting scale at random.
            5. Repeat steps 3-4 until we reach the end of the supplied data set.
        '''    
        #-----Generate notes to pick from-----#

        # If recieving letters, use this loop!
        if(isLetters == True):
            # Find highest value in int array from letters. 
            # This is the limit for how many notes to generate. 
            scale = []
            total = max(data)
            for i in range(total):
                note = "{}{}".format(root[n], octave)
                scale.append(note)
                n += 1
                '''NOTE: At most, the alphabet will map to 4 1/3 octaves.
                         Still didn't want to exceed octave 6'''
                if(i % 6 == 0):
                    octave += 1
                    if(octave > 6):
                        octave = randint(1, 3)
                        root = self.scales[randint(1, 12)]
                        # Re-decide if we're using minor (1) or major (2) again
                        if(randint(1, 2) == 1):
                            isMinor = True
                            print("Switching to a minor key!")
                        else:
                            isMinor = False
                            print("Staying in a major key!")
                        if(isMinor == True):
                            root = self.convertToMinor(root)
                            print("Key-change! Now using", root[0], "minor")
                        else:
                            print("Key-change! Now using", root[0], "major")
                    # Reset n to stay within len(root)
                    n = 0
        # Otherwise, this one!
        else:
            n = 0
            scale = []
            for i in range(len(data)):
                note = "{}{}".format(root[n], octave)
                scale.append(note)
                n += 1
                # If we've reached the end of the root scale,
                # increment the octave (until octave 6) 
                if(i % 6 == 0):
                    octave += 1
                    # If we reach highest octave (6), chose new
                    # starting octave and root
                    if(octave > 6):
                        octave = randint(1, 3)
                        root = self.scales[randint(1, 12)]
                        # Re-decide if we're using minor (1) or major (2) again
                        if(randint(1, 2) == 1):
                            isMinor = True
                            print("Switching to a minor key!")
                        else:
                            isMinor = False
                            print("Staying in a major key!")
                        if(isMinor == True):
                            root = self.convertToMinor(root)
                            print("Key-change! Now using", root[0], "minor")
                        else:
                            print("Key-change! Now using", root[0], "major")
                    # Reset n to stay within len(root)
                    n = 0
        # Pick notes according to integers in data array
        notes = []
        for i in range(len(data) - 1):
            notes.append(scale[data[i]])
        # Check results
        if(len(notes) == 0):
            print("ERROR: Unable to generate notes!")
            return -1
        return notes

    # Generate a scale of n length to be picked from in newNotes()
    '''
    NOTE: 
        Make a generation function that builds scales off randomly chosen
        intervals, rather than a pre-defined major scale. Each sub-set/sub-scale
        must span one octave. 
    '''

    # Returns a randomly generated scale within one octave to be used
    # as a 'root'
    def newScale(self, octave):
        '''
        Requires a starting octave. Returns a randomly generated scale 
        within one octave to be used as a 'root'. Returns -1 on failure.

        NOTE: Might return enharmonically spelled notes, which will just 
              sound like the same note being played twice to the user. 
              See the interval/index mapping in the note above the array.
        '''
        print("\nGenerating new root scale...")
        pcs = []
        # generate an ascending set of integers/note array indices starting
        # with a randomly chosen note.
        n = randint(0, 16)
        while(len(pcs) < 8):
            # add it
            pcs.append(n)
            # remove any duplicates
            pcs = list(set(pcs))
            # pick another
            n = randint(0, 16)
        # sort in ascending order
        pcs.sort()
        # convert to strings
        scale = []
        for i in range(len(scale) - 1):
            note = "{}{}".format(self.notes[pcs[i]], octave)
            scale.append(note)
        if(len(scale) == 0):
            print("ERROR: unable to generate scale!")
            return -1
        return scale

    # Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        print("\nConverting scale to relative minor...")
        if(len(scale) == 0):
            print("ERROR: no scale inputted!")
            return -1
        k = 5
        minorScale = []
        for i in range(len(scale)):
            minorScale.append(scale[k])
            k += 1
            if(k > len(scale) - 1):
                k = 0
        if(len(minorScale) == 0):
            print("ERROR: unable to generate minor scale!")
            return -1
        return minorScale


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

    #Generate a list containing a rhythmic pattern
    def newRhythms(self, total):
        '''
        Generates a series of rhythms of n length, where n is supplied
        from elsewhere.
        '''
        rhythms = []
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            #Pick rhythm and add to list    
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            #Repeat this rhythm or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                #Limit reps to no more than 1/3 of the total no. of rhythms
                limit = math.floor(len(rhythms)/3)
                '''Note: This limit will increase rep levels w/longer list lengths
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit) 
                for i in range(reps):
                    rhythms.append(rhythm)
                    if(len(rhythms) == total):
                        break
            else:
                if(rhythm not in rhythms):
                    rhythms.append(rhythm)
        if(len(rhythms) == 0):
            print("ERROR: Unable to generate pattern!")
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

    #Generate a list of dynamics. 
    def newDynamics(self, total):
        '''
        Generates a list of dynamics (MIDI velocites) of n length, 
        where n is supplied from elsewhere. Uses infrequent repetition.
        '''
        dynamics = []
        print("\nGenerating", total, "dynamics...")
        while(len(dynamics) < total):
            #Pick dynamic    
            dynamic = self.dynamics[randint(0, 9)]
            #Repeat this dynamic or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                #Limit reps to no more than 1/3 of the supplied total
                limit = math.floor(total/3)
                '''Note: This limit will increase rep levels w/longer totals
                         May need to scale for larger lists'''
                if(limit == 0):
                    limit += 2
                reps = randint(1, limit) 
                for i in range(reps):
                    dynamics.append(dynamic)
                    if(len(dynamics) == total):
                        break
            else:
                if(dynamic not in dynamics):
                    dynamics.append(dynamic)
        if(len(dynamics) == 0):
            print("ERROR: Unable to generate pattern!")
            return -1
        return dynamics


    #--------------------------------------------------------------------------------#
    #--------------------------------------Chords------------------------------------#
    #--------------------------------------------------------------------------------#


    # Generates a single chord from a given scale
    def newChord(self, scale):
        '''
        Generates a single new chord from the notes in a given scale.
        '''
        if(len(scale) == 0):
            print("ERROR: no input!")
            return -1
        chord = []
        # How many notes? 2 to however many notes in the scale(!)
        total = randint(2, len(scale))
        while(len(chord) < total):
            # Pick note
            note = scale[randint(0, len(scale) - 1)]
            # Append if not already in chord
            if(note not in chord):
                chord.append(note)
        if(len(chord) == 0):
            print("ERROR: no chord generated!")
            return -1
        return chord

    # Generates a chord progression from the notes of a given scale
    def newChordsFromScale(self, scale):
        '''
        Generates a progression from the notes of a given scale.
        Returns -1 if recieving bad input, and -2 if generation was unsuccessfull
        
        NOTE: Chords will be derived from the given scale ONLY! Could possibly
              add more randomly inserted chromatic tones to give progressions more
              variance and color. 
        '''
        if(len(scale) == 0):
            print("ERROR: no scale inputted!")
            return -1
        # How many chords?
        chords = []
        # Create between 3 and however many notes there are in the scale
        total = randint(3, len(scale) - 1)
        print("\nGenerating", total, "chords...")
        # Pick notes
        while(len(chords) < total):
            chord = []
            # How many notes in this chord?
            totalNotes = randint(2, 7)
            while(len(chord) < totalNotes):
                # Pick note
                note = scale[randint(0, len(scale) - 1)]
                # Add if not already in list
                if(note not in chord):
                    chord.append(note)
                elif(note in chord and len(chord) > 2):
                    break
            chords.append(chord)
        if(len(chords) == 0):
            print("ERROR: Unable to generate chords!")
            return -1
        return chords


    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    #Generate a melody from an array of integers. 
    def newMelody(self, data, dataType):
        '''
        Picks a tempo, notes, rhythms, and dynamics. Rhythms and dynamics are picked randomly (total
        for each is len(data), notes come from user. Should (ideally) handle either a character
        array for a person's name (or any random set of characters), or an array of 
        either floats or integers of n length.

        Appends to pretty_midi object and exports a MIDI file. Returns a newMelody() object.
        '''
        # Melody container object
        newMelody = melody()

        #------------------Process incoming data-----------------#
       
        print("\nProcessing incoming data...")

        # If ints, scale as necessary
        if(dataType == 1):
            data = self.scaleTheScale(data)

        # If floats then convert to ints and scale
        if(dataType == 2):
            data = self.floatToInt(data)
            data = self.scaleTheScale(data)

        # If letters/chars then match letters to their corresponding index numbers.
        isLetters = False
        if(dataType == 3):
            data = self.mapLettersToNumbers(data)
            isLetters = True
            print("\nInputted data after processing:", data)

        # If hex convert to array of ints and scale
        if(dataType == 4):
            data = self.hexToIntArray(data)
            print("\nInputted data after processing:", data)


        #-----------------------Generate!------------------------#
        
        print("\nGenerating melody...")

        # Pick tempo
        newMelody.tempo = self.newTempo()
        # Pick notes
        newMelody.notes = self.newNotes(data, isLetters)
        # Pick rhythms
        newMelody.rhythms = self.newRhythms(len(newMelody.notes))
        # Pick dynamics
        newMelody.dynamics = self.newDynamics(len(newMelody.notes))

        #------------Check data, display, and export-------------#

        print("\nChecking results...")

        # Make sure all data was inputted
        if(newMelody.hasData() == False):
            print("ERROR: missing melody data!")
            return -1

        # Add data to MIDI object and write out file.
        '''NOTE: fileName is returning an OS error??'''
        fileName = self.newFileName('solo melody ')
        if(mid.saveMelody(self, newMelody, fileName) == -1):
            print("ERROR: unable to export melody!")
            return -1

        # Display results
        self.display(newMelody)

        return newMelody