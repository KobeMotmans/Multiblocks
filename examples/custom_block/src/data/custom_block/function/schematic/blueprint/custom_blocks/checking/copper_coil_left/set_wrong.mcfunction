# Set the scale of the coil marker parts to 0 and store their original scale
execute on passengers if entity @s[tag=cb.copper_coil_marker,tag=cb.left,tag=!cb.wrong_marker] run data modify entity @s data.default_scale set from entity @s transformation.scale
execute on passengers if entity @s[tag=cb.copper_coil_marker,tag=cb.left,tag=!cb.wrong_marker] run data modify entity @s transformation.scale set value [0f, 0f, 0f]

# Show the wrong marker
execute on passengers if entity @s[tag=cb.wrong_marker,tag=cb.left,tag=cb.copper_coil_marker] run data modify entity @s transformation.scale set value [1.01f, 1.01f, 1.01f]

tag @s add cb.left.wrong
tag @s remove cb.left.correct