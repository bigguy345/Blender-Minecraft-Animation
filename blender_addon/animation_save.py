import bpy
from .constants import getImportName, setImportName

script_name = "animation_export.py"


class SaveAnimation(bpy.types.Operator):
    """My Operator Description"""

    bl_idname = "minecraft.save_animation"
    bl_label = "Save animation"
    bl_description = "Saves and exports current keyframes as a .json according to animation_export.py"
    animation_name: bpy.props.StringProperty(name="Animation name", default="")

    def invoke(self, context, event):
        self.animation_name = getImportName(self.animation_name)
        return context.window_manager.invoke_props_dialog(self)

    bl_options = {"REGISTER", "UNDO"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "animation_name", text="Enter name")

    def execute(self, context):
        if script_name not in bpy.data.texts or len(self.animation_name) < 1:
            return {"CANCELLED"}

        setImportName(self.animation_name)

        text_area = None
        for area in bpy.context.screen.areas:
            if area.type == "TEXT_EDITOR":
                text_area = area
                break

        if text_area is None:
            bpy.ops.screen.area_split(direction="VERTICAL", factor=0.66)
            text_area = bpy.context.screen.areas[-1]
            text_area.type = "TEXT_EDITOR"

        with bpy.context.temp_override(area=text_area):
            text_area.spaces[0].text = bpy.data.texts[script_name]
            bpy.ops.text.run_script()  # Execute the script

        self.report({"INFO"}, "Saved animation!")
        return {"FINISHED"}


# bpy.utils.register_class(SaveAnimation)
# bpy.ops.minecraft.save_animation("INVOKE_DEFAULT")
