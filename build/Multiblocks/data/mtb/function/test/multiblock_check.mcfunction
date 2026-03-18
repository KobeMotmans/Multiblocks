function mtb:find_id
execute as @e[type=interaction, tag=test, predicate=mtb:match_id] at @s run function mtb:test/interaction
execute if score @s mtb_complete matches 41 run say "Full house!"
