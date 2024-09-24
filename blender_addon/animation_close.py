import bpy
from .constants import body_parts
from .constants import getAddonObject


class CloseAnimationOp(bpy.types.Operator):
    """My Operator Description"""

    bl_idname = "minecraft.close_animation"
    bl_label = "Close animation"
    bl_description = "Close animation and unlink all actions"

    def execute(self, context):
        closeAnimation()
        self.report({"INFO"}, "Operator was executed!")
        return {"FINISHED"}


def closeAnimation():
    bpy.context.scene.frame_set(0)
    bpy.ops.minecraft.reset_model()
    for name in body_parts:
        if name not in bpy.data.objects:
            continue

        bone = bpy.data.objects[name]
        if bone.animation_data is None:
            continue
        bone.animation_data.action = None

        bendName = f"{name}_bend"
        if bendName not in bpy.data.objects:
            continue
        bendBone = bpy.data.objects[bendName]
        if bendBone.animation_data is None:
            continue
        bendBone.animation_data.action = None

    from .constants import setImportName

    setImportName("")
