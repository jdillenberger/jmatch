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


def copy_subtree(pattern_handler, data):
    # ToDo: Implement function copy_subtree
    pass
