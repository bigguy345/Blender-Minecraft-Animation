import bpy, json, os
from blender_addon.constants import getImportName

HOLD_ON_LAST_FRAME = True

animation_name = "test_format_temp"
animation_name = getImportName(animation_name)

# Export path here i.e C:\Users\user\Desktop
# Exports to model's directory if path is empty or invalid
EXPORT_PATH = r"Z:\old desktop\projects\jjk-addon\src\main\resources\assets\jujutsucraftaddon\player_animation"

# Add "version", "_comments", "uuid" metadatas to this dictionary
main_file_dict = {
    "name": animation_name,
    "author": "goatee",
    "description": "description",
    "emote": {
        "beginTick": bpy.context.scene.frame_start,
        "endTick": 0,  # Calculated on run
        "stopTick": bpy.context.scene.frame_end + 1,
        "isLoop": False,
        "returnTick": 0,
        "nsfw": False,
        "degrees": False,
        "moves": [],
    },
}

data_sort_order = ["x", "y", "z", "pitch", "yaw", "roll", "bend", "axis"]
partdata = {}
endtick = 0


def getPartData(name):
    global partdata
    if (
        name in bpy.data.objects
        and bpy.data.objects[name].animation_data is not None
        and bpy.data.objects[name].animation_data.action is not None
    ):
        for fcurve in bpy.data.objects[name].animation_data.action.fcurves:

            if fcurve.data_path == "location":
                if fcurve.array_index == 0:
                    type = "x"
                elif fcurve.array_index == 1:
                    type = "z"
                elif fcurve.array_index == 2:
                    type = "y"

            elif "rotation_euler" in fcurve.data_path:
                if fcurve.array_index == 0:
                    type = "pitch"
                elif fcurve.array_index == 1:
                    type = "roll"
                elif fcurve.array_index == 2:
                    type = "yaw"
            else:
                continue

            for keyframe in fcurve.keyframe_points:
                frame = int(keyframe.co[0])
                value = float(keyframe.co[1])
                if frame == 0:
                    continue

                if name not in partdata:
                    partdata[name] = {}
                if type not in partdata[name]:
                    partdata[name][type] = {}

                partdata[name][type][frame] = [
                    correctValue(value, name, type, fcurve),
                    getEasing(keyframe),
                ]

    ###########################################################################
    ###########################################################################
    # Bending data
    bendName = name + "_bend"

    if (
        bendName in bpy.data.objects
        and bpy.data.objects[bendName].animation_data is not None
        and bpy.data.objects[bendName].animation_data.action is not None
    ):
        for fcurve in bpy.data.objects[bendName].animation_data.action.fcurves:
            if fcurve.data_path == "rotation_euler":
                if fcurve.array_index == 0:
                    type = "bend"
                elif fcurve.array_index == 1:
                    type = "axis"

                for keyframe in fcurve.keyframe_points:
                    frame = int(keyframe.co[0])
                    value = float(keyframe.co[1])
                    if frame == 0:
                        continue

                    if name not in partdata:
                        partdata[name] = {}
                    if type not in partdata[name]:
                        partdata[name][type] = {}

                    partdata[name][type][frame] = [
                        correctValue(value, name, type, fcurve),
                        getEasing(keyframe),
                    ]


def correctValue(value, name, type, fcurve):
    if (name == "head" or name == "rightLeg" or name == "leftLeg") and type == "y":
        value -= 3

    if fcurve.data_path == "location":
        if not name == "torso":
            value = value * -4
        else:
            value = value * 0.25
            if type == "z":
                value = value * -1
    elif not (name == "torso" and not (type == "roll" or type == "bend")) and not (
        type == "axis"
    ):  # rotation correction (*-1) except for torzo roll/bend
        value = value * -1

    if type == "y":
        if name == "rightLeg" or name == "leftLeg":
            value += 12

    if type == "z" or type == "x":
        if name == "rightLeg":
            value += 0.1
        elif name == "leftLeg":
            value -= 0.1

    if name == "rightArm" or name == "leftArm":
        if type == "y":
            value += 12

    return roundValue(value)


def getEasing(keyframe):
    if keyframe is None:
        return "INOUTQUAD"

    if keyframe.easing == "AUTO":
        easing = "INOUT"
    elif "_" in keyframe.easing:
        easing = "".join(keyframe.easing.split("_")[1::])

    if keyframe.interpolation == "BEZIER":
        easing = easing + "QUAD"
    else:
        if not (
            keyframe.interpolation == "CONSTANT" or keyframe.interpolation == "LINEAR"
        ):
            easing = easing + str(keyframe.interpolation)
        else:
            easing = str(keyframe.interpolation)
    return easing


def roundValue(number):
    if number == 0:
        return 0
    return round(number, 4 - len(str(int(abs(number)))))


getPartData("head")
getPartData("torso")
getPartData("rightArm")
getPartData("leftArm")
getPartData("rightLeg")
getPartData("leftLeg")

for name, types in partdata.items():
    types = {key: types[key] for key in data_sort_order if key in types}  # Sorts data
    for type, frames in types.items():
        for frame, value in frames.items():

            frame_output = {
                "tick": frame,
                "easing": value[1],
                "turn": 0,
                name: {type: value[0]},
            }
            main_file_dict["emote"]["moves"].append(frame_output)

            if frame > endtick:
                endtick = frame

main_file_dict["emote"]["endTick"] = endtick
if HOLD_ON_LAST_FRAME:
    main_file_dict["emote"]["isLoop"] = True
    main_file_dict["emote"]["returnTick"] = endtick

if not os.path.isdir(EXPORT_PATH) or not EXPORT_PATH:
    EXPORT_PATH = os.path.dirname(bpy.data.filepath)
output_file = os.path.join(EXPORT_PATH, f"{animation_name}.json")
with open(output_file, "w") as f:
    json.dump(main_file_dict, f, indent=4)


def ShowMessageBox(title="Message Box", message="", icon="CHECKMARK"):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


ShowMessageBox(f"Successfully saved {animation_name}!", f"Exported to {output_file}")

GREEN = "\033[92m"
print(f"{GREEN}Successfully saved {animation_name}!", f"Exported to {output_file}")
