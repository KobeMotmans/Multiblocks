execute unless function mtb-generated:custom_block/steam_engine/verify_root run return fail
execute if entity @s[tag=mtb.has_blueprint] run return fail
function mtb-generated:custom_block/steam_engine/place_blueprint/summon
execute at @s run function custom_block:schematic/blueprint/on_edit
