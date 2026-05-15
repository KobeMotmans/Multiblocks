# This function runs from the on_edit callback specified in the json file

# When the blueprint is moved, rotated or edited in any way, we have to re-position our blueprint markers
execute if function #mtb-generated:custom_block/steam_engine/blueprint/is_visible if entity @s[tag=cb.has_custom_markers] run \
    function custom_block:schematic/blueprint/custom_blocks/move_markers

# When showing the blueprint, summon the markers
execute if function #mtb-generated:custom_block/steam_engine/blueprint/is_visible unless entity @s[tag=cb.has_custom_markers] run \
    function custom_block:schematic/blueprint/custom_blocks/summon_markers

# When hiding the blueprunt, kill the markers
execute unless function #mtb-generated:custom_block/steam_engine/blueprint/is_visible run \
    function custom_block:schematic/blueprint/custom_blocks/remove_markers