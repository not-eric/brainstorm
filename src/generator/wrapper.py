from generate import generate

create = generate()


def gen(name):

    if name == '':
        return "ERROR.mid", ''

    result, abc = create.newComposition(name, 3)

    if(result != -1):
        return result, abc

    else:
        print("ERROR: composition not received in wrapper")
        return "ERROR.mid", ''


def msg():
    return "hello!"
