execute store success score #success temp run function mtb:check_for_custom_blocks_function_or_something
execute if score #success temp matches 0 run return fail
return 1
