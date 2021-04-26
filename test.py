'''
----------------------------------------------------------------------------------------------------
                        THIS FILE IS FOR TESTING GENERATIVE FUNCTIONS

NOTE:



----------------------------------------------------------------------------------------------------
'''

# Import and new object
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
print("result:", key)

# Convert to minor test
print("\nconvert to natural minor test")
key = create.pickKey()
print("major key:", key)
minor = create.convertToMinor(key)
print("minor key:", minor)


