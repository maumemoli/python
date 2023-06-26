import bpy
from bpy.types import Operator, Macro
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

#pour sauver le tmp
from os.path import isfile, join
import os
from os import remove, listdir
from .functions import *

import bmesh

##------------------------------------------------------  
#
# Save Tmp
#
##------------------------------------------------------  
def save_tmp():
    """ Save the current blend in the blender tmp file """
 
    tmp_file = bpy.context.preferences.filepaths.temporary_directory
    if isfile(join(tmp_file, "speedsculpt_backup.blend")):
        os.remove(join(tmp_file, "speedsculpt_backup.blend"))
 
    bpy.ops.wm.save_as_mainfile(
        filepath = join(tmp_file, "speedsculpt_backup.blend"),
        copy = True
        )                           
##------------------------------------------------------  
#
# Check Options
#
##------------------------------------------------------      

# def DyntopoValue(context):
#     speedsculpt_dyntopo_value = get_addon_preferences().speedsculpt_dyntopo_value
#     # act = getattr(bpy.context, 'active_object')
#
#     # Setup dyntopo variable
#     toolsettings = context.context.scene.tool_settings
#     sculpt = toolsettings.sculpt
#
#     for o in context.selected_objects:
#
#         if sculpt.detail_type_method == 'CONSTANT':
#             o["Speedsculpt"] = str(sculpt.constant_detail_resolution)
#             sculpt.constant_detail_resolution = speedsculpt_dyntopo_value

        # elif sculpt.detail_type_method == 'BRUSH':
        #     o["Speedsculpt"] = str(sculpt.detail_percent)
        #     sculpt.detail_percent = speedsculpt_dyntopo_value
        #
        # elif sculpt.detail_type_method == 'RELATIVE':
        #     o["Speedsculpt"] = str(sculpt.detail_size)
        #     sculpt.detail_size = speedsculpt_dyntopo_value



#Dyntopo
def CheckDyntopo():
    prefs = get_addon_preferences()
    update_detail_flood_fill = prefs.update_detail_flood_fill
    flat_shading = prefs.flat_shading

    bpy.ops.view3d.snap_cursor_to_selected()
    saved_cursor_location = bpy.context.scene.cursor.location.copy()

    #Check modes
    constant = False
    relative = False
    brush = False
    if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
        constant = True

    elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
        brush = True

    elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'RELATIVE':
        relative = True

          
    subdiv_collapse = False
    collapse = False
    subdivide = False
    if bpy.context.scene.tool_settings.sculpt.detail_refine_method == 'SUBDIVIDE':
        subdivide = True
    elif bpy.context.scene.tool_settings.sculpt.detail_refine_method == 'COLLAPSE':
        collapse = True
    elif bpy.context.scene.tool_settings.sculpt.detail_refine_method == 'SUBDIVIDE_COLLAPSE':
        subdiv_collapse = True
        
#++++++++++++++++++++++++++++++++++++        
    #Add detail flood fill
    # if WM.update_detail_flood_fill :
    if update_detail_flood_fill:

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        # bpy.ops.object.mode_set(mode = 'SCULPT')
        bpy.ops.object.mode_set_or_submode(mode='SCULPT')

        # print("detail F L ON")

        #Check Dyntopo
        if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
            pass
        else :
            bpy.ops.sculpt.dynamic_topology_toggle()
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'


        bpy.ops.sculpt.detail_flood_fill()
        bpy.ops.sculpt.optimize()



    #activate dyntopo
    else :
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        bpy.ops.object.mode_set(mode = 'SCULPT')
        #Check Dyntopo
        if bpy.context.sculpt_object.use_dynamic_topology_sculpting :
            pass
        else :
            bpy.ops.sculpt.dynamic_topology_toggle()


    # shading
    if not flat_shading:
        bpy.context.scene.tool_settings.sculpt.use_smooth_shading = True
    else:
        bpy.context.scene.tool_settings.sculpt.use_smooth_shading = False
#++++++++++++++++++++++++++++++++++++

    #Assign previous mode
    if constant:
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
    elif relative :
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'RELATIVE'
    elif brush :
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'BRUSH'

    if subdivide:
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE'
    elif collapse:
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'COLLAPSE'
    elif subdiv_collapse :
        bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'

    # DyntopoValue()

    bpy.ops.object.mode_set(mode = 'OBJECT')

    # Restore Origin
    bpy.context.scene.cursor.location = saved_cursor_location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = saved_cursor_location
            
#Smoothmesh    
def CheckSmoothMesh():
    prefs = get_addon_preferences()
    smooth_mesh = prefs.smooth_mesh

    # if WM.smooth_mesh :
    if smooth_mesh :
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.modifier_add(type='SMOOTH')
        bpy.context.object.modifiers["Smooth"].factor = 1
        bpy.context.object.modifiers["Smooth"].iterations = 2
        #Apply
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")   
        
#Smoothmesh for mask
class SPEEDSCULPT_OT_check_smooth_mesh(bpy.types.Operator):
    bl_idname = "speedsculpt.check_smooth_mesh"
    bl_label = "Check Smooth Mesh"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        obj = context.active_object

        prefs = get_addon_preferences()
        smooth_mesh = prefs.smooth_mesh
        
        # if WM.smooth_mesh :
        if smooth_mesh:
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.modifier_add(type='SMOOTH')
            bpy.context.object.modifiers["Smooth"].factor = 1
            bpy.context.object.modifiers["Smooth"].iterations = 2
            #Make smooth only on the vertexgroup if it exist
            for vgroup in obj.vertex_groups:
                if vgroup.name == "Mask_Group":
                    bpy.context.object.modifiers["Smooth"].vertex_group = "Mask_Group"
            #Apply        
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Smooth")   
        return {"FINISHED"}
        
selection = list() 
#convert Metaballs
def convert_mataballs_curve(to_convert):
    
    # on selectionne les metaballs et on les convertit
    for obj in to_convert:
        obj.select_set(state=True)
        
    bpy.context.scene.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.convert(target='MESH')
    
    #remove holes
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.select_mode(type='EDGE')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    sel_edges=[e for e in bm.edges if e.select]
    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
    if len(sel_edges)>0:
      for e in bm.edges:
        if e not in sel_edges: e.select=False
    bpy.ops.mesh.edge_face_add()
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode = 'OBJECT')  

#Apply and Separate 
class ApplySeparate(bpy.types.Operator):
    bl_idname = "object.apply_separate"
    bl_label = "Apply and Separate"
    bl_description = "Apply Modifiers and Separate objects"
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        
        # recuperation de la liste des obj selectionne mais sans les metaballs ni les curves
        # elles seront ajoutees une fois converties
        for obj in context.selected_objects:
            if obj.type not in ['META', 'CURVE', 'FONT']:
                selection.append(obj)
 
        # recuperation des metaballs et curves       
        to_convert = [obj for obj in context.selected_objects if obj.type in [ 'META', 'CURVE', 'FONT']]
 
        bpy.ops.object.select_all(action = 'DESELECT')
 
        # si il y a des metaballs ou des curves
        if to_convert:
            # convertion des metaballs et curves via la fonction
            convert_mataballs_curve(to_convert)
            # on ajoute le nouvel obj a la list "selection"
            selection.append(context.active_object)
 
        for obj in selection:
            obj.select_set(state=True)

            if obj.modifiers:
                context.view_layer.objects.active = obj
                # bpy.context.scene.objects.active=obj
                for mod in obj.modifiers :
                    if mod.show_viewport == False :
                        bpy.ops.object.modifier_remove(modifier=mod.name)

                    if mod.type == 'MIRROR':
                        if not "Mirror_Skin" in obj.modifiers:
                            mod.use_mirror_merge = False
                            mod.use_clip = False
                        bpy.ops.object.convert(target='MESH')

                        # bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

                    else:
                        bpy.ops.object.convert(target='MESH')

                        # bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
 
        for obj in context.selected_objects :
            context.view_layer.objects.active = obj
            # bpy.context.scene.objects.active = obj
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.mode_set(mode = 'OBJECT')
 
            if not obj in selection:
                selection.append(obj)

        context.view_layer.objects.active = context.selected_objects[0]
 
        del(selection[:])
 
        return {"FINISHED"}   
     
##------------------------------------------------------  
#
# Update Dyntopo
#
##------------------------------------------------------ 
class UpdateDyntopo(bpy.types.Operator):
    bl_idname = "object.update_dyntopo"
    bl_label = "Update Dyntopo"
    bl_description = "Update object with the current detail size"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        prefs = get_addon_preferences()
        self.auto_save = prefs.auto_save
        object = bpy.context.active_object
        fill_holes_dyntopo = prefs.fill_holes_dyntopo
        add_remesh = prefs.add_remesh
        
        if self.auto_save:
            save_tmp()
        bpy.context.preferences.edit.use_global_undo = True


        for obj in context.selected_objects:

            context.view_layer.objects.active = obj
            # bpy.context.scene.objects.active=obj
            if obj.modifiers :
                for mod in obj.modifiers:
                    if mod.type == 'HOOK':
                        bpy.ops.object.convert(target='MESH')


        #SCULPT
        if context.object.mode == "SCULPT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bpy.ops.object.mode_set(mode = 'SCULPT')
            
            #Fill Hole
            if fill_holes_dyntopo:
                #Fill Holes
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='EDGE')
                bm = bmesh.from_edit_mesh(bpy.context.object.data)
                sel_edges=[e for e in bm.edges if e.select]
                bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
                if len(sel_edges)>0:
                  for e in bm.edges:
                    if e not in sel_edges: e.select=False
                bpy.ops.mesh.edge_face_add()
                bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
                
                bpy.ops.mesh.select_more()
                bpy.ops.mesh.select_more()
                
                #create vertex group and assign vertices   
                object.vertex_groups.new(name="Mask_Group")
                for vgroup in object.vertex_groups:
                    if vgroup.name == "Mask_Group":
                        bpy.ops.object.vertex_group_assign()
                
                #mask from faces
                bpy.ops.mesh.hide(unselected=False)
                bpy.ops.object.mode_set(mode='SCULPT')
                bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
                bpy.ops.paint.hide_show(action='SHOW', area='ALL')
                bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

            
            #Check Dyntopo and smooth
            bpy.ops.speedsculpt.check_smooth_mesh()
            CheckDyntopo()
            
            bpy.ops.object.mode_set(mode = 'SCULPT')
            
        #OBJECT
        elif bpy.context.object.mode == "OBJECT":
            
            for obj in context.selected_objects:
                bpy.ops.object.select_all(action='DESELECT')
                obj.select_set(state=True)
                context.view_layer.objects.active = obj
                     
                if obj.type == 'META' : 
                    bpy.ops.object.convert(target='MESH')  
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                
                if obj.type in ['CURVE', 'FONT'] :   
                    bpy.ops.object.convert(target='MESH')
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    
                    #remove holes
                    bpy.ops.object.mode_set(mode = 'EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.select_mode(type='EDGE')
                    bm = bmesh.from_edit_mesh(bpy.context.object.data)
                    sel_edges=[e for e in bm.edges if e.select]
                    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
                    if len(sel_edges)>0:
                      for e in bm.edges:
                        if e not in sel_edges: e.select=False
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    bpy.ops.object.mode_set(mode='EDIT')  
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles()
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
                    
                if obj.modifiers:
                    if not "Mirror_primitive" in obj.modifiers:
                        bpy.ops.object.apply_separate()
                        bpy.ops.object.boolean_sculpt_union_difference() 
                
                
                # if WM.fill_holes_dyntopo:
                if fill_holes_dyntopo:
                    #Fill Holes
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_mode(type='EDGE')
                    bm = bmesh.from_edit_mesh(bpy.context.object.data)
                    sel_edges=[e for e in bm.edges if e.select]
                    bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
                    if len(sel_edges)>0:
                      for e in bm.edges:
                        if e not in sel_edges: e.select=False
                    bpy.ops.mesh.edge_face_add()
                    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
                    
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.select_more()
                    
                    #create vertex group and assign vertices   
                    obj.vertex_groups.new(name="Mask_Group")
                    for vgroup in obj.vertex_groups:
                        if vgroup.name == "Mask_Group":
                            bpy.ops.object.vertex_group_assign()

                    bpy.ops.mesh.hide(unselected=False)
                    bpy.ops.object.mode_set(mode='SCULPT')
                    bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
                    bpy.ops.paint.hide_show(action='SHOW', area='ALL')
                    bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

                    bpy.ops.object.mode_set(mode='OBJECT')
                    


                if add_remesh:
                    bpy.ops.speedsculpt.simple_remesh()
                    # bpy.ops.object.remesh()
                    bpy.ops.object.apply_separate()



                bpy.ops.speedsculpt.check_smooth_mesh()
                CheckDyntopo()



                bpy.ops.object.mode_set(mode = 'OBJECT')

                # WM = context.window_manager
                # # Setup dyntopo variable
                # toolsettings = context.tool_settings
                # sculpt = toolsettings.sculpt
                # for o in context.selected_objects:
                #     # if hasattr(sculpt, "constant_detail"):
                #     o["Speedsculpt"] = str(WM.speedsculpt_dyntopo_value)

        #Remove Vgroup
        for vgroup in object.vertex_groups:
            if vgroup.name == "Mask_Group":
                object.vertex_groups.remove(vgroup)

        bpy.context.scene.tool_settings.use_snap = False
        # shading = context.space_data.shading
        # shading.show_xray = False



        return {"FINISHED"}
        
##------------------------------------------------------  
#
# Boolean Union/Difference
#
##------------------------------------------------------    
# UNION / Difference 
class BooleanSculptUnionDifference(bpy.types.Operator):
    bl_idname = "object.boolean_sculpt_union_difference"
    bl_label = "Boolean Union Difference"
    bl_description = "Combine objects !!10x faster on blender 2.77.3!!"
    bl_options = {"REGISTER", "UNDO"}
    
    operation_type : bpy.props.EnumProperty(
                items = (('UNION', "", ""),
                ('DIFFERENCE', "", "")),
                default = 'UNION',
                )
             
    def execute(self, context):
        WM = context.window_manager
        Detailsize = bpy.context.window_manager.detail_size

        prefs = get_addon_preferences()
        self.auto_save = prefs.auto_save
        add_remesh = prefs.add_remesh

        #save Temp
        if self.auto_save:
            save_tmp()
        
        bpy.context.preferences.edit.use_global_undo = True
        
        actObj = context.active_object  

        #Separate objects
        if self.operation_type == 'UNION':
            bpy.ops.object.apply_separate()

        #Union
        actObj = context.active_object
        for selObj in bpy.context.selected_objects:

            if selObj != context.active_object and(selObj.type == "MESH"):
                act_obj = context.active_object
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                newMod = act_obj.modifiers.new("Boolean"+ selObj.name,"BOOLEAN")
                newMod.operation = self.operation_type

                # if (2, 79, 4) < bpy.app.version:
                #     # Check Remesh
                #     remesh = False
                #     for mod in bpy.context.active_object.modifiers:
                #         if mod.type == "REMESH":
                #             remesh = True

                    # if not remesh :
                    #     newMod.solver = 'BMESH'

                    
                newMod.object = selObj
                bpy.ops.object.modifier_apply (modifier=newMod.name)
                bpy.ops.object.select_all(action='DESELECT')
                selObj.select_set(state=True)
                bpy.ops.object.delete()
                act_obj.select_set(state=True)
                # act_obj.select=True

                if add_remesh:
                    bpy.ops.speedsculpt.simple_remesh()
                    # bpy.ops.object.remesh()
                    bpy.ops.object.apply_separate()
        
        #Update Dyntopo and Smooth
        CheckDyntopo()
        CheckSmoothMesh()
        
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {"FINISHED"}

# Boolean Rebool       
class BooleanSculptRebool(bpy.types.Operator):
    bl_idname = "object.boolean_sculpt_rebool"
    bl_label = "Boolean Rebool"
    bl_description = "Slice object in two parts !!10x faster on blender 2.77.3!!"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        WM = context.window_manager

        prefs = get_addon_preferences()
        self.auto_save = prefs.auto_save
        add_remesh = prefs.add_remesh
        actObj = context.active_object  
        
        #save Temp
        if self.auto_save:
            save_tmp()



        bpy.context.preferences.edit.use_global_undo = True
   
        final_list = []
        act_obj = context.active_object
        obj_bool_list = [obj for obj in context.selected_objects if obj != act_obj and obj.type == 'MESH']
        bpy.ops.object.select_all(action='DESELECT')

        final_list.append(act_obj)
        for obj in obj_bool_list:
            obj.select_set(state=True)
            # act_obj.select=True
            act_obj.modifiers.new("Boolean", 'BOOLEAN')
            act_obj.modifiers["Boolean"].object = obj
            act_obj.modifiers["Boolean"].operation = 'DIFFERENCE'
                
            bpy.ops.object.duplicate_move()
            
#            bpy.context.active_object.name= "temptoto"
            tempobj = context.active_object
            
            final_list.append(tempobj)
            
            tempobj.modifiers["Boolean"].operation = 'INTERSECT'
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            actObj.select_set(state=True)
            context.view_layer.objects.active = actObj

            # act_obj.select=True
            # bpy.context.scene.objects.active = act_obj
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Boolean')

            actObj.select_set(state=False)
            tempobj.select_set(state=False)
            obj.select_set(state=True)

            # act_obj.select=False
            # tempobj.select=False
            # obj.select = True
            bpy.ops.object.delete(use_global=False)

            actObj.select_set(state=True)
            # act_obj.select=True
            

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY') 
        bpy.ops.object.select_all(action='DESELECT')   
        
        for obj in final_list :
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            if add_remesh:
                bpy.ops.speedsculpt.simple_remesh()
                # bpy.ops.object.remesh()
                bpy.ops.object.apply_separate()

            CheckDyntopo()
            CheckSmoothMesh()
            # obj.select = False
            obj.select_set(state=False)

        actObj.select_set(state=True)
        context.view_layer.objects.active = actObj

        if add_remesh:
            bpy.ops.speedsculpt.simple_remesh()
            # bpy.ops.object.remesh()
            bpy.ops.object.apply_separate()

        return {"FINISHED"}



# import random
# # Create Material
# class SPEEDSCULPT_OT_create_random_materials(bpy.types.Operator):
#     bl_idname = 'speedsculpt.create_random_materials'
#     bl_label = "Create Random Materials"
#     bl_options = {'REGISTER'}
#
#     @classmethod
#     def poll(cls, context):
#         return True
#
#     def execute(self, context):
#         obj = bpy.context.active_object
#         bpy.context.scene.tool_settings.sculpt.show_diffuse_color = True
#
#         for obj in bpy.context.selected_objects:
#             bpy.context.scene.objects.active=obj
#
#             # Create a new material
#             material = bpy.data.materials.new(name=obj.name)
#             material.use_nodes = True
#             material_output = material.node_tree.nodes.get('Material Output')
#             # remove diffuse
#             diffuse = material.node_tree.nodes['Diffuse BSDF']
#             material.node_tree.nodes.remove(diffuse)
#             # add Principled
#             shader = material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
#             shader.location[0] = 50
#             shader.location[1] = 306
#
#             # link shader to material
#             material.node_tree.links.new(material_output.inputs[0], shader.outputs[0])
#             # set active material to your new material
#             obj.active_material = material
#
#             val = lambda: random.random()
#             C = (val(), val(), val())
#             bpy.context.object.active_material.diffuse_color = (C[0], C[1], C[2])
#             bpy.context.object.active_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (
#                 C[0], C[1], C[2], 1)
#
#         return {'FINISHED'}
#
# class SPEEDSCULPT_OT_SC_Remove_Shaders(bpy.types.Operator):
#     bl_idname = 'speedsculpt.sc_remove_shaders'
#     bl_label = "Remove Shader from selection"
#     bl_options = {'REGISTER'}
#
#     @classmethod
#     def poll(cls, context):
#         return True
#
#     def execute(self, context):
#         selection = bpy.context.selected_objects
#
#         for obj in selection:
#             obj.select_set(state=True)
#             context.view_layer.objects.active = obj
#             if obj.material_slots:
#                 bpy.ops.object.material_slot_remove()
#
#         return {'FINISHED'}
#
#
# class SPEEDSCULPT_OT_Random_Color(bpy.types.Operator):
#     """    RANDOM COLOR
#
#     CLICK - Add Random Color
#     SHIFT - Add the same Shader to Selection
#     CTRL  - Remove Shader
#     ALT    - Link Shader
#     CTRL + SHIFT - Select objects with the same material
#     CTRL + ALT - Single User"""
#
#     bl_idname = "speedsculpt.random_color"
#     bl_label = "Speedsculpt Random Color"
#     bl_options = {"REGISTER", "UNDO"}
#
#     def invoke(self, context, event):
#         selection = bpy.context.selected_objects
#
#         bpy.context.object.show_transparent = True
#         bpy.context.space_data.show_backface_culling = True
#
#         if event.ctrl and event.shift:
#             bpy.ops.object.select_linked(type='MATERIAL')
#
#         elif event.ctrl and event.alt:
#             bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=False, obdata=False, material=True,
#                                             texture=True, animation=False)
#
#         elif event.shift:
#             for obj in selection:
#                 obj.select_set(state=True)
#                 context.view_layer.objects.active = obj
#                 bpy.ops.object.create_random_materials()
#                 bpy.ops.object.make_links_data(type='MATERIAL')
#
#         elif event.ctrl:
#             for obj in selection:
#                 obj.select_set(state=True)
#                 context.view_layer.objects.active = obj
#                 if obj.material_slots:
#                     bpy.ops.object.material_slot_remove()
#
#         elif event.alt:
#             bpy.ops.object.make_links_data(type='MATERIAL')
#
#         else:
#             bpy.ops.object.create_random_materials()
#
#         return {"FINISHED"}
#
#
# def Speedsculpt_Set_Material_Color(self, context):
#     selection = bpy.context.selected_objects
#     WM = bpy.context.window_manager
#
#     for obj in selection:
#         obj.select_set(state=True)
#         context.view_layer.objects.active = obj
#
#         if len(obj.material_slots):
#             bpy.context.object.active_material.diffuse_color = WM.speedsculpt_set_material_color
#             bpy.context.object.active_material.node_tree.nodes['Principled BSDF'].inputs[0].default_value = (
#                 WM.speedsculpt_set_material_color[0], WM.speedsculpt_set_material_color[1],
#                 WM.speedsculpt_set_material_color[2], 1)