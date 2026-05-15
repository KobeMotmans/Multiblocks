execute if score #rot.target temp matches 0 run function #mtb-generated:custom_block/steam_engine/rotate/set_rotation {rotation:0}
execute if score #rot.target temp matches 90 run function #mtb-generated:custom_block/steam_engine/rotate/set_rotation {rotation:90}
execute if score #rot.target temp matches 180 run function #mtb-generated:custom_block/steam_engine/rotate/set_rotation {rotation:180}
execute if score #rot.target temp matches 270 run function #mtb-generated:custom_block/steam_engine/rotate/set_rotation {rotation:270}
function #mtb-generated:custom_block/steam_engine/move/set_pos

function #mtb-generated:custom_block/steam_engine/outline/show