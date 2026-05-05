function mtb:find_id
kill @e[type=block_display,tag=mtb.outline,predicate=mtb:match_id,tag=mtb.example-test_one]
tag @s remove mtb.has_outline
