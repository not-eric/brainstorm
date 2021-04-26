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
result = create.convertNums(data)
print("result:", result)

# Map letters to numbers test
print("\nletter to number map test")
data = ['J', 'a', 'y']
print("inputted data:", data)
print("expected result: [9, 0, 24]")
result = create.mapLettersToNumbers(data)
print("result:", result)

# Find largest int test
print("\nfind largest int test")
data = [4, 20, 1, 399, 24, 3, 4, 93849384]
print("inputted data:", data)
print("expected result: 93849384")
result = create.findLargest(data)
print("result:", result)

# Pick key test
print("\npick key test")
key = create.pickKey()
print("result:", key)

# Convert to minor test
print("\nconvert to minor test")
key = create.pickKey()
print("major key:", key)
minor = create.convertToMinor(key)
print("minor key:", minor)


