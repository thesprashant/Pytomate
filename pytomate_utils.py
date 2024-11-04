import traceback
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


def dumpException(e):
    print("%s EXCEPTION:" % e.__class__.__name__, e)
    traceback.print_tb(e.__traceback__)
