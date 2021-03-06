
import bpy
import webbrowser
from bpy.props import (FloatProperty,
                        IntProperty, 
                        BoolProperty )

bl_info = {
    'name': 'Breakdown-fy',
    'description': 'A plugin to create breakdown animations with breeze',
    'author': 'KripC',
    'version': (0, 1, 2),
    "blender": (3, 1, 0),
    'location': 'View3D > Tools > Breakdown-fy',
    'link': 'https://github.com/KripC2160/Breakdown-fy/issues',
    'category': 'Animate'
}

class bkfyProperties(bpy.types.PropertyGroup):
    height: IntProperty(
        name = "Height",
        description = "value for the height of the object which it will fall from",
        default = 30
    )
    offset : FloatProperty(
        name = "Offset",
        description = "offset to change the speed of keyframes falling",
        default = 5.0, precision = 2,
    )
        
    key_str : IntProperty(
        name = "Start Frame",
        description = "value for the start frame of the breakdown animation",
        default = 1,
    )
    
    key_end : IntProperty(
        name = "End Frame",
        description = "value for the end frame of the breakdown animation",
        default = 30,
    )
    
    nScene : BoolProperty(
        name = "Create New Scene",
        description = "creates a new scene for the breakdown animation when checked",
        default = True
    )
    
    nMat : BoolProperty(
        name = "Clay Render",
        description = "converts all the objects into a same clay material",
        default = False
    )

class bkfy_process(bpy.types.Operator):
    bl_idname = "bkfy.process"
    bl_label = "breakdown-fy"
    bl_options = {'REGISTER', 'UNDO'}
         
    def execute(self, context):
        if len(bpy.context.selected_objects) > 0:

            #selection_names = [] 
            #original_pos = []
            val = 0
            scene = context.scene
            mytool = scene.my_tools
            offset = mytool.offset
            nscene = mytool.nScene
            nMat = mytool.nMat

            if nscene == True:
                bpy.ops.scene.new(type='FULL_COPY')
                bpy.context.scene.my_tools.nScene = False
        
            for obj in bpy.context.selected_objects:
                print(obj)
                #original_pos.append(obj.location)
                #selection_names.append(obj.name)
                #print(original_pos[val])
                #num = val + offset
                obj.location.z += (mytool.height + offset)
                obj.keyframe_insert(data_path="location", frame=mytool.key_str)
                obj.location.z -= (mytool.height + offset) 
                obj.keyframe_insert(data_path="location", frame=mytool.key_end + offset + val)
                val += 1
            
            if nMat == True: 
                if 'bkfyclay' not in bpy.data.materials:
                    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0,0,0), scale=(0.1, 0.1, 0.1))
                    obj = bpy.context.object
                    mat = bpy.data.materials.new(name='bkfyclay')
                    #bpy.context.object.active_material.specular_intensity = 0 TODO: find out what is causing error
                    bpy.context.object.active_material.roughness = 1
                    bpy.data.objects.remove(bpy.context.object, do_unlink=True)
                    """
                    bpy.context.scene.render.engine = 'CYCLES'
                    bpy.context.scene.view_layers["ViewLayer"].material_override = bpy.data.materials["bkfyclay"]
                    """
                bpy.ops.object.select_all(action='SELECT')
                for obj in bpy.context.selected_objects:
                    for slot in obj.material_slots:
                        slot.material = bpy.data.materials["bkfyclay"]
                                
            return {'FINISHED'}
        else:
            return {'FINISHED'}

class bkfy_man(bpy.types.Operator):
    bl_idname = 'bkfy.manual'
    bl_label = 'Manual'
    
    def execute(self, context):
        webbrowser.open('https://github.com/KripC2160/Breakdown-fy/blob/main/README.md#manual')
        return {'FINISHED'}

class bkfy_sup(bpy.types.Operator):
    bl_idname = 'bkfy.support'
    bl_label = 'Support'
    
    def execute(self, context):
        webbrowser.open('https://github.com/KripC2160/Breakdown-fy/issues/new')
        return {'FINISHED'}
    
        
class Breakdown(bpy.types.Panel):
    bl_label = "Breakdown-fy"
    bl_idname = "bkfy"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Breakdown-fy"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tools

        layout.operator(bkfy_process.bl_idname, text="Breakdown-fy!", icon="SORT_ASC")
        layout.prop(mytool, "nScene")
        layout.prop(mytool, "nMat")
        layout.prop(mytool, "height")
        layout.prop(mytool, "offset") 
        r = layout.row(align=True)
        r.prop(mytool, "key_str")
        r.prop(mytool, "key_end")
        layout.separator()
        layout.operator(bkfy_man.bl_idname, text="Manual", icon='TEXT')
        layout.operator(bkfy_sup.bl_idname, text="Support/Report a bug", icon="ERROR")

classes = (
    bkfyProperties,
    Breakdown,
    bkfy_process,
    bkfy_man,
    bkfy_sup,
)
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tools = bpy.props.PointerProperty(type=bkfyProperties)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.my_tools
        
if __name__ == "__main__":
    register() 

