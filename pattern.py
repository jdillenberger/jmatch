from typing import Union, Callable
import copy
import match_extensions

IMPOSSIBLE_VALUE = '_-NONE-_'
TreeType = Union[None, bool, int, float, str, list, dict]

class Pattern:

    def __init__(self, pattern: TreeType, function_prefix: str = '_'):
        self.function_prefix: str = function_prefix
        self.pattern: TreeType = pattern
        self._result: bool = False
        self._state: dict = {
            'traces': [],
            'variables': {}
        }

    def node_matches(self, node: TreeType, new_pattern: TreeType = IMPOSSIBLE_VALUE):

        pattern: TreeType = self.pattern if new_pattern is IMPOSSIBLE_VALUE else new_pattern

        # Handle filter functions
        if isinstance(pattern, dict) \
            and len(pattern) == 1 \
            and self.function_prefix in list(pattern.keys())[0]:

            key: list = list(pattern.keys())[0]

            extension: Union[Callable, None] = match_extensions.get('{0}_node'.format(key[1:]))

            if callable(extension):

                result = extension(self, {
                    'node': node,
                    'pattern': copy.deepcopy(pattern[key]),
                    'state': self._state,
                })

                if result is not None:
                    return result

        # Handle non function matching
        if isinstance(node, dict):
            if isinstance(pattern, dict):
                return set(pattern.keys()).intersection(set(node.keys())) == pattern.keys()
            return False
        elif isinstance(node, list):
            return isinstance(pattern, list)
        else:
            return type(node) == type(pattern) and node == pattern

    def subtree_matches(self, subtree: TreeType, new_pattern: TreeType = IMPOSSIBLE_VALUE):

        pattern: TreeType = self.pattern if new_pattern is IMPOSSIBLE_VALUE else new_pattern

        results: list = []

        if self.node_matches(subtree, pattern):

            # Handle filter functions
            if isinstance(pattern, dict) \
                and len(pattern) == 1 \
                and self.function_prefix in list(pattern.keys())[0]:
                key = list(pattern.keys())[0]

                extension: Union[Callable, None] = match_extensions \
                                                        .get('{0}_subtree'.format(key[1:]))

                if callable(extension):

                    result: bool = extension(self, {
                        'subtree': subtree,
                        'pattern': copy.deepcopy(pattern[key]),
                        'state': self._state,
                    })

                    if result in [True, False]:
                        return result

            # Handle non function matching
            if isinstance(subtree, dict) and isinstance(pattern, dict):
                for key, child_pattern in pattern.items():
                    results.append((self.subtree_matches(subtree[key], child_pattern)))

            elif isinstance(subtree, list) and isinstance(pattern, list):
                for child_pattern in pattern:
                    element_found: list = []
                    for element in subtree:
                        element_found.append(self.subtree_matches(element, child_pattern))
                    results.append(any(element_found))
            else:
                results.append(True)

            return all(results)

        else:
            return False

    def matches(self, tree: TreeType, modifiers: dict = {}):

        if 'trace' not in modifiers.keys():
            modifiers['trace'] = []

        if self.subtree_matches(tree):
            self._state['traces'].append(' > '.join(map(str, modifiers['trace'])))
            return (True, self._state)

        results: list = []

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
