



# Reset the marker parts back to their normal state
execute unless entity @s[tag=!cb.left.wrong,tag=!cb.left.correct] unless function custom_block:schematic/blueprint/custom_blocks/checking/check_block unless function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_left/set_none

# Reset the marker parts back to their normal state
execute unless entity @s[tag=cb.left.wrong] if function custom_block:schematic/blueprint/custom_blocks/checking/check_block unless function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_left/set_wrong

# Reset the marker parts back to their normal state
execute unless entity @s[tag=cb.left.correct] if function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_left/set_correct

