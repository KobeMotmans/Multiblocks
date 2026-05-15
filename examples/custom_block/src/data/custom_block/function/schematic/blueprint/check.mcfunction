# This function runs as an additional condition specified in the multiblock json file


# Run the markings for wrong blocks
execute positioned ^ ^ ^1 run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_left/tick
execute positioned ^ ^ ^-1 run function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil_right/tick

# Return true if both copper coils are placed correctly
execute positioned ^ ^ ^1 if function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil positioned ^ ^ ^-2 if function custom_block:schematic/blueprint/custom_blocks/checking/copper_coil run return 1
return fail