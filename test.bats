#!/usr/bin/env bats

# Test application exectution
@test "Check if jMatch executes in general" {
    # No error because the error pattern matches
    run python jmatch.py --help
    [ "$status" -eq 0 ]
}


# Test return values for simple value patterns
@test "Check single value null patterns" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_null.json
    [ "$status" -eq 1 ]

    # No error because the error pattern matches
    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_null.json
    [ "$status" -eq 0 ]
}


@test "Check single value boolean patterns" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_true.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_true.json
    [ "$status" -eq 0 ]
}


@test "Check single value integer patterns" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_42.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_42.json
    [ "$status" -eq 0 ]
}


@test "Check single value float patterns" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_0_65.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_0_65.json
    [ "$status" -eq 0 ]
}


@test "Check single value sting patterns" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_apple.json
    [ "$status" -eq 0 ]
}


# Test return values for basic dictionary type elements

@test "Check empty dict" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/hero.json examples/patterns/contains_empty_dictionary.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/ingredients.json examples/patterns/contains_empty_dictionary.json
    [ "$status" -eq 0 ]

}

@test "Check single key: value pair" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_key_value_pair.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_key_value_pair.json
    [ "$status" -eq 0 ]
}


@test "Check multiple key: value pairs" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 0 ]

    run python jmatch.py -t examples/json/fruit3.json examples/patterns/contains_key_value_pairs.json
    [ "$status" -eq 0 ]

}


# Test return values for basic array types


@test "Check empty list" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/hero.json examples/patterns/contains_empty_list.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/person.json examples/patterns/contains_empty_list.json
    [ "$status" -eq 0 ]

}


@test "Check multiple values in a list" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/hero.json examples/patterns/list_contains_multiple_values.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/list_contains_multiple_values.json
    [ "$status" -eq 0 ]

}

# Test functions


@test "Check function: '_not' -> there is a element which is not XXX" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/null.json examples/patterns/contains_not_null.json
    [ "$status" -eq 0 ]

    run python jmatch.py -t examples/json/null.json examples/patterns/contains_not_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_not_null.json
    [ "$status" -eq 1 ]

}


@test "Check function: '_regex' on string value" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_regex_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_regex_apple.json
    [ "$status" -eq 0 ]

}


# Test list, dict and value compositions


@test "Check multiple dictionaries in a list" {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 0 ]

    run python jmatch.py -t examples/json/fruit3.json examples/patterns/dictionary_in_list.json
    [ "$status" -eq 0 ]

}
