tp @s ^2.0 ^1.5 ^2.0
tag @s remove INIT
execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id

scoreboard players operation #marker_id temp = @s mtb_id
scoreboard players set @s mtb_complete 0
function mtb-generated:example/test_one/summon
