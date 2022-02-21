#*******************************************************************************************************#
#-----------------------------Utility functions for working with MIDI I/O ------------------------------#
#*******************************************************************************************************#

''' 
    NOTE: Double check the math for how strt and end are incremented according to
    the supplied durations. Either Finale is doing something weird or the compounding
    values are creating highly precice floating point numbers that might make sheet music
    representation very messy. 
  
'''
import urllib.request
from random import randint
from datetime import datetime
import pretty_midi as pm


class midiStuff():
    '''
    This class is for handling MIDI I/O with generous help from the pretty_midi library.
    '''

    def __init__(self, alive=True):
        self.alive = alive

    # Autogenerates a new filename
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
            words = open('./public/wordlist.txt').read().splitlines()
            # Pick two random words
            name = words[randint(0, len(words) - 1)] + \
                '_' + words[randint(0, len(words) - 1)]
        except urllib.error.URLError:
            name = ensemble + ' - '

        # Get date and time.
        date = datetime.now()
        # Convert to str d-m-y (hh:mm:ss)
        dateStr = date.strftime("%d-%b-%y (%H:%M:%S.%f)")

        # Name and date, and add file extension
        fileName = '{}{}{}.mid'.format(name, ensemble, dateStr)
        return fileName

    # Outputs a single melody/instrument to a MIDI file

    def saveMelody(self, fileName, newMelody):
        '''
        Outputs a single instrument MIDI file (ideally). Returns 0 on success, -1 on failure. 
        To be used with melody generation.
        '''
        # Check incoming data
        if(newMelody.hasData() == False):
            return -1

        # Variables
        strt = 0
        end = 0

        # Create PM object and single instrument.
        # PM object is mainly used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo=newMelody.tempo)
        instrument = pm.instrument_name_to_program(newMelody.instrument)
        melody = pm.Instrument(program=instrument)

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        for i in range(len(newMelody.notes)):
            # Converts note name strings to MIDI note numbers
            note = pm.note_name_to_number(newMelody.notes[i])
            # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
            note = pm.Note(
                velocity=newMelody.dynamics[i], pitch=note, start=strt, end=end)
            # Then places container in melody notes list.
            melody.notes.append(note)
            # Increment rhythms (note event strt/end times)
            try:
                strt += newMelody.rhythms[i]
                end += newMelody.rhythms[i+1]
            except IndexError:
                break

        # Write out file from MIDI object
        mid.instruments.append(melody)
        mid.write(fileName)
        return 0

    # Outputs a single MIDI chord.

    def saveChord(self, newChord):
        '''
        Takes a single chord() object and outputs a MIDI file of that chord.
        '''
        # Create PrettyMIDI object
        mid = pm.PrettyMIDI(initial_tempo=newChord.tempo)
        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program=instrument)

        # Add data to pm object
        for i in range(len(newChord.notes)):
            note = pm.note_name_to_number(newChord.notes[i])
            note = pm.Note(
                velocity=newChord.dynamics[i], pitch=note, start=0.0, end=newChord.rhythm)
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
        # Create PrettyMIDI object
        myChords = pm.PrettyMIDI(initial_tempo=newChords.tempo)

        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program=instrument)

        strt = 0
        end = newChords[0].rhythm
        for i in range(len(newChords)):
            # Add *this* chord's notes
            for j in range(len(newChords[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(newChords[i].notes[j])
                achord = pm.Note(
                    velocity=newChords[i].dynamics[j], pitch=note, start=strt, end=end)
                # Add to instrument object
                chord.notes.append(achord)
            try:
                # Increment strt/end times
                strt += newChords[i].rhythm
                end += newChords[i+1].rhythm
            except IndexError:
                break

        # Add chord to instrument list
        myChords.instruments.append(chord)

        # Write out file from MIDI object
        myChords.write('new-chords.mid')
        print("\n'new-chords.mid' saved successfully!")
        return 0

    # Save a melody and chords

    def saveComposition(self, newMelody, newChords, fileName):
        '''
        Save a single-line melody with chords generated to a MIDI file. 
        Returns a PrettyMIDI() object, or -1 if failure
        '''
        # Check incoming data
        if(newMelody.hasData() == False):
            return -1
        if(len(newChords) == 0):
            return -1

        # Variables
        strt = 0
        end = 0

        # Create PM object PM object is used to just write out the file.
        mid = pm.PrettyMIDI(initial_tempo=newMelody.tempo)

        # Create melody instrument (strings)
        instrument = pm.instrument_name_to_program(newMelody.instrument)
        melody = pm.Instrument(program=instrument)

        #----------------------------Add Melody----------------------------------#

        # Attach notes, rhythms, and dynamics to melody instrument/MIDI object
        end += newMelody.rhythms[0]
        for i in range(len(newMelody.notes)):
            # Converts note name strings to MIDI note numbers
            note = pm.note_name_to_number(newMelody.notes[i])
            # Attaches MIDI note number, dynamic, and strt/end time to pm.Note container
            note = pm.Note(
                velocity=newMelody.dynamics[i], pitch=note, start=strt, end=end)
            # Then places container in melody notes list.
            melody.notes.append(note)
            # Increment rhythms (note event strt/end times)
            try:
                strt += newMelody.rhythms[i]
                end += newMelody.rhythms[i+1]
            except IndexError:
                break

        # Add melody to instrument list
        mid.instruments.append(melody)

        #----------------------------Add Harmonies-------------------------------#

        # Create instrument object.
        instrument = pm.instrument_name_to_program('Acoustic Grand Piano')
        chord = pm.Instrument(program=instrument)

        strt = 0
        end = newChords[0].rhythm
        for i in range(len(newChords)):
            # Add *this* chord's notes
            for j in range(len(newChords[i].notes)):
                # Translate note to MIDI note
                note = pm.note_name_to_number(newChords[i].notes[j])
                achord = pm.Note(
                    velocity=newChords[i].dynamics[j], pitch=note, start=strt, end=end)
                # Add to instrument object
                chord.notes.append(achord)
            try:
                # Increment strt/end times
                strt += newChords[i].rhythm
                end += newChords[i+1].rhythm
            except IndexError:
                break

        # Add chord to instrument list
        mid.instruments.append(chord)
        # Write to MIDI file
        print("\nSaving", fileName, "...")
        mid.write(f'./build/midi/{fileName}')

        # Return PrettyMIDI() object
        return mid
