execute unless function mtb-generated:basic/house/verify_marker run return fail
execute align xyz run tp @s ~0.5 ~0.5 ~0.5
execute at @s run function mtb-generated:basic/house/place_blueprint/init_marker
function mtb:v0.1.2-alpha/find_id
kill @e[tag=mtb.basic-house, predicate=mtb:v0.1.2-alpha/match_id,type=#mtb:v0.1.2-alpha/display]
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:basic/house/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:basic/house/outline/spawn_correct_outline
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Repositioning house instance","color":"white"}]
