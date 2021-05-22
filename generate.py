#****************************************************************************************************************#
#-----------------------------------This class handles generative functions--------------------------------------#
#****************************************************************************************************************#

'''
----------------------------------------------------NOTES-------------------------------------------------------
    
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.  

    TODO:
        Create a way to export newMelody() metadata (console output) to a text file.

    NOTE:
        newMelody()

        Long data sets will have the same note associated with different 
        values elsewhere in the array. 
        
        If we ascend through the available octaves we can pick a new 
        key/scale and cycle through the octaves again. This will allow for 
        some cool chromaticism to emerge rather "organiclly" while minimizing
        the amount of repeated notes associated with different elements in 
        the data array (unless we get the same scale chosen again, or there's
        a lot of common tones between the scales that are picked) .

    NOTE: 
        Should newNotes()'s total output be contingent on the total data elements
        inputted? Is there a way to scale integers to a randomly chosen index within
        the bounds of a new array of notes that's already been generated? Probably. 

    NOTE:
        Consolidate newRhythms() and newDynamics() into single generative loop, with an
        additional 'type' (int) argument. Each type chooses which resource data to draw from. 

----------------------------------------------------------------------------------------------------------------
'''

# IMPORTS
import math
import datetime
import instruments
import urllib.request
from random import randint
from midi import midiStuff as mid
from containers.composition import music
from containers.melody import melody
from containers.chord import chord

# Generative functions
class generate():
    '''
    This class handles all generative functions. It contains a set of resource data
    that is accessed by a variety of generative algorithms and mapping functions.
    '''

    # Constructor
    def __init__(self):


        #---------------------------------------------------------------------#
        #--------------------------Resource data------------------------------#
        #---------------------------------------------------------------------#


        # ----------------------------Letters---------------------------------#  

        '''
        Used to search against and return an integer representing an 
        Array index. The array will be used to generate a scale from
        whos total is the len(alphabet) - 1
        '''

        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                         'h', 'i', 'j', 'k', 'l', 'm', 'n',
                         'o', 'p', 'q', 'r', 's', 't', 'u',
                         'v', 'w', 'x', 'y', 'z']


        #----------------------------Tempo-----------------------------------#

        # Tempos (indices: 0-38)
        self.tempos = [40.0, 42.0, 44.0, 46.0, 50.0, 52.0, 54.0, 56.0, 58.0, #1-9 (0-8)
                       60.0, 63.0, 66.0, 69.0, 72.0, 76.0, 80.0, 84.0, 88.0, #10-18 (9-17)
                       92.0, 96.0, 100.0, 104.0, 108.0, 112.0, 116.0, 120.0, # 19-27 (18-26)
                       126.0, 132.0, 128.0, 144.0, 152.0, 160.0, 168.0, 176.0, #28-36 (27-35)
                       184.0, 200.0, 208.0] #37-39 (36-38)


        #-----------------------Instrumentation------------------------------#
        # Ensemble size
        self.size = {1: 'solo',
                     2: 'duo', 
                     3: 'trio',
                     4: 'quartet',
                     5: 'quintet',
                     6: 'sextet',
                     7: 'septet',
                     8: 'octet',
                     9: 'nonet',
                     10: 'decet',
                     11: 'large ensemble', 
                     12: 'open instrumentation'}
        
        # Instrument list
        self.instruments = instruments.INSTRUMENT_MAP


        #-----------------------Notes and Scales------------------------------#

        # Enharmonically spelled note names starting on A. Indicies: 0-16.
        '''
        Interval mappings for enhamonicly spelled chromatic scale array starting on C
            0 - 0        = unison
            0 - 1 or 2   = half-step
            0 - 3        = whole-step
            0 - 4        = minor third
            0 - 5 or 6   = major third
            0 - 7        = perfect 4th
            0 - 8 or 9   = tritone
            0 - 10       = perfect 5th
            0 - 11       = minor 6th
            0 - 12 or 13 = major 6th/dim 7th
            0 - 14       = minor 7th
            0 - 15 or 16 = major 7th
        '''
        self.notes = ["C ", "C#", "Db", "D ", 
                      "D#", "Eb", "E ", "F ", 
                      "F#", "Gb", "G ", "G#",
                      "Ab", "A ", "A#", "Bb", "B "]

        # Chormatic scale (using all sharps). Indicies 0 - 11.
        self.chromaticScaleSharps = ["C", "C#", "D", "D#", "E", "F",
                                     "F#", "G", "G#", "A", "A#", "B"] 

        # Chormatic scale (using all flats). Indicies 0 - 11.
        self.chromaticScaleFlats = ["C", "Db", "D", "Eb", "E", "F",
                                    "Gb", "G", "Ab", "A", "Bb", "B"]        

        # Major Scales
        self.scales = {1: ["C", "D", "E", "F", "G", "A", "B"], 
                       2: ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
                       3: ["D", "E", "F#", "G", "A", "B", "C#"],
                       4: ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
                       5: ["E", "F#", "G#", "A", "B", "C#", "D#"],
                       6: ["F", "G", "A", "Bb", "C", "D", "E"],
                       7: ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
                       8: ["G", "A", "B", "C", "D", "E", "F#"],
                       9: ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
                       10:["A", "B", "C#", "D", "E", "F#", "G#"],
                       11:["Bb", "C", "D", "Eb", "F", "G", "A"],
                       12:["B", "C#", "D#", "E", "F#", "G#", "A#"]}

     
        #---------------------------Rhythm-----------------------------------#

        '''
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


        #--------------------------Dynamics---------------------------------#
        
        '''
        MIDI velocity/dynamics range: 0 - 127
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
    #-----------------------------------Utility Functions-------------------------------------#
    #-----------------------------------------------------------------------------------------#


    # Auto generate a file/composition name (type - date:time)
    def newFileName(self, ensemble):
        '''
        Generates a title/file name by picking two random words
        then attaching the composition type (solo, duo, ensemble, etc..),
        followed by the date.

        Format: "<words> - <type> - <date: d-m-y (hh:mm:ss)>"
        
        Random word generation technique from:
            https://stackoverflow.com/questions/18834636/random-word-generator-python
        '''
        try:
            # Get word list
            url = "https://www.mit.edu/~ecprice/wordlist.10000"
            # response = requests.get(url)
            response = urllib.request.urlopen(url)
            # words = response.content.splitlines()
            text = response.read().decode()
            words = text.splitlines()
            # Pick two random words
            name = words[randint(0, len(words) - 1)] + '_' + words[randint(0, len(words) - 1)]
        except urllib.error.URLError:
            name = ensemble + ' - '

        # Get date and time.
        date = datetime.now()
        # Convert to str d-m-y (hh:mm:ss)
        dateStr = date.strftime("%d-%b-%y (%H:%M:%S.%f)")

        # Name and date, and add file extension
        fileName = '{}{}{}.mid'.format(name, ensemble, dateStr)
        return fileName
    
    
    # Generates a new file to save a new composition's meta-data to
    def saveInfo(self, data, fileName, newMelody, newChords):
        '''
        Generates a new file to save a new composition's meta-data to
        '''
        # Create a new file opening object thing
        f = open(fileName, 'w')
        
        # Generate a header
        header = '\n\n*****************************************************************'
        f.write(header)
        header = '\n------------------------NEW COMPOSITION--------------------------'
        f.write(header)
        header = '\n*****************************************************************'
        f.write(header)

        # Save piece title and inputted data
        title = '\n\n\nTITLE: ' + fileName
        f.write(title)

        dataStr = ''.join([str(i) for i in data])
        dataInfo = '\n\nInputted data:' + dataStr
        f.write(dataInfo)

        # Save melody data
        header = "\n\n\n----------------MELODY DATA-------------------"
        f.write(header)

        tempo = '\n\nTempo: ' + str(newMelody.tempo) + 'bpm'
        f.write(tempo)

        totalNotes = '\n\nTotal Notes: ' + str(len(newMelody.notes))
        f.write(totalNotes)

        noteStr = ''.join(newMelody.notes)
        notes = '\nNotes: ' + noteStr
        f.write(notes)

        totalRhythms = '\n\nTotal rhythms:' + str(len(newMelody.rhythms))
        f.write(totalRhythms)

        rhythmStr = ''.join([str(i) for i in newMelody.rhythms])
        rhythms = '\nRhythms: ' +  rhythmStr
        f.write(rhythms)
        
        totalDynamics = '\n\nTotal dynamics:' + str(len(newMelody.dynamics))
        f.write(totalDynamics)

        dynamicStr = ''.join([str(i) for i in newMelody.dynamics])
        dynamics = '\nDynamics:' + dynamicStr
        f.write(dynamics)

        # Save harmony data
        header = "\n\n\n----------------HARMONY DATA-------------------"
        f.write(header)

        for j in range(len(newChords)):
            i = 0
            noteStr = ''.join([str(i) for i in newChords[j].notes])
            notes = '\n\nNotes: ' + noteStr
            f.write(notes)

            rhythm = '\nRhythm: ' + str(newChords[j].rhythm)
            f.write(rhythm)
            
            i = 0
            dynamicsStr = ''.join([str(i) for i in newChords[j].dynamics])
            dynamics = '\nDynamics: ' + dynamicsStr
            f.write(dynamics)

        # Close instance
        f.close()
        return 0


    #-----------------------------------------------------------------------------------------#
    #----------------------------------Conversion Functions-----------------------------------#
    #-----------------------------------------------------------------------------------------#


    # Converts an array of floats to an array of ints
    def floatToInt(self, data):
        '''
        Converts an array of floats to an array of ints
        '''
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
        for i in range(len(data)):
            if(data[i] > len(data) - 1):
                # Which scaling method should we use?
                s = randint(1, 3)
                # Divide data[i] by len(data) - 1
                if(s == 1):
                    data[i] = math.floor(data[i] / len(data) - 1)
                # Subtract by len(data) - 1    
                elif(s == 2):
                    while(data[i] > len(data) - 1):
                        data[i] -= len(data) - 1
                # Subtract by 1                    
                else:
                    while(data[i] > len(data) - 1):
                        data[i] -= 1
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
        return numArr


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
    def newNote(self, num, octave):
        '''
        Converts a given integer to a pitch in a specified octave (ex C#6).
        Requires an integer and the required octave. Returns a single string.

        NOTE: use randint(0, 11) and randint(2, 5) for num/octave args to get a 
              randomly chosen note
        '''
        if(num < 0 or num > 11 or 
           octave > 6 or octave < 0):
            return -1
        # Sharps or flats
        if(randint(1, 2) == 1):
            note = self.chromaticScaleSharps[num]
        else:
            note = self.chromaticScaleFlats[num]
        # Add octave
        note = "{}{}".format(note, octave)
        return note

    # Generate a series of notes based off an inputted array of integers
    def newNotes(self, data):
        '''
        Generates a set of notes based on inputted data (an array of integers).
        Data is used as index numbers to select notes from this series in order
        to generate a melody.

        Note generation algorithm:

            1. Total notes is equivalent to *highest single integer* in supplied data set.
            2. Generate a starting key/scale, and a starting octave.
            3. Cycle through this scale appending each note to a list
                of available notes until we reach the last note in the scale
                in octave 6.
            4. If we reach this note, reset octave to a new starting point, and 
                pick a new starting scale at random.
            5. Repeat steps 3-4 until we have as many notes as the highest single
                integer from the supplied data set.
        '''
        if(len(data) == 0):
            print("ERROR: no data inputted!")
            return -1

        # Pick starting octave (1 - 3)
        octave = randint(1, 3)

        # Pick initial root/starting scale (major or minor)
        root = self.scales[randint(1, len(self.scales) - 1)]
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

        #-----Generate notes to pick from-----#

        n = 0
        scale = []
        total = max(data)
        for i in range(total + 1):
            note = "{}{}".format(root[n], octave)
            scale.append(note)
            n += 1
            '''NOTE: At most, the alphabet will map to 4 1/3 octaves.
                        Still didn't want to exceed octave 6'''
            if(i % 7 == 0):
                octave += 1
                if(octave > 6):
                    # Reset starting octave
                    octave = randint(1, 3)
                    # Pick new root scale
                    root = self.scales[randint(1, len(self.scales) - 1)]
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
        for i in range(len(data)):
            notes.append(scale[data[i]])
        # Check results
        if(len(notes) == 0):
            print("ERROR: Unable to generate notes!")
            return -1
        return notes

    # Generate a new scale to function as a "root"
    def newScale(self, octave):
        '''
        Requires a starting octave. Returns a randomly generated scale 
        within one octave to be used as a 'root'. Returns -1 on failure.
        '''
        print("\nGenerating new root scale...")
        if(octave < 1 or octave > 6):
            print("\nERROR: octave out of range!")
            return -1
        pcs = []
        # Use sharps (1) or flats (2)?
        sof = randint(1, 2)
        # generate an ascending set of 7 integers/note array indices 
        while(len(pcs) < 7):
            # pick note 
            n = randint(0, 11)
            if(n not in pcs):
                pcs.append(n)
        # sort in ascending order
        pcs.sort()
        # convert to strings
        print("new ints:", pcs)
        print("total:", len(pcs))
        scale = []
        for i in range(len(pcs)):
            if(sof == 1):
                note = "{}{}".format(self.chromaticScaleSharps[pcs[i]], octave)
            else:
                note = "{}{}".format(self.chromaticScaleFlats[pcs[i]], octave)
            scale.append(note)
        if(len(scale) == 0):
            print("ERROR: unable to generate scale!")
            return -1
        return scale

    # Picks one of twelve major scales
    def newMajorScale(self):
        '''
        Picks one of twelve major scales.
        '''
        print("\nPicking major scale...")
        finalScale = []
        # Pick scale
        scale = self.scales[randint(1, len(self.scales) - 1)]
        # Assign octave
        octave = randint(3, 5)
        for i in range(len(scale)):
            note = "{}{}".format(scale[i], octave)
            finalScale.append(note)
        return finalScale

    # Picks one of twelve melodic minor scales
    def newMinorScale(self):
        '''
        Picks one of twelve melodic minor scales
        '''
        print("\nPicking minor scale...")
        # Pick major scale
        scale = self.newMajorScale()
        # Convert to minor
        scale = self.convertToMinor(scale)
        return scale

    # Converts a major scale to its relative minor
    def convertToMinor(self, scale):
        print("\nConverting major scale to relative minor...")
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


    # Pick a rhythm
    def newRhythm(self):
        '''
        Generates a single new rhythm
        '''
        rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
        return rhythm

    # Generate a list containing a rhythmic pattern
    def newRhythms(self, total):
        '''
        Generates a series of rhythms of n length, where n is supplied
        from elsewhere. Uses infrequent repetition.
        '''
        rhythms = []
        print("\nGenerating", total, "rhythms...")
        while(len(rhythms) < total):
            # Pick rhythm and add to list    
            rhythm = self.rhythms[randint(0, len(self.rhythms) - 1)]
            # Repeat this rhythm or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                # Limit reps to no more than 1/3 of the total no. of rhythms
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

    # New rhythmic pattern
    def newRhythmPattern(self, total):
        '''
        Generates a short rhythmic pattern of n length to be played t (total) times
        '''
        riff = []
        # Pick 3 to 8 rhythms
        riffLen = randint(3, 8)
        # Stay within provided bounds
        if(riffLen > total):
            while(riffLen > math.floor(total/2)):
                riff -= 1
        # Generate pattern
        while(len(riff) < riffLen):
            riff.append(self.newRhythm())
        if(len(riff) == 0):
            print("\nERROR: unable to generate rhythmic pattern!")
            return -1
        return riff


    #--------------------------------------------------------------------------------#
    #-------------------------------------Dynamics-----------------------------------#
    #--------------------------------------------------------------------------------#


    # Generate a single dynamic (to be used such that a passage doesn't have consistenly
    # changing dynamics)
    def newDynamic(self):
        '''
        Generates a single dynamic/velocity between 20 - 124
        '''
        dynamic = self.dynamics[randint(0, len(self.dynamics) - 1)]
        return dynamic

    # Generate a list of dynamics. 
    def newDynamics(self, total):
        '''
        Generates a list of dynamics (MIDI velocites) of n length, 
        where n is supplied from elsewhere. Uses infrequent repetition.
        '''
        dynamics = []
        print("\nGenerating", total, "dynamics...")
        while(len(dynamics) < total):
            # Pick dynamic    
            dynamic = self.dynamics[randint(0, 9)]
            # Repeat this dynamic or not? 1 = yes, 2 = no
            if(randint(1, 2) == 1):
                # Limit reps to no more than 1/3 of the supplied total
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

    # Display single chord
    def displayChord(self, chord):      
        print("\n------------Chord:-------------")
        print("\nnotes:", chord.notes)
        print("rhythm:", chord.rhythm)
        print("dynamics:", chord.dynamics)

    # Display a list of chords
    def displayChords(self, chords):
        print("\n----------------HARMONY DATA:-------------------")
        for i in range(len(chords)):
            print('\n', i + 1,': ', 'Notes:', chords[i].notes)
            print('      Rhythm:', chords[i].rhythm)
            print('      Dynamics:', chords[i].dynamics) 

    # Generates a chord with randomly chosen notes
    def newRandChord(self):
        '''
        Generates a chord with randomly chosen notes. 
        Returns a chord() object (has no tempo or dynamics data!)
        '''
        # Create new chord() object
        newChord = chord()
        # Total notes
        total = randint(2, 9)
        while(len(newChord.notes) < total):
            newChord.notes.append(self.newRandNote())
        return newChord

    # Generates a single chord from a given scale
    def newChordFromScale(self, scale, tempo):
        '''
        Generates a single new chord from the notes in a given scale and
        rhythm returns a chord() object. Does not double/repeat notes!
        '''
        if(len(scale) == 0):
            print("ERROR: no input!")
            return -1
        # newchord object
        newchord = chord()
        # how many notes in this chord? 2 to 9 (for now)
        total = randint(2, 9)
        while(len(newchord.notes) < total):
            # Pick note
            note = scale[randint(0, len(scale) - 1)]
            newchord.notes.append(note)
        if(len(newchord.notes) == 0):
            print("\nERROR: no chord generated!")
            return -1
        # Remove duplicate notes/doublings
        '''NOTE: This is avoids getting the while loop stuck
                 if there's a lot of repeated notes in the melody '''
        newchord.notes = list(dict.fromkeys(newchord.notes))
        # Use inputted tempo    
        newchord.tempo = tempo
        # Pick a rhythm
        newchord.rhythm = self.newRhythm()
        # Pick a dynamic (randomize for each note? probably)
        dynamic = self.newDynamic()
        while(len(newchord.dynamics) < len(newchord.notes)):
            newchord.dynamics.append(dynamic)
        return newchord

    # Generates a chord progression from the notes of a given scale
    def newChordsFromScale(self, scale, tempo):
        '''
        Generates a progression from the notes of a given scale.
        Returns a list of chord objects (notes only).
        
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
            newchord = self.newChordFromScale(scale, tempo)
            chords.append(newchord)
        if(len(chords) == 0):
            print("ERROR: Unable to generate chords!")
            return -1
        # Test output
        # if(mid.saveChords(self, chords) != -1):
        #     print("chords saved!")
        # else:
        #     print("unable to save chords!")
        #     return -1
        # Display chords
        self.displayChords(chords)
        return chords


    #---------------------------------------------------------------------------------#
    #-------------------------------MELODIC GENERATION--------------------------------#
    #---------------------------------------------------------------------------------#


    # Display newMelody() object data
    def displayMelody(self, newMelody):
        '''
        Displays newMelody() object data and exports to .txt file
        '''
        if(newMelody.hasData() == False):
            print("ERROR: no melody data!")
            return -1

        # Display data
        print("\n-----------MELODY Data:------------")
        print("\nTempo:", newMelody.tempo, "bpm")
        print("\nTotal Notes:", len(newMelody.notes))
        print("Notes:", newMelody.notes)
        print("\nTotal rhythms:", len(newMelody.rhythms))
        print("Rhythms:", newMelody.rhythms)
        print("\nTotal dynamics:", len(newMelody.dynamics))
        print("Dynamics:", newMelody.dynamics)

        return 0

    #Generate a melody from an array of integers. 
    def newMelody(self, data, dataType):
        '''
        Picks a tempo, notes, rhythms, and dynamics. Rhythms and dynamics are picked randomly (total
        for each is len(data), notes come from user. Should (ideally) handle either a character
        array for a person's name (or any random set of characters), or an array of 
        either floats or integers of n length.

        Appends to newMelody() object and exports a MIDI file. Returns a newMelody() object.
        '''
        # Melody container object
        newMelody = melody()

        #------------------Process incoming data-----------------#
       
        print("\nProcessing incoming data...")

        # If ints, scale as necessary
        if(dataType == 1):
            data = self.scaleTheScale(data)
            print("\nTotal elements:", len(data))
            print("Inputted data after processing:", data)

        # If floats then convert to ints and scale
        if(dataType == 2):
            data = self.floatToInt(data)
            data = self.scaleTheScale(data)
            print("\nTotal elements:", len(data))
            print("Inputted data after processing:", data)

        # If letters/chars then match letters to their corresponding index numbers.
        if(dataType == 3):
            data = self.mapLettersToNumbers(data)
            print("\nTotal elements:", len(data))
            print("Inputted data after processing:", data)

        # If hex convert to array of ints and scale
        if(dataType == 4):
            data = self.hexToIntArray(data)
            print("\nTotal elements:", len(data))
            print("Inputted data after processing:", data)


        #-----------------------Generate!------------------------#
        
        print("\nGenerating melody...")

        # Pick tempo
        newMelody.tempo = self.newTempo()
        # Pick notes
        newMelody.notes = self.newNotes(data)
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

        # Display results
        self.displayMelody(newMelody)

        # # Write out to MIDI file
        # if(mid.saveMelody(self, newMelody, 'new-melody.mid') == -1):
        #     print("\nERROR: unable to save file!")
        #     return -1
        # else:
        #     print("\nFile saved as 'new-melody.mid'")

        return newMelody

    #-------------------------------------------------------------------------------------#
    #-------------------------------COMPOSITION GENERATION--------------------------------#
    #-------------------------------------------------------------------------------------#

    # Outputs a melody with lots of notes but using a short rhythmic pattern
    def newRiff(self):
        print("\nGenerating riff...")
        # New melody() object
        riff = melody()
        # Pick tempo
        riff.tempo = self.newTempo()
        # Use 8 to 20 notes
        riffLen = randint(8, 20)
        # Pick rhythmic pattern first
        pattern = self.newRhythmPattern(riffLen)
        # Pick notes and dynamics
        r = 0
        for i in range(riffLen):
            riff.notes.append(self.newNote(randint(0, 11), randint(2, 5)))
            riff.dynamics.append(self.newDynamic())
            riff.rhythms.append(pattern[r])
            r += 1
            # If we reach the end of the pattern, reset to beginning
            if(r > len(pattern) - 1):
                r = 0
        # Check data
        if(riff.hasData() == False):
            print("\nERROR: Unable to generate riff!")
            return -1
        # Save to MIDI file
        if(mid.saveMelody(self, riff) != -1):
            print("\nRiff saved!")
        else:
            print("\nUnable to save riff!")
            return -1
        return riff


    # Outputs a single melody with chords in a MIDI file
    def newComposition(self, data, dataType):
        '''
        Takes an array of ints of any length as an arg, plus the data type 
        (int (1), float (2), char (3), or hex number (4)).

        Outputs a single melody with chords in a MIDI file (hopefully).
        Returns a music() object containing lists of melody() and chord()
        objects
        '''
        # newPiece = music()

        # Check incoming data
        if(len(data) == 0):
            print("\nERROR: no data inputted!")
            return -1
        if(dataType < 1 or dataType > 4):
            print("\nERROR: bad data type!")
            return -1
        
        '''NOTE: append at start or end of lists???'''
        # Generate melody
        newTune = self.newMelody(data, dataType)
        # music.melodies.append(newTune)

        # Generate harmonies
        newChords = self.newChordsFromScale(newTune.notes, newTune.tempo)
        # music.chords.append(newChords)

        # Check data
        if(newTune.hasData() == False or len(newChords) == 0):
            print("\nERROR: No composition data created")
            return -1
        # if(len(music.melodies) == 0 or len(music.chords) == 0):
        #     print("\ERROR: unable to create music() object")
        #     return -1

        # Save to MIDI file
        # fileName = self.newFileName(' - duet - ')
        fileName = 'untitled duet.txt'
        if(mid.saveComposition(self, newTune, newChords, 'duet.mid') != -1):
            print("\nPiece saved as", 'duet.mid')
        else:
            print("\nERROR:Unable to export piece to MIDI file!")
            return -1

        # Save composition data to a .txt file
        self.saveInfo(data, fileName, newTune, newChords)
        return 0