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

# Scaling test
print("\nscaling test")
nums = newInts()
print("\nnew array:", nums)
print("\ntotal elements:", len(nums) - 1)
print("\nexpected result: an array who's element values don't exceed", len(nums) - 2)
result = create.scaleTheScale(nums)
# Check result
for i in range(len(result) - 1):
    if(result[i] > len(nums) - 2):
        print("failed! i = ", i)
        break
print("\nresult:", result)

# Map integers to notes test
print("\nintegers to notes test")
nums = newInts()
print("\nnew numbers:", nums)
if(randint(1, 2) == 1):
    isMinor = True
    print("using a minor key!")
else:
    isMinor = False
    print("using a major key!")
newNotes = create.newNotes(nums, isMinor)
print("\ntotal notes:", len(newNotes))
print("new notes:", newNotes)


# # Map letters to numbers test
# print("\nletter to number map test")
# data = ['J', 'a', 'y']
# print("inputted data:", data)
# print("expected result: [9, 0, 24]")
# print(create.mapLettersToNumbers(data))

