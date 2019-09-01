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
    # Get Member functions
    member_functions = []
    for member in inspect.getmembers(match_extensions):
        funct = getattr(match_extensions, member[0])
        if inspect.isfunction(funct) and inspect.stack()[0][3] is not member[0]:
            member_functions.append(funct)

    # Create pattern-function dictionary
    pattern_functions = {func.__name__: func for func in member_functions}

    if 'node' in name and name.replace('node', 'subtree') in pattern_functions.keys():
        default = lambda x1, x2: True
    else:
        default = None

    return pattern_functions.get(name, default)
