import bpy, json, os


main_dict = {
    "head": {
        "location": [0.0, 0.0, 3.0],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "torso": {
        "location": [0.0, 0.0, 0.0],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "torso_bend": {
        "location": [0.0, 0.0, 4.5],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "rightArm": {
        "location": [1.25, 0.0, 2.5],
        "rotation": [0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "rightArm_bend": {
        "location": [0.25, 0.0, -1],
        "rotation": [0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "leftArm": {
        "location": [-1.25, 0.0, 2.5],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "leftArm_bend": {
        "location": [-0.25, 0.0, -1],
        "rotation": [0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "rightLeg": {
        "location": [0.5, 0.0, 3.0],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "rightLeg_bend": {
        "location": [0, 0.0, -1.5],
        "rotation": [0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "leftLeg": {
        "location": [-0.5, 0.0, 3.0],
        "rotation": [-0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
    "leftLeg_bend": {
        "location": [0, 0.0, -1.5],
        "rotation": [0.0, -0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    },
}


def getData(name):
    if name not in bpy.data.objects:
        return

    obj = bpy.data.objects[name]
    obj.location = main_dict[name]["location"]
    obj.rotation_euler = main_dict[name]["rotation"]
    obj.scale = main_dict[name]["scale"]


class ResetModelOp(bpy.types.Operator):
    """My Operator Description"""

    bl_idname = "minecraft.reset_model"
    bl_label = "Reset model"
    bl_description = "Reset model transformations to default values"

    def execute(self, context):
        for name in main_dict.keys():
            getData(name)
        self.report({"INFO"}, "Operator was executed!")
        return {"FINISHED"}
