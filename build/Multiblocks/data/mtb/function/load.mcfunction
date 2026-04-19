execute store result score #mtb.debug_enabled temp if entity @a[tag=mtb.debug]
execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text": "[Server]: Multiblocks v0.1-alpha loaded successfully","color":"green"}]
scoreboard objectives add mtb_complete dummy
scoreboard objectives add mtb_prev_state dummy
scoreboard objectives add mtb_id dummy
scoreboard objectives add mirror trigger
scoreboard objectives add rotate trigger
scoreboard objectives add temp dummy
function #mtb:init_storage
schedule function mtb:slow_tic 1t replace
