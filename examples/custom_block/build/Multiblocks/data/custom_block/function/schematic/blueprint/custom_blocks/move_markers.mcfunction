
# our markers are symmetrical so we don't have to account for mirroring.
# If your parts aren't, you should check for the function #mtb-generated:<namespace>/<mtb_id>/is_mirrored
# and make your behaviour dependant on that (you may need to re-summon them with different offsets)

# Rotate the parts in the right direction
# Whoops I accidentally modelled the markers with a 90° offset so account for that here :P
execute rotated as @s on passengers if entity @s[tag=cb.copper_coil_marker] run rotate @s ~90 ~