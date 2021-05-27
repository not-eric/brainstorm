'''
----------------------------------------------------------------------------------------------------
                        THIS FILE IS FOR TESTING GENERATIVE FUNCTIONS
----------------------------------------------------------------------------------------------------
'''

# Import and new object
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

# Generate new data 
def newData(dataType):
    # Generate ints
    if(dataType == 1):
        print("\ninputting ints...")
        data = newInts()
    # Generate floats
    elif(dataType == 2):
        print("\ninputting floats...")
        data = newFloats()
    # Generate chars
    elif(dataType == 3):
        print("\ninputting letters...")
        data = newChars()
    # Generate a new hex
    else:
        print("\ninputting hex number...")
        data = newHex()
    print("\ntotal elements:", len(data))
    return data


#---------------------------------------------------------------------------#

# Solo melody test
# print("\n***generating melody ***")
# dataType = randint(1, 4)
# data = newData(dataType)
# print("\ninputting:", data)
# result = create.aNewMelody(data, dataType)
# if(result != -1):
#     print("\n...Here's some new music! :)\n")
# else:
#     print("\n... :(\n")


# Put together melody and harmony data and output as single MIDI file
print("\n***generating melody with harmony***")
dataType = randint(1, 4)
data = newData(dataType)
print("\ninputting:", data)
result = create.newComposition(data, dataType)
if(result != -1):
    print("\n...Here's some new music! :)\n")
else:
    print("\n... :(\n")
