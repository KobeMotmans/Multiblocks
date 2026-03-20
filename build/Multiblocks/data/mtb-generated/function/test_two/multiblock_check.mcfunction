function mtb-generated:find_id
execute as @e[type=interaction, tag=test_two, predicate=mtb:match_id] at @s run function mtb-generated:test_two/interaction
execute if score @s mtb_complete matches 9 run say "Full house!"
