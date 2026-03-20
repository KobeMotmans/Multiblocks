from beet import Context, Function, TextFile
from pathlib import Path

test = [('minecraft:dirt', 'dirt', [0, 1, 0]), ('minecraft:dirt', 'dirt', [0, 1, 1]), ('minecraft:dirt', 'dirt', [1, 1, 0]), ('minecraft:structure_block', 'structure_block', [0, 0, 0])]

mtb_list = {"test": (test, ['minecraft:dirt', 'minecraft:structure_block'])}


# Runs during the build
def beet_default(ctx: Context):
    mtb_block_check(ctx)
    yield ## Stuff after yield runs after the build is almost finished
    ## A sound when the build is (**mostly**) finished
    create_player(ctx)
    create_marker(ctx)
    create_mtb(ctx)



def create_player(ctx: Context):
    path = f"mtb:player"
    player_code = []
    for mtb in mtb_list.keys():
        lines = [
            f"execute as @s at @e[distance=(0,10),type=marker,tag=rotor, tag=INIT] align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:{mtb}/spawn_marker",
            f"execute as @e[distance=(0,10),type=minecraft:block_display,tag={mtb}] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:{mtb}/multiblock_block_check",
            f"execute as @e[distance=(0,10),type=marker,tag={mtb}] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function mtb:{mtb}/multiblock_check_"
        ]
        player_code.extend(lines)
    ctx.data.functions[path] = Function(player_code)

def create_marker(ctx: Context):
    for mtb in mtb_list.keys():
        path = f"mtb-generated:{mtb}/spawn_marker"
        lines = [
            "execute if entity @s[y_rotation=135..225] run summon marker ~ ~ ~ {Rotation:[180f,0f], Tags:[mtb,INIT]}",
            "execute if entity @s[y_rotation=225..315] run summon marker ~ ~ ~ {Rotation:[270f,0f], Tags:[mtb,INIT]}",
            "execute if entity @s[y_rotation=315..] run summon marker ~ ~ ~ {Rotation:[0f,0f], Tags:[mtb,INIT]}",
            "execute if entity @s[y_rotation=..45] run summon marker ~ ~ ~ {Rotation:[0f,0f], Tags:[mtb,INIT]}",
            "execute if entity @s[y_rotation=45..135] run summon marker ~ ~ ~ {Rotation:[90f,0f], Tags:[mtb,INIT]}",
            f"execute as @e[distance=(0,0.1),type=marker,tag={mtb}, tag=INIT] at @s rotated as @s run function mtb:{mtb}/multiblock_init",
            "kill @e[distance=(0,1),type=marker,tag=rotor, tag=INIT]"
        ]
        ctx.data.functions[path] = Function(lines)


def create_mtb(ctx):
    for mtb in mtb_list.keys():
        path = f"mtb-generated:{mtb}/mtb_init"
        function_code = []
        for item in mtb_list[mtb][0]:
            block, block_stripped, pos = item[0], item[1], item[2]
            lines = [
                'summon block_display ^%d ^%d ^%d {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]},block_state:{Name:"%s"},Tags:[%s, %s]}' % (pos[0], pos[1], pos[2], block, mtb, block_stripped)
            ]
            function_code.extend(lines)
    ctx.data.functions[path] = Function(function_code)


def mtb_block_check(ctx):
    bolt_code =""
    for mtb in mtb_list.keys():
        bolt_code += f"function mtb-generated:{mtb}/multiblock_block_check:"
        for block in mtb_list[mtb][1]:
            path = f"mtb-generated:{mtb}/multiblock_block_check"
            bolt_code += """
    if entity @s[tag=%s]:
        if block ~ ~ ~ minecraft:air unless score @s got_block matches 0:
            if score @s got_block matches 2 run execute as @e[distance=(0,5),type=marker,tag=%s] scoreboard players remove @s mtb_complete 1
            scoreboard players set @s got_block 0
            kill @e[distance=..0.1, type=item_display, tag=outline]
        if block ~ ~ ~ %s unless score @s got_block matches 2:
            scoreboard players set @s got_block 2
            execute as @e[distance=(0,5),type=marker,tag=%s] scoreboard players add @s mtb_complete 1
        unless block ~ ~ ~ %s unless block ~ ~ ~ minecraft:air unless score @s got_block matches 1:
            scoreboard players set @s got_block 1
            summon item_display ~ ~ ~ {item:{id:"minecraft:poisonous_potato",count:1,components:{"minecraft:item_model":"mtb:red_outline"}},Tags:[outline]}\n""" % (block.replace("minecraft:", ""), mtb, block, mtb, block)
    with open("src/data/mtb/modules/generated_logic.bolt", "w", encoding="utf8") as f:
        f.write(bolt_code)
        f.close()

    