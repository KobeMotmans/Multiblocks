function mtb-generated:find_id
execute as @e[type=interaction, tag=test, predicate=mtb:match_id] at @s run function mtb-generated:test/interaction
execute if score @s mtb_complete matches 41 run say "Full house!"
