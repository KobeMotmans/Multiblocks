from __future__ import annotations
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
import re as re

from beet import Context, Function, FunctionTag, JsonFile, Structure, Predicate, EntityTypeTag, Advancement

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
#  Blockstate properties class                            
# -------------------------------

class BlockStates:
    rot_0 = []
    rot_90 = []
    rot_180 = []
    rot_270 = []

    mirrored_rot_0 = []
    mirrored_rot_90 = []
    mirrored_rot_180 = []
    mirrored_rot_270 = []

    curr_rot = 0

    @staticmethod
    def of(states: list[str]) -> BlockStates: # Make an object from a list of blockstates so we can also create an empty object using BlockStates()
        object = BlockStates()

        # Pre calculate the different rotations for this block's blockstates 
        # so we don't have to do it whilst generating files
        object.rot_0 = states
        object.rot_90 = [rotate_blockstate(state) for state in object.rot_0]
        object.rot_180 = [rotate_blockstate(state) for state in object.rot_90]
        object.rot_270 = [rotate_blockstate(state) for state in object.rot_180]

        object.mirrored_rot_0 = [mirror_blockstate_z_axis(state, states) for state in states]
        object.mirrored_rot_90 = [rotate_blockstate(state) for state in object.mirrored_rot_0]
        object.mirrored_rot_180 = [rotate_blockstate(state) for state in object.mirrored_rot_90]
        object.mirrored_rot_270 = [rotate_blockstate(state) for state in object.mirrored_rot_180]

        return object # Return the new blockstate object
    
    def get_string(self, rotation: int, mirrored: bool) -> str: # Return the blockstate as a string
        if mirrored:
            match rotation:
                case 90:
                    return ", ".join(self.mirrored_rot_90)
                case 180:
                    return ", ".join(self.mirrored_rot_180)
                case 270:
                    return ", ".join(self.mirrored_rot_270)
                case _: # default
                    return ", ".join(self.mirrored_rot_0)
        else:
            match rotation:
                case 90:
                    return ", ".join(self.rot_90)
                case 180:
                    return ", ".join(self.rot_180)
                case 270:
                    return ", ".join(self.rot_270)
                case _: # default
                    return ", ".join(self.rot_0)
            
    def get_safe_string(self, rotation: int, mirrored: bool) -> str: # get a safe string for file paths
        if mirrored:
            match rotation:
                case 90:
                    return "_".join(self.mirrored_rot_90).replace("=","-")
                case 180:
                    return "_".join(self.mirrored_rot_180).replace("=","-")
                case 270:
                    return "_".join(self.mirrored_rot_270).replace("=","-")
                case _: # default
                    return "_".join(self.mirrored_rot_0).replace("=","-")
        else:
            match rotation:
                case 90:
                    return "_".join(self.rot_90).replace("=","-")
                case 180:
                    return "_".join(self.rot_180).replace("=","-")
                case 270:
                    return "_".join(self.rot_270).replace("=","-")
                case _: # default
                    return "_".join(self.rot_0).replace("=","-")


    def get_dict_like_string(self, rotation: int, mirrored: bool) -> str:
        """Return the blockstates in the form of a stringified dict,
        EG: {<key>: "<value>", <key2>: "<value2>"}
        """

        return "{" + re.sub(r"([^,]*?)=([^,]*)", r"\g<1>:'\g<2>'", self.get_string(rotation, mirrored)) + "}"
            
    
    def rotate_cw(self, amount = 90) -> BlockStates:
        if amount % 90 == 0: # Only rotate by multiples of 90
            self.curr_rot += amount
        return self


# -------------------------------
#  Block class                            
# -------------------------------
# This class defines all ettributes corresponding to a block

class Block:
    
    block_id = ""           # The id of this block
    blockstates = BlockStates()  # The blockstates from this block
    palette = []            # Unique blocks in the function

    def __init__(self, x: float, y: float, z: float, block_id: str, blockstates: BlockStates):
        self.pos = (x, y, z)

        self.block_id = block_id
        self.blockstates = blockstates

    def __repr__(self) -> str:
        return f'Block(pos={self.pos}, block_id={self.block_id}, states={self.blockstates})'

# -------------------------------
#  The main multiblock class                            
# -------------------------------

class MultiblockCode:

    name = ""           # The name of this multiblock structure
    namespace = ""      # The namespace that adds this multiblock
    blocks = []         # A list of block objects within the structure
    center = (0, 0, 0)  # The center of the structure
    palette = []        # Unique blocks plus states
    anchor_mode = ""
    place_mode = ""
    size = (0, 0, 0)    # The size of the structure

    callback = Callback("", "")

    def __init__(self, name: str, namespace: str, blocks: list[Block], center: tuple, callback: Callback, palette: list, anchor_mode: str, place_mode: str, size: tuple):
        self.name = name
        self.blocks = blocks
        self.center = center
        self.callback = callback
        self.namespace = namespace
        self.palette = palette
        self.size = size
        self.anchor_mode = anchor_mode
        self.place_mode = place_mode

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

# -------------------------------
#  Rotate a blockstate clocwise                            
# -------------------------------
# Format: <property>=<value>
# Yup hardcoded blockstate rotation

def rotate_blockstate(blockstate: str) -> str:
    match blockstate:
        case "axis=x":
            return "axis=z"
        case "axis=z":
            return "axis=x"
        
        case "north=true":
            return "east=true"
        case "north=false":
            return "east=false"
        case "north=none":
            return "east=none"
        case "north=side":
            return "east=side"
        case "north=up":
            return "east=up"
        case "north=low":
            return "east=low"
        case "north=tall":
            return "east=tall"
        
        case "east=true":
            return "south=true"
        case "east=false":
            return "south=false"
        case "east=none":
            return "south=none"
        case "east=side":
            return "south=side"
        case "east=up":
            return "south=up"
        case "east=low":
            return "south=low"
        case "east=tall":
            return "south=tall"
        
        case "south=true":
            return "west=true"
        case "south=false":
            return "west=false"
        case "south=none":
            return "west=none"
        case "south=side":
            return "west=side"
        case "south=up":
            return "west=up"
        case "south=low":
            return "west=low"
        case "south=tall":
            return "west=tall"
        
        case "west=true":
            return "north=true"
        case "west=false":
            return "north=false"
        case "west=none":
            return "north=none"
        case "west=side":
            return "north=side"
        case "west=up":
            return "north=up"
        case "west=low":
            return "north=low"
        case "west=tall":
            return "north=tall"
        
        case "facing=north":
            return "facing=east"
        case "facing=east":
            return "facing=south"
        case "facing=south":
            return "facing=west"
        case "facing=west":
            return "facing=north"
        
        case "orientation=down_north":
            return "orientation=down_east"
        case "orientation=down_east":
            return "orientation=down_south"
        case "orientation=down_south":
            return "orientation=down_west"
        case "orientation=down_west":
            return "orientation=down_north"
        case "orientation=up_north":
            return "orientation=up_east"
        case "orientation=up_east":
            return "orientation=up_south"
        case "orientation=up_south":
            return "orientation=up_west"
        case "orientation=up_west":
            return "orientation=up_north"
        case "orientation=north_up":
            return "orientation=east_up"
        case "orientation=east_up":
            return "orientation=south_up"
        case "orientation=south_up":
            return "orientation=west_up"
        case "orientation=west_up":
            return "orientation=north_up"
        
        case "rotation=0":
            return "rotation=4"
        case "rotation=1":
            return "rotation=5"
        case "rotation=2":
            return "rotation=6"
        case "rotation=3":
            return "rotation=7"
        case "rotation=4":
            return "rotation=8"
        case "rotation=5":
            return "rotation=9"
        case "rotation=6":
            return "rotation=10"
        case "rotation=7":
            return "rotation=11"
        case "rotation=8":
            return "rotation=12"
        case "rotation=9":
            return "rotation=13"
        case "rotation=10":
            return "rotation=14"
        case "rotation=11":
            return "rotation=15"
        case "rotation=12":
            return "rotation=0"
        case "rotation=13":
            return "rotation=1"
        case "rotation=14":
            return "rotation=2"
        case "rotation=15":
            return "rotation=3"
        
        case "shape=ascending_north":
            return "shape=ascending_east"
        case "shape=ascending_east":
            return "shape=ascending_south"
        case "shape=ascending_south":
            return "shape=ascending_west"
        case "shape=ascending_west":
            return "shape=ascending_north"
        case "shape=east_west":
            return "shape=north_south"
        case "shape=north_south":
            return "shape=east_west"
        
        case "shape=north_east":
            return "shape=south_east"
        case "shape=south_east":
            return "shape=south_west"
        case "shape=south_west":
            return "shape=north_west"
        case "shape=north_west":
            return "shape=north_east"

    return blockstate # No need to rotate this specific blockstate

# -------------------------------
# mirror a blockstate around x
# -------------------------------

def mirror_blockstate_z_axis(blockstate: str, states: list[str]) -> str:
    match blockstate:
        # cardinal directions
        case "east=true":
            return "west=true"
        case "east=false":
            return "west=false"
        case "east=none":
            return "west=none"
        case "east=side":
            return "west=side"
        case "east=up":
            return "west=up"
        case "east=low":
            return "west=low"
        case "east=tall":
            return "west=tall"

        case "west=true":
            return "east=true"
        case "west=false":
            return "east=false"
        case "west=none":
            return "east=none"
        case "west=side":
            return "east=side"
        case "west=up":
            return "east=up"
        case "west=low":
            return "east=low"
        case "west=tall":
            return "east=tall"

        # facing
        case "facing=east":
            return "facing=west"
        case "facing=west":
            return "facing=east"

        # orientation (alleen de east/west swaps)
        case "orientation=down_east":
            return "orientation=down_west"
        case "orientation=down_west":
            return "orientation=down_east"
        case "orientation=up_east":
            return "orientation=up_west"
        case "orientation=up_west":
            return "orientation=up_east"
        case "orientation=east_up":
            return "orientation=west_up"
        case "orientation=west_up":
            return "orientation=east_up"

        case "rotation=1":
            return "rotation=15"
        case "rotation=2":
            return "rotation=14"
        case "rotation=3":
            return "rotation=13"
        case "rotation=4":
            return "rotation=12"
        case "rotation=5":
            return "rotation=11"
        case "rotation=6":
            return "rotation=10"
        case "rotation=7":
            return "rotation=9"
        case "rotation=9":
            return "rotation=7"
        case "rotation=10":
            return "rotation=6"
        case "rotation=11":
            return "rotation=5"
        case "rotation=12":
            return "rotation=4"
        case "rotation=13":
            return "rotation=3"
        case "rotation=14":
            return "rotation=2"
        case "rotation=15":
            return "rotation=1"

        # shapes
        case "shape=ascending_east":
            return "shape=ascending_west"
        case "shape=ascending_west":
            return "shape=ascending_east"

        case "shape=north_east":
            return "shape=north_west"
        case "shape=north_west":
            return "shape=north_east"
        case "shape=south_east":
            return "shape=south_west"
        case "shape=south_west":
            return "shape=south_east"
        
        case "shape=inner_left":
            return "shape=inner_right"
        case "shape=inner_right":
            return "shape=inner_left"
        case "shape=outer_left":
            return "shape=outer_right"
        case "shape=outer_right":
            return "shape=outer_left"

    return blockstate

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
        blocks, center, palette, size = process_nbt(json_file['structure'], ctx, namespace)

        # Process modes
        anchor_mode = json_file['anchor_mode']
        place_mode = json_file['place_mode']
    
        # Generate the callback
        callback = Callback(
            json_file['callback']['on_place'] if 'on_place' in json_file['callback'] else None,  #type: ignore
            json_file['callback']['while_complete'] if 'while_complete' in json_file['callback'] else None
        )


        # Finally, construct the multiblock code
        MultiblockCode(json_file['id'], namespace, blocks, center, callback, palette, anchor_mode, place_mode, size)


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
        report_error(f"Key 'on_place' in field callback must be of type string, {type(json['callback']['on_place'])} given", namespace, path)

    if "while_complete" in json["callback"] and not isinstance(json["callback"]["while_complete"], str):
        report_error(f"Key 'while_complete' in field callback must be of type string, {type(json['callback']['while_complete'])} given", namespace, path)

    # ======= The Mode field =======
    if not "anchor_mode" in json:
        report_error(f"Missing key: anchor_mode", namespace, path)
    if not "place_mode" in json:
        report_error(f"Missing key: place_mode", namespace, path)

    if len(json["anchor_mode"]) >= 1 and not isinstance(json['anchor_mode'][0], str):
        report_error(f"Key: anchor_mode must be of type str, {type(json['anchor_mode'])} given", namespace, path)

    if len(json["place_mode"]) >= 1 and not isinstance(json['place_mode'][0], str):
        report_error(f"Key: place_mode must be of type str, {type(json['place_mode'])} given", namespace, path)

    if json["anchor_mode"] not in ["center", "corner"]:
        report_error(f"Key: place_mode must be one of: center | corner", namespace, path)

    if json["place_mode"] not in ["center", "corner", "facing"]:
        report_error(f"Key: place_mode must be one of: center | corner | facing", namespace, path)
    
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

def process_nbt(path: str, ctx: Context, namespace: str):
    blocks = []
    center = ()

    nbt_path = find_structure(path, ctx)
    if not nbt_path:
        report_error("Failed to parse nbt", namespace, path)
        exit()

    nbt_file = nbtlib.load(nbt_path.source_path).root

    size = nbt_file["size"]
    center = (
        (float(size[0]) + 1) / 2,
        (float(size[1]) + 1) / 2,
        (float(size[2]) + 1) / 2,
    )

    palette = []
    for entry in nbt_file["palette"]:
        blockstates = []
        if "Properties" in entry:
            for prop, value in entry["Properties"].items():
                blockstates.append(f"{prop}={value}")

        palette.append({
            "block_id": entry["Name"],
            "blockstates": BlockStates.of(blockstates)
        })

    block_map = {
        tuple(b["pos"]): b["state"]
        for b in nbt_file["blocks"]
    }

    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                pos = (x, y, z)

                if pos in block_map:
                    state = palette[block_map[pos]]
                    if "four" in path:
                        print(state["block_id"])

                    block_data = state
                else:
                    continue

                blocks.append(Block(
                    x - center[0] + 1,
                    y - center[1],
                    z - center[2] + 1,
                    block_id=block_data["block_id"],
                    blockstates=block_data["blockstates"],
                ))
    print(len(blocks))
    return (blocks, center, palette, size)


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
    ctx.data.predicates["mtb:match_id"] = Predicate({
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

    # ======= Advancements =======

    # An advancement to detect block placement
    ctx.data.advancements["mtb:events/place_block"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:item_used_on_block"
            }
        },
        "rewards": {
            "function": "mtb:slow_tick"
        }
    })

    ctx.data.advancements["mtb:tool_use/axe"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {
                            "condition": "minecraft:any_of",
                            "terms": [
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_wood_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_stone_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_gold_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_copper_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_iron_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_diamond_axe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_netherite_axe": {
                                            "min": 1
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": "mtb:tool_use/axe"
        }
    })

    ctx.data.advancements["mtb:tool_use/hoe"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {
                            "condition": "minecraft:any_of",
                            "terms": [
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_wood_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_stone_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_gold_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_copper_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_iron_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_diamond_hoe": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_netherite_hoe": {
                                            "min": 1
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": "mtb:tool_use/hoe"
        }
    })

    ctx.data.advancements["mtb:tool_use/pick"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {
                            "condition": "minecraft:any_of",
                            "terms": [
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_wood_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_stone_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_gold_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_copper_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_iron_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_diamond_pick": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_netherite_pick": {
                                            "min": 1
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": "mtb:tool_use/pick"
        }
    })

    ctx.data.advancements["mtb:tool_use/shovel"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:tick",
                "conditions": {
                    "player": [
                        {
                            "condition": "minecraft:any_of",
                            "terms": [
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_wood_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_stone_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_gold_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_copper_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_iron_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_diamond_shovel": {
                                            "min": 1
                                        }
                                    }
                                },
                                {
                                    "condition": "minecraft:entity_scores",
                                    "entity": "this",
                                    "scores": {
                                        "mtb_netherite_shovel": {
                                            "min": 1
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": "mtb:tool_use/shovel"
        }
    })

    # ======= Function Files =======

    # A function to run a command without causing the function to crash during loading
    ctx.data.functions["mtb:run_command"] = Function([
        "$$(command)"
    ])

    ctx.data.functions["mtb:load"] = Function([
        "execute store result score #mtb.debug_enabled temp if entity @a[tag=mtb.debug]",
        f"execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{\"text\": \"[Server]: Multiblocks {VERSION} loaded successfully\",\"color\":\"green\"}}]",
        "scoreboard objectives add mtb_complete dummy",
        "scoreboard objectives add mtb_prev_state dummy",
        "scoreboard objectives add mtb_id dummy",

        "scoreboard objectives add mtb_wood_pick used:wooden_pickaxe",
        "scoreboard objectives add mtb_stone_pick used:stone_pickaxe",
        "scoreboard objectives add mtb_gold_pick used:golden_pickaxe",
        # Put the copper scoreboards in a macro function so the load function doesn't crash when loading a version where
        # the copper tools don't exist
        "function mtb:run_command {\"command\":\"scoreboard objectives add mtb_copper_pick used:copper_pickaxe\"}",
        "scoreboard objectives add mtb_iron_pick used:iron_pickaxe",
        "scoreboard objectives add mtb_diamond_pick used:diamond_pickaxe",
        "scoreboard objectives add mtb_netherite_pick used:netherite_pickaxe",

        "scoreboard objectives add mtb_wood_axe used:wooden_axe",
        "scoreboard objectives add mtb_stone_axe used:stone_axe",
        "scoreboard objectives add mtb_gold_axe used:golden_axe",
        "function mtb:run_command {\"command\":\"scoreboard objectives add mtb_copper_axe used:copper_axe\"}",
        "scoreboard objectives add mtb_iron_axe used:iron_axe",
        "scoreboard objectives add mtb_diamond_axe used:diamond_axe",
        "scoreboard objectives add mtb_netherite_axe used:netherite_axe",

        "scoreboard objectives add mtb_wood_shovel used:wooden_shovel",
        "scoreboard objectives add mtb_stone_shovel used:stone_shovel",
        "scoreboard objectives add mtb_gold_shovel used:golden_shovel",
        "function mtb:run_command {\"command\":\"scoreboard objectives add mtb_copper_shovel used:copper_shovel\"}",
        "scoreboard objectives add mtb_iron_shovel used:iron_shovel",
        "scoreboard objectives add mtb_diamond_shovel used:diamond_shovel",
        "scoreboard objectives add mtb_netherite_shovel used:netherite_shovel",

        "scoreboard objectives add mtb_wood_hoe used:wooden_hoe",
        "scoreboard objectives add mtb_stone_hoe used:stone_hoe",
        "scoreboard objectives add mtb_gold_hoe used:golden_hoe",
        "function mtb:run_command {\"command\":\"scoreboard objectives add mtb_copper_hoe used:copper_hoe\"}",
        "scoreboard objectives add mtb_iron_hoe used:iron_hoe",
        "scoreboard objectives add mtb_diamond_hoe used:diamond_hoe",
        "scoreboard objectives add mtb_netherite_hoe used:netherite_hoe",

        "scoreboard objectives add temp dummy",

        "function #mtb:init_storage",
        "schedule function mtb:slow_tick 1t replace"
    ])

    ctx.data.functions["mtb:slow_tick"] = Function([
        "execute as @a at @s run function #mtb:players",
        "schedule function mtb:slow_tick 10t replace",
        "advancement revoke @s only mtb:events/place_block"
    ])

    ctx.data.functions["mtb:assign_id"] = Function([
        "scoreboard players operation @s mtb_id = .max mtb_id",
        "tag @s add has_mtb_id",

        "scoreboard players add .max mtb_id 1"  # Increment the max player ID by one
    ])

    ctx.data.functions["mtb:find_id"] = Function([
        "scoreboard players operation .this mtb_id = @s mtb_id" # Set .this to the current entity's ID
    ])

    ctx.data.functions["mtb:tool_use/axe"] = Function([
        "advancement revoke @s only mtb:tool_use/axe",
        "scoreboard players set @s mtb_wood_axe 0",
        "scoreboard players set @s mtb_stone_axe 0",
        "scoreboard players set @s mtb_gold_axe 0",
        "scoreboard players set @s mtb_copper_axe 0",
        "scoreboard players set @s mtb_iron_axe 0",
        "scoreboard players set @s mtb_diamond_axe 0",
        "scoreboard players set @s mtb_netherite_axe 0",
        "execute at @s run function #mtb:players"
    ])

    ctx.data.functions["mtb:tool_use/hoe"] = Function([
        "advancement revoke @s only mtb:tool_use/hoe",
        "scoreboard players set @s mtb_wood_hoe 0",
        "scoreboard players set @s mtb_stone_hoe 0",
        "scoreboard players set @s mtb_gold_hoe 0",
        "scoreboard players set @s mtb_copper_hoe 0",
        "scoreboard players set @s mtb_iron_hoe 0",
        "scoreboard players set @s mtb_diamond_hoe 0",
        "scoreboard players set @s mtb_netherite_hoe 0",
        "execute at @s run function #mtb:players"
    ])

    ctx.data.functions["mtb:tool_use/pick"] = Function([
        "advancement revoke @s only mtb:tool_use/pick",
        "scoreboard players set @s mtb_wood_pick 0",
        "scoreboard players set @s mtb_stone_pick 0",
        "scoreboard players set @s mtb_gold_pick 0",
        "scoreboard players set @s mtb_copper_pick 0",
        "scoreboard players set @s mtb_iron_pick 0",
        "scoreboard players set @s mtb_diamond_pick 0",
        "scoreboard players set @s mtb_netherite_pick 0",
        "execute at @s run function #mtb:players"
    ])

    ctx.data.functions["mtb:tool_use/shovel"] = Function([
        "advancement revoke @s only mtb:tool_use/shovel",
        "scoreboard players set @s mtb_wood_shovel 0",
        "scoreboard players set @s mtb_stone_shovel 0",
        "scoreboard players set @s mtb_gold_shovel 0",
        "scoreboard players set @s mtb_copper_shovel 0",
        "scoreboard players set @s mtb_iron_shovel 0",
        "scoreboard players set @s mtb_diamond_shovel 0",
        "scoreboard players set @s mtb_netherite_shovel 0",
        "execute at @s run function #mtb:players"
    ])

    

# -------------------------------
#  Gen multiblock specific files                            
# -------------------------------

def gen_multiblock_files(self: MultiblockCode, ctx: Context):
    common_funcpath = f"mtb-generated:{self.namespace}/{self.name}"

    # ======= Function Files =======
    # init_blueprint
    ctx.data.functions[f"{common_funcpath}/init_blueprint"] = Function([
        "data remove storage mtb:temp args",
        "$data modify storage mtb:temp args set value $(args)",

        f"execute align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/place_blueprint/aligned"
    ])

    ctx.data.function_tags[f"{common_funcpath}/place_blueprint"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/place_blueprint/pre_summon", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/init_blueprint"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/init_blueprint", "required": False}
        ]
    })

    # place_blueprint/aligned
    ctx.data.functions[f"{common_funcpath}/place_blueprint/aligned"] = Function([
        f"function {common_funcpath}/place_blueprint/handle_rotation",
        f"execute as @e[type=marker, sort=nearest, limit=1, tag=mtb.{self.namespace}-{self.name}, tag=INIT, distance=..0.1] if data storage mtb:temp {{\"args\":{{\"mirrored\":true}}}} run tag @s add mtb.mirrored",
        f"execute as @e[type=marker, sort=nearest, limit=1, tag=mtb.{self.namespace}-{self.name}, tag=INIT, distance=..0.1] at @s rotated as @s run function {common_funcpath}/place_blueprint/pre_summon"
    ])

    # place_blueprint/handle_rotation
    ctx.data.functions[f"{common_funcpath}/place_blueprint/handle_rotation"] = Function([
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 180}}}} run return run summon marker ~ ~ ~ {{Rotation:[180f,0f], Tags:[mtb.{self.namespace}-{self.name},\"INIT\",mtb.rot_180]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 270}}}} run return run summon marker ~ ~ ~ {{Rotation:[270f,0f], Tags:[mtb.{self.namespace}-{self.name},\"INIT\",mtb.rot_270]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 90}}}} run return run summon marker ~ ~ ~ {{Rotation:[90f,0f], Tags:[mtb.{self.namespace}-{self.name},\"INIT\",mtb.rot_90]}}",
        f"summon marker ~ ~ ~ {{Rotation:[0f,0f], Tags:[mtb.{self.namespace}-{self.name},\"INIT\",mtb.rot_0]}}" # fallback
    ])
    # Handle the position of the blueprint placement
    if self.place_mode == "corner":
        ctx.data.functions[f"{common_funcpath}/place_blueprint/pre_summon"] = Function([
            f"tp @s ^{self.center[0]-1 if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2]-1 if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            "execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id",
            
            f"execute at @s rotated as @s run {self.callback.on_place}", # run the on_place callback

            "scoreboard players operation #marker_id temp = @s mtb_id",
            "scoreboard players set @s mtb_complete 0",
        ])
    elif self.place_mode == "facing":
        # Init function
        ctx.data.functions[f"{common_funcpath}/place_blueprint/pre_summon"] = Function([
            f"tp @s ^{self.center[0]-int(self.center[0]) if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2] if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            "execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id",

            f"execute at @s rotated as @s run {self.callback.on_place}", # run the on_place callback
            
            "scoreboard players operation #marker_id temp = @s mtb_id",
            "scoreboard players set @s mtb_complete 0",
        ])
    elif self.place_mode == "center": 
        # Init function
        ctx.data.functions[f"{common_funcpath}/place_blueprint/pre_summon"] = Function([
            f"tp @s ^{self.center[0]-int(self.center[0]) if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2]-int(self.center[2]) if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            "execute unless entity @s[tag=has_mtb_id] run function mtb:assign_id",

            f"execute at @s rotated as @s run {self.callback.on_place}", # run the on_place callback
            
            "scoreboard players operation #marker_id temp = @s mtb_id",
            "scoreboard players set @s mtb_complete 0",
        ])
    
    # Generate the function that acutally places the displays
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon"] = Function([
        "tag @s add mtb.has_blueprint",
        # Store the rotation in a temp score so we can use it later to modify the display's tags
        "execute if entity @s[tag=mtb.rot_0] run scoreboard players set #rotation temp 0",       
        "execute if entity @s[tag=mtb.rot_90] run scoreboard players set #rotation temp 90",
        "execute if entity @s[tag=mtb.rot_180] run scoreboard players set #rotation temp 180",
        "execute if entity @s[tag=mtb.rot_270] run scoreboard players set #rotation temp 270",
        "execute if entity @s[tag=mtb.mirrored] run scoreboard players set #is_mirrored temp 1",
        "execute if entity @s[tag=!mtb.mirrored] run scoreboard players set #is_mirrored temp 0"
    ])

    lines = [] # generate lines for each block's summon

    for block in self.blocks:
        match block.block_id:
            # ======= Handle water item-display placement =======
            case "minecraft:water": # if water
                lines.append(f'execute if entity @s[tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')           
                lines.append(f'execute if entity @s[tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')

            # ======= Handle lava item-display placement =======
            case "minecraft:lava": # if lava
                lines.append(f'execute if entity @s[tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, block_id: "{block.block_id.replace(":",".")}"}}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}')
                lines.append(f'execute if entity @s[tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, block_id: "{block.block_id.replace(":",".")}"}}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}')

            case _: # Basically an else

                # Each blockdisplay has a tag that contains it's default non rotated / mirrored blockstates. During the check a corresponding function is called that handles the rotation for that specific blockstate
                lines.append(f'execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=0, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=90, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=180, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=270, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                
                lines.append(f'execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=0, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=90, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=180, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=270, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
    
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon"].append(lines)
        

    # Modify the block display on summon
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon/modify_block_display"] = Function([
        f"$data merge entity @s {{view_range:0.12f,transformation:{{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]}},block_state:$(display_data),Tags:[\"mtb.{self.namespace}-{self.name}\", \"$(block_id)\"]}}",
        "scoreboard players operation @s mtb_id = #marker_id temp",
        "scoreboard players set @s mtb_prev_state 0",
        "tag @s add mtb.blueprint",

        # Modify the rotation according to the rotation tag of the marker
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 0 run tag @s add mtb.rot_0",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 90 run tag @s add mtb.rot_90",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 180 run tag @s add mtb.rot_180",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 270 run tag @s add mtb.rot_270",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #is_mirrored temp matches 1 run tag @s add mtb.mirrored",
        "tag @s add mtb.has_rot_tag" # Make sure to only set the rotation from the beginning
    ])
    # Modify the item display on summon
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon/modify_item_display"] = Function([
        f"$data merge entity @s {{view_range:0.12f,transformation:{{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[0f,-0f,0f],scale:[0.6f,0.6f,0.6f]}},item:$(display_data),Tags:[\"mtb.{self.namespace}-{self.name}\", \"$(block_id)\"]}}",
        "scoreboard players operation @s mtb_id = #marker_id temp",
        "scoreboard players set @s got_block 0",
        "tag @s add mtb.rot_0", # Add rot 0 for the default behaviour
        "tag @s add mtb.blueprint"
    ])

    ctx.data.functions[f"{common_funcpath}/place_blueprint/remove_blueprint"] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        'tag @s remove mtb.has_blueprint',
        f'kill @e[type=#mtb:display, predicate=mtb:match_id,tag=mtb.{self.namespace}-{self.name}, tag=mtb.blueprint]'
    ])


    # -------------------------------
    #  Checking functions                            
    # -------------------------------

    ctx.data.functions[f'{common_funcpath}/checking/main'] = Function()
    for unique_block in self.palette:
        state = unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)
        specific_funcpath = f'checking/{unique_block["block_id"].replace("minecraft:", "")}/{state if state != "" else "default"}'

        # -------------------------------
        #  NB Funcs                            
        # -------------------------------
        ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/check"] = Function([
            f'scoreboard players set #success temp 0',
            f'execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=0,mirrored=False)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=90,mirrored=False)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=180,mirrored=False)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=270,mirrored=False)}] run scoreboard players set #success temp 2',

            # No Mirror
            f'execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=0,mirrored=True)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=90,mirrored=True)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=180,mirrored=True)}] run scoreboard players set #success temp 2',
            f'execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] if block ~ ~ ~ {unique_block["block_id"]}[{unique_block["blockstates"].get_string(rotation=270,mirrored=True)}] run scoreboard players set #success temp 2',

            f'execute if score #success temp matches 0 if block ~ ~ ~ {unique_block["block_id"]} run scoreboard players set #success temp 1',
            # success = 0: completely wrong block
            # success = 1: wrong blockstate only
            # success = 2: perfect fit

            f'execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function {common_funcpath}/{specific_funcpath}/set_none',
            f'execute if score #success temp matches 0..1 run return run execute unless score @s mtb_prev_state matches 1 run function {common_funcpath}/{specific_funcpath}/set_wrong',
            f'execute unless score @s mtb_prev_state matches 2 run function {common_funcpath}/{specific_funcpath}/set_correct'
        ])

        ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"] = Function([
            'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Removed block","color":"gold"}]',
            'function mtb:find_id',
            f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:match_id,type=marker,tag=mtb.{self.namespace}-{self.name}] run scoreboard players remove @s mtb_complete 1',
            'scoreboard players set @s mtb_prev_state 0'
        ])

        # modify the display back to it's original state
        if unique_block["block_id"] == "minecraft:water":
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([f'execute if entity @s[type=minecraft:item_display] run return run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'])
        elif unique_block["block_id"] == "minecraft:lava":
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([f'execute if entity @s[type=minecraft:item_display] run return run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'])
        else:
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([
                f'execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=0, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=90, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=180, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=270, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                
                f'execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=0, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=90, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=180, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=270, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'
            ])
        
        ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_wrong"] = Function([
            'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Wrong block placed","color":"red"}]',
            'function mtb:find_id',
            f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:match_id,type=marker,tag=mtb.{self.namespace}-{self.name}] run scoreboard players remove @s mtb_complete 1',
            'scoreboard players set @s mtb_prev_state 1',
            # Make the display invisible
            "execute if entity @s[type=minecraft:item_display] if score #success temp matches 0 run return run data merge entity @s {view_range:0.06f,brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0.0f,0.0f,0.0f],scale:[1.01f,1.01f,1.01f]},item:{id:\"minecraft:red_stained_glass\"}}",
            "execute if entity @s[type=minecraft:item_display] if score #success temp matches 1 run return run data merge entity @s {view_range:0.06f,brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0.0f,0.0f,0.0f],scale:[1.01f,1.01f,1.01f]},item:{id:\"minecraft:orange_stained_glass\"}}",
            f'execute if score #success temp matches 0 run return run data merge entity @s {{view_range:0.06f,brightness:{{sky:15,block:15}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.501f,-0.501f,-0.501f],scale:[1.01f,1.01f,1.01f]}},block_state:{{Name:"{"minecraft:purple_stained_glass" if unique_block["block_id"] == "minecraft:air" else "minecraft:red_stained_glass"}"}}}}',
            'execute if score #success temp matches 1 run return run data merge entity @s {view_range:0.06f,brightness:{sky:15,block:15},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.501f,-0.501f,-0.501f],scale:[1.01f,1.01f,1.01f]},block_state:{Name:"minecraft:orange_stained_glass"}}'
        ])

        ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_correct"] = Function([
            'scoreboard players set @s mtb_prev_state 2',
            # hide the display
            'data modify entity @s transformation.scale set value [0f, 0f, 0f]', 
            f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Correct block: {unique_block["block_id"]} was placed","color":"green"}}]',
            
            'function mtb:find_id',
            f'execute as @e[predicate=mtb:match_id,type=marker,tag=mtb.{self.namespace}-{self.name}] run scoreboard players add @s mtb_complete 1'
        ])


        ctx.data.functions[f'{common_funcpath}/checking/main'].append(f'execute if entity @s[tag={unique_block["block_id"].replace(":",".")}-{state}] run function {common_funcpath}/{specific_funcpath}/check')


    ctx.data.functions[f"{common_funcpath}/checking/full_multiblock"] = Function([
        f'execute if score @s mtb_complete matches {len(self.blocks)} run {self.callback.on_complete}'
    ])
    ctx.data.function_tags[f"{common_funcpath}/remove_all"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/remove", "required": False}
        ]
    })

    ctx.data.functions[f"{common_funcpath}/remove"] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'kill @e[predicate=mtb:match_id,tag=mtb.{self.namespace}-{self.name}]'
    ])

    # ----------------------------------
    #  Mirroring and Rotating functions                    
    # ----------------------------------



    ctx.data.functions[f"{common_funcpath}/mirror_nested"] = Function([
        'execute if entity @s[tag=mtb.mirrored] run tag @s add mtb.was_mirrored',
        'execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.mirrored',
        'execute unless entity @s[tag=mtb.was_mirrored] run tag @s add mtb.mirrored',
        'execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.was_mirrored',
        f'function {common_funcpath}/place_blueprint/summon'
    ])

    ctx.data.functions[f"{common_funcpath}/mirror"] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'scoreboard players set @s mtb_complete 0',
        'kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]',
        f'execute as @s at @s rotated as @s run function {common_funcpath}/mirror_nested',
    ])
    ctx.data.function_tags[f"{common_funcpath}/mirror"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/mirror", "required": False}
        ]
    })

    ctx.data.functions[f"{common_funcpath}/rot/0_to_90"] = Function([
        "tag @s remove mtb.rot_0",
        "tag @s add mtb.rot_90"
    ])

    ctx.data.functions[f"{common_funcpath}/rot/90_to_180"] = Function([
        "tag @s remove mtb.rot_90",
        "tag @s add mtb.rot_180"
    ])

    ctx.data.functions[f"{common_funcpath}/rot/180_to_270"] = Function([
        "tag @s remove mtb.rot_180",
        "tag @s add mtb.rot_270"
    ])

    ctx.data.functions[f"{common_funcpath}/rot/270_to_0"] = Function([
        "tag @s remove mtb.rot_270",
        "tag @s add mtb.rot_0"
    ])

    ctx.data.functions[f"{common_funcpath}/rot/find_rot"] = Function([
        f"execute if entity @s[tag=mtb.rot_0] run return run function {common_funcpath}/rot/0_to_90",
        f"execute if entity @s[tag=mtb.rot_90] run return run function {common_funcpath}/rot/90_to_180",
        f"execute if entity @s[tag=mtb.rot_180] run return run function {common_funcpath}/rot/180_to_270",
        f"execute if entity @s[tag=mtb.rot_270] run return run function {common_funcpath}/rot/270_to_0"

    ])

    ctx.data.functions[f"{common_funcpath}/center_rotate_nested"] = Function([
        'rotate @s ~90 ~',
        f'execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] rotated as @s run function {common_funcpath}/outline/spawn_right_outline'
    ])
    
    if self.size[0]%2 == self.size[2]:
        ctx.data.functions[f"{common_funcpath}/center_rotate"] = Function([
            f"function {common_funcpath}/rot/find_rot",
            f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
            'function mtb:find_id',
            f'scoreboard players set @s mtb_complete 0',
            'kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]',
            f'execute as @s at @s rotated as @s run function {common_funcpath}/center_rotate_nested',
        ])
    else:
        ctx.data.functions[f"{common_funcpath}/center_rotate"] = Function([
            f"function {common_funcpath}/rot/find_rot",
            f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
            'function mtb:find_id',
            f'scoreboard players set @s mtb_complete 0',
            # fix een tp shit
            "tp @s ^-0.5 ^ ^-0.5",
            'kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]',
            f'execute as @s at @s rotated as @s run function {common_funcpath}/center_rotate_nested',
        ])

    ctx.data.functions[f"{common_funcpath}/corner_rotate"] = Function([
        f"function {common_funcpath}/rot/find_rot",
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'scoreboard players set @s mtb_complete 0',
        'kill @e[sort=nearest, type=#mtb:display, predicate=mtb:match_id]',
        f"tp @s ^{-(self.center[0]-1) if self.center[0] != 0 else ''} ^ ^{-(self.center[2]-1) if self.center[2] != 0 else ''}",
        'rotate @s ~90 ~',
        f"execute at @s rotated as @s run tp @s ^{self.center[0]-1 if self.center[0] != 0 else ''} ^ ^{self.center[2]-1 if self.center[2] != 0 else ''}",
        f'execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function {common_funcpath}/outline/spawn_right_outline'

    ])
    
    ctx.data.function_tags[f"{common_funcpath}/rotate"] = FunctionTag()

    if self.anchor_mode == "center":
        ctx.data.function_tags[f"{common_funcpath}/rotate"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/center_rotate", "required": False}]}))
    else:
        ctx.data.function_tags[f"{common_funcpath}/rotate"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/corner_rotate", "required": False}]}))


    # -------------------------------
    #  Move functions                      
    # -------------------------------

    ctx.data.functions[f'{common_funcpath}/incr_x'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~1 ~ ~'
    ])

    ctx.data.functions[f'{common_funcpath}/decr_x'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~-1 ~ ~'
    ])

    ctx.data.functions[f'{common_funcpath}/incr_y'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~ ~1 ~'
    ])

    ctx.data.functions[f'{common_funcpath}/decr_y'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~ ~-1 ~'
    ])

    ctx.data.functions[f'{common_funcpath}/incr_z'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~ ~ ~1'
    ])

    ctx.data.functions[f'{common_funcpath}/decr_z'] = Function([
        f'execute unless entity @s[type=marker, tag=mtb.{self.namespace}-{self.name}] run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Must run this command as the marker","color":"red"}}',
        'function mtb:find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.name}, predicate=mtb:match_id] at @s run tp @s ~ ~ ~-1'
    ])

    ctx.data.functions[f"{common_funcpath}/player"] = Function([
        f'execute as @e[distance=..10,type=#mtb:display,tag=mtb.{self.namespace}-{self.name}] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/checking/main',
        f'execute as @e[distance=..10,type=marker,tag=mtb.{self.namespace}-{self.name}] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/checking/full_multiblock'
    ])

     # -------------------------------
    #  Outline Functions                            
    # -------------------------------
    ctx.data.functions[f"{common_funcpath}/outline/spawn_right_outline"] = Function([
        "say jow runt dit?",
        "scoreboard players operation #marker_id mtb_id = @s mtb_id",
        "tag @s add mtb.has_outline",
        f"execute if entity @s[tag=mtb.rot_0] at @s run return run function {common_funcpath}/outline/spawn_outline_0",
        f"execute if entity @s[tag=mtb.rot_90] at @s run return run function {common_funcpath}/outline/spawn_outline_90",
        f"execute if entity @s[tag=mtb.rot_180] at @s run return run function {common_funcpath}/outline/spawn_outline_180",
        f"execute if entity @s[tag=mtb.rot_270] at @s run return run function {common_funcpath}/outline/spawn_outline_270"
    ])

    ctx.data.function_tags[f"{common_funcpath}/summon_outline"] = FunctionTag({"values": [{"id": f"{common_funcpath}/outline/spawn_right_outline", "required": False}]})

    ctx.data.function_tags[f"{common_funcpath}/remove_outline"] = FunctionTag({"values": [{"id": f"{common_funcpath}/outline/remove_outline", "required": False}]})

    ctx.data.functions[f"{common_funcpath}/outline/modify_display"] = Function([
        f'$data merge entity @s {{Tags:[mtb.outline, mtb.{self.namespace}-{self.name}],view_range:0.15f, Glowing:1b, glow_color_override:3847130, Rotation:$(Rotation), transformation:$(transformation),block_state:{{Name:"minecraft:blue_stained_glass_pane"}}}}',
        'scoreboard players operation @s mtb_id = #marker_id mtb_id'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/remove_outline"] = Function([
        'function mtb:find_id',
        f'kill @e[type=block_display,tag=mtb.outline,predicate=mtb:match_id,tag=mtb.{self.namespace}-{self.name}]',
        'tag @s remove mtb.has_outline'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_0"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_90"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_180"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_270"] = Function([
    ])

    outline_size = 0.2
    suffixes = ['0', '90', '180', '270']

    for i in range(4):
        for j, suffix in enumerate(suffixes):
            is_even = (i + j) % 2 == 0
            px, pz = (-self.center[0]+0.5, -self.center[2]+0.5) if is_even else (-self.center[2]+0.5, -self.center[0]+0.5)
            edge_len = float(self.size[0] if is_even else self.size[2])
            rot = 90 * i - 90 * j

            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{-self.center[1]-0.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[{90*i}F,0F], transformation:{{left_rotation:[0f,0f,-0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,{outline_size/2}f,-{outline_size/2}f],scale:[{outline_size}f,{edge_len}f,{outline_size}f]}}}}')
            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{self.center[1]-1.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[{90*i}F,0F], transformation:{{left_rotation:[0f,0f,-0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,{outline_size/2}f,-{outline_size/2}f],scale:[{outline_size}f,{edge_len}f,{outline_size}f]}}}}')
            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{-self.center[1]-0.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[0F,0F], transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-{outline_size/2}f,0f,-{outline_size/2}f],scale:[{outline_size}f,{float(self.size[1])}f,{outline_size}f]}}}}')
    ctx.data.function_tags[f"mtb:players"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/player", "required": False}]}))
