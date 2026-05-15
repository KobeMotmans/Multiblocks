
execute store result score #progress temp run function #mtb-generated:custom_block/steam_engine/get_progress
execute store result score #block_count temp run function #mtb-generated:custom_block/steam_engine/get_total_block_count

execute if score #progress temp = #block_count temp if function #mtb-generated:custom_block/steam_engine/check_conditions run function custom_block:schematic/blueprint/completed/run


