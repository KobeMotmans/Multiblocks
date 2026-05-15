# This function runs from the on_creative_place callback specified in the json file

execute positioned ^ ^0.5 ^1 if block ~ ~ ~ air run function custom_block:copper_engine_coil/place
execute positioned ^ ^0.5 ^-1 if block ~ ~ ~ air run function custom_block:copper_engine_coil/place