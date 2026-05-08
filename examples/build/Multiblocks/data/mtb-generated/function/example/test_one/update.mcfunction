execute as @e[distance=..10,type=#mtb:v0.1-alpha/display,tag=mtb.example-test_one] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:example/test_one/checking/main
execute as @e[distance=..10,type=marker,tag=mtb.example-test_one] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb-generated:example/test_one/checking/full_multiblock
