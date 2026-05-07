execute unless function mtb-generated:example/test_one/verify_marker run return fail
function mtb:v0.1-alpha/find_id
tag @s remove mtb.has_blueprint
kill @e[type=#mtb:v0.1-alpha/display, predicate=mtb:v0.1-alpha/match_id,tag=mtb.example-test_one, tag=mtb.blueprint]
scoreboard players set @s mtb_complete 0
