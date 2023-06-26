import bpy
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

from .operators import (CheckDyntopo,
                        save_tmp,
                        CheckSmoothMesh)

from .functions import *  

import bmesh                    
                        
                        
##------------------------------------------------------  
#
# Curves
#
##------------------------------------------------------ 

#class Smooth_Result(bpy.types.Operator):
#    bl_idname = "object.smooth_result"
#    bl_label = "Smooth Result"
#    bl_description = ""
#    bl_options = {"REGISTER","UNDO"}

#    @classmethod
#    def poll(cls, context):
#        return True

#    def execute(self, context):
#        if WM.smooth_result:
#            bpy.ops.object.mode_set(mode = 'EDIT')
#            bpy.ops.mesh.select_all(action='SELECT')
#            bpy.ops.mesh.vertices_smooth(repeat=100)
#            bpy.ops.object.mode_set(mode = 'OBJECT')

#        return {"FINISHED"}




# class SPEEDSCLUPT_OT_convert_lathe(bpy.types.Operator):
#     bl_idname = "speedsculpt.convert_lathe"
#     bl_label = "Convert Mesh to Dyntopo"
#     bl_options ={'REGISTER', 'UNDO'}
#
#     def invoke(self,context,event):
#         bpy.ops.object.mode_set(mode = 'OBJECT')
#         bpy.ops.object.convert(target='MESH')
#
#
#         bpy.ops.object.mode_set(mode = 'EDIT')
#         bpy.ops.mesh.select_all(action='DESELECT')
#         bpy.ops.mesh.select_all(action='SELECT')
#
#         bpy.ops.mesh.select_mode(type='EDGE')
#         bm = bmesh.from_edit_mesh(bpy.context.object.data)
#         sel_edges=[e for e in bm.edges if e.select]
#         bpy.ops.mesh.select_non_manifold(extend=False, use_wire=False, use_boundary=True, use_multi_face=False, use_non_contiguous=False, use_verts=False)
#         if len(sel_edges)>0:
#           for e in bm.edges:
#             if e not in sel_edges: e.select=False
#         bpy.ops.mesh.edge_face_add()
#
#         bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
#
#
#         bpy.ops.object.mode_set(mode = 'OBJECT')
#
#         bpy.ops.object.modifier_add(type='SUBSURF')
#
#         bpy.ops.object.update_dyntopo()
#         return {'FINISHED'}

    
#Create lathe          
class SPEEDSCULPT_OT_create_lathe(bpy.types.Operator):
    bl_idname = "speedsculpt.create_lathe"
    bl_label = "Create Lathe"
    bl_description = "Create Lathe"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        if context.object is not None :
        
            actObj = context.active_object if context.object is not None else None
            if actObj :
                bpy.context.scene.obj1 = actObj.name
            
            
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            #Create Curve
            bpy.ops.curve.primitive_bezier_curve_add(align='VIEW')
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.curve.delete(type='VERT')
            
            #Create Modifier
            bpy.ops.object.modifier_add(type='SCREW')
            bpy.context.object.modifiers["Screw"].use_normal_flip = True
            bpy.context.object.modifiers["Screw"].steps = 48

            
            if actObj :
                bpy.context.object.modifiers["Screw"].object = actObj

        else :
            #Create Curve
            bpy.ops.curve.primitive_bezier_curve_add(align='VIEW')
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.curve.delete(type='VERT')
            
            #Create Modifier
            bpy.ops.object.modifier_add(type='SCREW')
            bpy.context.object.modifiers["Screw"].use_normal_flip = False
            bpy.context.object.modifiers["Screw"].steps = 48

            
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.mode_set(mode = 'EDIT')
        # bpy.context.object.data.show_normal_face = False
        bpy.ops.curve.draw('INVOKE_DEFAULT')
        
        return {"FINISHED"}

#Create Empty
class SPEEDSCULPT_OT_create_empty(bpy.types.Operator):
    bl_idname = "speedsculpt.create_empty"
    bl_label = "Create Empty"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        curve_obj = context.active_object if context.object is not None else None
        if curve_obj :
            context.scene.obj1 = curve_obj.name
     
        if context.object is not None :
            bpy.ops.object.mode_set(mode = 'OBJECT')
        
        bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')   
        
        #create Empty 
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        empty_obj = context.active_object
        # bpy.context.object.show_x_ray = True
        bpy.ops.transform.resize(value=(2, 2, 2))

        bpy.ops.object.select_all(action='DESELECT')

        #Select Curve and add empty as ref object
        curve_obj.select_set(state=True)
        context.view_layer.objects.active = curve_obj
        bpy.context.object.modifiers["Screw"].object = empty_obj
        bpy.ops.object.select_all(action='DESELECT')
        
        #Select Empty
        empty_obj.select_set(state=True)
        context.view_layer.objects.active = empty_obj
        bpy.ops.transform.translate('INVOKE_DEFAULT')

        bpy.context.scene.cursor.location[0] = 0
        bpy.context.scene.cursor.location[1] = 0
        bpy.context.scene.cursor.location[2] = 0

        return {"FINISHED"}        

#BBox
class SPEEDSCULPT_OT_bbox(bpy.types.Operator):
    bl_idname = "speedsculpt.bbox"
    bl_label = "Bbox"
    bl_description = "Create surface from curve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        WM = context.window_manager
        Detailsize = bpy.context.window_manager.detail_size
        bbox_depth = bpy.context.window_manager.bbox_depth
        bbox_bevel = bpy.context.window_manager.bbox_bevel
        bbox_offset = bpy.context.window_manager.bbox_offset
 
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.mode_set(mode = 'EDIT')
            bpy.ops.curve.cyclic_toggle()
            bpy.context.object.data.dimensions = '2D'
            bpy.context.object.data.resolution_u = 12
            bpy.context.object.data.fill_mode = 'BOTH'
            bpy.context.object.data.bevel_depth = bbox_bevel
            bpy.context.object.data.offset = bbox_offset
            bpy.context.object.data.bevel_resolution = 5
            bpy.context.object.data.extrude = bbox_depth
            
        elif bpy.context.object.mode == "EDIT":
            bpy.ops.curve.cyclic_toggle()
            bpy.context.object.data.dimensions = '2D'
            bpy.context.object.data.resolution_u = 12
            bpy.context.object.data.fill_mode = 'BOTH'
            bpy.context.object.data.bevel_depth = bbox_bevel
            bpy.context.object.data.offset = bbox_offset
            bpy.context.object.data.bevel_resolution = 5
            bpy.context.object.data.extrude = bbox_depth
         
        #Convert poly
        if not WM.bbox_convert :
            bpy.ops.object.mode_set(mode = 'OBJECT') 
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
            bpy.ops.object.mode_set(mode = 'OBJECT')

            CheckDyntopo()
            CheckSmoothMesh()
            
            if WM.smooth_result:
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.vertices_smooth(repeat=100)
                bpy.ops.object.mode_set(mode = 'OBJECT')

        # bpy.context.object.show_x_ray = False
        return {"FINISHED"}
    
#Create Curve          
class SPEEDSCULPT_OT_create_curve(bpy.types.Operator):
    bl_idname = "speedsculpt.create_curve"
    bl_label = "Create Curve"
    bl_description = "Create a Curve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        actObj = context.active_object if context.object is not None else None
        if actObj :
            context.scene.obj1 = actObj.name
            
        WM = context.window_manager
        ref_obj = context.window_manager.ref_obj
        
        if context.object is not None :
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        #Create Vertex
        bpy.ops.curve.primitive_bezier_curve_add(align='VIEW')
        context.active_object.name= "BS_Curve"
        
        if WM.add_mirror :
            bpy.ops.object.modifier_add(type='MIRROR')
            bpy.context.object.modifiers["Mirror"].use_axis[0] = True
            bpy.context.object.modifiers["Mirror"].use_mirror_merge = False

            if WM.ref_obj :
                bpy.context.object.modifiers["Mirror"].mirror_object = bpy.data.objects[ref_obj]
                skin_origin = False
                
            elif actObj :
                bpy.context.object.modifiers["Mirror"].mirror_object = actObj
                skin_origin = False
                
            else :
                bpy.ops.object.modifier_remove(modifier="Mirror")
                
                
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.curve.delete(type='VERT')
        # bpy.context.object.data.show_normal_face = False
        # bpy.context.object.show_x_ray = True
        bpy.ops.curve.draw('INVOKE_DEFAULT')
        
        return {"FINISHED"}

#convert To skin    
class SPEEDSCULPT_OT_Convert_Curve_To_Skin(bpy.types.Operator):
    bl_idname = "speedsculpt.convert_curve_to_skin"
    bl_label = "Convert Curve To Skin"
    bl_description = "Convert Curve To Skin"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        WM = context.window_manager
        ref_obj = context.window_manager.ref_obj
        
        actObj = context.active_object
        
        if "Mirror" in actObj.modifiers:
            bpy.ops.object.modifier_remove(modifier="Mirror")

        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.curve.spline_type_set(type='POLY')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.convert(target='MESH')
        
        #Add Subdiv base
        newSubdiv = actObj.modifiers.new("Smooth_skin","SUBSURF")
        newSubdiv.levels = 2
        
        #Add Skin modifier
        newSkin = actObj.modifiers.new("Skin","SKIN")
        newSkin.use_smooth_shade = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.object.skin_root_mark()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Add Subdiv
        newMod = actObj.modifiers.new("Subsurf","SUBSURF")
        newMod.levels = 3

        #Enter in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        # if bpy.context.space_data.use_occlude_geometry == True :
        #     bpy.context.space_data.use_occlude_geometry = False
        #
        # bpy.context.object.show_x_ray = False

        if WM.add_mirror :
            newMirror = actObj.modifiers.new("Mirror","MIRROR")
            newMirror.use_axis[0] = True
            newMirror.use_mirror_merge = False

            if WM.ref_obj :
                newMirror.mirror_object = bpy.data.objects[ref_obj]
            
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror")
            bpy.ops.object.modifier_move_up(modifier="Mirror") 
            bpy.ops.object.modifier_move_up(modifier="Mirror") 
            bpy.ops.object.modifier_move_up(modifier="Mirror")  
        return {"FINISHED"}

# Cut Boolean      
class SPEEDSCULPT_OT_cut_boolean(bpy.types.Operator):
    bl_idname = "speedsculpt.cut_boolean"
    bl_label = "Cut Boolean"
    bl_description = "Cut Object with curve"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len([obj for obj in context.selected_objects if obj.type == 'MESH']) and len([obj for obj in context.selected_objects if obj.type == 'CURVE' and obj != context.active_object])
    
    def convert_curve(self, obj, context):
        WM = bpy.context.window_manager

        prefs = get_addon_preferences()
        self.auto_save = prefs.auto_save

        context.view_layer.objects.active = obj
        
        #save Temp
        if self.auto_save:
            save_tmp()
        
        obj.select_set(state=True)
        
        if not WM.direct_cut :
            bpy.ops.object.mode_set(mode='EDIT') 
            bpy.ops.curve.cyclic_toggle()
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            
            bpy.ops.object.mode_set(mode='OBJECT')  
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].offset = 0
            bpy.context.object.modifiers["Solidify"].thickness = 10
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
        else:
            bpy.context.object.data.extrude = 100
            bpy.ops.object.convert(target='MESH')

        obj.select_set(state=True)
        
    def execute(self, context):
        WM = bpy.context.window_manager
        
        act_obj = context.active_object
        # on recupere seulement l'objet curve
        curve = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        # on recupere tout les autres objets selectionnees
        obj_list = [obj for obj in context.selected_objects if obj.type == "MESH"]
        
        bpy.ops.object.select_all(action='DESELECT')
        
        # on convertit la curve en mesh grace a la fonction cree dans la class, d'ou le besoin de mettre self devant
        self.convert_curve(curve[0], context)



        for obj in obj_list:
            # mise en place du boolean DIFFERENCE sur l'obj  faisant partie de la selection
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            obj.modifiers.new("Boolean", 'BOOLEAN')
            obj.modifiers["Boolean"].object = curve[0]
            # obj.modifiers["Boolean"].object = curve_selected
            obj.modifiers["Boolean"].operation = 'DIFFERENCE'
            bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = 'Boolean')
            obj.select_set(state=False)



        # suppression de l obj curve
        for coll in curve[0].users_collection:
            coll.objects.unlink(curve[0])
        bpy.data.objects.remove(curve[0])

        # selection des objs de la selection
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            prefs = get_addon_preferences()
            add_remesh = prefs.add_remesh
            if add_remesh:
                bpy.ops.speedsculpt.simple_remesh()
                # bpy.ops.object.remesh()
                bpy.ops.object.apply_separate()

            # if update_detail_flood_fill:
            #Update Dyntopo
            CheckDyntopo()
            # if smooth_mesh:
            CheckSmoothMesh()

            if WM.direct_cut :
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')


        context.view_layer.objects.active = act_obj



        return {"FINISHED"}

# Cut Boolean Rebool 
class SPEEDSCULPT_OT_cut_boolean_rebool(bpy.types.Operator):
    bl_idname = "speedsculpt.cut_boolean_rebool"
    bl_label = "Cut Boolean Rebool"
    bl_description = "Slice object with curve"
    bl_options = {"REGISTER", "UNDO"}
 
    @classmethod
    def poll(cls, context):
        return len([obj for obj in context.selected_objects if obj.type == 'MESH']) and len([obj for obj in context.selected_objects if obj.type == 'CURVE' and obj != context.active_object])
        
    
    def convert_curve(self, obj, context):
        WM = bpy.context.window_manager
        prefs = get_addon_preferences()
        self.auto_save = prefs.auto_save
        context.view_layer.objects.active = obj
        
        #save Temp
        if self.auto_save:
            save_tmp()
        
        obj.select_set(state=True)
        
        if not WM.direct_cut :
            bpy.ops.object.mode_set(mode='EDIT') 
            bpy.ops.curve.cyclic_toggle()
            bpy.ops.object.mode_set(mode='OBJECT') 
            bpy.ops.object.convert(target='MESH')
            bpy.ops.object.mode_set(mode='EDIT')  
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.edge_face_add()
            
            bpy.ops.object.mode_set(mode='OBJECT')  
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].use_even_offset = True
            bpy.context.object.modifiers["Solidify"].offset = 0
            bpy.context.object.modifiers["Solidify"].thickness = 10
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Solidify")
        else:
            bpy.context.object.data.extrude = 30
            bpy.ops.object.convert(target='MESH')

        self.cut_obj = context.active_object
        obj.select_set(state=True)
        
    def execute(self, context):
        WM = bpy.context.window_manager
        RB_list = []  #a utiliser si tu veux faire une action sur les objs rebool
        act_obj = context.active_object
        # on recupere seulement l'objet curve
        curve = [obj for obj in context.selected_objects if obj.type == 'CURVE']
        # on recupere tout les autres objets selectionnees
        obj_list = [obj for obj in context.selected_objects if obj.type == "MESH"]
        
        bpy.ops.object.select_all(action='DESELECT')
        
        # on convertit la curve en mesh grace a la fonction cree dans la class, d'ou le besoin de mettre self devant
        self.convert_curve(curve[0], context)

        bpy.ops.object.select_all(action='DESELECT')

        for obj in obj_list:
            # mise en place du boolean DIFFERENCE sur l'obj  faisant partie de la selection
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            obj.modifiers.new("Boolean", 'BOOLEAN')
            obj.modifiers["Boolean"].object = curve[0]
            obj.modifiers["Boolean"].operation = 'DIFFERENCE'

            # creation de l'obj rebool
            bpy.ops.object.duplicate_move()
            RB_obj = context.active_object
            RB_list.append(RB_obj) #a utiliser si tu veux faire une action sur les objs rebool
            
            # changement d'operation en INTERSECT + application du boolean INTERSECT
            RB_obj.modifiers["Boolean"].operation = 'INTERSECT'
            bpy.ops.object.convert(target='MESH')
            # bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = 'Boolean')
            RB_obj.select_set(state=False)
            
            # on repasse sur l'obj faisant parti de la selection et on applique le boolean DIFFERENCE
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')
            # bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = 'Boolean')
            obj.select_set(state=False)

        # suppression de l obj curve
        for coll in curve[0].users_collection:
            coll.objects.unlink(curve[0])
        bpy.data.objects.remove(curve[0])



        for obj in obj_list + RB_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

        prefs = get_addon_preferences()
        add_remesh = prefs.add_remesh
        if add_remesh:
            bpy.ops.speedsculpt.simple_remesh()
            bpy.ops.object.apply_separate()

        for obj in obj_list + RB_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

            CheckDyntopo()
            CheckSmoothMesh()

            if WM.direct_cut :
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')

            obj.select_set(state=True)
            context.view_layer.objects.active = obj

        # selection des objs de la selection
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj



        return {"FINISHED"} 