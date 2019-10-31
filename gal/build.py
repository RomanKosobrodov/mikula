import os


def build_from(directory):
    for x in os.walk(directory):
        print(x)