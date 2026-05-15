execute if score #rot.target temp matches 0 run function #mtb-generated:advanced/industrial_furnace/rotate/set_rotation {rotation:0}
execute if score #rot.target temp matches 90 run function #mtb-generated:advanced/industrial_furnace/rotate/set_rotation {rotation:90}
execute if score #rot.target temp matches 180 run function #mtb-generated:advanced/industrial_furnace/rotate/set_rotation {rotation:180}
execute if score #rot.target temp matches 270 run function #mtb-generated:advanced/industrial_furnace/rotate/set_rotation {rotation:270}
function #mtb-generated:advanced/industrial_furnace/move/set_pos

function #mtb-generated:advanced/industrial_furnace/outline/show