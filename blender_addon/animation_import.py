bl_info = {
    "name": "Minecraft Animations",
    "author": "goatee",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "location": "View3D > Tools",
    "description": "An example addon with multiple modules",
}

import bpy, json, math
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator, Action, Keyframe
from bpy.props import StringProperty


main_file_dict = {}


class ImportAnimationOp(Operator, ImportHelper):
    bl_idname = "minecraft.import_animation"
    bl_label = "Import animation"
    bl_description = "Import animation JSON"

    filter_glob = StringProperty(default="*.json", options={"HIDDEN"})

    def execute(self, context):
        with open(self.filepath, "r") as f:
            readAnimation(json.load(f))
        try:
            print()
        except Exception as e:
            RED = "\033[91m"
            print(f"{RED}Error loading file {self.filepath}: {e}")

        return {"FINISHED"}


action = None
moves = {}
animation_name = ""
isDegrees = None

body_parts = ["head", "torso", "rightArm", "leftArm", "rightLeg", "leftLeg"]


def readAnimation(main_file_dict):
    global moves, animation_name, isDegrees
    animation_name = main_file_dict["name"]
    isDegrees = main_file_dict["emote"]["degrees"]

    moves = {
        index: value for index, value in enumerate(main_file_dict["emote"]["moves"])
    }

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = main_file_dict["emote"]["stopTick"] - 1
    bpy.ops.minecraft.close_animation()

    for key, frameData in dict(moves).items():
        # if name in frameData:
        frame = frameData["tick"]
        easing = frameData["easing"]
        for name, data in frameData.items():
            if name in body_parts:
                readPart(name, data, frame, easing)

    from .constants import setImportName

    setImportName(animation_name)


def readPart(name, data: dict, frame, easing):
    if name not in bpy.data.objects:
        return

    bone = bpy.data.objects[name]
    if bone.animation_data is None:
        bone.animation_data_create()

    action = createAction(f"{animation_name}.{name}")
    bone.animation_data.action = action
    initPart(bone, name, action)

    for type, value in data.items():
        if type == "bend" or type == "axis":
            readBendableType(name, type, frame, value, easing)
        else:
            readType(action, name, type, frame, value, easing)


init_complete = []


def initPart(bone, name: str, action: Action):
    if name not in init_complete:
        for i in range(3):
            fcurve = action.fcurves.find("location", index=i)
            if fcurve is None:
                fcurve = action.fcurves.new("location", index=i)
            fcurve.keyframe_points.insert(0, bone.location[i])

            fcurve = action.fcurves.find("rotation_euler", index=i)
            if fcurve is None:
                fcurve = action.fcurves.new("rotation_euler", index=i)
            fcurve.keyframe_points.insert(0, bone.rotation_euler[i])

        init_complete.append(name)


def readType(action: Action, name, type, frame, value, easing):
    data_path = ""
    if type == "x":
        data_path = "location"
        index = 0
    elif type == "z":
        data_path = "location"
        index = 1
    elif type == "y":
        data_path = "location"
        index = 2
    elif type == "pitch":
        data_path = "rotation_euler"
        index = 0
    elif type == "roll":
        data_path = "rotation_euler"
        index = 1
    elif type == "yaw":
        data_path = "rotation_euler"
        index = 2
    elif type == "bend":
        data_path = "rotation_euler"
        index = 0
    elif type == "axis":
        data_path = "rotation_euler"
        index = 1

    if len(data_path) > 0:
        fcurve = action.fcurves.find(data_path, index=index)
        if fcurve is None:
            fcurve = action.fcurves.new(data_path, index=index)

        keyframe = fcurve.keyframe_points.insert(
            frame, value=correctValue(name, data_path, type, value), options={"FAST"}
        )
        readInterpolation(keyframe, easing)


def readBendableType(name, type, frame, value, easing):
    bendName = f"{name}_bend"
    if bendName not in bpy.data.objects:
        return

    bone = bpy.data.objects[bendName]
    if bone.animation_data is None:
        bone.animation_data_create()

    actionName = f"{animation_name}.{bendName}"
    if actionName in bpy.data.actions:
        bendAction = bpy.data.actions[actionName]
    else:
        bendAction = createAction(actionName)

    bone.animation_data.action = bendAction
    initPart(bone, bendName, bendAction)

    readType(bendAction, name, type, frame, value, easing)


def createAction(animationName) -> Action:
    if animationName in bpy.data.actions:
        return bpy.data.actions[animationName]
        # while animationName in bpy.data.actions:
        #     animationName += "_"

    return bpy.data.actions.new(animationName)


def readInterpolation(keyframe: Keyframe, interpolation: str):
    ease = ""
    print(interpolation[:2])
    if "INOUT" in interpolation:
        ease = "EASE_IN_OUT"
        if "EASEINOUT" in interpolation:
            interpolation = interpolation.replace("EASEINOUT", "")
        else:
            interpolation = interpolation.replace("INOUT", "")
    elif "EASEIN" in interpolation or interpolation[:2] == "IN":
        ease = "EASE_IN"
        if "EASEIN" in interpolation:
            interpolation = interpolation.replace("EASEIN", "")
        else:
            interpolation = interpolation.replace("IN", "")
    elif "EASEOUT" in interpolation or interpolation[:3] == "OUT":
        ease = "EASE_OUT"
        if "EASEOUT" in interpolation:
            interpolation = interpolation.replace("EASEOUT", "")
        else:
            interpolation = interpolation.replace("OUT", "")

    if len(ease) > 0:
        keyframe.easing = ease
    keyframe.interpolation = interpolation


def correctValue(name, data_path, type, value):
    global isDegrees

    if isDegrees and data_path == "rotation_euler":
        value = math.radians(value)

    if name == "rightArm" or name == "leftArm":
        if type == "y":
            value -= 12

    if type == "z" or type == "x":
        if name == "rightLeg":
            value -= 0.1
        elif name == "leftLeg":
            value += 0.1

    if type == "y":
        if name == "rightLeg" or name == "leftLeg":
            value -= 12

    if data_path == "location":
        if not name == "torso":
            value = value * -0.25
        else:
            value = value * 4
            if type == "z":
                value = value * -1
    elif not (name == "torso" and not (type == "roll" or type == "bend")) and not (
        type == "axis"
    ):  # rotation correction (*-1) except for torzo roll/bend
        value = value * -1

    if (name == "head" or name == "rightLeg" or name == "leftLeg") and type == "y":
        value += 3

    return value


# bpy.utils.register_class(ImportAnimationOp)
# bpy.ops.minecraft.import_animation("INVOKE_DEFAULT")
