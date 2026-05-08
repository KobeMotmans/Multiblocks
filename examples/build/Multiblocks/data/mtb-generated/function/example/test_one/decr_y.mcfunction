execute unless function mtb-generated:example/test_one/verify_marker run return fail
function mtb:v0.1-alpha/find_id
execute as @e[tag=mtb.example-test_one, predicate=mtb:v0.1-alpha/match_id] at @s run tp @s ~ ~-1 ~
