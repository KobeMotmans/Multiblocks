



# Reset the marker parts back to their normal state
execute unless entity @s[tag=!cb.right.wrong,tag=!cb.right.correct] unless function custom_block:schematic/blueprint/custom_blocks/checking/check_block unless function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_right/set_none

# Reset the marker parts back to their normal state
execute unless entity @s[tag=cb.right.wrong] if function custom_block:schematic/blueprint/custom_blocks/checking/check_block unless function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_right/set_wrong

# Reset the marker parts back to their normal state
execute unless entity @s[tag=cb.right.correct] if function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_right/set_correct

