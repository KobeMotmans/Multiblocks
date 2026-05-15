# check if there is a (custom) block at the current position

execute unless block ~ ~ ~ air run return 1
execute align xyz if entity @e[tag=smithed.block,dy=0] run return 1
execute align xyz if entity @e[tag=smithed.block,distance=..0.001] run return 1

return fail