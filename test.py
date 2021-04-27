'''
----------------------------------------------------------------------------------------------------
                        THIS FILE IS FOR TESTING GENERATIVE FUNCTIONS

NOTE:



----------------------------------------------------------------------------------------------------
'''

# Import and new object
from random import randint
from generate import generate 
create = generate()


# Test converting raw data to integers
print("\nconvert floats to ints test")
data = [1.575, 23.3, 9.6, 5.543454554, 13.2222]
print("inputted data:", data)
print("expected result: [1, 23, 9, 5, 13]")
result = create.floatToInt(data)
if(result != -1):
    print("result:", result)
else:
    print("failed!")


# Map letters to numbers test
print("\nletter to number map test")
data = ['J', 'a', 'y']
print("inputted data:", data)
print("expected result: [9, 0, 24]")
result = create.mapLettersToNumbers(data)
if(result != -1):
    print("result:", result)
else:
    print("failed!")


# Pick key test
print("\npick key test")
key = create.pickKey()
print("result: key of", key[0], "major. scale:", key)


# Scale the scale test
print("\nData scaling test")
key = create.pickKey()


# Convert to minor test
print("\nconvert to relative minor test")
key = create.pickKey()
print("major key:", key)
minor = create.convertToMinor(key)
print("minor key:", minor)


# New notes test
print("\nnote generation test")
data = []
if(randint(1, 2) == 1):
    isMinor = True
else:
    isMinor = False
notes = create.newNotes()
