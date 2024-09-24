import bpy

from .animation_close import CloseAnimationOp
from .animation_import import ImportAnimationOp
from .reset_model import ResetModelOp
from .animation_save import SaveAnimation


class VIEW3D_PT_minecraft_animation(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Minecraft"
    bl_label = "Animation"

    def draw(self, context):
        coloumn = self.layout.column(align=True)
        coloumn.operator(ImportAnimationOp.bl_idname, text="Import")

        row = coloumn.row(align=True)
        row.operator(SaveAnimation.bl_idname, text="Save")
        row.operator(CloseAnimationOp.bl_idname, text="Close")


class VIEW3D_PT_minecraft_model(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_category = "Minecraft"
    bl_label = "Model"

    def draw(self, context):
        coloumn = self.layout.column()
        coloumn.operator(ResetModelOp.bl_idname, text="Reset")
