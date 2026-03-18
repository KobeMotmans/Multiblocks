scoreboard players operation .x temp = .t temp
scoreboard players operation .x temp /= .10 temp
scoreboard players operation .x temp *= .t temp
scoreboard players operation .x temp *= .-1 temp
scoreboard players operation .x temp /= .1000 temp
scoreboard players operation .2t temp = .t temp
scoreboard players operation .2t temp *= .2 temp
return run scoreboard players operation .x temp += .2t temp
