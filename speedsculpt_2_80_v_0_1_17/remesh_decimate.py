import bpy
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)
from .functions import *
##------------------------------------------------------  
#
# Remesh/Decimate
#
##------------------------------------------------------ 
# Add Remesh modifier
class SPEEDSCULPT_OT_simple_remesh(bpy.types.Operator):
    bl_idname = "speedsculpt.simple_remesh"
    bl_label = "Remesh Object"
    bl_description = "Add simple remesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        prefs = get_addon_preferences()
        obj = context.active_object

        for obj in context.selected_objects:
            simple_remesh = obj.modifiers.new("R_Remesh", 'REMESH')
            simple_remesh.octree_depth = prefs.remesh_value
            simple_remesh.mode = 'SMOOTH'
            simple_remesh.use_smooth_shade = True
            simple_remesh.scale = 0.99

        return {"FINISHED"}

# Add Remesh modifier
class SPEEDSCULPT_OT_remesh(bpy.types.Operator):
    bl_idname = "speedsculpt.remesh"
    bl_label = "Remesh Object"
    bl_description = "Prepare object for clean remesh"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        modcount = len(obj.modifiers)
        WM = context.window_manager
        prefs = get_addon_preferences()
        remesh_value = prefs.remesh_value
        
        for obj in context.selected_objects:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            if obj.type != 'MESH':
                bpy.ops.object.convert(target='MESH')
                obj = context.active_object


            skin = context.object.modifiers.get("Skin")
            remesh = context.object.modifiers.get("R_Remesh")
            smooth = context.object.modifiers.get("R_Smooth")
            subsurf = context.object.modifiers.get("Subsurf")

            # check for Skin and Apply
            if skin:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")
                if subsurf:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")


            if not remesh and not smooth:
                # Add Remesh
                r_remesh = obj.modifiers.new("R_Remesh", 'REMESH')
                r_remesh.octree_depth = remesh_value
                r_remesh.mode = 'SMOOTH'
                r_remesh.use_smooth_shade = True
                r_remesh.scale = 0.99

                # Add Smooth
                r_smooth = obj.modifiers.new("R_Smooth", 'SMOOTH')
                r_smooth.factor = 1
                r_smooth.iterations = WM.remesh_smooth_repeat

                bpy.ops.object.modifier_move_down(modifier="R_Smooth")
                bpy.ops.object.modifier_move_down(modifier="R_Smooth")


                if modcount:
                    for i in range(modcount):
                        bpy.ops.object.modifier_move_up(modifier="R_Remesh")
                        bpy.ops.object.modifier_move_down(modifier="R_Smooth")

            else:
                for i in range(modcount):
                    bpy.ops.object.modifier_move_up(modifier="R_Remesh")
                    bpy.ops.object.modifier_move_down(modifier="R_Smooth")

        return {"FINISHED"}

# Remove the Remesh modifier
class SPEEDSCULPT_OT_remove_remesh_smooth(bpy.types.Operator):
    bl_idname = "speedsculpt.remove_remesh_smooth"
    bl_label = "Remove Remesh Smooth"
    bl_description = "Delete the Remesh modifier"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        for obj in context.selected_objects:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            remesh = context.object.modifiers.get("R_Remesh")
            smooth = context.object.modifiers.get("R_Smooth")
            if remesh and smooth:
                bpy.ops.object.modifier_remove(modifier="R_Remesh")
                bpy.ops.object.modifier_remove(modifier="R_Smooth")
            
            
        return {"FINISHED"}

# Apply the Remesh modifier
class SPEEDSCULPT_OT_apply_remesh_smooth(bpy.types.Operator):
    bl_idname = "speedsculpt.apply_remesh_smooth"
    bl_label = "Apply Remesh Smooth"
    bl_description = "Apply Remesh and smooth"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        for obj in context.selected_objects:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            remesh = context.object.modifiers.get("R_Remesh")
            smooth = context.object.modifiers.get("R_Smooth")
            if remesh and smooth:
                bpy.ops.object.modifier_apply(modifier="R_Remesh")
                bpy.ops.object.modifier_apply(modifier="R_Smooth")

        return {"FINISHED"}

# Hide Remesh    
def HideRemeshSmooth(self, context):
    bl_description = "Hide the Remesh Modifier"

    for obj in context.selected_objects:
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        if context.object.modifiers["R_Remesh"].show_viewport == True :
            context.object.modifiers["R_Remesh"].show_viewport = False
            context.object.modifiers["R_Smooth"].show_viewport = False
        else:
            context.object.modifiers["R_Remesh"].show_viewport = True
            context.object.modifiers["R_Smooth"].show_viewport = True

# Remesh Octree Depth
def RemeshOctreeDepth(self, context):
    bl_description = "Remesh Octree Depth"
    prefs = get_addon_preferences()
    remesh_value = prefs.remesh_value
    # WM = context.window_manager

    for obj in context.selected_objects:
        context.view_layer.objects.active = obj
        remesh = context.object.modifiers.get("R_Remesh")
        if remesh:
            # obj.modifiers["R_Remesh"].octree_depth = WM.remesh_octree_depth
            obj.modifiers["R_Remesh"].octree_depth = remesh_value

# Remesh Smooth Repeat
def RemeshSmoothRepeat(self, context):
    bl_description = "Remesh Smooth Repeat"
    WM = context.window_manager

    for obj in context.selected_objects:
        context.view_layer.objects.active = obj
        smooth = context.object.modifiers.get("R_Smooth")
        if smooth:
            obj.modifiers["R_Smooth"].iterations = WM.remesh_smooth_repeat


# Decimate
class SPEEDSCULPT_OT_decimate(bpy.types.Operator):
    bl_idname = "speedsculpt.decimate"
    bl_label = "Decimate Object"
    bl_description = "Decimate for lighter object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object

        for obj in context.selected_objects:
            context.view_layer.objects.active = obj
            decimate = context.object.modifiers.get("Decimate")
            if not decimate :
                obj.modifiers.new("Decimate", 'DECIMATE')

        return {"FINISHED"}    

# Apply Decimate
class SPEEDSCULPT_OT_apply_decimate(bpy.types.Operator):
    bl_idname = "speedsculpt.apply_decimate"
    bl_label = "Apply decimate"
    bl_description = "Apply Decimate modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object

        for obj in context.selected_objects:
            context.view_layer.objects.active = obj
            decimate = context.object.modifiers.get("Decimate")
            if decimate:
                bpy.ops.object.modifier_apply(modifier="Decimate")

        return {"FINISHED"}

# Hide Decimate
def Hidedecimate(self, context):
    bl_description = "Hide the Decimate Modifier"

    for obj in context.selected_objects:
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        if context.object.modifiers["Decimate"].show_viewport == True:
            context.object.modifiers["Decimate"].show_viewport = False
        else:
            context.object.modifiers["Decimate"].show_viewport = True

# Decimate Ratio
def DecimateRatio(self, context):
    bl_description = "Decimate Ratio"

    WM = context.window_manager

    for obj in context.selected_objects:
        context.view_layer.objects.active = obj
        decimate = context.object.modifiers.get("Decimate")
        if decimate:
            obj.modifiers["Decimate"].ratio = WM.decimate_ratio


# Remove Decimate
class SPEEDSCULPT_OT_remove_decimate(bpy.types.Operator):
    bl_idname = "speedsculpt.remove_decimate"
    bl_label = "Remove decimate"
    bl_description = "Remove Decimate modifier"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object

        for obj in context.selected_objects:
            context.view_layer.objects.active = obj
            decimate = context.object.modifiers.get("Decimate")
            if decimate:
                bpy.ops.object.modifier_remove(modifier="Decimate")

        return {"FINISHED"}        

# Decimate Mask
class SPEEDSCULPT_OT_decimate_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.decimate_mask"
    bl_label = "Decimate Mask"
    bl_description = "Decimate the masking part"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj_list = [obj for obj in context.selected_objects]
        obj = context.active_object
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            
            #Remove Vgroups
            for vgroup in obj.vertex_groups:
                if vgroup.name == 'Mask_Group':
                    obj.vertex_groups.remove(vgroup)
            
            # bpy.ops.object.mode_set(mode='SCULPT')
            # bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
            # bpy.ops.object.mode_set(mode='EDIT')
            # bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            # bpy.ops.mesh.select_all(action='SELECT')
            # bpy.ops.mesh.select_all(action='INVERT')
            # bpy.ops.mesh.reveal()

            # convert mask to vertex group
            bpy.ops.object.mode_set(mode='SCULPT')
            bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.reveal()


            # create vertex group and assign vertices
            obj.vertex_groups.new(name="Mask_Group")
            for vgroup in obj.vertex_groups:
                if vgroup.name == "Mask_Group":
                    bpy.ops.object.vertex_group_assign()

            bpy.ops.object.mode_set(mode='OBJECT')        
            bpy.ops.object.modifier_add(type='DECIMATE')
            context.object.modifiers["Decimate"].vertex_group = "Mask_Group"
            context.object.modifiers["Decimate"].ratio = 1
   
        return {"FINISHED"}   
  
# Edit Decimate
class SPEEDSCULPT_OT_edit_decimate_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.edit_decimate_mask"
    bl_label = "Edit Decimate Mask"
    bl_description = "Edit the Decimate mask"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        
        context.object.modifiers["Decimate"].show_viewport = False
        bpy.ops.object.mode_set(mode='SCULPT')
        return {"FINISHED"}

# Valid the Decimate Mask            
class SPEEDSCULPT_OT_valid_decimate_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.valid_decimate_mask"
    bl_label = "Valide Decimate Mask"
    bl_description = "Valid the Decimate mask"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        
        obj_list = [obj for obj in context.selected_objects]
        obj = context.active_object
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            
            #Remove Vgroups
            for vgroup in obj.vertex_groups:
                if vgroup.name == 'Mask_Group':
                    obj.vertex_groups.remove(vgroup)
            

            bpy.ops.paint.hide_show(action='HIDE', area='MASKED')

            bpy.ops.object.mode_set(mode='EDIT')
            
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.reveal()                           
            
            #Add Vgroup
            obj.vertex_groups.new(name="Mask_Group")
            for vgroup in obj.vertex_groups:
                if vgroup.name == 'Mask_Group':
                    bpy.ops.object.vertex_group_assign()
            
            context.object.modifiers["Decimate"].vertex_group = "Mask_Group"
            bpy.ops.object.mode_set(mode='OBJECT')          
            context.object.modifiers["Decimate"].show_viewport = True
            
        return {"FINISHED"}   

# Add Mask
class SPEEDSCULPT_OT_add_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.add_mask"
    bl_label = "Add Mask"
    bl_description = "Add Mask to Decimate custom areas"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        obj = context.active_object
        paint = context.tool_settings.image_paint
        
        context.object.modifiers["Decimate"].show_viewport = False
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.brush_select(sculpt_tool='MASK')

        
        return {"FINISHED"}
        

# Remove Mask
class SPEEDSCULPT_OT_remove_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.remove_mask"
    bl_label = "Remove Mask"
    bl_description = "Remove Mask"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        obj = context.active_object
        #Remove Vgroups
        for vgroup in obj.vertex_groups:
            if vgroup.name == 'Mask_Group':
                obj.vertex_groups.remove(vgroup)
        context.object.modifiers["Decimate"].vertex_group = ""
        
        return {"FINISHED"}