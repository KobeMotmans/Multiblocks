from __future__ import annotations
# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                                  SETTINGS                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

VERSION_NUMBER = 1   # Increment dit voor elke release
VERSION = 'v0.1.4-alpha' # moet ascii lowercase zijn

# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                            Imports and globals                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

import nbtlib
import re as re
import json

from beet import Context, Function, FunctionTag, JsonFile, Structure, Predicate, EntityTypeTag, Advancement


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
    on_edit = ""
    on_creative_place = ""
    on_uncomplete = ""
    on_clear_area = ""

    def __init__(self, on_place: str, on_complete: str | None, on_edit: str | None, on_creative_place: str | None, on_uncomplete: str | None, on_clear_area: str | None):
        self.on_place = on_place if on_place else ""
        self.on_complete = on_complete if on_complete else ""
        self.on_edit = on_edit if on_edit else ""
        self.on_creative_place = on_creative_place if on_creative_place else ""
        self.on_uncomplete = on_uncomplete if on_uncomplete else ""
        self.on_clear_area = on_clear_area if on_clear_area else ""

    def __repr__(self) -> str:
        return f'Callback(on_place={self.on_place}, on_complete={self.on_complete}, on_edit={self.on_edit}, on_creative_place={self.on_creative_place}, on_uncomplete={self.on_uncomplete}, on_clear_area={self.on_clear_area})'

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
            
    def get_safe_string(self, rotation: int, mirrored: bool) -> str: # get a safe string for file paths and shit
        regex = r"[^_\n-]*-([^_\n]*)" # a magical regex that removes the property from the list
        sub = r"\g<1>"

        if mirrored:
            match rotation:
                case 90:
                    return re.sub(regex, sub, "_".join(self.mirrored_rot_90).replace("=","-"))
                case 180:
                    return re.sub(regex, sub, "_".join(self.mirrored_rot_180).replace("=","-"))
                case 270:
                    return re.sub(regex, sub, "_".join(self.mirrored_rot_270).replace("=","-"))
                case _: # default
                    return re.sub(regex, sub, "_".join(self.mirrored_rot_0).replace("=","-"))
        else:
            match rotation:
                case 90:
                    return re.sub(regex, sub, "_".join(self.rot_90).replace("=","-"))
                case 180:
                    return re.sub(regex, sub, "_".join(self.rot_180).replace("=","-"))
                case 270:
                    return re.sub(regex, sub, "_".join(self.rot_270).replace("=","-"))
                case _: # default
                    return re.sub(regex, sub, "_".join(self.rot_0).replace("=","-"))


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
#  Entity class                            
# -------------------------------

class Entity:
    
    entity_id = ""              # Always "minecraft:item_display"
    pos = (0.0, 0.0, 0.0)       # Position of the entity
    custom_tag = ""             # Safe string version from mtb_type (for tags, dispatch, file paths)
    mtb_type_raw = ""           # Raw value from data.mtb_type (for exact nbt matching)
    item_id = ""                # Item ID from item.id (e.g., "minecraft:poisonous_potato")
    item_components = {}        # Item components dict (e.g., {"minecraft:item_model": "tpmg:furnace/alloy_furnace"})

    item_snbt = ""              # SNBT string for item (used in summon macro)
    transformation_snbt = ""    # SNBT string for transformation (used in summon macro)
    data_snbt = ""              # SNBT string for data component (used in summon macro)

    def __init__(self, x: float, y: float, z: float, entity_id: str, custom_tag: str = "",
                 mtb_type_raw: str = "",
                 item_id: str = "", item_components: dict | None = None,
                 item_snbt: str = "{}", transformation_snbt: str = "{}", data_snbt: str = "{}"):
        self.pos = (x, y, z)
        self.entity_id = entity_id
        self.custom_tag = custom_tag
        self.mtb_type_raw = mtb_type_raw
        self.item_id = item_id
        self.item_components = item_components or {}
        self.item_snbt = item_snbt
        self.transformation_snbt = transformation_snbt
        self.data_snbt = data_snbt

    def __repr__(self) -> str:
        return f'Entity(pos={self.pos}, entity_id={self.entity_id}, custom_tag={self.custom_tag}, mtb_type_raw={self.mtb_type_raw}, item_id={self.item_id})'

# -------------------------------
#  The main multiblock class                            
# -------------------------------

class MultiblockCode:

    name = ""           # The name of this multiblock structure
    namespace = ""      # The namespace that adds this multiblock
    blocks = []         # A list of block objects within the structure
    entities = []       # A list of entity objects within the structure
    center = (0, 0, 0)  # The center of the structure
    palette = []        # Unique blocks plus states
    entity_palette = []  # Unique entity types plus data
    anchor_mode = ""
    place_mode = ""
    size = (0, 0, 0)    # The size of the structure
    conditions = []

    callback = Callback("", "", "", "", "", "")

    def __init__(self, name: str, namespace: str, blocks: list[Block], entities: list[Entity], center: tuple, callback: Callback, conditions: list[str], palette: list, entity_palette: list, anchor_mode: str, place_mode: str, size: tuple, structure_path: str, multiblocks: list):
        self.name = name
        self.blocks = blocks
        self.entities = entities
        self.center = center
        self.callback = callback
        self.conditions = conditions
        self.namespace = namespace
        self.palette = palette
        self.entity_palette = entity_palette
        self.size = size
        self.anchor_mode = anchor_mode
        self.place_mode = place_mode
        self.structure_path = structure_path

        multiblocks.append(self)

    def __repr__(self) -> str:
        return f'Multiblock(name={self.name}, namespace={self.namespace}, center={self.center}, callback={self.callback}, blocks={self.blocks}, entities={self.entities})'
    
    def get_safe_name(self) -> str:
        """Convert name to Minecraft-safe tag format by replacing / with -"""
        return self.name.replace("/", "-")
    
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


def nbt_to_dict(nbt_obj) -> dict:
    """Convert nbtlib NBT object to a JSON-serializable dict"""
    if nbt_obj is None:
        return None
    
    # If it's already a dict, return it
    if isinstance(nbt_obj, dict):
        return {k: nbt_to_dict(v) for k, v in nbt_obj.items()}
    
    # Handle nbtlib types by converting to their Python equivalents
    if hasattr(nbt_obj, '__class__'):
        class_name = nbt_obj.__class__.__name__
        
        # For Compound (nbtlib dict-like objects)
        if class_name == 'Compound':
            result = {}
            for key, val in nbt_obj.items():
                result[key] = nbt_to_dict(val)
            return result
        
        # For List (nbtlib list-like objects)
        elif class_name == 'List':
            return [nbt_to_dict(item) for item in nbt_obj]
        
        # For primitive types, get their value
        elif hasattr(nbt_obj, 'value'):
            return nbt_obj.value
    
    # Fallback for primitives
    return nbt_obj

def dict_to_json_string(obj) -> str:
    """Convert a dict/NBT object to a JSON string for mcfunction macro"""
    if obj is None:
        return ""
    
    converted = nbt_to_dict(obj)
    return json.dumps(converted)

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
        
        # facing
        case "hinge=left":
            return "hinge=right"
        case "hinge=right":
            return "hinge=left"

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
    multiblocks = []

    ctx.data.extend_namespace.append(MultiblockFile) #type: ignore

    yield # Wait for beet to collect all the files

    parse_json_files(ctx, multiblocks) # Process the json files

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

def parse_json_files(ctx: Context, multiblocks):

    for refrence_id in ctx.data[MultiblockFile]: #type: ignore
        json_file = ctx.data[MultiblockFile][refrence_id].data #type: ignore
        
        # Grab the namespace and path of this multiblock
        namespace = refrence_id.split(":")[0]
        path = refrence_id.split(':')[1] 

        # Check the json file for any syntax errors
        verify_json(json_file, namespace, path, ctx)

        # Process the nbt file
        blocks, entities, center, palette, size = process_nbt(json_file['structure'], ctx, namespace)

        # Process modes
        anchor_mode = json_file['anchor_mode']
        place_mode = json_file['place_mode']
    
        # Generate the callback
        callback = Callback(
            json_file['callback']['on_place'] if 'on_place' in json_file['callback'] else None,  #type: ignore
            json_file['callback']['on_complete'] if 'on_complete' in json_file['callback'] else None,
            json_file['callback']['on_edit'] if 'on_edit' in json_file['callback'] else None,
            json_file['callback']['on_creative_place'] if 'on_creative_place' in json_file['callback'] else None,
            json_file['callback']['on_uncomplete'] if 'on_uncomplete' in json_file['callback'] else None,
            json_file['callback']['on_clear_area'] if 'on_clear_area' in json_file['callback'] else None
        )

        conditions = json_file['conditions']

        # Build entity palette (unique custom tags, similar to block palette)
        entity_tags_seen = set()
        entity_palette = []
        for entity in entities:
            if entity.custom_tag not in entity_tags_seen:
                entity_tags_seen.add(entity.custom_tag)
                entity_palette.append(entity)

        # Finally, construct the multiblock code
        MultiblockCode(json_file['id'], namespace, blocks, entities, center, callback, conditions, palette, entity_palette, anchor_mode, place_mode, size, json_file['structure'], multiblocks)


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

    if "on_complete" in json["callback"] and not isinstance(json["callback"]["on_complete"], str):
        report_error(f"Key 'on_complete' in field callback must be of type string, {type(json['callback']['on_complete'])} given", namespace, path)

    if "on_edit" in json["callback"] and not isinstance(json["callback"]["on_edit"], str):
        report_error(f"Key 'on_edit' in field callback must be of type string, {type(json['callback']['on_edit'])} given", namespace, path)

    if "on_creative_place" in json["callback"] and not isinstance(json["callback"]["on_creative_place"], str):
        report_error(f"Key 'on_creative_place' in field callback must be of type string, {type(json['callback']['on_creative_place'])} given", namespace, path)
    
    if "on_uncomplete" in json["callback"] and not isinstance(json["callback"]["on_uncomplete"], str):
        report_error(f"Key 'on_uncomplete' in field callback must be of type string, {type(json['callback']['on_uncomplete'])} given", namespace, path)
    
    if "on_clear_area" in json["callback"] and not isinstance(json["callback"]["on_clear_area"], str):
        report_error(f"Key 'on_clear_area' in field callback must be of type string, {type(json['callback']['on_clear_area'])} given", namespace, path)

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
    entities = []
    center = ()

    nbt_path = find_structure(path, ctx)
    if not nbt_path:
        report_error("Failed to parse nbt", namespace, path)
        exit()

    nbt_file = nbtlib.load(nbt_path.source_path).root

    size = nbt_file["size"]
    center = (
        (float(size[0]) + 1) / 2,
        (float(size[1]) + 1) / 2 - 1,
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

                # Remove structure voids completely from the list
                if pos in block_map:
                    state = palette[block_map[pos]]
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
    
    # Process entities from NBT
    
    if "entities" in nbt_file:
        for entity_data in nbt_file["entities"]:
            nbt = entity_data["nbt"]
            entity_id = nbt["id"]

            # Only process item_display entities
            if entity_id != "minecraft:item_display":
                continue

            pos = entity_data["pos"]
            
            # Calculate position relative to center
            entity_x = pos[0] - center[0] + 0.5
            entity_y = pos[1] - center[1] - 0.5
            entity_z = pos[2] - center[2] + 0.5

            # SNBT strings for summon macro
            item_str = nbtlib.serialize_tag(nbt["item"]) if "item" in nbt else "{}"
            transformation_str = nbtlib.serialize_tag(nbt["transformation"]) if "transformation" in nbt else "{}"
            custom_data_str = nbtlib.serialize_tag(nbt["data"]) if "data" in nbt else "{}"

            # Parse structured fields for checking logic
            item_id = "minecraft:air"
            item_components = {}
            if "item" in nbt:
                item_nbt = nbt["item"]
                item_id = str(item_nbt.get("id", "minecraft:air"))
                if "components" in item_nbt:
                    comps_nbt = item_nbt["components"]
                    if hasattr(comps_nbt, 'items'):
                        item_components = {str(k): nbt_to_dict(v) for k, v in comps_nbt.items()}

            mtb_type_raw = "unknown"
            if "data" in nbt:
                data_nbt = nbt["data"]
                if hasattr(data_nbt, 'get') and "mtb_type" in data_nbt:
                    mtb_type_raw = str(data_nbt["mtb_type"])
            custom_tag = mtb_type_raw.replace(":", ".").replace("/", "-")

            entities.append(Entity(
                entity_x,
                entity_y,
                entity_z,
                entity_id=entity_id,
                custom_tag=custom_tag,
                mtb_type_raw=mtb_type_raw,
                item_id=item_id,
                item_components=item_components,
                item_snbt=item_str,
                transformation_snbt=transformation_str,
                data_snbt=custom_data_str
            ))

    
    return (blocks, entities, center, palette, size)


# ==========================================================================================================================================
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                                        HANDLE FILE GENERATION                                                                       
# ------------------------------------------------------------------------------------------------------------------------------------------
# ==========================================================================================================================================

# -------------------------------
#  Gen unified files                            
# -------------------------------

def gen_common_files(ctx: Context):

    # ======= Lantern Load =======

    # Load function
    if not "minecraft:load" in ctx.data.function_tags:
        ctx.data.function_tags["minecraft:load"] = FunctionTag()

    ctx.data.function_tags["minecraft:load"].prepend(FunctionTag({
        "values": [
            {"id":"#load:_private/load", "required": False}
        ]
    }))

    # Run the lantern load tree. This splits the load into 3 phases
    ctx.data.function_tags['load:_private/load'] = FunctionTag({
        "values": [
            "load:_private/init", # Reset all version scores
            {
                "id": "#load:pre_load", # can be used for dependencies that need to load before their main packs
                "required": False
            },
            {
                "id": "#load:load", # Normal use, the main load (our library)
                "required": False
            },
            {
                "id": "#load:post_load", # Can be used for addons
                "required": False
            }
        ]
    })

    # Reset scoreboards so packs can set values accurately for current load.
    ctx.data.functions['load:_private/init'] = Function([
        "scoreboard objectives add load.status dummy",
        "scoreboard players reset * load.status"
    ])

    # The main load tag from lantern load, this is were we start loading our own stuff
    if not "load:load" in ctx.data.function_tags:
        ctx.data.function_tags["load:load"] = FunctionTag()

    ctx.data.function_tags["load:load"].prepend(FunctionTag({
        "values": [
            {"id":"#mtb:load/load", "required": False}
        ]
    }))

    # Our own loading is also split in another 2 phases
    ctx.data.function_tags["mtb:load/load"] = FunctionTag({
        "values": [
            "#mtb:load/enumerate", # First we try to find the highest loaded version
            "#mtb:load/resolve" # Then we only load the one with the highest version
        ]
    })

    # Find the highest loaded instance of this library
    ctx.data.function_tags["mtb:load/enumerate"] = FunctionTag({
        "values": [
            # each different pack instance will add it's own enumerate function here so 
            # they all run in the enumerate phase before the resolve phase
            {"id":f"mtb:{VERSION}/load/enumerate", "required": False} 
        ]
    })

    ctx.data.functions[f"mtb:{VERSION}/load/enumerate"] = Function([
        # if the currently enumerated version is lower than the one for our pack instance increase it to our version
        f"execute unless score #max_mtb_version load.status matches {VERSION_NUMBER}.. run scoreboard players set #max_mtb_version load.status {VERSION_NUMBER}"
    ])

    # only load the instance with the highest version
    ctx.data.function_tags["mtb:load/resolve"] = FunctionTag({
        "values": [
            # each different pack instance will add it's own resolve function here
            {"id":f"mtb:{VERSION}/load/resolve", "required": False} 
        ]
    })

    ctx.data.functions[f"mtb:{VERSION}/load/resolve"] = Function([
        # if the max loaded version number is the same as the current one, load our load function
        f"execute if score #max_mtb_version load.status matches {VERSION_NUMBER} run function mtb:{VERSION}/load"
    ])


    # ======= Tag files =======

    # display entity tag
    ctx.data.entity_type_tags[f"mtb:{VERSION}/display"] = EntityTypeTag({
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
    ctx.data.function_tags[f"mtb:update_multiblock"] = FunctionTag()

    

    # ======= Predicates =======

    # A predicate to match multiblock id's
    ctx.data.predicates[f"mtb:{VERSION}/match_id"] = Predicate({
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
    ctx.data.advancements[f"mtb:{VERSION}/events/place_block"] = Advancement({
        "criteria": {
            "requirement": {
                "trigger": "minecraft:item_used_on_block",
                "conditions": {
                    "player": [
                        {
                            "condition": "minecraft:value_check",
                            "value": {
                                "type": "minecraft:score",
                                "target": {
                                    "type": "minecraft:fixed",
                                    "name": "#max_mtb_version"
                                },
                                "score": "load.status"
                            },
                            "range": VERSION_NUMBER
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": f"mtb:{VERSION}/slow_tick"
        }
    })

    ctx.data.advancements[f"mtb:{VERSION}/tool_use/axe"] = Advancement({
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
                        },
                        {
                            "condition": "minecraft:value_check",
                            "value": {
                                "type": "minecraft:score",
                                "target": {
                                    "type": "minecraft:fixed",
                                    "name": "#max_mtb_version"
                                },
                                "score": "load.status"
                            },
                            "range": VERSION_NUMBER
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": f"mtb:{VERSION}/tool_use/axe"
        }
    })

    ctx.data.advancements[f"mtb:{VERSION}/tool_use/hoe"] = Advancement({
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
                        },
                        {
                            "condition": "minecraft:value_check",
                            "value": {
                                "type": "minecraft:score",
                                "target": {
                                    "type": "minecraft:fixed",
                                    "name": "#max_mtb_version"
                                },
                                "score": "load.status"
                            },
                            "range": VERSION_NUMBER
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": f"mtb:{VERSION}/tool_use/hoe"
        }
    })

    ctx.data.advancements[f"mtb:{VERSION}/tool_use/pick"] = Advancement({
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
                        },
                        {
                            "condition": "minecraft:value_check",
                            "value": {
                                "type": "minecraft:score",
                                "target": {
                                    "type": "minecraft:fixed",
                                    "name": "#max_mtb_version"
                                },
                                "score": "load.status"
                            },
                            "range": VERSION_NUMBER
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": f"mtb:{VERSION}/tool_use/pick"
        }
    })

    ctx.data.advancements[f"mtb:{VERSION}/tool_use/shovel"] = Advancement({
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
                        },
                        {
                            "condition": "minecraft:value_check",
                            "value": {
                                "type": "minecraft:score",
                                "target": {
                                    "type": "minecraft:fixed",
                                    "name": "#max_mtb_version"
                                },
                                "score": "load.status"
                            },
                            "range": VERSION_NUMBER
                        }
                    ]
                }
            }
        },
        "rewards": {
            "function": f"mtb:{VERSION}/tool_use/shovel"
        }
    })

    # ======= Function Files =======

    # A function to run a command without causing the function to crash during loading
    ctx.data.functions[f"mtb:{VERSION}/run_command"] = Function([
        "$$(command)"
    ])

    ctx.data.functions[f"mtb:{VERSION}/load"] = Function([
        "execute store result score #mtb.debug_enabled temp if entity @a[tag=mtb.debug]",
        f"execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{\"text\": \"[Server]: Multiblocks {VERSION} loaded successfully\",\"color\":\"green\"}}]",
        "scoreboard objectives add mtb_complete dummy",
        "scoreboard objectives add mtb_prev_state dummy",
        "scoreboard objectives add mtb_id dummy",
        "scoreboard objectives add mtb_prev_x dummy",
        "scoreboard objectives add mtb_prev_y dummy",
        "scoreboard objectives add mtb_prev_z dummy",

        "scoreboard objectives add mtb_wood_pick used:wooden_pickaxe",
        "scoreboard objectives add mtb_stone_pick used:stone_pickaxe",
        "scoreboard objectives add mtb_gold_pick used:golden_pickaxe",
        # Put the copper scoreboards in a macro function so the load function doesn't crash when loading a version where
        # the copper tools don't exist
        f"function mtb:{VERSION}/run_command {{\"command\":\"scoreboard objectives add mtb_copper_pick used:copper_pickaxe\"}}",
        "scoreboard objectives add mtb_iron_pick used:iron_pickaxe",
        "scoreboard objectives add mtb_diamond_pick used:diamond_pickaxe",
        "scoreboard objectives add mtb_netherite_pick used:netherite_pickaxe",

        "scoreboard objectives add mtb_wood_axe used:wooden_axe",
        "scoreboard objectives add mtb_stone_axe used:stone_axe",
        "scoreboard objectives add mtb_gold_axe used:golden_axe",
        f"function mtb:{VERSION}/run_command {{\"command\":\"scoreboard objectives add mtb_copper_axe used:copper_axe\"}}",
        "scoreboard objectives add mtb_iron_axe used:iron_axe",
        "scoreboard objectives add mtb_diamond_axe used:diamond_axe",
        "scoreboard objectives add mtb_netherite_axe used:netherite_axe",

        "scoreboard objectives add mtb_wood_shovel used:wooden_shovel",
        "scoreboard objectives add mtb_stone_shovel used:stone_shovel",
        "scoreboard objectives add mtb_gold_shovel used:golden_shovel",
        f"function mtb:{VERSION}/run_command {{\"command\":\"scoreboard objectives add mtb_copper_shovel used:copper_shovel\"}}",
        "scoreboard objectives add mtb_iron_shovel used:iron_shovel",
        "scoreboard objectives add mtb_diamond_shovel used:diamond_shovel",
        "scoreboard objectives add mtb_netherite_shovel used:netherite_shovel",

        "scoreboard objectives add mtb_wood_hoe used:wooden_hoe",
        "scoreboard objectives add mtb_stone_hoe used:stone_hoe",
        "scoreboard objectives add mtb_gold_hoe used:golden_hoe",
        f"function mtb:{VERSION}/run_command {{\"command\":\"scoreboard objectives add mtb_copper_hoe used:copper_hoe\"}}",
        "scoreboard objectives add mtb_iron_hoe used:iron_hoe",
        "scoreboard objectives add mtb_diamond_hoe used:diamond_hoe",
        "scoreboard objectives add mtb_netherite_hoe used:netherite_hoe",

        "scoreboard objectives add temp dummy",

        f"schedule function mtb:{VERSION}/slow_tick 1t replace"
    ])

    ctx.data.functions[f"mtb:{VERSION}/slow_tick"] = Function([
        "execute as @a at @s run function #mtb:update_multiblock",
        f"schedule function mtb:{VERSION}/slow_tick 10t replace",
        f"advancement revoke @s only mtb:{VERSION}/events/place_block"
    ])

    ctx.data.functions[f"mtb:{VERSION}/assign_id"] = Function([
        "scoreboard players operation @s mtb_id = .max mtb_id",
        "tag @s add has_mtb_id",

        "scoreboard players add .max mtb_id 1"  # Increment the max multiblock ID by one
    ])

    ctx.data.functions[f"mtb:{VERSION}/find_id"] = Function([
        "scoreboard players operation .this mtb_id = @s mtb_id" # Set .this to the current entity's ID
    ])

    ctx.data.functions[f"mtb:{VERSION}/tool_use/axe"] = Function([
        f"advancement revoke @s only mtb:{VERSION}/tool_use/axe",
        "scoreboard players set @s mtb_wood_axe 0",
        "scoreboard players set @s mtb_stone_axe 0",
        "scoreboard players set @s mtb_gold_axe 0",
        "scoreboard players set @s mtb_copper_axe 0",
        "scoreboard players set @s mtb_iron_axe 0",
        "scoreboard players set @s mtb_diamond_axe 0",
        "scoreboard players set @s mtb_netherite_axe 0",
        "execute at @s run function #mtb:update_multiblock"
    ])

    ctx.data.functions[f"mtb:{VERSION}/tool_use/hoe"] = Function([
        f"advancement revoke @s only mtb:{VERSION}/tool_use/hoe",
        "scoreboard players set @s mtb_wood_hoe 0",
        "scoreboard players set @s mtb_stone_hoe 0",
        "scoreboard players set @s mtb_gold_hoe 0",
        "scoreboard players set @s mtb_copper_hoe 0",
        "scoreboard players set @s mtb_iron_hoe 0",
        "scoreboard players set @s mtb_diamond_hoe 0",
        "scoreboard players set @s mtb_netherite_hoe 0",
        "execute at @s run function #mtb:update_multiblock"
    ])

    ctx.data.functions[f"mtb:{VERSION}/tool_use/pick"] = Function([
        f"advancement revoke @s only mtb:{VERSION}/tool_use/pick",
        "scoreboard players set @s mtb_wood_pick 0",
        "scoreboard players set @s mtb_stone_pick 0",
        "scoreboard players set @s mtb_gold_pick 0",
        "scoreboard players set @s mtb_copper_pick 0",
        "scoreboard players set @s mtb_iron_pick 0",
        "scoreboard players set @s mtb_diamond_pick 0",
        "scoreboard players set @s mtb_netherite_pick 0",
        "execute at @s run function #mtb:update_multiblock"
    ])

    ctx.data.functions[f"mtb:{VERSION}/tool_use/shovel"] = Function([
        f"advancement revoke @s only mtb:{VERSION}/tool_use/shovel",
        "scoreboard players set @s mtb_wood_shovel 0",
        "scoreboard players set @s mtb_stone_shovel 0",
        "scoreboard players set @s mtb_gold_shovel 0",
        "scoreboard players set @s mtb_copper_shovel 0",
        "scoreboard players set @s mtb_iron_shovel 0",
        "scoreboard players set @s mtb_diamond_shovel 0",
        "scoreboard players set @s mtb_netherite_shovel 0",
        "execute at @s run function #mtb:update_multiblock"
    ])

# -------------------------------
#  Gen multiblock specific files                            
# -------------------------------

def gen_multiblock_files(self: MultiblockCode, ctx: Context):
    common_funcpath = f"mtb-generated:{self.namespace}/{self.name}"

    # -------------------------------
    #  Function Tags                            
    # -------------------------------

    # Init blueprint ==> Spawn block display
    ctx.data.function_tags[f"{common_funcpath}/summon_instance"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/init_blueprint", "required": False}
        ]
    })

    # Remove the whole blueprint
    ctx.data.function_tags[f"{common_funcpath}/remove_instance"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/remove_all", "required": False}
        ]
    })

    # Build the whole blueprint
    ctx.data.function_tags[f"{common_funcpath}/build_structure"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/build_structure", "required": False}
        ]
    })

    # Clear the whole blueprint area
    ctx.data.function_tags[f"{common_funcpath}/clear_area"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/clear_area", "required": False}
        ]
    })

    # Spawn the outline
    ctx.data.function_tags[f"{common_funcpath}/outline/show"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/outline/show", "required": False}
        ]
    })

    # Remove the outline
    ctx.data.function_tags[f"{common_funcpath}/outline/hide"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/outline/remove_outline", "required": False}
        ]
    })

    # Modify the outline
    ctx.data.function_tags[f"{common_funcpath}/outline/modify"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/outline/modify", "required": False}
        ]
    })

    # Show the blueprint markers
    ctx.data.function_tags[f"{common_funcpath}/blueprint/show"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/place_blueprint/show_blueprint", "required": False}
        ]
    })

    # Hide the blueprint markers
    ctx.data.function_tags[f"{common_funcpath}/blueprint/hide"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/remove_blueprint", "required": False}
        ]
    })

    # Mirror the whole multiblock
    ctx.data.function_tags[f"{common_funcpath}/mirror"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/mirror", "required": False}
        ]
    })

    # Rotate clockwise tag
    ctx.data.function_tags[f"{common_funcpath}/rotate/clockwise"] = FunctionTag()

    if self.anchor_mode == "center":
        ctx.data.function_tags[f"{common_funcpath}/rotate/clockwise"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/center_rotate", "required": False}]}))
    else:
        ctx.data.function_tags[f"{common_funcpath}/rotate/clockwise"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/corner_rotate", "required": False}]}))

    # Rotate counter clockwise
    ctx.data.function_tags[f"{common_funcpath}/rotate/counter_clockwise"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/rotate_ccw", "required": False}
        ]
    })

    # Rotate counter clockwise
    ctx.data.function_tags[f"{common_funcpath}/rotate/set_rotation"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/rotate/set_rotation", "required": False}
        ]
    })

    # Set the rotation
    ctx.data.function_tags[f"{common_funcpath}/rotate/counter_clockwise"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/rotate_ccw", "required": False}
        ]
    })

    # Move function tags
    axis = ["x", "y", "z"]
    methods = ["incr","decr"]

    for curr_axis in axis:
        for curr_meth in methods:
            ctx.data.function_tags[f"{common_funcpath}/move/{curr_meth}_{curr_axis}"] = FunctionTag({
                "values": [
                    {"id": f"{common_funcpath}/{curr_meth}_{curr_axis}", "required": False}
                ]
            })

    ctx.data.function_tags[f"{common_funcpath}/move/set_pos"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/set_pos", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/get_rotation"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/get_rotation", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/is_mirrored"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/is_mirrored", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/get_progress"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/get_progress", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/get_total_block_count"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/get_total_block_count", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/check_conditions"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/check_conditions", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/outline/is_visible"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/outline/is_visible", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/blueprint/is_visible"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/blueprint/is_visible", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/get_block_count"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/get_block_count", "required": False}
        ]
    })

    ctx.data.function_tags[f"{common_funcpath}/get_remaining_block_count"] = FunctionTag({
        "values": [
            {"id": f"{common_funcpath}/get_remaining_block_count", "required": False}
        ]
    })

    # -------------------------------
    #  Remove / spawn functions                            
    # -------------------------------
    
    # spawn the root for this blueprint
    ctx.data.functions[f"{common_funcpath}/init_blueprint"] = Function([
        "data remove storage mtb:temp args",
        "$data modify storage mtb:temp args set value $(args)",

        f"execute align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/place_blueprint/aligned",
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Summoned new {self.name} instance","color":"white"}}]'
    ])

    # Remove everything from this multiblock
    ctx.data.functions[f"{common_funcpath}/remove_all"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",        
        "tag @s remove mtb.has_outline",
        "tag @s remove mtb.has_blueprint",
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else "",
        f'function mtb:{VERSION}/find_id',
        f'kill @e[predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}]',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Removed {self.name} instance","color":"white"}}]',

    ])

    # Place the whole multiblock structure
    ctx.data.functions[f"{common_funcpath}/build_structure"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'execute at @s positioned ^{-(self.center[0]-1) if self.center[0] != 0 else ''} ^{-(self.center[1]) if self.center[1] != 0 else ''} ^{-(self.center[2]-1) if self.center[2] != 0 else ''} run function {common_funcpath}/place_template',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: {self.name} instance built","color":"white"}}]',
        f'execute at @s run {self.callback.on_creative_place}' if self.callback.on_creative_place else ""
    ])

    ctx.data.functions[f"{common_funcpath}/place_template"] = Function([
        f"execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run place template {self.structure_path} ~{self.size[0]-1} ~ ~ none front_back",
        f"execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~{self.size[2]-0} clockwise_90 front_back", # yap blijf deze -0 af
        f"execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run place template {self.structure_path} ~{-self.size[0]+1} ~ ~ 180 front_back",
        f"execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~{-self.size[2]-0} counterclockwise_90 front_back",

        f"execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~ none",
        f"execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~ clockwise_90",
        f"execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~ 180",
        f"execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run place template {self.structure_path} ~ ~ ~ counterclockwise_90"
    ])

    # Verify if we currently are the correct root (or even a block display at all) for this multiblock
    ctx.data.functions[f"{common_funcpath}/verify_root"] = Function([
        f'execute if entity @s[type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()}] run return 1',
        f'execute unless entity @s[type=minecraft:block_display] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Error: failed to interact with multiblock. Please run the command as the multiblock root.","color":"red"}}',
        f'execute if entity @s[type=minecraft:block_display] unless entity @s[tag=mtb.{self.namespace}-{self.get_safe_name()}] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: Error: to interact with multiblock. Please run the correct function for this multiblock.","color":"red"}}',
        "return fail"
    ])

    ctx.data.functions[f"{common_funcpath}/clear_area"] = Function([
        "execute unless entity @s[tag=mtb.has_blueprint] run scoreboard players set #mtb_blueprint temp 1",
        f"execute if score #mtb_blueprint temp matches 1 run function {common_funcpath}/place_blueprint/show_blueprint",
        f"function mtb:{VERSION}/find_id",
        f"execute as @e[type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=mtb.blueprint] at @s run setblock ~ ~ ~ air",
        f"execute if score #mtb_blueprint temp matches 1 run function {common_funcpath}/remove_blueprint",
        "scoreboard players reset #mtb_blueprint temp",
        f"execute at @s run {self.callback.on_clear_area}" if self.callback.on_clear_area else "",
        "execute as @a at @s run function #mtb:update_multiblock"
    ])

    # -------------------------------
    #   Show / Hide mtb functions
    # -------------------------------

    # place_blueprint/aligned
    ctx.data.functions[f"{common_funcpath}/place_blueprint/aligned"] = Function([
        f"function {common_funcpath}/place_blueprint/handle_rotation",
        f"execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=INIT, tag=mtb.root, distance=..0.1] if data storage mtb:temp {{\"args\":{{\"mirrored\":true}}}} run tag @s add mtb.mirrored",
        f"execute as @e[type=minecraft:block_display, sort=nearest, limit=1, tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=INIT, tag=mtb.root, distance=..0.1] at @s rotated as @s run function {common_funcpath}/place_blueprint/init_root"
    ])

    # place_blueprint/handle_rotation
    ctx.data.functions[f"{common_funcpath}/place_blueprint/handle_rotation"] = Function([
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 180}}}} run return run summon minecraft:block_display ~ ~ ~ {{Rotation:[180f,0f], Tags:[mtb.{self.namespace}-{self.get_safe_name()},\"INIT\",mtb.rot_180,mtb.root]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 270}}}} run return run summon minecraft:block_display ~ ~ ~ {{Rotation:[270f,0f], Tags:[mtb.{self.namespace}-{self.get_safe_name()},\"INIT\",mtb.rot_270,mtb.root]}}",
        f"execute if data storage mtb:temp {{\"args\":{{\"rotation\": 90}}}} run return run summon minecraft:block_display ~ ~ ~ {{Rotation:[90f,0f], Tags:[mtb.{self.namespace}-{self.get_safe_name()},\"INIT\",mtb.rot_90,mtb.root]}}",
        f"summon minecraft:block_display ~ ~ ~ {{Rotation:[0f,0f], Tags:[mtb.{self.namespace}-{self.get_safe_name()},\"INIT\",mtb.rot_0,mtb.root]}}" # fallback
    ])

    # Handle the position of the blueprint placement
    if self.place_mode == "corner":
        ctx.data.functions[f"{common_funcpath}/place_blueprint/init_root"] = Function([
            f"tp @s ^{self.center[0]-1 if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2]-1 if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            f"execute unless entity @s[tag=has_mtb_id] run function mtb:{VERSION}/assign_id",

            "scoreboard players set @s mtb_complete 0",
            f"{self.callback.on_place}" if self.callback.on_place else "",
        ])
    elif self.place_mode == "facing":
        # Init function
        ctx.data.functions[f"{common_funcpath}/place_blueprint/init_root"] = Function([
            f"tp @s ^{self.center[0]-int(self.center[0]) if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2] if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            f"execute unless entity @s[tag=has_mtb_id] run function mtb:{VERSION}/assign_id",
            
            "scoreboard players set @s mtb_complete 0",
            f"{self.callback.on_place}" if self.callback.on_place else "",
        ])
    elif self.place_mode == "center": 
        # Init function
        ctx.data.functions[f"{common_funcpath}/place_blueprint/init_root"] = Function([
            f"tp @s ^{self.center[0]-int(self.center[0]) if self.center[0] != 0 else ''} ^{self.center[1] if self.center[1] != 0 else ''} ^{self.center[2]-int(self.center[2]) if self.center[2] != 0 else ''}",

            "tag @s remove INIT",
            f"execute unless entity @s[tag=has_mtb_id] run function mtb:{VERSION}/assign_id",
            
            "scoreboard players set @s mtb_complete 0",
            f"{self.callback.on_place}" if self.callback.on_place else "",
        ])
    
    ctx.data.functions[f"{common_funcpath}/place_blueprint/show_blueprint"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.has_blueprint] run return fail",
        f"function {common_funcpath}/place_blueprint/summon",
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
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
        "execute if entity @s[tag=!mtb.mirrored] run scoreboard players set #is_mirrored temp 0",
        "scoreboard players operation #root_id temp = @s mtb_id",
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Showing blueprint for {self.name} instance","color":"white"}}]', # also store the id :P
    ])

    lines = [] # generate lines for each block's summon

    for block in self.blocks:
        match block.block_id:
            # ======= Handle water item-display placement =======
            case "minecraft:water": # if water
                lines.append(f'execute if entity @s[tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, entity_type:"{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}", transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", data:{{}}}}')           
                lines.append(f'execute if entity @s[tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, entity_type:"{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}", transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", data:{{}}}}')

            # ======= Handle lava item-display placement =======
            case "minecraft:lava": # if lava
                lines.append(f'execute if entity @s[tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, entity_type:"{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}", transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", data:{{}}}}')
                lines.append(f'execute if entity @s[tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:item_display run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, entity_type:"{block.block_id.replace(":",".")}-{block.blockstates.get_safe_string(rotation=0, mirrored=False)}", transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", data:{{}}}}')

            case _: # Basically an else

                # Each blockdisplay has a tag that contains it's default non rotated / mirrored blockstates. During the check a corresponding function is called that handles the rotation for that specific blockstate
                lines.append(f'execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=0, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=90, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=180, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] at @s positioned ^{block.pos[0] if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=270, mirrored=False)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                
                lines.append(f'execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=0, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=90, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=180, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
                lines.append(f'execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] at @s positioned ^{(-block.pos[0]) if block.pos[0] != 0 else ""} ^{block.pos[1] if block.pos[1] != 0 else ""} ^{block.pos[2] if block.pos[2] != 0 else ""} summon minecraft:block_display run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{block.block_id}", Properties: {block.blockstates.get_dict_like_string(rotation=270, mirrored=True)} }}, block_id: "{block.block_id.replace(":",".")}", blockstates: "{block.blockstates.get_safe_string(rotation=0, mirrored=False)}"}}')
    
    
    # Process entities - same pattern as blocks (consistent ^x ^y ^z, no x/z swap)
    for entity in self.entities:
        if entity.item_id == "minecraft:air" or not entity.item_id:
            continue

        lines.append(
            f'execute if entity @s[tag=!mtb.mirrored] at @s positioned '
            f'^{entity.pos[0] if entity.pos[0] != 0 else ""} '
            f'^{entity.pos[1] if entity.pos[1] != 0 else ""} '
            f'^{entity.pos[2] if entity.pos[2] != 0 else ""} '
            f'summon minecraft:item_display run function '
            f'{common_funcpath}/place_blueprint/summon/modify_item_display '
            f'{{display_data:{entity.item_snbt}, entity_type:"{entity.custom_tag}", '
            f'transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", '
            f'data:{{}}}}'
        )
        lines.append(
            f'execute if entity @s[tag=mtb.mirrored] at @s positioned '
            f'^{-entity.pos[0] if entity.pos[0] != 0 else ""} '
            f'^{entity.pos[1] if entity.pos[1] != 0 else ""} '
            f'^{entity.pos[2] if entity.pos[2] != 0 else ""} '
            f'summon minecraft:item_display run function '
            f'{common_funcpath}/place_blueprint/summon/modify_item_display '
            f'{{display_data:{entity.item_snbt}, entity_type:"{entity.custom_tag}", '
            f'transformation:"{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}", '
            f'data:{{}}}}'
        )
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon"].append(lines)
                

    # Modify the block display on summon
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon/modify_block_display"] = Function([
        f"$data merge entity @s {{view_range:0.12f,transformation:{{left_rotation:[0f,0f,0f,1f], right_rotation:[0f,0f,0f,1f],translation:[-0.3f,-0.3f,-0.3f],scale:[0.6f,0.6f,0.6f]}},block_state:$(display_data),Tags:[\"mtb.{self.namespace}-{self.get_safe_name()}\", \"$(block_id)-$(blockstates)\"]}}",
        "scoreboard players operation @s mtb_id = #root_id temp",
        "scoreboard players set @s mtb_prev_state 0",
        "tag @s add mtb.blueprint",

        # Modify the rotation according to the rotation tag of the block_display
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 0 run tag @s add mtb.rot_0",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 90 run tag @s add mtb.rot_90",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 180 run tag @s add mtb.rot_180",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 270 run tag @s add mtb.rot_270",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #is_mirrored temp matches 1 run tag @s add mtb.mirrored",
        "tag @s add mtb.has_rot_tag" # Make sure to only set the rotation from the beginning
    ])
    
    # Modify the item display on summon (analogous to modify_block_display)
    ctx.data.functions[f"{common_funcpath}/place_blueprint/summon/modify_item_display"] = Function([
        f"$data merge entity @s {{view_range:0.12f,transformation:$(transformation),item:$(display_data),data:$(data),Tags:[\"mtb.{self.namespace}-{self.get_safe_name()}\", \"$(entity_type)\"]}}",
        "scoreboard players operation @s mtb_id = #root_id temp",
        "scoreboard players set @s mtb_prev_state 0",
        "tag @s add mtb.blueprint",
        # Modify the rotation according to the rotation tag of the block_display
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 0 run tag @s add mtb.rot_0",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 90 run tag @s add mtb.rot_90",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 180 run tag @s add mtb.rot_180",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #rotation temp matches 270 run tag @s add mtb.rot_270",
        "execute unless entity @s[tag=mtb.has_rot_tag] if score #is_mirrored temp matches 1 run tag @s add mtb.mirrored",
        "tag @s add mtb.has_rot_tag"
    ])

    # Remove the bluprint
    ctx.data.functions[f"{common_funcpath}/remove_blueprint"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        'tag @s remove mtb.has_blueprint',
        f'kill @e[type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=mtb.blueprint, tag=!mtb.root]',
        'scoreboard players set @s mtb_complete 0',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Hiding blueprint for {self.name} instance","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
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
            f'function mtb:{VERSION}/find_id',
            f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players remove @s mtb_complete 1',
            'scoreboard players set @s mtb_prev_state 0',
            'data remove entity @s brightness'
        ])

        # modify the display back to it's original state
        if unique_block["block_id"] == "minecraft:water":
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([f'execute if entity @s[type=minecraft:item_display] run return run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:water_bucket"}}, entity_type:"{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'])
        elif unique_block["block_id"] == "minecraft:lava":
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([f'execute if entity @s[type=minecraft:item_display] run return run function {common_funcpath}/place_blueprint/summon/modify_item_display {{display_data:{{id:"minecraft:lava_bucket"}}, entity_type:"{unique_block["block_id"].replace(":",".")}-{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'])
        else:
            ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_none"].append([
                f'execute if entity @s[tag=mtb.rot_0,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=0, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_90,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=90, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_180,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=180, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_270,tag=!mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=270, mirrored=False)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                
                f'execute if entity @s[tag=mtb.rot_0,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=0, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_90,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=90, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_180,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=180, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}',
                f'execute if entity @s[tag=mtb.rot_270,tag=mtb.mirrored] run return run function {common_funcpath}/place_blueprint/summon/modify_block_display {{display_data:{{ Name: "{unique_block["block_id"]}", Properties: {unique_block["blockstates"].get_dict_like_string(rotation=270, mirrored=True)} }}, block_id: "{unique_block["block_id"].replace(":",".")}",blockstates:"{unique_block["blockstates"].get_safe_string(rotation=0, mirrored=False)}"}}'
            ])
        
        ctx.data.functions[f"{common_funcpath}/{specific_funcpath}/set_wrong"] = Function([
            'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Wrong block placed","color":"red"}]',
            f'function mtb:{VERSION}/find_id',
            f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players remove @s mtb_complete 1',
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
            
            f'function mtb:{VERSION}/find_id',
            f'execute as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players add @s mtb_complete 1'
        ])


        ctx.data.functions[f'{common_funcpath}/checking/main'].append(f'execute if entity @s[tag={unique_block["block_id"].replace(":",".")}-{state}] run function {common_funcpath}/{specific_funcpath}/check')

    # Add entity checking functions using entity palette (like block palette)
    entity_count = len(self.entities)
    entity_palette_used = len(self.entity_palette) > 0
    if entity_palette_used:
        for entity_entry in self.entity_palette:
            safe_type = entity_entry.custom_tag
            entity_palette_path = f'checking/entity/{safe_type}'

            # Check function - tag comparison on the entity
            ctx.data.functions[f"{common_funcpath}/{entity_palette_path}/check"] = Function([
                f'scoreboard players set #success temp 0',

                # success=2: item_display with matching tag + mtb_type found (excluding this ghost)
                f'execute if entity @e[type=minecraft:item_display,distance=..0.01,tag=!mtb.blueprint,nbt={{data:{{mtb_type:"{entity_entry.mtb_type_raw}"}}}}] run scoreboard players set #success temp 2',
                # success=1: some item_display nearby (excluding this ghost) — guarded so it doesn't overwrite success=2
                f'execute if score #success temp matches 0 if entity @e[type=minecraft:item_display,distance=..0.5,tag=!mtb.blueprint] run scoreboard players set #success temp 1',

                # Dispatch
                f'execute if score #success temp matches 0 if block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 0 run function {common_funcpath}/{entity_palette_path}/set_none',
                f'execute if score #success temp matches 0 unless block ~ ~ ~ minecraft:air run return run execute unless score @s mtb_prev_state matches 1 run function {common_funcpath}/{entity_palette_path}/set_wrong_block',
                f'execute if score #success temp matches 1 run return run execute unless score @s mtb_prev_state matches 1 run function {common_funcpath}/{entity_palette_path}/set_wrong',
                f'execute unless score @s mtb_prev_state matches 2 run function {common_funcpath}/{entity_palette_path}/set_correct'
            ])

            # Set none
            ctx.data.functions[f"{common_funcpath}/{entity_palette_path}/set_none"] = Function([
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"Entity preview restored","color":"gold"}]',
                f'function mtb:{VERSION}/find_id',
                f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players remove @s mtb_complete 1',
                'scoreboard players set @s mtb_prev_state 0',
                'data modify entity @s transformation.scale set value [0.6f,0.6f,0.6f]',
                f'execute as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,distance=..0.5,limit=1] run data merge entity @s {{block_state:{{Name:"minecraft:air"}},transformation:{{scale:[0f,0f,0f]}}}}'
            ])

            # Set wrong (entity exists but has wrong type)
            ctx.data.functions[f"{common_funcpath}/{entity_palette_path}/set_wrong"] = Function([
                f'data merge entity @e[type=minecraft:item_display,distance=..0.5,limit=1,tag=!mtb.blueprint] {{item:{{id:"minecraft:orange_stained_glass"}}, brightness:{{sky:15,block:15}}, transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1.01f,1.01f,1.01f]}}}}'
            ])

            # Set wrong block (solid block placed but entity missing)
            ctx.data.functions[f"{common_funcpath}/{entity_palette_path}/set_wrong_block"] = Function([
                'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{"text":"[Debug]: Block placed but entity missing","color":"red"}]',
                f'function mtb:{VERSION}/find_id',
                f'execute if score @s mtb_prev_state matches 2 as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players remove @s mtb_complete 1',
                'scoreboard players set @s mtb_prev_state 1',
                'data modify entity @s transformation.scale set value [0f,0f,0f]',
                f'execute as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,distance=..0.5,limit=1] run data merge entity @s {{brightness:{{sky:15,block:15}},block_state:{{Name:"minecraft:red_stained_glass"}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.501f,-0.501f,-0.501f],scale:[1.01f,1.01f,1.01f]}}}}'
            ])

            # Set correct
            ctx.data.functions[f"{common_funcpath}/{entity_palette_path}/set_correct"] = Function([
                'scoreboard players set @s mtb_prev_state 2',
                'data modify entity @s transformation.scale set value [0f,0f,0f]',
                f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Correct entity placed","color":"green"}}]',
                f'function mtb:{VERSION}/find_id',
                f'execute as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] run scoreboard players add @s mtb_complete 1',
                f'execute as @e[predicate=mtb:{VERSION}/match_id,type=minecraft:block_display,distance=..0.5,limit=1] run data modify entity @s transformation.scale set value [0f,0f,0f]'
            ])

            # Dispatch via tag (like blocks)
            ctx.data.functions[f'{common_funcpath}/checking/main'].append(f'execute if entity @s[tag={safe_type}] run function {common_funcpath}/{entity_palette_path}/check')



    # Update the completion check to include entities
    total_items = len(self.blocks) + len(self.entities)

    # Check if the full multiblock is complete
    ctx.data.functions[f"{common_funcpath}/checking/full_multiblock"] = Function([
        f'execute store success score #cond_met temp run function {common_funcpath}/checking/conditions',
        f'execute if score @s mtb_complete matches {total_items} unless score #cond_met temp matches 1 unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] {{"text":"[Debug]: {self.name} almost completed: mtb built but conditions are not met","color":"gold"}}',
        f'execute if score #cond_met temp matches 1 if score @s mtb_complete matches {total_items} unless entity @s[tag=mtb.completed] if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: {self.name} was completed!","color":"green"}}]',
        f'execute if score #cond_met temp matches 1 if score @s mtb_complete matches {total_items} unless entity @s[tag=mtb.completed] at @s rotated as @s run {self.callback.on_complete}' if self.callback.on_complete else "",
        f'execute unless score #cond_met temp matches 1 if score @s mtb_complete matches {total_items} if entity @s[tag=mtb.completed] at @s rotated as @s run {self.callback.on_uncomplete}' if self.callback.on_uncomplete else "",

        f'execute if score @s mtb_complete matches {total_items} if score #cond_met temp matches 1 run tag @s add mtb.completed',
        f'execute unless score @s mtb_complete matches {total_items} run tag @s remove mtb.completed',
        f'execute unless score #cond_met temp matches 1 run tag @s remove mtb.completed'
    ])

    # Check the additional conditions
    ctx.data.functions[f"{common_funcpath}/checking/conditions"] = Function()

    for cond in self.conditions:
        ctx.data.functions[f"{common_funcpath}/checking/conditions"].append([
            f'execute store success score #success temp run {cond}',
            f'execute if score #success temp matches 0 run return fail' # Fail this function when the conditions don't match
        ])

    ctx.data.functions[f"{common_funcpath}/checking/conditions"].append('return 1') # Else, succeed

    # ----------------------------------
    #  Mirroring functions                  
    # ----------------------------------

    ctx.data.functions[f"{common_funcpath}/mirror_nested"] = Function([
        'execute if entity @s[tag=mtb.mirrored] run tag @s add mtb.was_mirrored',
        'execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.mirrored',
        'execute unless entity @s[tag=mtb.was_mirrored] run tag @s add mtb.mirrored',
        'execute if entity @s[tag=mtb.was_mirrored] run tag @s remove mtb.was_mirrored',
        f'execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function {common_funcpath}/outline/spawn_correct_outline'
    ])

    ctx.data.functions[f"{common_funcpath}/mirror"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'scoreboard players set @s mtb_complete 0',
        f'kill @e[type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id, tag=!mtb.root]',
        f'execute as @s at @s rotated as @s run function {common_funcpath}/mirror_nested',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Mirrored {self.name} instance","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else "",
    ])

    # -------------------------------
    #  Rotate functions                            
    # -------------------------------

    ctx.data.functions[f"{common_funcpath}/rotate/set_rotation"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "$scoreboard players set #rot.target temp $(rotation)",
        f'execute unless score #rot.target temp matches 0 unless score #rot.target temp matches 90 unless score #rot.target temp matches 180 unless score #rot.target temp matches 270 run return run execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Failed to set {self.name} rotation. Rotation must be one of 0, 90, 180 or 270","color":"red"}}]',

        "$execute if entity @s[tag=mtb.rot_$(rotation)] run return fail",

        "tag @s remove mtb.rot_0",
        "tag @s remove mtb.rot_90",
        "tag @s remove mtb.rot_180",
        "tag @s remove mtb.rot_270",

        "$tag @s add mtb.rot_$(rotation)",

        "$rotate @s $(rotation) 0",
        f'function mtb:{VERSION}/find_id',
        f'scoreboard players set @s mtb_complete 0',
        f'kill @e[type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id, tag=!mtb.root]',

        f'execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] rotated as @s run function {common_funcpath}/outline/spawn_correct_outline',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Modified rotation of {self.name} instance","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f"{common_funcpath}/rotate_ccw"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f"function #{common_funcpath}/rotate/clockwise",
        f"function #{common_funcpath}/rotate/clockwise",
        f"function #{common_funcpath}/rotate/clockwise",
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Rotating {self.name} instance clockwise","color":"white"}}]'
    ])

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

    # ======= Center Rotation =======
    ctx.data.functions[f"{common_funcpath}/center_rotate_nested"] = Function([
        'rotate @s ~90 ~',
        f'execute if entity @s[tag=mtb.has_blueprint] rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] rotated as @s run function {common_funcpath}/outline/spawn_correct_outline'
    ])
    
    # Laat dit ook werken voor even op oneven multiblocks
    if self.size[0] % 2 == self.size[2] % 2:
        ctx.data.functions[f"{common_funcpath}/center_rotate"] = Function([
            f"execute unless function {common_funcpath}/verify_root run return fail",
            f"function {common_funcpath}/rot/find_rot",
            f'function mtb:{VERSION}/find_id',
            f'scoreboard players set @s mtb_complete 0',
            f'kill @e[type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id, tag=!mtb.root]',
            f'execute at @s rotated as @s run function {common_funcpath}/center_rotate_nested',
            f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else "",
        ])
    else:
        ctx.data.functions[f"{common_funcpath}/center_rotate"] = Function([
            f"execute unless function {common_funcpath}/verify_root run return fail",
            f"function {common_funcpath}/rot/find_rot",
            f'function mtb:{VERSION}/find_id',
            f'scoreboard players set @s mtb_complete 0',
            # fix een tp shit (yay een willekeurige offset)
            'execute at @s run tp @s ^0.5 ^ ^0.5',
            f'kill @e[sort=nearest, type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id, tag=!mtb.root]',
            f'execute as @s at @s rotated as @s run function {common_funcpath}/center_rotate_nested',
            f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else "",
        ])

    # ======= Corner Rotation =======
    ctx.data.functions[f"{common_funcpath}/corner_rotate"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f"function {common_funcpath}/rot/find_rot",
        f'function mtb:{VERSION}/find_id',
        f'scoreboard players set @s mtb_complete 0',
        f'kill @e[sort=nearest, type=#mtb:{VERSION}/display, predicate=mtb:{VERSION}/match_id, tag=!mtb.root]',
        f"execute at @s run tp @s ^{-(self.center[0]-1) if self.center[0] != 0 else ''} ^ ^{-(self.center[2]-1) if self.center[2] != 0 else ''}",
        'execute rotated as @s run rotate @s ~90 ~',
        f"execute at @s rotated as @s run tp @s ^{self.center[0]-1 if self.center[0] != 0 else ''} ^ ^{self.center[2]-1 if self.center[2] != 0 else ''}",
        f'execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function {common_funcpath}/outline/spawn_correct_outline',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""

    ])

    # -------------------------------
    #  Move Functions                            
    # -------------------------------
    ctx.data.functions[f'{common_funcpath}/incr_x'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~1 ~ ~',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance +X","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/decr_x'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~-1 ~ ~',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance -X","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/incr_y'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~ ~1 ~',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance +Y","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/decr_y'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~ ~-1 ~',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance -Y","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/incr_z'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~ ~ ~1',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance +Z","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/decr_z'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'execute as @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id] at @s run tp @s ~ ~ ~-1',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Moving {self.name} instance -Z","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    ctx.data.functions[f'{common_funcpath}/set_pos'] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'execute align xyz run tp @s ~0.5 ~0.5 ~0.5',
        f'execute at @s run function {common_funcpath}/place_blueprint/init_root',

        # Don't move when no change in position is made (optimize + prevent flickering)
        "execute store result score #pos_x temp run data get entity @s Pos[0]",
        "execute store result score #pos_y temp run data get entity @s Pos[1]",
        "execute store result score #pos_z temp run data get entity @s Pos[2]",
        "execute if score #pos_x temp = @s mtb_prev_x if score #pos_y temp = @s mtb_prev_y if score #pos_z temp = @s mtb_prev_z run return fail",
        "scoreboard players operation @s mtb_prev_x = #pos_x temp",
        "scoreboard players operation @s mtb_prev_y = #pos_y temp",
        "scoreboard players operation @s mtb_prev_z = #pos_z temp",

        f'function mtb:{VERSION}/find_id',
        f'kill @e[tag=mtb.{self.namespace}-{self.get_safe_name()}, predicate=mtb:{VERSION}/match_id, tag=!mtb.root,type=#mtb:{VERSION}/display]',
        f'execute if entity @s[tag=mtb.has_blueprint] at @s rotated as @s run function {common_funcpath}/place_blueprint/summon',
        f'execute if entity @s[tag=mtb.has_outline] at @s rotated as @s run function {common_funcpath}/outline/spawn_correct_outline',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Repositioning {self.name} instance","color":"white"}}]',
        f'execute at @s run {self.callback.on_edit}' if self.callback.on_edit else ""
    ])

    # -------------------------------
    #  Updating functions                            
    # -------------------------------

    ctx.data.functions[f"{common_funcpath}/update"] = Function([
        f'execute as @e[distance=..10,type=#mtb:{VERSION}/display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=!mtb.root] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/checking/main',
        f'execute as @e[distance=..10,type=minecraft:block_display,tag=mtb.{self.namespace}-{self.get_safe_name()},tag=mtb.root] at @s align xyz positioned ~0.50 ~0.50 ~0.50 run function {common_funcpath}/checking/full_multiblock'
    ])

    # Hook this multiblock into the update event (per player)
    ctx.data.function_tags[f"mtb:update_multiblock"].append(FunctionTag({"values": [{"id": f"{common_funcpath}/update", "required": False}]}))

    # -------------------------------
    #  Getter functions                            
    # -------------------------------

    ctx.data.functions[f"{common_funcpath}/get_rotation"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.rot_0] run return 0",
        "execute if entity @s[tag=mtb.rot_90] run return 90",
        "execute if entity @s[tag=mtb.rot_180] run return 180",
        "execute if entity @s[tag=mtb.rot_270] run return 270"
    ])

    ctx.data.functions[f"{common_funcpath}/is_mirrored"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.mirrored] run return 1",
        "return 0"
    ])

    ctx.data.functions[f"{common_funcpath}/get_progress"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f"return run scoreboard players get @s mtb_complete"
    ])

    ctx.data.functions[f"{common_funcpath}/get_total_block_count"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f"return {total_items}"
    ])

    ctx.data.functions[f"{common_funcpath}/check_conditions"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f"return run function {common_funcpath}/checking/conditions"
    ])

    ctx.data.functions[f"{common_funcpath}/outline/is_visible"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.has_outline] run return 1",
        "return 0"
    ])

    ctx.data.functions[f"{common_funcpath}/blueprint/is_visible"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.has_blueprint] run return 1",
        "return 0"
    ])

    ctx.data.functions[f"{common_funcpath}/get_block_count"] = Function([
        f"function mtb/{VERSION}/find_id",
        f"$execute store result score #entity_count temp if entity @e[type=#mtb:{VERSION}/display,scores=!{{mtb_prev_state=0}},nbt={{block_state:{{ Name:'$(block)'}} }},predicate=mtb:{VERSION}/match_id, tag=mtb.{self.namespace}-{self.get_safe_name()}]",
        "execute run return run scoreboard players get #entity_count temp"
    ])

    ctx.data.functions[f"{common_funcpath}/get_remaining_block_count"] = Function([
        f"function mtb/{VERSION}/find_id",
        f"$execute store result score #entity_count temp if entity @e[type=#mtb:{VERSION}/display,scores={{mtb_prev_state=0}},nbt={{block_state:{{ Name:'$(block)'}} }},predicate=mtb:{VERSION}/match_id, tag=mtb.{self.namespace}-{self.get_safe_name()}]",
        "execute run return run scoreboard players get #entity_count temp"
    ])

    # -------------------------------
    #  Outline Functions                            
    # -------------------------------
    ctx.data.functions[f"{common_funcpath}/outline/show"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute if entity @s[tag=mtb.has_outline] run return fail",
        "data remove storage mtb:temp args",
        "$data modify storage mtb:temp args set value $(args)",

        f"function {common_funcpath}/outline/spawn_correct_outline"
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_correct_outline"] = Function([
        "scoreboard players operation #root_id mtb_id = @s mtb_id",
        "tag @s add mtb.has_outline",
        f"execute if entity @s[tag=mtb.rot_0] at @s run return run function {common_funcpath}/outline/spawn_outline_0",
        f"execute if entity @s[tag=mtb.rot_90] at @s run return run function {common_funcpath}/outline/spawn_outline_90",
        f"execute if entity @s[tag=mtb.rot_180] at @s run return run function {common_funcpath}/outline/spawn_outline_180",
        f"execute if entity @s[tag=mtb.rot_270] at @s run return run function {common_funcpath}/outline/spawn_outline_270",
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Showing outline for {self.name} instance","color":"white"}}]'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/modify_display"] = Function([


        f'$data merge entity @s {{Tags:[mtb.outline, mtb.{self.namespace}-{self.get_safe_name()}],view_range:0.15f, Rotation:$(Rotation), transformation:$(transformation), brightness:{{block:15,sky:15}}}}',
        
        f"function {common_funcpath}/outline/modify_display/set_glowing",
        f"function {common_funcpath}/outline/modify_display/set_color",
        f"function {common_funcpath}/outline/modify_display/set_glow_color",

        'scoreboard players operation @s mtb_id = #root_id mtb_id'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/modify_display/set_glowing"] = Function([
        "execute if data storage mtb:temp {args:{glowing:false}} run return run data merge entity @s {Glowing:0b}",
        "data merge entity @s {Glowing:1b}"
    ])

    ctx.data.functions[f"{common_funcpath}/outline/modify_display/set_color"] = Function([
        'execute if data storage mtb:temp {args:{color:"white"}} run return run data merge entity @s {block_state:{Name:"white_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"light_gray"}} run return run data merge entity @s {block_state:{Name:"light_gray_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"gray"}} run return run data merge entity @s {block_state:{Name:"gray_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"black"}} run return run data merge entity @s {block_state:{Name:"black_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"brown"}} run return run data merge entity @s {block_state:{Name:"brown_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"red"}} run return run data merge entity @s {block_state:{Name:"red_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"orange"}} run return run data merge entity @s {block_state:{Name:"orange_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"yellow"}} run return run data merge entity @s {block_state:{Name:"yellow_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"lime"}} run return run data merge entity @s {block_state:{Name:"lime_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"green"}} run return run data merge entity @s {block_state:{Name:"green_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"cyan"}} run return run data merge entity @s {block_state:{Name:"cyan_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"blue"}} run return run data merge entity @s {block_state:{Name:"blue_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"purple"}} run return run data merge entity @s {block_state:{Name:"purple_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"magenta"}} run return run data merge entity @s {block_state:{Name:"magenta_stained_glass_pane"}}',
        'execute if data storage mtb:temp {args:{color:"pink"}} run return run data merge entity @s {block_state:{Name:"pink_stained_glass_pane"}}',
        'data merge entity @s {block_state:{Name:"light_blue_stained_glass_pane"}}'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/modify_display/set_glow_color"] = Function([
        'execute if data storage mtb:temp args.glow_color run return run data modify entity @s glow_color_override set from storage mtb:temp args.glow_color',
        'data merge entity @s {glow_color_override:3847130}' 
    ])

    ctx.data.functions[f"{common_funcpath}/outline/modify"] = Function ([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        "execute unless entity @s[tag=mtb.has_outline] run return fail",
        "data remove storage mtb:temp args",
        "$data modify storage mtb:temp args set value $(args)",


        f"function mtb:{VERSION}/find_id",
        f"execute as @e[type=block_display,tag=mtb.outline,predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=!mtb.root] run function {common_funcpath}/outline/modify_display/set_glowing",
        f"execute as @e[type=block_display,tag=mtb.outline,predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=!mtb.root] run function {common_funcpath}/outline/modify_display/set_color",
        f"execute as @e[type=block_display,tag=mtb.outline,predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=!mtb.root] run function {common_funcpath}/outline/modify_display/set_glow_color",
    ])



    ctx.data.functions[f"{common_funcpath}/outline/remove_outline"] = Function([
        f"execute unless function {common_funcpath}/verify_root run return fail",
        f'function mtb:{VERSION}/find_id',
        f'kill @e[type=block_display,tag=mtb.outline,predicate=mtb:{VERSION}/match_id,tag=mtb.{self.namespace}-{self.get_safe_name()}, tag=!mtb.root]',
        'tag @s remove mtb.has_outline',
        f'execute if score #mtb.debug_enabled temp matches 1 run tellraw @a[tag=mtb.debug] [{{"text":"[Debug]: Hiding outline for {self.name} instance","color":"white"}}]'
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_0"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_90"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_180"] = Function([
    ])

    ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_270"] = Function([
    ])

    # Die ene funcking gignatische block code die de outline summont, maar dan compacted door AI (yay)
    outline_size = 0.2 # dikte van uw glass shit
    suffixes = ['0', '90', '180', '270']

    for i in range(4):
        for j, suffix in enumerate(suffixes):
            is_even = (i + j) % 2 == 0
            px, pz = (-self.center[0]+0.5, -self.center[2]+0.5) if is_even else (-self.center[2]+0.5, -self.center[0]+0.5)
            edge_len = float(self.size[0] if is_even else self.size[2])
            rot = 90 * i - 90 * j

            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{-self.center[1]-0.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[{90*i}F,0F], transformation:{{left_rotation:[0f,0f,-0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,{outline_size/2}f,-{outline_size/2}f],scale:[{outline_size}f,{edge_len}f,{outline_size}f]}}}}')
            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{self.center[1]+0.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[{90*i}F,0F], transformation:{{left_rotation:[0f,0f,-0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,{outline_size/2}f,-{outline_size/2}f],scale:[{outline_size}f,{edge_len}f,{outline_size}f]}}}}')
            ctx.data.functions[f"{common_funcpath}/outline/spawn_outline_{suffix}"].append(f'execute rotated ~{rot} 0 positioned ^{px} ^{-self.center[1]-0.5} ^{pz} summon block_display run function {common_funcpath}/outline/modify_display {{Rotation:[0F,0F], transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-{outline_size/2}f,0f,-{outline_size/2}f],scale:[{outline_size}f,{float(self.size[1])}f,{outline_size}f]}}}}')
