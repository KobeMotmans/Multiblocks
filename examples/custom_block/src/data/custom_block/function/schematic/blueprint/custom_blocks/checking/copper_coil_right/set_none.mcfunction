
# reset the scale of the coil marker parts back to their default
execute on passengers if entity @s[tag=cb.copper_coil_marker,tag=cb.right,tag=!cb.wrong_marker] run data modify entity @s transformation.scale set from entity @s data.default_scale

# Hide the wrong marker
execute on passengers if entity @s[tag=cb.wrong_marker,tag=cb.right,tag=cb.copper_coil_marker] run data modify entity @s transformation.scale set value [0f, 0f, 0f]

tag @s remove cb.right.wrong
tag @s remove cb.right.correct