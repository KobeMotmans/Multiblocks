function mtb/v0.1.2-alpha/find_id
$execute store result score #entity_count temp if entity @e[type=#mtb:v0.1.2-alpha/display,scores={mtb_prev_state=0},nbt={block_state:{ Name:'$(block)'} },predicate=mtb:v0.1.2-alpha/match_id, tag=mtb.advanced-industrial_furnace]
execute run return run scoreboard players get #entity_count temp
