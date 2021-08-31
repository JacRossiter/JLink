bl_info = {
    "name" : "JLink: Link Transforms",
    "author" : "Jac Rossiter",
    "description" : "Adds Link Transforms to Link Menu (Ctrl L in object mode)",
    "blender" : (2, 90, 1),
    "version" : (0, 0, 0, 4),
    "warning" : "",
    "category" : "Object"
}

import bpy
import mathutils
from bpy.types import Panel, Operator

class LinkLocation_Operator(Operator):
    bl_idname = "link.location"
    bl_label = "Link Location"
    bl_description = "Copy Location from active object" 
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        active_location = bpy.context.view_layer.objects.active.location
        for obj in bpy.context.selected_objects:
            try:
                bpy.context.view_layer.objects.active = obj
                bpy.context.view_layer.objects.active.location = active_location
            except:
                pass
        return {'FINISHED'}

class LinkRotation_Operator(Operator):
    bl_idname = "link.rotation"
    bl_label = "Link Rotation"
    bl_description = "Copy Rotation from active object" 
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        active_rotation = bpy.context.view_layer.objects.active.rotation_euler
        for obj in bpy.context.selected_objects:
            try:
                bpy.context.view_layer.objects.active = obj
                bpy.context.view_layer.objects.active.rotation_euler = active_rotation
            except:
                pass
        return {'FINISHED'}

class LinkScale_Operator(Operator):
    bl_idname = "link.scale"
    bl_label = "Link Scale"
    bl_description = "Copy Scale from active object" 
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        active_scale = bpy.context.view_layer.objects.active.scale
        for obj in bpy.context.selected_objects:
            try:
                bpy.context.view_layer.objects.active = obj
                bpy.context.view_layer.objects.active.scale = active_scale
            except:
                pass
        return {'FINISHED'}

class LinkTransform_Operator(Operator):
    bl_idname = "link.transform"
    bl_label = "Link Transform"
    bl_description = "Copy Transforms from active object" 
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        active_location = bpy.context.view_layer.objects.active.location
        active_rotation = bpy.context.view_layer.objects.active.rotation_euler
        active_scale = bpy.context.view_layer.objects.active.scale

        for obj in bpy.context.selected_objects:
            try:
                bpy.context.view_layer.objects.active = obj
                bpy.context.view_layer.objects.active.location = active_location
                bpy.context.view_layer.objects.active.rotation_euler = active_rotation
                bpy.context.view_layer.objects.active.scale = active_scale
            except:
                pass
        return {'FINISHED'}

class RotationFromCursor_Operator(Operator):
    bl_idname = "link.cursor_rotation"
    bl_label = "Set Object Rotation using 3D Cursor"
    bl_description = "Sets your selected objects rotation to that of the 3D Cursor, maintains scene position and rotation" 
    bl_options = {'REGISTER'}
    
    def execute(self, context): # Code from Sergey Kritskiy

        bpy.context.scene.cursor.rotation_mode = 'XYZ' # If this is not set the function will not work.
        
        def Rotate(myMesh, mat):
            for v in myMesh.vertices:
                vec = mat @ v.co
                v.co = vec
        def RotateFromCursor():
            source = bpy.context.scene.cursor
            objects = bpy.context.selected_objects
            mat_source = source.rotation_euler.to_matrix()
            mat_source.invert()
            for ob in objects:
                mat_ob = ob.rotation_euler.to_matrix()
                if ob.type == 'MESH':
                    mat = mat_source @ mat_ob
                    Rotate(ob.data, mat)
                    ob.rotation_euler = source.rotation_euler
        RotateFromCursor()
        return {'FINISHED'}

def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("link.location", text="Location")
    layout.operator("link.rotation", text="Rotation")
    layout.operator("link.scale", text="Scale")
    layout.operator("link.transform", text="All Transforms")
    layout.operator("link.cursor_rotation", text="Rotation from 3D Cursor")

classes = (
    LinkLocation_Operator,
    LinkRotation_Operator,
    LinkScale_Operator,
    LinkTransform_Operator,
    RotationFromCursor_Operator

)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.VIEW3D_MT_make_links.append(draw_menu)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_MT_make_links.remove(draw_menu)

if __name__ == "__main__":
    register()