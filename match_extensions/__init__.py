'''
Loader for pattern functions.
'''

from typing import Callable
import inspect
import match_extensions
from match_extensions.general import *
from match_extensions.string  import *
from match_extensions.number  import *
from match_extensions.tree    import *

def get(name) -> Callable:
    '''
    Function: get
    returns available package functions by name
    '''
    member_functions = []
    for member in inspect.getmembers(match_extensions):
        funct = getattr(match_extensions, member[0])
        if inspect.isfunction(funct) and inspect.stack()[0][3] is not member[0]:
            member_functions.append(funct)
    return {func.__name__: func for func in member_functions}.get(name, None)
