#!/usr/bin/env bats

# Test return values for simple value patterns

@test "Check single value null patterns " {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_null.json
    [ "$status" -eq 1 ]

    # No error because the error pattern matches
    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_null.json
    [ "$status" -eq 0 ]
}


@test "Check single value boolean patterns " {
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


@test "Check single value sting patterns " {
    # Error because the error pattern matches
    run python jmatch.py -t examples/json/fruit1.json examples/patterns/contains_apple.json
    [ "$status" -eq 1 ]

    run python jmatch.py -t examples/json/fruit2.json examples/patterns/contains_apple.json
    [ "$status" -eq 0 ]
}


