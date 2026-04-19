scoreboard players set @s mtb_prev_state 2
data modify entity @s transformation.scale set value [0f, 0f, 0f]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Correct block: minecraft:spruce_stairs was placed","color":"green"}]
function mtb:find_id
execute as @e[predicate=mtb:match_id,type=marker,tag=mtb.example-test_three] run scoreboard players add @s mtb_complete 1
