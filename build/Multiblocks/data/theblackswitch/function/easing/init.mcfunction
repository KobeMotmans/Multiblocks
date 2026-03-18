$data modify storage theblackswitch:temp easing set value {duration:$(duration),x:$(x),y:$(y),z:$(z),yaw:$(yaw),pitch:$(pitch),ease:"$(ease)"}
tag @s add tbs.easing
scoreboard players add .tbs.easing_entity_count tbs.server_data 1
scoreboard players set @s tbs.easing.prev_x 0
scoreboard players set @s tbs.easing.prev_y 0
scoreboard players set @s tbs.easing.prev_z 0
scoreboard players set @s tbs.easing.prev_yaw 0
scoreboard players set @s tbs.easing.prev_pitch 0
execute store result score @s tbs.easing.duration run data get storage theblackswitch:temp easing.duration 1
execute store result score @s tbs.easing.current_tick run data get storage theblackswitch:temp easing.duration 1
execute store result score @s tbs.easing.x run data get storage theblackswitch:temp easing.x 1000
execute store result score @s tbs.easing.y run data get storage theblackswitch:temp easing.y 1000
execute store result score @s tbs.easing.z run data get storage theblackswitch:temp easing.z 1000
execute store result score @s tbs.easing.yaw run data get storage theblackswitch:temp easing.yaw 1000
execute store result score @s tbs.easing.pitch run data get storage theblackswitch:temp easing.pitch 1000
function theblackswitch:easing/internal/set_ease
execute at @s run function theblackswitch:easing/internal/ease
