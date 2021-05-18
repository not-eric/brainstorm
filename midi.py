#*******************************************************************************************************#
#-----------------------------Utility functions for working with MIDI I/O ------------------------------#
#*******************************************************************************************************#

'''
    This module is for handling MIDI I/O with generous help from the pretty_midi library.
'''
from datetime import datetime
import pretty_midi as pm
from pretty_midi import constants as inst

class midiStuff():
    '''
    This class is for handling MIDI I/O with generous help from the pretty_midi library.
    '''

    def __init__(self):
        super().__init__()

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

    # Imports a MIDI file
    def load(self, fileName):
        '''
        Imports a MIDI file from a given file name or path.
        Returns a PrettyMIDI object using the given filename.
        '''
        print("\nImporting MIDI file...")
        # Import file
        thisTune = pm.PrettyMIDI(fileName) 
        if(not thisTune):
            print("...Unable to import file!")
            return -1
        print("...File imported!")
        return thisTune


    # Save a MIDI object to a pre-existing file
    # def saveCurrent(self, fileName, notes, rhythms, dynamics, tempo, instTotal)
    '''
    Saves a MIDI object to a pre-existing MIDI file. Input must be a 
    string with the format 'filename.mid'
    '''
    def save(self, fileName):
        if(fileName is None):
            return -1
        print("\nSaving", fileName, "...")
        pm.PrettyMIDI.write(fileName)
        return 0
    
    # Outputs a single melody/instrument to a MIDI file
    def saveMelody(self, newMelody, fileName):
        '''
        Outputs a single instrument MIDI file (ideally). Returns 0 on success, -1 on failure. 
        To be used with melody generation.

        NOTE: Double check the math for how strt and end are incremented according to
        the supplied durations. Either Finale is doing something weird or the compounding
        values are creating highly precice floating point numbers that might make sheet music
        representation very messy. 
        '''
        # Check incoming data
        if(newMelody.hasData() == False):
            return -1

        # Variables
        strt = 0
        end = 0

        # Create PM object and single instrument. 
        # PM object is mainly used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo = newMelody.tempo)
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        '''
        Randomly choose an instrument? 
        instrument = pm.instrument_name_to_program(inst.INSTRUMENT_MAP[randint(0, 110))
        '''
        melody = pm.Instrument(program = instrument)

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        for i in range(len(newMelody.notes)):
            # Converts note name strings to MIDI note numbers
            note = pm.note_name_to_number(newMelody.notes[i])
            # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
            note = pm.Note(velocity= newMelody.dynamics[i], pitch= note, start= strt, end= end)
            # Then places container in melody notes list.
            melody.notes.append(note)
            # Increment rhythms (note event strt/end times)
            try:
                strt += newMelody.rhythms[i]
                end += newMelody.rhythms[i + 1]
            except IndexError:
                break  

        # Write out file from MIDI object
        mid.instruments.append(melody)
        # print("saving", fileName, "...")
        # mid.write(fileName)
        mid.write('test-melody.mid')
        return 0


    # Outputs a single MIDI chord.
    def saveChord(self, newChord):
        '''
        Outputs a single MIDI chord (ideally). Also returns a pretty_midi object. 
        To be used with chord generation.
        '''
        # if(newChord.hasData() == False):
        #     print("\nERROR: no data inputted!")
        #     return -1

        print("\nRecieved chord data:", newChord)

        # Create PrettyMIDI object
        mid = pm.PrettyMIDI(initial_tempo=60)
        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program = instrument)

        print("Created instrument:", 'Acoustic Grand Piano')

        # Add data to pm object
        for i in range(len(newChord.notes)):
            note = pm.note_name_to_number(newChord.notes[i])
            note = pm.Note(velocity= newChord.dynamics[i], pitch= note, start= 0.0, end= newChord.rhythm)
            chord.notes.append(note)
        
        # Write out file from MIDI object
        mid.instruments.append(chord)
        mid.write('new-chord.mid')

        print("'new-chord.mid' file saved!")
        return 0


    # Generates a MIDI file of the chords created by newChord()
    def saveChords(self, newChords):
        '''
        Takes a chord() object as an argument and generates a MIDI file.
        Returns a pretty_midi object. Returns 0.
        '''

        print("\nGenerating MIDI chords...")
        
        # Create PrettyMIDI object
        myChords = pm.PrettyMIDI(initial_tempo = 60)

        strt = 0
        end = newChords[0].rhythm
        for i in range(len(newChords)):
            # Create instrument object.
            instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
            chord = pm.Instrument(program = instrument)
            for j in range(len(newChords[i].notes)):
                note = pm.note_name_to_number(newChords[i].notes[j])
                note = pm.Note(velocity= newChords[i].dynamics[j], pitch= note, start= strt, end= end)
                chord.notes.append(note)
            # # Add chord to instrument list (will this consolidate to one track?)
            # myChords.instruments.append(chord)
            try:
                # Increment strt/end times
                strt += newChords[i].rhythm
                end += newChords[i].rhythm
                # # Add chord to instrument list (original spot)
                # myChords.instruments.append(chord)
            except IndexError:
                break

        # Write out file from MIDI object
        myChords.write('test-chords.mid')

        return 0








'''
i = 0: first subarray in newChords[]
i = 1: second sub-array ""
etc...

i < newChords(len(i)) ??? 
Need to iterate for the length of each individual sub-arrays.

strt = 0
end = rhythms[0]
for i in range(len(rhythms)):
    for j in newChords[i[j]]:
        note_number = pm.note_name_to_number(note_name)
        note = pm.Note(velocity= vel, pitch= note_number, start= strt, end= end)
        chords.notes.append(note)
    strt += end
    end += rhythms[i]

Add returning object from newChord as an argument?
'''