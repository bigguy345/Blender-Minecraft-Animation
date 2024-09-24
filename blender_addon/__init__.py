bl_info = {
    "name": "Minecraft Animations",
    "author": "goatee",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "location": "View3D > Tools",
    "description": "An example addon with multiple modules",
}

import bpy

from . import animation_close, animation_import, panel, reset_model, animation_save


def register():
    bpy.utils.register_class(animation_close.CloseAnimationOp)
    bpy.utils.register_class(animation_import.ImportAnimationOp)
    bpy.utils.register_class(animation_save.SaveAnimation)
    bpy.utils.register_class(reset_model.ResetModelOp)
    bpy.utils.register_class(panel.VIEW3D_PT_minecraft_animation)
    bpy.utils.register_class(panel.VIEW3D_PT_minecraft_model)


def unregister():
    bpy.utils.unregister_class(animation_close.CloseAnimationOp)
    bpy.utils.unregister_class(animation_import.ImportAnimationOp)
    bpy.utils.unregister_class(animation_save.SaveAnimation)
    bpy.utils.unregister_class(reset_model.ResetModelOp)
    bpy.utils.unregister_class(panel.VIEW3D_PT_minecraft_animation)
    bpy.utils.unregister_class(panel.VIEW3D_PT_minecraft_model)


if __name__ == "__main__":
    register()
