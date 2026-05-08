execute unless function mtb-generated:example/test_two/verify_marker run return fail
execute align xyz run tp @s ~0.5 ~0.5 ~0.5
execute at @s run function mtb-generated:example/test_two/place_blueprint/init_marker
function mtb:v0.1-alpha/find_id
kill @e[tag=mtb.example-test_two, predicate=mtb:v0.1-alpha/match_id,type=#mtb:v0.1-alpha/display]
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:example/test_two/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:example/test_two/outline/spawn_correct_outline
