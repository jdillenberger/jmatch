'''
# General pattern functions
Node and subtree match functions, to be executed from
a Patterns node_matches and subtree_matches function
if they are requested by the given pattern.

Functions with a _node suffix, are executed by a Patterns
"node_matches" method and functions with a _subtree suffix
are executed by a Patterns "subtree_matches" method.

The functions defined here make the pattern true
for matching nummeric values.
'''

def range_node(pattern_handler, data):
    #pylint: disable=unused-argument
    assert '..' in data['pattern'], 'The range defined in your pattern has no valid range format'
    num1, num2 = data['pattern'].split('..').sort()

    if num1.isnumeric() and num2.isnumeric():
        if not str(data['node']).isnumeric():
            return False
        return num1 < float(data['node']) and num2 > float(data['node'])

    raise ValueError


def bigger_then_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if not str(data['pattern']).isnumeric() and not str(data['pattern']).isnumeric():
        raise ValueError('The "bigger_then" function can only be applied to a nummeric value.')
    return data['node'] > data['pattern']


def bigger_then_equal_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if not str(data['pattern']).isnumeric() and not str(data['pattern']).isnumeric():
        error = 'The "bigger_then_equal" function can only be applied to a nummeric value.'
        raise ValueError(error)
    return data['node'] >= data['pattern']


def smaller_then_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if not str(data['pattern']).isnumeric() and not str(data['pattern']).isnumeric():
        raise ValueError('The "smaller_then" function can only be applied to a nummeric value.')
    return data['node'] < data['pattern']


def smaller_then_equal_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if not str(data['pattern']).isnumeric() and not str(data['pattern']).isnumeric():
        error = 'The "smaller_then_equal" function can only be applied to a nummeric value.'
        raise ValueError(error)
    return data['node'] <= data['pattern']
