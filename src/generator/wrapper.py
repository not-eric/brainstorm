from generate import generate

create = generate()


def gen(name):

    if name == '':
        return "ERROR.mid"

    print("\n===================================================")
    print("Generating music for user:", name)
    result = create.newComposition(name, 3)
    print("===================================================\n")

    if(result != -1):
        return result

    else:
        print("ERROR: composition not received in wrapper")
        return "ERROR.mid"


def msg():
    return "hello!"
