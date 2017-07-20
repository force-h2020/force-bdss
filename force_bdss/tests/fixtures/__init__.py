from os.path import join, dirname, abspath


def get(filename):
    return join(dirname(abspath(__file__)), filename)
