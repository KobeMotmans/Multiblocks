# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  SETTINGS                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

VERSION = 'v0.1-alpha' # moet ascii lowercase zijn

# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                            Imports and globals                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

import nbtlib

from beet import Context, Function, FunctionTag, JsonFile, Structure, Predicate, EntityTypeTag

# -------------------------------
#  Globals                            
# -------------------------------

multiblocks = []

# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                               CLASSES                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

# -------------------------------
#  Beet file class                            
# -------------------------------

class MultiblockFile(JsonFile):
    scope = ("multiblock",)
    extension = ".json"

# -------------------------------
#  A class for styling text                            
# -------------------------------

class STYLE:
    HEADER = '\033[95m'
    GRAY = '\033[90m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# -------------------------------
#  A callback class                            
# -------------------------------

class Callback:
    on_place = ""
    on_complete = ""

    def __init__(self, on_place: str, on_complete: str | None):
        self.on_place = on_place if on_place else ""
        self.on_complete = on_complete if on_complete else ""

    def __repr__(self) -> str:
        return f'Callback(on_place={self.on_place}, on_complete={self.on_complete})'

# -------------------------------
#  Block class                            
# -------------------------------
# This class defines all ettributes corresponding to a block

class Block:
    
    block_id = ""   # The id of this block
    states = []     # A list of blockstates
    palette = []    # Unique blocks in the function

    def __init__(self, x: int, y: int, z: int, block_id: str, states: list[str]):
        self.pos = (x, y, z)

        self.block_id = block_id
        self.states = states

    def __repr__(self) -> str:
        return f'Block(pos={self.pos}, block_id={self.block_id}, states={self.states})'

# -------------------------------
#  The main multiblock class                            
# -------------------------------

class MultiblockCode:

    name = ""           # The name of this multiblock structure
    namespace = ""      # The namespace that adds this multiblock
    blocks = []         # A list of block objects within the structure
    center = (0, 0, 0)  # The center of the structure
    palette = []        # Unique blocks plus states

    callback = None

    def __init__(self, name: str, namespace: str, blocks: list[Block], center: tuple, callback: Callback, palette: list):
        self.name = name
        self.blocks = blocks
        self.center = center
        self.callback = callback
        self.namespace = namespace
        self.palette = palette

        multiblocks.append(self)

    def __repr__(self) -> str:
        return f'Multiblock(name={self.name}, namespace={self.namespace}, center={self.center}, callback={self.callback}, blocks={self.blocks})'
    
    def generate(self, ctx: Context):
        gen_multiblock_files(self, ctx) # Generate the function files for this multiblock


# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                             Helper Functions                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

# ----------------------------------
#  Check if a structure file exists                            
# ----------------------------------

def find_structure(refrence: str ,ctx: Context):
    for struct_id, file in ctx.data.all(refrence):
        if isinstance(file, Structure):
            return file
    return None

# -------------------------------
# print an error in the console                            
# -------------------------------

def report_error(message: str, file_namespace: str, file_path: str, note:str = ""):
    print("")
    print(f'{STYLE.ERROR}ERROR  | {STYLE.GRAY}beet multiblocks{STYLE.ERROR} {message}')
    print(f'{STYLE.ERROR}ERROR  | {STYLE.OKCYAN}data/{file_namespace}/multiblock/{file_path}.json')
    if note:
        print(f'{STYLE.ERROR}ERROR  | {STYLE.ENDC}Notes:')
        print(f'{STYLE.ERROR}ERROR  | {STYLE.ENDC}  - {note}')
    print(f'{STYLE.ERROR}ERROR  | ')
    print("")
    print(f"{STYLE.ERROR}Error: Reported 1 error.")
    exit()

# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                           MAIN PIPELINE                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

def beet_default(ctx: Context):
    ctx.data.extend_namespace.append(MultiblockFile) #type: ignore

    yield # Wait for beet to collect all the files

    parse_json_files(ctx) # Process the json files

    gen_common_files(ctx)
    
    for multiblock in multiblocks:
        multiblock.generate(ctx)


# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                           File Parsing                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

# ----------------------------------
#  Parse json files into multicocks                           
# ----------------------------------

def parse_json_files(ctx: Context):

    for refrence_id in ctx.data[MultiblockFile]: #type: ignore
        json_file = ctx.data[MultiblockFile][refrence_id].data #type: ignore
        
        # Grab the namespace and path of this multiblock
        namespace = refrence_id.split(":")[0]
        path = refrence_id.split(':')[1] 

        # Check the json file for any syntax errors
        verify_json(json_file, namespace, path, ctx)

        # Process the nbt file
        blocks, center, palette = process_nbt(json_file['structure'], ctx)
        # Generate the callback

        callback = Callback(
            json_file['callback']['on_place'] if 'onplace' in json_file['callback'] else None,  #type: ignore
            json_file['callback']['on_complete'] if 'on_complete' in json_file['callback'] else None
        )

        # Finally, construct the multiblock code
        MultiblockCode(json_file['id'], namespace, blocks, center, callback, palette)


    # delete the json files so it doesn't show up in the build
    ctx.data[MultiblockFile].clear() #type: ignore

# -------------------------------
#  Veryfy the json file structure                            
# -------------------------------

def verify_json(json: dict, namespace: str, path: str, ctx: Context):

    # ======= The id field =======
    if not "id" in json:
        report_error(f"Missing key: id", namespace, path)

    if not isinstance(json["id"], str):
        report_error(f"Key 'id' must be of type string, {type(json['id'])} given", namespace, path)

    # ======= The structure field =======
    if not "structure" in json:
        report_error(f"Missing key: structure", namespace, path)

    if not isinstance(json["structure"], str):
        report_error(f"Key 'structure' must be of type string, {type(json['structure'])} given", namespace, path)

    # Check if the refrenced structure exists
    if not find_structure(json['structure'], ctx):
        report_error(f"Couldn\'t find structure {json['structure']}", namespace, path)

    # ======= The callback field =======
    if not "callback" in json:
        report_error(f"Missing key: callback", namespace, path)

    if not isinstance(json["callback"], dict):
        report_error(f"Key 'callback' must be of type dict, {type(json['callback'])} given", namespace, path)

    if "on_place" in json["callback"] and not isinstance(json["callback"]["on_place"], str):
        report_error(f"Key 'on_place' in field callback must be of type string, {type(json['callback']["on_place"])} given", namespace, path)

    if "on_complete" in json["callback"] and not isinstance(json["callback"]["on_complete"], str):
        report_error(f"Key 'on_complete' in field callback must be of type string, {type(json['callback']["on_complete"])} given", namespace, path)

    # ======= The Conditions field =======
    if not "conditions" in json:
        report_error(f"Missing key: conditions", namespace, path)

    if not isinstance(json["conditions"], list):
        report_error(f"Key 'conditions' must be of type list, {type(json['conditions'])} given", namespace, path)

    # Check if the conditions given are of type string
    if len(json["conditions"]) >= 1 and not isinstance(json['conditions'][0], str):
        report_error(f"Entries must be of type str in key 'conditions', {type(json['conditions'])} given", namespace, path)

# -------------------------------
#  Process the nbt file                            
# -------------------------------

def process_nbt(path: str, ctx: Context):
    blocks = []
    center = ()  

    nbt_path = find_structure(path, ctx)

    if nbt_path:
        nbt_file = nbtlib.load(nbt_path.source_path).root
        
        # ======= Handle the size =======
        size = nbt_file['size']
        center = (
            ( float(size[0]) + 1 ) / 2,
            ( float(size[1]) + 1 ) / 2,
            ( float(size[2]) + 1 ) / 2
        )

        # ======= Handle the blocks =======
        # Process the palette into a more useful structure
        palette = []
        for entry in nbt_file['palette']:
            
            blockstates = []
            if "Properties" in entry:
                for property in entry['Properties'].keys():
                    value = entry['Properties'][property]
                    blockstates.append(f"{property}={value}")

            palette.append({
                "block_id": entry['Name'],
                "blockstates": blockstates
            })

        # Generate block objects from the whole structure
        for curr_block in nbt_file['blocks']:
            pos = curr_block['pos'] # the position
            block_data = palette[curr_block['state']] # get the data from the block

            blocks.append(Block(
                int(pos[0]), int(pos[1]), int(pos[2]),             # the position
                block_id=block_data['block_id'],    # the block id
                states=block_data['blockstates'],    # a list of blockstates
            ))

    return (blocks, center, palette)


# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                        HANDLE FILE GENERATION                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

# -------------------------------
#  Gen unified files                            
# -------------------------------

def gen_common_files(ctx: Context):

    # ======= Tag files =======

    # Tick function
    if not "minecraft:tick" in ctx.data.function_tags:
        ctx.data.function_tags["minecraft:tick"] = FunctionTag()

    ctx.data.function_tags["minecraft:tick"].append(FunctionTag({
        "values": [
            {"id": "mtb:tick", "required": False}
        ]
    }))

    # Load function
    if not "minecraft:load" in ctx.data.function_tags:
        ctx.data.function_tags["minecraft:load"] = FunctionTag()

    ctx.data.function_tags["minecraft:load"].append(FunctionTag({
        "values": [
            {"id":"mtb:load", "required": False}
        ]
    }))

    # display entity tag
    ctx.data.entity_type_tags["mtb:display"] = EntityTypeTag({
        "values":[
            {
                "id": "minecraft:item_display",
                "required": False
            },
            {
                "id": "minecraft:block_display",
                "required": False
            }
        ]
    })
    ctx.data.function_tags[f"mtb:players"] = FunctionTag()

    

    # ======= Predicates =======

    # A predicate to match multiblock id's
    ctx.data.predicates["mtb:match-id"] = Predicate({
        "condition": "minecraft:entity_scores",
        "entity": "this",
        "scores": {
            "mtb_id": {
                "min": { 
                    "type": "minecraft:score", 
                    "target": {
                        "type": "minecraft:fixed", 
                        "name": ".this" 
                    },
                    "score": "mtb_id" 
                },
                "max": { 
                    "type": "minecraft:score", 
                    "target": { 
                        "type": "minecraft:fixed", 
                        "name": ".this" 
                    }, 
                    "score": "mtb_id" 
                }
            }
        }
    })

    # ======= Function Files =======

    ctx.data.functions["mtb:load"] = Function([
        "execute store result score #mtb.debug_enabled temp if entity @a[tag=mtb.debug]",
        f"execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{\"text\": \"[Server]: Multiblocks {VERSION} loaded successfully\",\"color\":\"green\"}}]",
        "scoreboard objectives add mtb_complete dummy",
        "scoreboard objectives add got_block dummy",
        "scoreboard objectives add mtb_id dummy",

        "scoreboard objectives add mirror trigger",
        "scoreboard objectives add rotate trigger",

        "scoreboard objectives add temp dummy",

        "function #mtb:init_storage"
    ])

    ctx.data.functions["mtb:tick"] = Function([
        "execute as @a at @s run function #mtb:players"
    ])

    ctx.data.functions["mtb:assign_id"] = Function([
        "scoreboard players operation @s mtb_id = .max mtb_id",
        "tag @s add has_mtb_id",

        "scoreboard players add .max mtb_id 1"  # Increment the max player ID by one
    ])

    ctx.data.functions["mtb:find_id"] = Function([
        "scoreboard players operation .this mtb_id = @s mtb_id" # Set .this to the current entity's ID
    ])

# -------------------------------
#  Gen multiblock specific files                            
# -------------------------------

def gen_multiblock_files(self: MultiblockCode, ctx: Context):
    common_funcpath = f"mtb-generated:{self.namespace}/{self.name}"

    # ======= Tag files =======

    ctx.data.function_tags[f"{common_funcpath}/place_blueprint"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/spawn_marker", "required": False}
        ]
    })

    # ======= Function Files =======

    # /place_blueprint
    ctx.data.functions[f"{common_funcpath}/place_blueprint"] = Function([
        "data remove storage mtb:temp args",
        "$data modify storage mtb:temp args set value $(args)",

        f"execute align xyz positioned ~0.50 ~ ~0.50 run function {common_funcpath}/place_blueprint/aligned"
    ])

    # place_blueprint/aligned
    ctx.data.functions[f"{common_funcpath}/place_blueprint/aligned"] = Function([
        f"function {common_funcpath}/place_blueprint/handle_rotation",

        f"execute as @e[sort=nearest, limit=1, distance=0..0.1,type=marker,tag={self.namespace}-{self.name}] at @s rotated as @s run function {common_funcpath}/summon"
    ])

    # place_blueprint/handle_rotation
    ctx.data.functions[f"{common_funcpath}/place_blueprint/handle_rotation"] = Function([
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": \"180\"}}}} run return run summon marker ~ ~ ~ {{Rotation:[180f,0f], Tags:[{self.namespace}-{self.name},\"INIT\"]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": \"270\"}}}} run return run summon marker ~ ~ ~ {{Rotation:[270f,0f], Tags:[{self.namespace}-{self.name},\"INIT\"]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": \"90\"}}}} run return run summon marker ~ ~ ~ {{Rotation:[90f,0f], Tags:[{self.namespace}-{self.name},\"INIT\"]}}",
        f"summon marker ~ ~ ~ {{Rotation:[0f,0f], Tags:[{self.namespace}-{self.name},\"INIT\"]}}" # fallback
    ])   

    # Init function
    ctx.data.functions[f"{common_funcpath}/summon"] = Function([
        f"tp @s ^ ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2] if self.center[2] != 0 else ''}",

        "tag @s remove INIT",
        "execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id",

        f"{self.callback.on_place}", # run the on_place callback
        
        "scoreboard players operation #marker_id temp = @s mtb_id"
    ])

    lines = [] # generate lines for each block's summon

    for block in self.blocks:
        match block.block_id:
            # ======= Handle water item-display placement =======
            case "water": # if water
                lines.append(f'execute unless entity @s[tag=mirrored] positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:item_display run function {common_funcpath}/init/modify_display {{block_state:"minecraft:water_bucket", block_id: "{block.block_id}"}}')           
                lines.append(f'execute if entity @s[tag=mirrored] positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:item_display run function {common_funcpath}/init/modify_display {{block_state:"minecraft:water_bucket", block_id: "{block.block_id}"}}')
            
            # ======= Handle lava item-display placement =======
            case "lava": # if lava
                lines.append(f'execute unless entity @s[tag=mirrored] positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:item_display run function {common_funcpath}/init/modify_display {{block_state:"minecraft:lava_bucket", block_id: "{block.block_id}"}}')
                lines.append(f'execute if entity @s[tag=mirrored] positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:item_display run function {common_funcpath}/init/modify_display {{block_state:"minecraft:lava_bucket", block_id: "{block.block_id}"}}')

            case _: # Basically een else
                lines.append(f'execute unless entity @s[tag=mirrored] positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:block_display run function {common_funcpath}/init/modify_display {{block_state:"{block.block_id}", block_id: "{block.block_id}"}}')
                lines.append(f'execute if entity @s[tag=mirrored] positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ''} ^{block.pos[2] if block.pos[2] != 0 else ''} summon minecraft:block_display run function {common_funcpath}/init/modify_display {{block_state:"{block.block_id}", block_id: "{block.block_id}"}}')
    
    ctx.data.functions[f"{common_funcpath}/summon"].append(lines)
        

    # Modify the item/block display on summon
    ctx.data.functions[f"{common_funcpath}/summon/modify_display"] = Function([
        f"$data merge entity @s {{transformation:{{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]}},item:{{id:\"$(block_state)\"}},block_state:{{Name:\"$(block_state)\"}},Tags:[\"{self.namespace}-{self.name}\", \"$(block_id)\"]}}",
        "scoreboard players operation @s mtb_id = #marker_id temp",
        "scoreboard players set @s got_block 0"
    ])


    # -------------------------------
    #  Checking functions                            
    # -------------------------------
    for unique_block in self.palette:
        if not unique_block["block_id"] == "minecraft:air":
            specific_funcpath = f'checking/{unique_block["block_id"].replace("minecraft:", "")}/{str(unique_block["blockstates"]).replace('[', '').replace(']', '').replace("'", "").replace(',', '').replace(' ', '_').replace('=', '_')}'

            # -------------------------------
            #  NB Funcs                            
            # -------------------------------
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/nb_to_wb_nested"] = Function([
                f'data merge entity @s {{item:{{id:"minecraft:poisonous_potato",count:1,components:{{"minecraft:item_model":"minecraft:red_stained_glass"}}}},Tags:[outline],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.01f,1.01f,1.01f]}},brightness:{{sky:15,block:15}}}}',
                'scoreboard players operation @s mtb_id = #marker_id temp'
            ])


            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/nb_to_wb"] = Function([
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Wrong block was placed","color":"red"}]',
                'scoreboard players set @s got_block 1',
                f'execute at @s summon item_display run function {common_funcpath}/{specific_funcpath}/nb_to_wb_nested'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/nb_to_rb"] = Function([
                'scoreboard players set @s got_block 2',
                f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"{unique_block["block_id"]} was placed","color":"green"}}]',
                f'execute as @e[predicate=mtb:match_id,type=marker,tag={self.name}] run scoreboard players add @s mtb_complete 1'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/nb"] = Function([
                #to nb
                'execute if block ~ ~ ~ minecraft:air run return fail',
                #to wb
                f'execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ {unique_block["block_id"]} run return run function {common_funcpath}/{specific_funcpath}/nb_to_wb',
                #to rb
                f'execute if block ~ ~ ~ {unique_block["block_id"]} run return run function {common_funcpath}/{specific_funcpath}/nb_to_rb'
            ])

            # -------------------------------
            #  WB Funcs                            
            # -------------------------------
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/wb_to_nb"] = Function([
                'kill @e[distance=..0.1,type=item_display,tag=outline]',
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Wrong block removed","color":"gold"}]',
                'scoreboard players set @s got_block 0'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/wb_to_rb"] = Function([
                'kill @e[distance=..0.1,type=item_display,tag=outline]',
                'scoreboard players set @s got_block 2',
                f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"{unique_block["block_id"]} was placed","color":"green"}}]',
                f'execute as @e[predicate=mtb:match_id,type=marker,tag={self.name}] run scoreboard players add @s mtb_complete 1'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/wb"] = Function([
                f'execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ {unique_block["block_id"]} run return fail',
                f'execute if block ~ ~ ~ minecraft:air run return run function {common_funcpath}/{specific_funcpath}/wb_to_nb',
                f'execute if block ~ ~ ~ {unique_block["block_id"]} run return run function {common_funcpath}/{specific_funcpath}/wb_to_rb'
            ])

            # -------------------------------
            #  RB Funcs                            
            # -------------------------------

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/rb_to_wb_nested"] = Function([
                f'data merge entity @s {{item:{{id:"minecraft:poisonous_potato",count:1,components:{{"minecraft:item_model":"minecraft:red_stained_glass"}}}},Tags:[outline],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.01f,1.01f,1.01f]}},brightness:{{sky:15,block:15}}}}',
                'scoreboard players operation @s mtb_id = #marker_id temp'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/rb_to_nb"] = Function([
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Right block removed","color":"red"}]',
                f'execute as @e[predicate=mtb:match_id,type=marker,tag={self.name}] run scoreboard players remove @s mtb_complete 1',
                'scoreboard players set @s got_block 0'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/rb_to_wb"] = Function([
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Right block was switched with wrong block","color":"red"}]',
                'scoreboard players set @s got_block 1',
                f'execute at @s summon item_display run function {common_funcpath}/{specific_funcpath}/rb_to_wb_nested',
                f'execute as @e[predicate=mtb:match_id,type=marker,tag={self.name}] run scoreboard players remove @s mtb_complete 1'
            ])

            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/rb"] = Function([
                f'execute if block ~ ~ ~ {unique_block["block_id"]} run return fail',
                f'execute if block ~ ~ ~ minecraft:air run return run function {common_funcpath}/{specific_funcpath}/rb_to_nb',
                f'execute unless block ~ ~ ~ minecraft:air unless block ~ ~ ~ {unique_block["block_id"]} run return run function {common_funcpath}/{specific_funcpath}/rb_to_wb',
            ])



            # -------------------------------
            #  Common Funcs                       
            # -------------------------------
            
            
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/right_tag"] = Function([
                'function mtb:find_id',
                'scoreboard players operation #marker_id temp = @s mtb_id',
                f'execute if score @s got_block matches 0 run return run function {common_funcpath}/{specific_funcpath}/nb',
                f'execute if score @s got_block matches 1 run return run function {common_funcpath}/{specific_funcpath}/wb',
                f'execute if score @s got_block matches 2 run return run function {common_funcpath}/{specific_funcpath}/rb'
            ])



            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/main"] = Function([
                f'execute if entity @s[tag={unique_block["block_id"].replace("minecraft:", "")}] run function {common_funcpath}/{specific_funcpath}/right_tag'
            ])

    ctx.data.functions[f"{common_funcpath}/checking/full_multiblock"] = Function([
        f'execute if score @s mtb_complete matches {len(self.blocks)} run {self.callback.on_complete}'
    ])
    ctx.data.function_tags[f"{common_funcpath}/build_blueprint"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/checking/full_multiblock", "required": False}
        ]
    })

    ctx.data.functions[f"{common_funcpath}/remove"] = Function([
        'function mtb:find_id',
        f'kill @e[predicate=mtb:match_id,tag={self.name}]'
    ])

    ctx.data.functions[f"{common_funcpath}/mirror_nested"] = Function([
        'execute if entity @s[tag=mirrored] run tag @s add was_mirrored',
        'execute if entity @s[tag=was_mirrored] run tag @s remove mirrored',
        'execute unless entity @s[tag=was_mirrored] run tag @s add mirrored',
        'execute if entity @s[tag=was_mirrored] run tag @s remove was_mirrored',
        f'function {common_funcpath}/summon'
    ])

    ctx.data.functions[f"{common_funcpath}/mirror"] = Function([
        'scoreboard players set @e[limit=1,sort=nearest,type=marker,tag=curr_mtb_id, predicate=mtb:match_id] mtb_complete 0',
        'kill @e[sort=nearest, type=minecraft:block_display, predicate=mtb:match_id]', # TODO: moet nog een opitmise voor vinden (max = mtb block amount?)
        'kill @e[sort=nearest, type=minecraft:item_display, predicate=mtb:match_id]',
        'execute as @e[sort=nearest, type=marker, predicate=mtb:match_id, limit=1] at @s run function mirror_nested',
        'scoreboard players set @p[sort=nearest, predicate=mtb:match_id, limit=1] mirror 0'
    ])

    ctx.data.functions[f"{common_funcpath}/rotate_nested"] = Function([
        'rotate @s facing ^90 ^ ^',
        f'execute rotated as @s run function {common_funcpath}/summon'
    ])

    ctx.data.functions[f"{common_funcpath}/rotate"] = Function([
        'scoreboard players set @e[limit=1,sort=nearest,type=marker,tag=curr_mtb_id, predicate=mtb:match_id] mtb_complete 0',
        'kill @e[sort=nearest, type=minecraft:block_display, predicate=mtb:match_id]',  # TODO: moet nog een opitmise voor vinden (max = mtb block amount?)
        'kill @e[sort=nearest, type=minecraft:item_display, predicate=mtb:match_id]',
        f'execute as @e[sort=nearest, type=marker, predicate=mtb:match_id, limit=1] at @s run function {common_funcpath}/rotate_nested',
        'scoreboard players set @p[sort=nearest, predicate=mtb:match_id, limit=1] rotate 0'
    ])


    ctx.data.functions[f"{common_funcpath}/player"] = Function([
        f'execute as @e[distance=..10,type=#mtb:display,tag=curr_mtb_id] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/multiblock_block_check',
        f'execute as @e[distance=..10,type=marker,tag=curr_mtb_id] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/multiblock_check'
    ])

    
    ctx.data.function_tags[f"mtb:players"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/player", "required": False}]}))
