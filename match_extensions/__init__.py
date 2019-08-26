import inspect
import match_extensions
from match_extensions.basic import *

def get(name):
    member_functions = []
    for member in inspect.getmembers(match_extensions):
        funct = getattr(match_extensions, member[0])
        if inspect.isfunction(funct) and inspect.stack()[0][3] is not member[0]:
            member_functions.append(funct)
    return {func.__name__: func for func in member_functions }[name]

