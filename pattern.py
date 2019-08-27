import inspect
import match_extensions
import copy

class Pattern:

    def __init__(self, pattern, function_prefix='_'):
        self.function_prefix = function_prefix
        self.pattern = pattern
        self._result = False
        self._state = {
            'traces': [],
            'variables': {}
        }

    def node_matches(self, node, modifier={}, _pattern=None):

        pattern = self.pattern if _pattern is None else _pattern

        # Handle filter functions
        if isinstance(pattern, dict) and len(pattern) is 1 and self.function_prefix in list(pattern.keys())[0]:

            key = list(pattern.keys())[0]

            extension = match_extensions.get('{0}_handler'.format(key[1:]))

            data = extension(self, {
                'scope': 'node',
                'element': node,
                'pattern': pattern[key],
                'modifier': modifier,
                'state': self._state,
            })

            return data['result']

        # Handle non function matching
        if isinstance(node, dict):
            if isinstance(pattern, dict):
                return set(pattern.keys()).intersection(set(node.keys())) == pattern.keys()
            return False
        elif isinstance(node, list):
            return isinstance(pattern, list)
        else:
            return type(node) == type(pattern) and node == pattern

    def subtree_matches(self, subtree, modifier={}, _pattern=None):

        pattern = self.pattern if _pattern is None else _pattern

        results = []

        if self.node_matches(subtree, modifier, _pattern):

            # Handle filter functions
            if isinstance(pattern, dict) and len(pattern) is 1 and self.function_prefix in list(pattern.keys())[0]:
                # ToDo: Add functions
                pass

            # Handle non function matching
            if isinstance(subtree, dict):
                for key, child_pattern in pattern.items():
                    results.append((self.subtree_matches(subtree[key], modifier, child_pattern)))

            elif isinstance(subtree, list):
                for child_pattern in pattern:
                    element_found = []
                    for element in subtree:
                        element_found.append(self.subtree_matches(element, modifier, child_pattern))
                    results.append(any(element_found))
            else:
                results.append(True)

            return all(results)

        else:
            return False

    def matches(self, tree, modifiers={}):

        if 'trace' not in modifiers.keys():
            modifiers['trace'] = []

        if self.subtree_matches(tree):
            self._state['traces'].append(' > '.join(map(str, modifiers['trace'])))
            return (True, self._state)

        results = []

        if isinstance(tree, dict):
            for key, element in tree.items():
                new_modifiers = copy.deepcopy(modifiers)
                new_modifiers['trace'].append('[{0}]'.format(key))
                results.append(self.matches(element, new_modifiers)[0])

        # LISTS
        elif isinstance(tree, list):
            for idx, element in enumerate(tree):
                new_modifiers = copy.deepcopy(modifiers)
                new_modifiers['trace'].append('[{0}]'.format(idx))
                results.append(self.matches(element, new_modifiers)[0])

        else:
            results.append(False)

        return (any(results), self._state)
