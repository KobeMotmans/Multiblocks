execute store success score #success temp run function custom_block:schematic/blueprint/check
execute if score #success temp matches 0 run return fail
return 1
