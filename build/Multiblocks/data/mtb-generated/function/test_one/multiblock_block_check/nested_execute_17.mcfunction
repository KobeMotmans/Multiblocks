function mtb:find_id
scoreboard players operation #marker_id temp = @s mtb_id
execute if score @s got_block matches 0 run return run function mtb-generated:test_one/multiblock_block_check/nested_return_63
execute if score @s got_block matches 1 run return run function mtb-generated:test_one/multiblock_block_check/nested_return_67
execute if score @s got_block matches 2 run return run function mtb-generated:test_one/multiblock_block_check/nested_return_71
