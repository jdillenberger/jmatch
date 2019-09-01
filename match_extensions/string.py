'''
# General pattern functions
Node and subtree match functions, to be executed from
a Patterns node_matches and subtree_matches function
if they are requested by the given pattern.

Functions with a _node suffix, are executed by a Patterns
"node_matches" method and functions with a _subtree suffix
are executed by a Patterns "subtree_matches" method.

The functions defined here can evaluate to true
for matching strings.
'''

import re

def regex_node(pattern_handler, data):
    #pylint: disable=unused-argument
    if isinstance(data['pattern'], (dict, list)):
        raise ValueError('Function "regex" does not support {0} args.'.format(type(data['node'])))
    if not isinstance(data['node'], (dict, list)):
        return re.compile(data['pattern']).match(str(data['node']))
    return False


def validate_node(pattern_handler, data):
    #pylint: disable=unused-argument
    validators = ['email', 'phone', 'digits', 'empty', 'base64', 'lowercase', 'uppercase']
    assert_message = '"{0}" is not a known validation pattern for validate'.format(data['pattern'])
    assert str(data['pattern']).lower() in validators, assert_message
    # ToDo: Implement function validate_node
    pass

