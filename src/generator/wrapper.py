from generate import generate

create = generate()


def gen(name):

    result = create.newComposition(name, 3)

    if(result != -1):
        return result

    else:
        print("ERROR: composition not received in wrapper")
        return "ERROR.mid"


def msg():
    return "hello!"
