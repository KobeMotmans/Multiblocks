data remove storage mtb:temp args
$data modify storage mtb:temp args set value $(args)
execute at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:example/test_two/place_blueprint/aligned
