execute unless function mtb-generated:example/test_one/verify_marker run return fail
function mtb:v0.1-alpha/find_id
kill @e[type=block_display,tag=mtb.outline,predicate=mtb:v0.1-alpha/match_id,tag=mtb.example-test_one]
tag @s remove mtb.has_outline
