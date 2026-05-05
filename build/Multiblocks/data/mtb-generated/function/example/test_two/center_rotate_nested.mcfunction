rotate @s ~90 ~
execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function mtb-generated:example/test_two/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] rotated as @s run function mtb-generated:example/test_two/outline/spawn_right_outline
