tp @s ^0.0 ^1.5 ^0.0
tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
execute at @s rotated as @s run say yay, my_test one multblock is placed
scoreboard players operation #marker_id temp = @s mtb_id
scoreboard players set @s mtb_complete 0
