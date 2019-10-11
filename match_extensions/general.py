'''
# General pattern functions
Node and subtree match functions, to be executed from
a Patterns node_matches and subtree_matches function
if they are requested by the given pattern.

Functions with a _node suffix, are executed by a Patterns
"node_matches" method and functions with a _subtree suffix
are executed by a Patterns "subtree_matches" method.

The functions defined here can match a pattern for various
datatypes.
'''

def not_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    return not pattern_handler.subtree_matches(data['subtree'], data['pattern'])


def or_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    if not isinstance(data['pattern'], list):
        raise ValueError('The "or" function takes a list of pattern-branches as input.')
    result = []
    for pattern in data['pattern']:
        result.append(pattern_handler.subtree_matches(data['subtree'], pattern))
    return any(result)


def and_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    if not isinstance(data['pattern'], list):
        raise ValueError('The "and" function takes a list of patterns as input.')
    result = []
    for pattern in data['pattern']:
        result.append(pattern_handler.subtree_matches(data['subtree'], pattern))
    return all(result)


def type_node(pattern_handler, data):
    #pylint: disable=unused-argument
    return type(data['node']) == data['pattern']

def type_node(pattern_handler, data):
    if data['pattern'] in ["string", "str"]:
        return isinstance(data['node'], str)
    elif data['pattern'] in ["integer", "int"]:
        return isinstance(data['node'], int)
    elif data['pattern'] in ["float"]:
        return isinstance(data['node'], float)
    elif data['pattern'] in ["list", "array"]:
        return isinstance(data['node'], list)
    elif data['pattern'] in ["dict", "object"]:
        return isinstance(data ['node'], dict)
    elif data['pattern'] in ["value"]:
        return not (isinstance(data['node'], list) or isinstance(data['node'], dict))
    elif data['pattern'] in ["anything"]:
        return True
    else:
        return False


def copy_subtree(pattern_handler, data):
    # ToDo: Implement function copy_subtree
    pass
