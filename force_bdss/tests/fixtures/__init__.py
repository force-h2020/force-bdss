from os.path import join, dirname, abspath


def get(filename):
    return join(dirpath(), filename)


def dirpath():
    return dirname(abspath(__file__))
