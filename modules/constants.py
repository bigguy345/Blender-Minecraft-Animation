import bpy

body_parts = ["head", "torso", "rightArm", "leftArm", "rightLeg", "leftLeg"]


def getAddonObject():
    if "minecraft_animation" not in bpy.data.objects:
        return bpy.data.objects.new("minecraft_animation", None)
    else:
        return bpy.data.objects.get("minecraft_animation")


def getImportName(default: str) -> str:
    obj = getAddonObject()
    if "import_name" in obj:
        return obj["import_name"]
    else:
        return default


def setImportName(name: str):
    getAddonObject()["import_name"] = name
