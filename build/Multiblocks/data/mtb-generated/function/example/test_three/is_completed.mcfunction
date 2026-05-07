execute unless function mtb-generated:example/test_three/verify_marker run return fail
execute if entity @s[tag=mtb.completed] at @s rotated as @s if function mtb-generated:example/test_three/checking/conditions run return 1
return 0
