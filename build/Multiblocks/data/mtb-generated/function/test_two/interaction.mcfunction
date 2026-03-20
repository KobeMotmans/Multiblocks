execute on target run function mtb-generated:test_two/interaction/nested_execute_0
data remove entity @s interaction
function mtb:find_id
execute if score @a[distance=..10, predicate=mtb:match_id, limit=1] rotate matches 10 run function mtb-generated:test_two/interaction/nested_execute_2
execute if score @a[distance=..10, predicate=mtb:match_id, limit=1] mirror matches 10 run function mtb-generated:test_two/interaction/nested_execute_4
