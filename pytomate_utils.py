import traceback
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4).pprint


def dumpException(e):
    print("EXCEPTION:", e)
    traceback.print_tb(e.__traceback__)
