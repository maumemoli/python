import bpy
import bmesh
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

##------------------------------------------------------  
#
# Extract Mask
#
##------------------------------------------------------ 
bpy.types.WindowManager.ref_obj : bpy.props.StringProperty()
#Cut
class SPEEDSCULPT_OT_cut_by_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.cut_by_mask"
    bl_label = "Cut By Mask"
    bl_description = "Cut By Mask"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object
        WM = context.window_manager
        
        #Ref object name
        context.window_manager.ref_obj = context.active_object.name 
        ref_obj = context.window_manager.ref_obj

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.delete(type='FACE')

        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)


        # # Go in object duplicate and deselect faces
        # bpy.ops.object.mode_set(mode='OBJECT')
        # bpy.ops.object.duplicate_move()
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.select_all(action='DESELECT')
        #
        # # hide non masked faces
        # bpy.ops.object.mode_set(mode='SCULPT')
        # bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        #
        # # Go in edit and delete those faces of the second object
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.normals_make_consistent(inside=False)
        # bpy.ops.mesh.delete(type='FACE')
        #
        # # Go in sculpt and unhide faces
        # bpy.ops.object.mode_set(mode='SCULPT')
        # bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        # bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        # bpy.ops.object.mode_set(mode='OBJECT')
        #
        # #select the first object
        # context.view_layer.objects.active = bpy.data.objects[ref_obj]
        # bpy.data.objects[ref_obj].select_set(state=True)
        #
        # bpy.ops.object.mode_set(mode='SCULPT')
        # bpy.ops.paint.mask_flood_fill(mode='INVERT')
        #
        # bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        # # Go in edit and delete those faces
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.normals_make_consistent(inside=False)
        # bpy.ops.mesh.delete(type='FACE')
        # # Go in sculpt and unhide faces
        # bpy.ops.object.mode_set(mode='SCULPT')
        # bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        # bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        # bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.update_dyntopo() 
        #Comme Back in Sculpt mode    
        if WM.comeback_in_sculpt_mode :
            bpy.ops.object.mode_set(mode='SCULPT')
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.sculpt.dynamic_topology_toggle()  
        return {"FINISHED"}

class SPEEDSCULPT_OT_activate_looptools(bpy.types.Operator):
    bl_idname = "speedsculpt.activate_looptools"
    bl_label = "Activate Looptools"
    bl_description = "Activate Looptools"
    bl_options = {"REGISTER"}


    def execute(self, context):
        bpy.ops.preferences.addon_enable(module="mesh_looptools")
        bpy.ops.wm.save_userpref()
        return {"FINISHED"}

class SPEEDSCULPT_OT_flatten_mask(bpy.types.Operator):
    bl_idname = 'speedsculpt.flatten_mask'
    bl_label = "Flatten Mask"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager

        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.reveal()
        bpy.ops.transform.create_orientation(name='Flatten_Mask', use=True, overwrite=True)

        bpy.ops.speedsculpt.activate_looptools()
        bpy.ops.mesh.looptools_flatten(influence=100, lock_x=False, lock_y=False, lock_z=False, plane='normal',
                                       restriction='none')

        # cutom_orientation = context.scene.transform_orientation_slots['Flatten_Mask'].custom_orientation.matrix
        # bpy.ops.transform.resize(value=(1, 0, 1), orient_type='Flatten_Mask', orient_matrix_type='GLOBAL', mirror=True)

        bpy.ops.transform.delete_orientation()

        if WM.update_dyntopo:
            bpy.ops.object.mode_set(mode='SCULPT')
            bpy.ops.paint.mask_flood_fill(mode='INVERT')
            bpy.ops.object.update_dyntopo()
            bpy.ops.object.mode_set(mode='OBJECT')


        if WM.comeback_in_sculpt_mode :
            bpy.ops.object.mode_set(mode='SCULPT')
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.sculpt.dynamic_topology_toggle()

            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)



        return {'FINISHED'}

class SPEEDSCULPT_OT_hook_mask(bpy.types.Operator):
    bl_idname = 'speedsculpt.hook_mask'
    bl_label = "Hook Mask"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager
        act_obj = context.active_object

        for mod in act_obj.modifiers:
            if mod.type == 'HOOK':
                mod.show_viewport = False

        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.reveal()
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.create_orientation(name='Flatten_Mask', use=True, overwrite=True)
        bpy.ops.object.hook_add_newob()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.transform.delete_orientation()

        for obj in bpy.context.selected_objects:
            context.view_layer.objects.active = obj

        for mod in act_obj.modifiers:
            if mod.type == 'HOOK':
                mod.show_viewport = True
                mod.show_in_editmode = True
                mod.show_on_cage = True

        # if WM.update_dyntopo:
        #     bpy.ops.object.mode_set(mode='SCULPT')
        #     bpy.ops.paint.mask_flood_fill(mode='INVERT')
        #     bpy.ops.object.update_dyntopo()
        #     bpy.ops.object.mode_set(mode='OBJECT')


        # if WM.comeback_in_sculpt_mode :
        #     bpy.ops.object.mode_set(mode='SCULPT')
        #     if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
        #         pass
        #     else :
        #         bpy.ops.sculpt.dynamic_topology_toggle()
        #
        #     bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

        return {'FINISHED'}


#Duplicate
class SPEEDSCULPT_OT_duplicate_by_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.duplicate_by_mask"
    bl_label = "Duplicate By Mask"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager
        
        # Go in object duplicate and deselect faces
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate_move()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        # hide non masked faces
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        # Go in edit and delete those faces
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.delete(type='FACE')
        # Go in sculpt and unhide faces
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        bpy.ops.object.mode_set(mode='OBJECT') 

        bpy.ops.object.update_dyntopo() 
        #Comme Back in Sculpt mode    
        if WM.comeback_in_sculpt_mode :
            bpy.ops.object.mode_set(mode='SCULPT')
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.sculpt.dynamic_topology_toggle()  
#        bpy.ops.object.mode_set(mode='SCULPT') 
        return {"FINISHED"}

#Delete
class SPEEDSCULPT_OT_delete_by_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.delete_by_mask"
    bl_label = "Delete By Mask"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        # hide non masked faces
        bpy.ops.paint.mask_flood_fill(mode='INVERT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        
        # Go in edit and delete those faces
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.delete(type='FACE')
        
        # Go in sculpt and unhide faces
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.update_dyntopo()  
        bpy.ops.object.mode_set(mode='SCULPT') 
        
        return {"FINISHED"}


#Extract
class SPEEDSCULPT_OT_extract_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.extract_mask"
    bl_label = "Extract Mask"
    bl_description = "Extract the mask to create a new object"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        solidify_thickness = bpy.context.window_manager.solidify_thickness
        solidify_offset = bpy.context.window_manager.solidify_offset
        rim_only = bpy.context.window_manager.rim_only
        WM = context.window_manager
        
        # Go in object duplicate and deselect faces
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate_move()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        # hide non masked faces
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        # Go in edit and delete those faces
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.delete(type='FACE')
        # Go in sculpt and unhide faces
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        bpy.ops.object.mode_set(mode='OBJECT') 
        
        #Add Solidify with options
        if WM.add_solidify :
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].offset = solidify_offset
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].use_quality_normals = True
            bpy.context.object.modifiers["Solidify"].thickness = solidify_thickness
            bpy.context.object.modifiers["Solidify"].use_rim_only = rim_only

            if WM.apply_solidify:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
                bpy.ops.object.update_dyntopo()
            
        #Comme Back in Sculpt mode    
        if WM.comeback_in_sculpt_mode :
            bpy.ops.object.mode_set(mode='SCULPT')
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
                pass
            else :
                bpy.ops.sculpt.dynamic_topology_toggle() 
        
#        if WM.update_dyntopo:
#            bpy.ops.object.update_dyntopo()        
                   
        return {"FINISHED"}

# Go in Sculpt to add Mask
class SPEEDSCULPT_OT_add_extract_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.add_extract_mask"
    bl_label = "Add Mask"
    bl_description = "Add a mask to the object"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                if mod.type == 'HOOK':
                    mod.show_viewport = False
        if context.object.mode != "SCULPT":
            bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.brush_select(sculpt_tool='MASK')

        return {"FINISHED"}
        
                        