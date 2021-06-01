from generate import generate

create = generate()


def gen():
    print("\n***generating melody with harmony***")
    # Get user's name
    name = "testinput"  # input("\nplease enter your name: ")
    print("\ninputting:", name)
    result = create.newComposition(name, 3)
    if(result != -1):
        print(result)
        return result
    else:
        print("ERROR")
        return "ERROR"


def msg():
    return "hello!"
