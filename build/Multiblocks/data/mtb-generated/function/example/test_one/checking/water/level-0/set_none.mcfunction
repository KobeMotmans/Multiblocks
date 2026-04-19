execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Removed block","color":"gold"}]
function mtb:find_id
execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:match_id,type=marker,tag=mtb.example-test_one] run scoreboard players remove @s mtb_complete 1
scoreboard players set @s mtb_prev_state 0
execute if entity @s[type=minecraft:item_display] run return run function mtb-generated:example/test_one/place_blueprint/summon/modify_item_display {display_data:{id:"minecraft:water_bucket"}, block_id: "minecraft.water-level-0"}
