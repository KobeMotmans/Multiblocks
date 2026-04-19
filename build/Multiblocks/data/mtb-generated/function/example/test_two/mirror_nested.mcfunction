execute if entity @s[tag=mtb.mirrored] run tag @s add mtb.was_mirrored
execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.mirrored
execute unless entity @s[tag=mtb.was_mirrored] run tag @s add mtb.mirrored
execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.was_mirrored
function mtb-generated:example/test_two/summon
