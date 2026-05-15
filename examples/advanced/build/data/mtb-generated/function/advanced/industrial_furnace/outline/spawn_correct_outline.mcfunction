scoreboard players operation #marker_id mtb_id = @s mtb_id
tag @s add mtb.has_outline
execute if entity @s[tag=mtb.rot_0] at @s run return run function mtb-generated:advanced/industrial_furnace/outline/spawn_outline_0
execute if entity @s[tag=mtb.rot_90] at @s run return run function mtb-generated:advanced/industrial_furnace/outline/spawn_outline_90
execute if entity @s[tag=mtb.rot_180] at @s run return run function mtb-generated:advanced/industrial_furnace/outline/spawn_outline_180
execute if entity @s[tag=mtb.rot_270] at @s run return run function mtb-generated:advanced/industrial_furnace/outline/spawn_outline_270
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Showing outline for industrial_furnace instance","color":"white"}]
