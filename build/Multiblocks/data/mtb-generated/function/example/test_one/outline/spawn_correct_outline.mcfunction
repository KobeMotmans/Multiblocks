execute unless function mtb-generated:example/test_one/verify_marker run return fail
scoreboard players operation #marker_id mtb_id = @s mtb_id
tag @s add mtb.has_outline
execute if entity @s[tag=mtb.rot_0] at @s run return run function mtb-generated:example/test_one/outline/spawn_outline_0
execute if entity @s[tag=mtb.rot_90] at @s run return run function mtb-generated:example/test_one/outline/spawn_outline_90
execute if entity @s[tag=mtb.rot_180] at @s run return run function mtb-generated:example/test_one/outline/spawn_outline_180
execute if entity @s[tag=mtb.rot_270] at @s run return run function mtb-generated:example/test_one/outline/spawn_outline_270
