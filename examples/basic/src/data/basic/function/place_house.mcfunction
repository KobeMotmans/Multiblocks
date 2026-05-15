
# Face the root in the direction the player is looking
execute facing entity @p feet rotated ~180 0 run rotate @s ~ ~

# Summon a multiblock instance
execute if entity @s[y_rotation=-45..45] run function #mtb-generated:basic/house/summon_instance {args:{rotation:0}}
execute if entity @s[y_rotation=45..135] run function #mtb-generated:basic/house/summon_instance {args:{rotation:90}}
execute if entity @s[y_rotation=135..225] run function #mtb-generated:basic/house/summon_instance {args:{rotation:180}}
execute if entity @s[y_rotation=225..315] run function #mtb-generated:basic/house/summon_instance {args:{rotation:270}}

# Kill the root that is spawned with the item
kill @s