data remove storage mtb:temp args
$data modify storage mtb:temp args set value $(args)
execute align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:example/test_three/place_blueprint/aligned
