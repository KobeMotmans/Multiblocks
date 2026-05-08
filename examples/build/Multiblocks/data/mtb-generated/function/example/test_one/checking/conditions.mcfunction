execute store success score #success temp run execute if score #test_three temp matches 5
execute if score #success temp matches 0 run return fail
return 1
