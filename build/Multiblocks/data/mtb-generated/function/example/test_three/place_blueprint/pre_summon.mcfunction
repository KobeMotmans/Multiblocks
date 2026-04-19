tp @s ^0.0 ^3.0 ^0.0
tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id
say yay, my_test three multblock is placed
scoreboard players operation #marker_id temp = @s mtb_id
scoreboard players set @s mtb_complete 0
function mtb-generated:example/test_three/place_blueprint/summon
