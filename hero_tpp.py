import bpy
from .common import *

WIDGET_COLLECTION_NAME = 'HeroTPPWidgets'

def load_rigify_script():

    filepath = get_addon_filepath() + 'lib.blend'
    data_name = 'rig_ui.py'

    # Exist data
    exist_datas = [data.name for data in bpy.data.texts]

    # Load new data
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        # Append new data
        data_to.texts.append(data_name)

    # Check just added data
    data = None
    if data_name not in exist_datas:
        data = bpy.data.texts.get(data_name)
    else:
        # If data already available
        added_datas = [data for data in bpy.data.texts if data.name not in exist_datas]
        if added_datas:
            data = added_datas[0]

    return data

def load_ue4_hero_tpp():

    filepath = get_addon_filepath() + 'lib.blend'
    armature_name = 'HeroTPP_rig'
    mesh_name = 'HeroTPP'

    blendfile = get_addon_filepath() + 'lib.blend'
    section   = "\\Object\\"
    object    = "HeroTPP"
    
    filepath  = blendfile + section + object
    directory = blendfile + section
    filename  = object

    existed_objs = [obj.name for obj in bpy.data.objects]
    
    bpy.ops.wm.append(
        filepath=filepath, 
        filename=filename,
        directory=directory)

    wgt_objs = [obj for obj in bpy.data.objects if obj.name not in existed_objs and obj.name.startswith('WGT')]
    rig_obj = [obj for obj in bpy.data.objects if obj.name not in existed_objs and obj.name.startswith('HeroTPP_rig')][0]
    mesh_obj = [obj for obj in bpy.data.objects if obj.name not in existed_objs and obj.name.startswith('HeroTPP')][0]

    if is_greater_than_280():
        scene  = bpy.context.scene
        col = get_set_collection(WIDGET_COLLECTION_NAME, scene.collection)
        #col.hide_viewport = True
        #col.hide_render = True
        for wgt_obj in wgt_objs:
            ori_col = wgt_obj.users_collection
            if ori_col: ori_col[0].objects.unlink(wgt_obj)
            col.objects.link(wgt_obj)
        
        # Exclude widget collections
        col = bpy.context.view_layer.layer_collection.children.get(WIDGET_COLLECTION_NAME)
        col.exclude = True
    else:
        for wgt_obj in wgt_objs:
            wgt_obj.layers[19] = True
            for i in range(19):
                wgt_obj.layers[i] = False

    script = load_rigify_script()
    exec(script.as_string(), {})

    return rig_obj, mesh_obj

class AddHeroTPP(bpy.types.Operator):
    bl_idname = "object.add_standard_ue4_tpp"
    bl_label = "Add Standard UE4 TPP"
    bl_description = "Add standard UE4 Third Person Character with Rigify"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        rig_obj, mesh_obj = load_ue4_hero_tpp()
        #scene.objects.active = rig_obj
        set_active(rig_obj)
        #rig_obj.location = scene.cursor_location.copy()
        rig_obj.location = cursor_location_get().copy()
        select_set(mesh_obj, False)
        return {'FINISHED'}

class UE4HELPER_PT_NewObjectsPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "objectmode"
    bl_label = "Add New Objects"
    bl_category = "UE4 Helper"

    def draw(self, context):
        c = self.layout.column(align=True)
        c.operator("object.add_standard_ue4_tpp", text="Add UE4 TPP Mesh", icon='ARMATURE_DATA')

def register():
    bpy.utils.register_class(AddHeroTPP)
    bpy.utils.register_class(UE4HELPER_PT_NewObjectsPanel)

def unregister():
    bpy.utils.unregister_class(AddHeroTPP)
    bpy.utils.unregister_class(UE4HELPER_PT_NewObjectsPanel)
