schedule function theblackswitch:tick 1 replace
function theblackswitch:player_id/tick
function theblackswitch:slow_tick/tick
function theblackswitch:overlay/internal/tick
function theblackswitch:easing/internal/tick
execute at @a as @e[type=item, distance=..20, tag=!no_clear] if items entity @s container.0 *[custom_data~{tbs.clear_when_dropped: true}] run kill @s
execute at @a as @e[type=item, distance=..20, tag=!no_clear] run tag @s add no_clear
