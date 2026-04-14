execute if entity @s[tag=mirrored] run tag @s add was_mirrored
execute if entity @s[tag=was_mirrored] run tag @s remove mirrored
execute unless entity @s[tag=was_mirrored] run tag @s add mirrored
execute if entity @s[tag=was_mirrored] run tag @s remove was_mirrored
function mtb-generated:example/test_one/summon
