$data modify storage mtb:temp args set value $(args)
execute align xyz positioned ~0.5 ~ ~0.5 run function mtb-generated:test_two/spawn_marker/nested_execute_2
