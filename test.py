'''
----------------------------------------------------------------------------------------------------
                        THIS FILE IS FOR TESTING GENERATIVE FUNCTIONS
----------------------------------------------------------------------------------------------------
'''

# Import and new object
from random import randint
from generate import generate 
create = generate()

#---------------------test functions---------------------------#

# Generate a list of 10-50 random numbers between 0-200
def newInts():
    nums = []
    total = randint(10, 50)
    for i in range(total):
        nums.append(randint(0, 200))
    return nums


#--------------------------------------------------------------#


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


# Map integers to notes test
print("\nintegers to notes test")
nums = newInts()
print("new numbers:", nums)
if(randint(1, 2) == 1):
    isMinor = True
    print("using a minor key!")
else:
    isMinor = False
    print("using a major key!")
newNotes = create.newNotes(nums, isMinor)
print("new notes:", newNotes)


# Map letters to numbers test
print("\nletter to number map test")
data = ['J', 'a', 'y']
print("inputted data:", data)
print("expected result: [9, 0, 24]")
print(create.mapLettersToNumbers(data))


# Pick key test
print("\npick key test")
key = create.pickKey()
print("result: key of", key[0], "major. scale:", key)


# Convert to minor test
print("\nconvert to relative minor test")
key = create.pickKey()
print("major key:", key)
minor = create.convertToMinor(key)
print("minor key:", minor)


# # New notes test
# print("\nnote generation test")
# data = []
# if(randint(1, 2) == 1):
#     isMinor = True
# else:
#     isMinor = False
# notes = create.newNotes()
