rotate @s ~90 ~
execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function mtb-generated:basic/house/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] rotated as @s run function mtb-generated:basic/house/outline/spawn_correct_outline
