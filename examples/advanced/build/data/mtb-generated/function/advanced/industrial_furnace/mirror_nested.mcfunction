execute if entity @s[tag=mtb.mirrored] run tag @s add mtb.was_mirrored
execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.mirrored
execute unless entity @s[tag=mtb.was_mirrored] run tag @s add mtb.mirrored
execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.was_mirrored
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/outline/spawn_correct_outline
