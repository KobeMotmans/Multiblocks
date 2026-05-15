execute unless function mtb-generated:advanced/industrial_furnace/verify_root run return fail
function mtb-generated:advanced/industrial_furnace/rot/find_rot
function mtb:v0.1.2-alpha/find_id
scoreboard players set @s mtb_complete 0
kill @e[sort=nearest, type=#mtb:v0.1.2-alpha/display, predicate=mtb:v0.1.2-alpha/match_id, tag=!mtb.root]
execute at @s run tp @s ^-1.0 ^ ^-1.0
execute rotated as @s run rotate @s ~90 ~
execute at @s rotated as @s run tp @s ^1.0 ^ ^1.0
execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/place_blueprint/summon
execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function mtb-generated:advanced/industrial_furnace/outline/spawn_correct_outline

