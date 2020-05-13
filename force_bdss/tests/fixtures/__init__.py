#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from os.path import join, dirname, abspath


def get(filename):
    return join(dirpath(), filename)


def dirpath():
    return dirname(abspath(__file__))
