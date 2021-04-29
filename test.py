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

#---------------------test functions---------------------------#

# Generate a list of 10 - 50 random numbers between 0-200
def newInts():
    nums = []
    total = randint(10, 50)
    for i in range(total):
        nums.append(randint(0, 200))
    return nums

# Generate a list of 10 - 50 floating point numbers between 0 - 200
def newFloats():
    floats = []
    total = randint(10, 50)
    for i in range(total):
        floats.append(uniform(0.001, 200.001))
    return floats

# Generates a hex color number
def newHex():
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

#--------------------------------------------------------------#


# Scaling test
print("\n***scaling test***")
nums = newInts()
print("\nnew array:", nums)
print("total elements:", len(nums) - 1)
print("expected result: an array who's element values don't exceed", len(nums) - 2)
result = create.scaleTheScale(nums)
# Check result
for i in range(len(result) - 1):
    if(result[i] > len(nums) - 2):
        print("failed! i = ", i)
        break
print("\ntotal elements:", len(result))
print("result:", result)


# Floats to ints test
print("\n***floats to ints test***")
floats = newFloats()
print("new array:", floats)
print("total elements:", len(floats))
result = create.floatToInt(floats)
print("result:", result)


# Hex to int array test
print("\n***hex to int array test***")
hex = newHex()
print("new hex:", hex)
result = create.hexToIntArray(hex)
print("result:", result)


# Map integers to notes test
print("\n***integers to notes test***")
nums = newInts()
print("\ntotal new numbers:", len(nums))
print("new numbers:", nums)
if(randint(1, 2) == 1):
    isMinor = True
    print("\nusing a minor key!")
else:
    isMinor = False
    print("\nusing a major key!")
newNotes = create.newNotes(nums, isMinor)
print("\ntotal notes:", len(newNotes))
print("new notes:", newNotes)


# Map letters to numbers test
print("\n***letter to number map test***")
data = ['J', 'a', 'y']
print("\ninputted data:", data)
print("expected result: [9, 0, 24]")
result = create.mapLettersToNumbers(data)
print("result", result)