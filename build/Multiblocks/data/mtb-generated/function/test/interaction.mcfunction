execute on target run function mtb-generated:test/interaction/nested_execute_0
data remove entity @s interaction
function mtb:find_id
execute if score @a[sort=nearest, predicate=mtb:match_id, limit=1] rotate matches 10 run function mtb-generated:test/rotate
execute if score @a[sort=nearest, predicate=mtb:match_id, limit=1] mirror matches 10 run function mtb-generated:test/mirror
