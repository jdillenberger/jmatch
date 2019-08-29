#!/usr/bin/env bats

# Test application exectution
@test "Check if jMatch executes in general" {
    # No error because the error pattern matches
    run python jmatch.py --help
    [ "$status" -eq 0 ]
}


# Test return values for simple value patterns
@test "Check single value null patterns" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_null.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_null.json
    [ "$status" -eq 0 ]
}


@test "Check single value boolean patterns" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_true.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_true.json
    [ "$status" -eq 0 ]
}


@test "Check single value integer patterns" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_42.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_42.json
    [ "$status" -eq 0 ]
}


@test "Check single value float patterns" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_0_65.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_0_65.json
    [ "$status" -eq 0 ]
}


@test "Check single value sting patterns" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_apple.json
    [ "$status" -eq 0 ]
}


# Test return values for basic dictionary type elements

@test "Check empty dict" {
    run python jmatch.py -f examples/json/hero.json examples/patterns/contains_empty_dictionary.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/ingredients.json examples/patterns/contains_empty_dictionary.json
    [ "$status" -eq 0 ]
}

@test "Check single key: value pair" {
    # Error because the error pattern matches
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_key_value_pair.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_key_value_pair.json
    [ "$status" -eq 0 ]
}


@test "Check multiple key: value pairs" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/fruit3.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 0 ]
}


# Test return values for basic array types
@test "Check empty list" {
    run python jmatch.py -f examples/json/hero.json examples/patterns/contains_empty_list.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/person.json examples/patterns/contains_empty_list.json
    [ "$status" -eq 0 ]
}


@test "Check multiple values in a list" {
    run python jmatch.py -f examples/json/hero.json examples/patterns/list_contains_multiple_values.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/list_contains_multiple_values.json
    [ "$status" -eq 0 ]
}

# Test functions
@test "Check function: '_not' -> there is a element which is not XXX" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/null.json examples/patterns/contains_not_null.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/null.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_not_null.json
    [ "$status" -eq 1 ]
}


@test "Check function: '_regex' on string value" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_regex_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_regex_apple.json
    [ "$status" -eq 0 ]
}


# Test list, dict and value compositions
@test "Check multiple dictionaries in a list" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/fruit3.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 0 ]
}


@test "Check multiple dictionaries in a list for YAML" {
    run python jmatch.py --format YAML -f examples/yaml/fruit1.yml examples/patterns/dictionary_in_list.yml
    [ "$status" -eq 1 ]

    run python jmatch.py --format YAML -f examples/yaml/fruit2.yml examples/patterns/dictionary_in_list.yml
    [ "$status" -eq 0 ]

    run python jmatch.py --format YAML -f examples/yaml/fruit3.yml examples/patterns/dictionary_in_list.yml
    [ "$status" -eq 0 ]
}

@test "Check for dictionary in 'not'" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_dict_in_not.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit3.json examples/patterns/contains_dict_in_not.json
    [ "$status" -eq 0 ]
}

@test "Check greater_then function" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_greater_then_42.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_greater_then_42.json
    [ "$status" -eq 1 ]
}

@test "Check greater_then_equal function" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_greater_then_equal_43.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_greater_then_equal_43.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit3.json examples/patterns/contains_greater_then_equal_43.json
    [ "$status" -eq 1 ]
}

@test "Check smaller_then_equal function" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_smaller_then_equal_42.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_smaller_then_equal_42.json
    [ "$status" -eq 0 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_smaller_then_equal_42.json
    [ "$status" -eq 0 ]
}

@test "Check smaller_then function" {
    run python jmatch.py -f examples/json/fruit1.json examples/patterns/contains_smaller_then_43.json
    [ "$status" -eq 1 ]

    run python jmatch.py -f examples/json/fruit2.json examples/patterns/contains_smaller_then_43.json
    [ "$status" -eq 0 ]
}







