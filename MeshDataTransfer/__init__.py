bl_info = {
    "name" : "MeshDataTransfer",
    "author" : "Maurizio Memoli",
    "description" : "This add on will transfer geometry data from one mesh to another based on 3 different spaces:"
                    " 'world, object, uv' ",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 0,),
    "location" : "",
    "warning" : "",
    "wiki_url": "",
    "category" : "Mesh"
}


import bpy
from bpy.types import (PropertyGroup)
from bpy.props import (PointerProperty)
from .operators import (TransferShapeData, TransferShapeKeyData, TransferVertexGroupsData)

def scene_chosenobject_poll(self , object):
    if bpy.context.active_object == object:
        return False
    return object.type == 'MESH'


class MeshDataSettings(PropertyGroup):
    mesh_object_space: bpy.props.EnumProperty(
        items=[('WORLD', 'World', '', 1),('LOCAL', 'Local', '', 2), ('UVS', 'Active UV', '', 3)],
        name="Object Space")

    search_method: bpy.props.EnumProperty(
        items=[('CLOSEST', 'Closest', '', 1),('RAYCAST', 'Raycast', '', 2)],
        name="Search method")

    transfer_shape: bpy.props.BoolProperty()

    transfer_shapekeys: bpy.props.BoolProperty()

    transfer_vertex_groups : bpy.props.BoolProperty()

    mesh_target: bpy.props.PointerProperty(type=bpy.types.Object, poll=scene_chosenobject_poll)

    transfer_shape_as_key : bpy.props.BoolProperty ()

class MeshDataGlobalSettings(PropertyGroup):

    transfer_modified_target : bpy.props.BoolProperty ()
    transfer_modified_source : bpy.props.BoolProperty ()



class ShapeKeysProp(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty()
    enabled : bpy.props.BoolProperty()

#========================================================================================================

class DATA_PT_mesh_data_transfer(bpy.types.Panel):
    bl_label = "Mesh Data Transfer"
    bl_idname = "MESH_PT_mesh_data_transfer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'


    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.mesh and (engine in {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'})


    def draw(self, context):
        active = bpy.context.active_object
        ob_prop = context.object.mesh_data_transfer_object
        sc_prop = context.scene.mesh_data_transfer_global
        ob = context.object

        # mesh_object_space layout
        main_box_layout = self.layout.box()
        sample_main_box = main_box_layout.box()

        option_label = sample_main_box.row()
        option_label.alignment = 'CENTER'
        option_label.label(text="Sample Space")
        option_row = main_box_layout.row()
        option_row.prop(ob_prop, "mesh_object_space", expand=True, text="Sample space")
        option_row2 = main_box_layout.row()
        option_row2.prop(ob_prop, 'search_method', expand=True, text="Search method")

        #option_row.use_property_split = True
        sample_target_mod = main_box_layout.row ()
        sample_target_mod.prop(sc_prop, 'transfer_modified_target', text="Sample Modified Target", icon='MESH_DATA')
        sample_source_mod = sample_target_mod.split()
        sample_source_mod.prop(sc_prop, 'transfer_modified_source', text="Sample Modified Source", icon='MESH_DATA')

        if ob_prop.mesh_object_space not in {'WORLD', 'LOCAL'}:
            sample_target_mod.enabled = False
            sample_source_mod.enabled = False

        #mesh picker layout
        mesh_picker_box_layout = main_box_layout.box()
        mesh_picker_box_layout.prop_search(ob_prop, "mesh_target", context.scene, "objects", text="Transfer to")

        #transfer shape layout
        transfer_shape_box_layout = main_box_layout.box()
        icon = 'TRIA_DOWN' if ob_prop.transfer_shape else 'TRIA_RIGHT'
        transfer_shape_box_layout.prop(ob_prop, "transfer_shape", text="Transfer Shape" , icon=icon)
        if ob_prop.transfer_shape:
            transfer_shape_box_layout.prop(ob_prop, "transfer_shape_as_key", text="Transfer as shape key")
            transfer_shape_box_layout.operator("object.transfer_shape_data", text="Transfer", icon="MOD_DATA_TRANSFER")

        #transfer shapekeys layout
        transfer_shapekeys_box_layout = main_box_layout.box()
        icon = 'TRIA_DOWN' if ob_prop.transfer_shapekeys else 'TRIA_RIGHT'
        transfer_shapekeys_box_layout.prop(ob_prop, "transfer_shapekeys" , text="Transfer Shapekeys", icon=icon)
        if ob_prop.transfer_shapekeys:
            transfer_shapekeys_box_layout.operator("object.transfer_shape_key_data" , text="Transfer" ,
                                                icon="MOD_DATA_TRANSFER")

        #transfer vertex groups layout
        transfer_shapekeys_box_layout = main_box_layout.box()
        icon = 'TRIA_DOWN' if ob_prop.transfer_vertex_groups else 'TRIA_RIGHT'
        transfer_shapekeys_box_layout.prop(ob_prop, "transfer_vertex_groups" , text="Transfer Vertex Groups", icon=icon)
        if ob_prop.transfer_vertex_groups:
            transfer_shapekeys_box_layout.operator("object.transfer_vertex_groups_data" , text="Transfer" ,
                                                icon="MOD_DATA_TRANSFER")


        #split = box_layout.split()
        #box_layout = split.column(align=True)
        # option_main_row = box_layout.row()


        # flow = box_layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=False, align=False)
        # box_layout.separator()
        #split = box_layout.row()
        # mesh_picker_row = box_layout.row()
        # mesh_picker_box = mesh_picker_row.box()
        # mesh_picker_box.label(text="Target Mesh:")
        # mesh_picker_box.prop(ob_prop, "mesh_target", text="")
        # mesh_picker_box.separator()
        # mesh_picker_box.separator ()
        # transfer_mod_target = mesh_picker_box.row ()
        # transfer_mod_target.prop(sc_prop , 'transfer_modified_target' , text="Sample Modified Target" , icon='BLANK1')
        # if ob_prop.mesh_object_space in {'WORLD', 'LOCAL'}:
        #     pass
        #
        # elif ob_prop.mesh_object_space == 'LOCAL':
        #     pass
        # if ob_prop.mesh_object_space != 'UVS' or ob.particle_systems:
        #     pass
        # col = split.column ()
        # source_box = col.box()
        # source_box.prop (ob_prop , "transfer_shape" , text="Transfer Shape" , icon='MESH_DATA')
        # source_box.prop (ob_prop , "transfer_shapekeys" , text="Transfer Shapekeys" , icon='SHAPEKEY_DATA')
        # source_box.prop (ob_prop , "transfer_vertex_groups" , text="Transfer Vertex Groups" , icon='GROUP_VERTEX')
        # transfer_mod_source =source_box.row()
        # transfer_mod_source.prop (sc_prop , 'transfer_modified_source' , text="Sample Modified Source" , icon='BLANK1')


#=================================================================================================================

classes = (DATA_PT_mesh_data_transfer, MeshDataSettings, MeshDataGlobalSettings, TransferShapeData,
           TransferShapeKeyData, TransferVertexGroupsData)

def register():
    global classes
    for cl in classes:
        bpy.utils.register_class(cl)

    bpy.types.Object.mesh_data_transfer_object = PointerProperty (type=MeshDataSettings)
    bpy.types.Scene.mesh_data_transfer_global = PointerProperty (type=MeshDataGlobalSettings)

def unregister():
    global classes
    for cl in classes:
        print (cl)
        bpy.utils.unregister_class (cl)

    del bpy.types.Object.mesh_data_transfer_object
    del bpy.types.Scene.mesh_data_transfer_global

if __name__ == "__main__":
    register()
