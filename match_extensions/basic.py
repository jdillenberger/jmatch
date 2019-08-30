import re

# Not Function
def not_node(pattern_handler, data):
    #pylint: disable=unused-argument
    return True

def not_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    return not pattern_handler.subtree_matches(data['subtree'], data['pattern'])

# Or Function
def or_node(pattern_handler, data):
    #pylint: disable=unused-argument
    return True

def or_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    if not isinstance(data['pattern'], list):
        raise ValueError('The "or" function takes a list of pattern-branches as input.')
    result = []
    for pattern in data['pattern']:
        result.append(pattern_handler.subtree_matches(data['subtree'], pattern))
    return any(result)

# And Function
def and_node(pattern_handler, data):
    #pylint: disable=unused-argument
    return True

def and_subtree(pattern_handler, data):
    #pylint: disable=unused-argument
    if not isinstance(data['pattern'], list):
        raise ValueError('The "and" function takes a list of patterns as input.')
    result = []
    for pattern in data['pattern']:
        result.append(pattern_handler.subtree_matches(data['subtree'], pattern))
    return all(result)


# Regex Function
def regex_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if isinstance(data['pattern'], (dict, list)):
        raise ValueError('Function "regex" does not support {0} args.'.format(type(data['node'])))
    if not isinstance(data['node'], (dict, list)):
        return re.compile(data['pattern']).match(str(data['node']))
    return False


# Range Node
def range_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if '..' in data['pattern']:
        num1, num2 = data['pattern'].split('..').sort()

        if num1.isnumeric() and num2.isnumeric():
            if not str(data['node']).isnumeric():
                raise ValueError('The "range" function can only be applied to a nummeric value.')
            return num1 < data['node'] and num2 > data['node']

    raise ValueError

# Bigger/Smaller then functions
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


# Type Function
def type_node(pattern_handler, data):
    #pylint: disable=unused-argument
    return type(data['node']) == data['pattern']
