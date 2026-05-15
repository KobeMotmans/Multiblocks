scoreboard players set @s mtb_prev_state 2
data modify entity @s transformation.scale set value [0f, 0f, 0f]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Correct block: minecraft:polished_granite_stairs was placed","color":"green"}]
function mtb:v0.1.2-alpha/find_id
execute as @e[predicate=mtb:v0.1.2-alpha/match_id,type=minecraft:block_display,tag=mtb.advanced-industrial_furnace,tag=mtb.root] run scoreboard players add @s mtb_complete 1
