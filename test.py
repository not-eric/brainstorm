'''
----------------------------------------------------------------------------------------------------
                        THIS FILE IS FOR TESTING GENERATIVE FUNCTIONS
----------------------------------------------------------------------------------------------------
'''

# Import and new object
from midi import midiStuff as mid
from random import uniform
from random import randint
from generate import generate 
create = generate()

#---------------------------test functions------------------------------#

# Generate a list of 10 - 50 random numbers between 0-200
def newInts():
    nums = []
    total = randint(10, 50)
    for i in range(total):
        nums.append(randint(0, 200))
    return nums

# Generate a list of 10 - 50 random floating point numbers between 0 - 200
def newFloats():
    floats = []
    total = randint(10, 50)
    for i in range(total):
        floats.append(uniform(0.001, 200.001))
    return floats

# Generates a random hex color number
def newHex():
    # 0 to 0xFFFFFF
    num = randint(0, 16777215)
    hexNum = format(num, 'x')
    hexNum = '0x'+ hexNum
    return hexNum

# Generate a list of 10 - 50 random upper/lower-case characters
def newChars():
    chars = []
    total = randint(10, 50)
    for i in range(total):
        # Pick letter
        char = create.alphabet[randint(0, 25)]
        # Captitalize? 1 = yes, 2 = no
        if(randint(1, 2) == 1):
            char = char.upper()
        chars.append(char)
    return chars    

#---------------------------------------------------------------------#


# # Scaling test
# print("\n***scaling test***")
# nums = newInts()
# print("\nnew array:", nums)
# print("total elements:", len(nums) - 1)
# print("expected result: an array who's element values don't exceed", len(nums) - 2)
# result = create.scaleTheScale(nums)
# # Check result
# for i in range(len(result) - 1):
#     if(result[i] > len(nums) - 2):
#         print("failed! i = ", result[i])
#         break
# print("\ntotal elements:", len(result))
# print("result:", result)


# # Floats to ints test
# print("\n***floats to ints test***")
# floats = newFloats()
# print("\ntotal elements:", len(floats))
# print("new array:", floats)
# result = create.floatToInt(floats)
# print("\nresult:", result)


# # Hex to int array test
# print("\n***hex to int array test***")
# hexNum = newHex()
# print("new hex:", hexNum)
# result = create.hexToIntArray(hexNum)
# print("result:", result)


# # Map integers to notes test
# print("\n***integers to notes test***")
# nums = newInts()
# print("\ntotal new numbers:", len(nums))
# print("new numbers:", nums)
# if(randint(1, 2) == 1):
#     isMinor = True
#     print("\nusing a minor key!")
# else:
#     isMinor = False
#     print("\nusing a major key!")
# newNotes = create.newNotes(nums, isMinor)
# print("\ntotal notes:", len(newNotes))
# print("new notes:", newNotes)


# # Map letters to numbers test
# print("\n***letter to number map test***")
# data = newChars()
# print("\ntotal letters:", len(data))
# print("inputted data:", data)
# result = create.mapLettersToNumbers(data)
# print("\nresult", result)


# # New root/scale test
# print("\n***new scale test***")
# scale = create.newScale(4)
# print("new scale:", scale)
# print("total:", len(scale))


# New chord from scale test
# print("\n***new chord from scale test***")
# scale = create.newScale(randint(3, 5))
# print("\nscale inputted:", scale)
# chord = create.newChordFromScale(scale)
# # Default rhythm and dynamic for testing purposes
# print("adding rhythm (whole note)...")
# chord.rhythm = 4.0
# print("adding dynamics...")
# for i in range(len(chord.notes)):
#     chord.dynamics.append(100)
# print("\ntotal notes:", len(chord.notes))
# print("notes:", chord.notes)
# print("dynamics:", chord.dynamics)
# print("rhythm:", chord.rhythm)
# # Save to MIDI file
# if(mid.saveChord(chord) == -1):
#     print("\nunable to save MIDI file!")
# else:
#     print("\nsaving file new-chord.mid...")


# New chords from scale test
print("\n***new chords from scale test***")
scale = create.newScale(randint(3, 5))
print("new scale:", scale)
chords = create.newChordsFromScale(scale)
print("total chords:", len(chords))
print("new chords:")
for i in range(len(chords)):
    print("chord:", chords[i].notes)
print("picking a chord from the set...")
chord = chords[randint(0, len(chords) - 1)]
print("chosen chord:", chord.notes)


# # New melody test fron integers
# print("\n***new melody from ints/floats/chars/hex test***")
# dataType = randint(1, 4)
# # Generate ints
# if(dataType == 1):
#     print("\ninputting ints...")
#     data = newInts()
# # Generate floats
# elif(dataType == 2):
#     print("\ninputting floats...")
#     data = newFloats()
# # Generate chars
# elif(dataType == 3):
#     print("\ninputting letters...")
#     data = newChars()
# # Generate a new hex
# else:
#     print("\ninputting hex number...")
#     data = newHex()
# print("\ntotal elements:", len(data))
# print("data inputted:", data)
# result = create.newMelody(data, dataType)