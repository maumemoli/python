import bpy
from .mesh_data_transfer import MeshDataTransfer,transfer_uvs, MeshData, UVMeshData, UVMeshDataTransfer

class TransferShapeData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.transfer_shape_data"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
               and context.active_object.mesh_data_transfer_object.mesh_source is not None

    def execute(self, context):

        active = context.active_object
        active_prop = context.object.mesh_data_transfer_object

        sc_prop = context.scene.mesh_data_transfer_global
        as_shape_key = active_prop.transfer_shape_as_key
        source = active.mesh_data_transfer_object.mesh_source
        # target_prop = target.mesh_data_transfer_global

        world_space = False
        uv_space = False

        search_method = active_prop.search_method
        sample_space = active_prop.mesh_object_space
        if sample_space == 'UVS':
            uv_space = True

        if sample_space == 'LOCAL':
            world_space = False

        if sample_space == 'WORLD':
            world_space = True
        transfer_data = MeshDataTransfer(target=active, source =source, world_space=world_space,
                                         uv_space=uv_space, search_method=search_method)
        transfer_data.transfer_vertex_position(as_shape_key=as_shape_key)

        return {'FINISHED'}


class TransferShapeKeyData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.transfer_shape_key_data"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
               and context.active_object.mesh_data_transfer_object.mesh_source is not None

    def execute(self, context):

        active = context.active_object
        active_prop = context.object.mesh_data_transfer_object

        sc_prop = context.scene.mesh_data_transfer_global
        as_shape_key = active_prop.transfer_shape_as_key
        source = active.mesh_data_transfer_object.mesh_source
        # target_prop = target.mesh_data_transfer_global

        world_space = False
        uv_space = False

        search_method = active_prop.search_method
        sample_space = active_prop.mesh_object_space
        if sample_space == 'UVS':
            uv_space = True

        if sample_space == 'LOCAL':
            world_space = False

        if sample_space == 'WORLD':
            world_space = True
        transfer_data = MeshDataTransfer(target=active, source =source, world_space=world_space,
                                         uv_space=uv_space, search_method=search_method)
        transfer_data.transfer_shape_keys()

        return {'FINISHED'}


class TransferVertexGroupsData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.transfer_vertex_groups_data"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
               and context.active_object.mesh_data_transfer_object.mesh_source is not None

    def execute(self, context):

        active = context.active_object
        active_prop = context.object.mesh_data_transfer_object

        sc_prop = context.scene.mesh_data_transfer_global
        as_shape_key = active_prop.transfer_shape_as_key
        source = active.mesh_data_transfer_object.mesh_source
        # target_prop = target.mesh_data_transfer_global

        world_space = False
        uv_space = False

        search_method = active_prop.search_method
        sample_space = active_prop.mesh_object_space
        if sample_space == 'UVS':
            uv_space = True

        if sample_space == 'LOCAL':
            world_space = False

        if sample_space == 'WORLD':
            world_space = True
        transfer_data = MeshDataTransfer(target=active, source =source, world_space=world_space,
                                         uv_space=uv_space, search_method=search_method)
        transfer_data.transfer_vertex_groups()

        return {'FINISHED'}

class TransferUVData(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.transfer_uv_data"
    bl_label = "Simple Object Operator"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None \
               and context.active_object.mesh_data_transfer_object.mesh_source is not None

    def execute(self, context):

        active = context.active_object
        active_prop = context.object.mesh_data_transfer_object

        sc_prop = context.scene.mesh_data_transfer_global
        as_shape_key = active_prop.transfer_shape_as_key
        source = active.mesh_data_transfer_object.mesh_source
        # target_prop = target.mesh_data_transfer_global

        world_space = False
        uv_space = False

        search_method = active_prop.search_method
        sample_space = active_prop.mesh_object_space
        if sample_space == 'UVS':
            uv_space = True

        if sample_space == 'LOCAL':
            world_space = False

        if sample_space == 'WORLD':
            world_space = True

        #transfer_uvs(active, target, world_space)
        transfer_data = MeshDataTransfer(target=active, source =source, world_space=world_space, search_method=search_method)
        transfer_data.transfer_uvs()


        return {'FINISHED'}
