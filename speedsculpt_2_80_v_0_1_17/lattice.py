import bpy
from mathutils import Vector
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

#Hide Lattice
def HideLattice(self, context):
    bl_description = "Hide the Lattice Modifier on selected objects"
    
    obj = context.active_object
    obj_list = [obj for obj in context.selected_objects]
    
    for obj in obj_list:
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        lattice = False
        for mod in obj.modifiers:                               
            if mod.type == "LATTICE":
                lattice = True
        if lattice:                                          
            if context.object.modifiers[mod.name].show_viewport == True :
                context.object.modifiers[mod.name].show_viewport = False
            else:
                context.object.modifiers[mod.name].show_viewport = True

# Add Mask
class SPEEDSCULPT_OT_lattice_add_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.lattice_add_mask"
    bl_label = "Lattice Add Mask"
    bl_description = "Add Mask to the Lattice"
    bl_options = {"REGISTER"}

    def execute(self, context):
        obj = context.active_object
        paint = context.tool_settings.image_paint
        
        context.object.modifiers["Lattice"].show_viewport = False
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.brush_select(sculpt_tool='MASK')
        return {"FINISHED"}
    
# Smooth Mask
class SPEEDSCULPT_OT_lattice_smooth_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.lattice_smooth_mask"
    bl_label = "Lattice Smooth Mask"
    bl_description = "Smooth The Mask"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        
        for vgroup in obj.vertex_groups:
            if vgroup.name == "SpeedLattice_Group":
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT') 
                bpy.context.object.data.use_paint_mask_vertex = True
                bpy.ops.object.vertex_group_set_active(group='SpeedLattice_Group')
                bpy.ops.object.vertex_group_select()
                bpy.ops.object.vertex_group_smooth(factor=1)
                bpy.ops.object.vertex_group_smooth(repeat=200)
                bpy.context.object.data.use_paint_mask_vertex = False
                bpy.ops.object.mode_set(mode = 'OBJECT')
        return {"FINISHED"}

# Valid the Lattice Mask            
class SPEEDSCULPT_OT_valid_lattice_mask(bpy.types.Operator):
    bl_idname = "speedsculpt.valid_lattice_mask"
    bl_label = "Valide Lattice Mask"
    bl_description = "Valid the Lattice mask"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        WM = bpy.context.window_manager
        obj = context.active_object

            
        #Remove Vgroups
        for vgroup in obj.vertex_groups:
            if vgroup.name == "SpeedLattice_Group":
                obj.vertex_groups.remove(vgroup)
        
        #Create selection
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.mesh.reveal()                           
        
        #Add Vgroup
        obj.vertex_groups.new(name="SpeedLattice_Group")

        bpy.ops.object.vertex_group_assign()
            
        bpy.ops.object.lattice_smooth_mask() 
            
        bpy.context.object.modifiers["Lattice"].show_viewport = True  

        for obj in context.selected_objects :
            for mod in obj.modifiers :
                mod.vertex_group = "SpeedLattice_Group"

        bpy.ops.object.mode_set(mode='OBJECT')    
            
        return {"FINISHED"}   
        
  

#Add Lattice        
class SPEEDSCULPT_OT_add_lattice(bpy.types.Operator):
    bl_idname = "speedsculpt.add_lattice"
    bl_label = "Add Lattice"
    bl_description = "Add a Lattice on selected objects"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        WM = context.window_manager
        obj = context.active_object
        
        lattice_u = bpy.context.window_manager.lattice_u  
        lattice_v = bpy.context.window_manager.lattice_v
        lattice_w = bpy.context.window_manager.lattice_w
        
        obj_list = [obj for obj in context.selected_objects]
        
        #Remove Vgroup             
        for vgroup in obj.vertex_groups:
            if vgroup.name == "SpeedLattice_Group":
                obj.vertex_groups.remove(vgroup)

        
        # Object 1 selection
        if len([obj for obj in context.selected_objects if obj.type == 'MESH' and not context.object.mode == 'SCULPT' and context.object.mode == "OBJECT"]) == 1:
            
            bpy.ops.object.duplicate_move()

            context.active_object.name= "BBox_Object"
            
            if WM.copy_orientation :
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        
        #EDIT           
        if context.object.mode == "EDIT":
                
            obj.vertex_groups.new(name="SpeedLattice_Group")
            
            for vgroup in obj.vertex_groups:
                if vgroup.name == "SpeedLattice_Group":
                    bpy.ops.object.vertex_group_assign()
               
            act_obj = context.active_object.name
            
            bpy.ops.mesh.duplicate_move()
            bpy.ops.mesh.separate(type="SELECTED")
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            obj_list1 = [obj for obj in context.selected_objects]
            for obj in obj_list1:
                act_obj = context.active_object
                act_obj.select_set(state=False)

            
            for obj in context.selected_objects :
                context.view_layer.objects.active = obj
                context.active_object.name= "BBox_Object"
                if WM.copy_orientation :
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            

            del(obj_list1[:]) 
                
        #SCULPT        
        if bpy.context.object.mode == "SCULPT":
            
            #convert mask to vertex group
            bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.reveal()
             
            #create vertex group and assign vertices
            obj.vertex_groups.new(name="SpeedLattice_Group")
            for vgroup in obj.vertex_groups:
                if vgroup.name == "SpeedLattice_Group":
                    bpy.ops.object.vertex_group_assign()



            #Smooth vertex group
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
            bpy.context.object.data.use_paint_mask_vertex = True
            bpy.ops.object.vertex_group_set_active(group='SpeedLattice_Group')
            bpy.ops.object.vertex_group_select()
            bpy.ops.object.vertex_group_smooth(factor=1)
            bpy.ops.object.vertex_group_smooth(repeat=100)
            bpy.context.object.data.use_paint_mask_vertex = False


            bpy.ops.object.mode_set(mode = 'EDIT')

            act_obj = context.active_object.name

            bpy.ops.mesh.duplicate_move()
            bpy.ops.mesh.separate(type="SELECTED")
            bpy.ops.object.mode_set(mode = 'OBJECT')

            obj_list1 = [obj for obj in bpy.context.selected_objects]
            for obj in obj_list1:
                act_obj = context.active_object
                act_obj.select_set(state=False)

            for obj in context.selected_objects :
                context.view_layer.objects.active = obj
                bpy.context.active_object.name= "BBox_Object"
                if WM.copy_orientation :
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


            del(obj_list1[:])
             

        #Check Mirror
        for obj in obj_list:
            if obj.modifiers:
                if "Mirror_primitive" in obj.modifiers:
                    context.object.modifiers["Mirror_primitive"].show_viewport = False




        # Si object > 1
        if len([obj for obj in context.selected_objects if obj.type == 'MESH' and not context.object.mode == 'SCULPT']) > 1:

            bpy.ops.object.duplicate_move()
            bpy.ops.object.join()
            context.active_object.name= "BBox_Object"
            if WM.copy_orientation :
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


        # 3
        selected = context.selected_objects
        for obj in selected:
            #ensure origin is centered on bounding box center
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
            #create a cube for the bounding box
            bpy.ops.object.add(radius=1, type='LATTICE', align='WORLD', enter_editmode=False, location=(0, 0, 0))

            #our new cube is now the active object, so we can keep track of it in a variable:
            bound_box = context.active_object

            #copy transforms
            bound_box.dimensions = obj.dimensions
            bound_box.location = obj.location
            bound_box.rotation_euler = obj.rotation_euler

        lattice_object = context.active_object
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            newMod = obj.modifiers.new(lattice_object.name, 'LATTICE')
            bpy.ops.object.modifier_move_up(modifier="Lattice")
            bpy.ops.object.modifier_move_up(modifier="Lattice")
            bpy.ops.object.modifier_move_up(modifier="Lattice")
            bpy.ops.object.modifier_move_up(modifier="Lattice")

            newMod.object = lattice_object

            # Assign Vertex Group
            for v in bpy.context.object.vertex_groups:
                newMod.vertex_group = "SpeedLattice_Group"

        #Affiche le mirror
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            if obj.modifiers:
                if "Mirror_primitive" in obj.modifiers:
                    context.object.modifiers["Mirror_primitive"].show_viewport = True


        #On deselectionne tout et on supprime le BBox_Object
        if "BBox_Object" in context.scene.objects:

            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects["BBox_Object"].select_set(state=True)
            bpy.ops.object.delete(use_global=False)

        #Make Lattice Active object
        bpy.ops.object.select_all(action='DESELECT')
        lattice_object.select_set(state=True)
        context.view_layer.objects.active = lattice_object

        bpy.ops.object.mode_set(mode = 'EDIT')


        del(obj_list[:])

        bpy.context.scene.cursor.location[0] = 0
        bpy.context.scene.cursor.location[1] = 0
        bpy.context.scene.cursor.location[2] = 0

        return {"FINISHED"}

#Remove Lattice
class SPEEDSCULPT_OT_remove_lattice_modifier(bpy.types.Operator):
    bl_idname = "speedsculpt.remove_lattice_modifier"
    bl_label = "Remove Lattice Modifier"
    bl_description = "Remove Lattice from selected objects"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        obj = context.active_object
        obj_list = [obj for obj in context.selected_objects]
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            
            lattice = False
            for mod in obj.modifiers:
                if mod.type == "LATTICE":
                    lattice = True
            if lattice:
                bpy.ops.object.modifier_remove(modifier=mod.name)
            
        del(obj_list[:])    
        return {"FINISHED"}

#Apply Lattice Modifier
class SPEEDSCULPT_OT_apply_lattice_modifier(bpy.types.Operator):
    bl_idname = "speedsculpt.apply_lattice_modifier"
    bl_label = "Apply Lattice Modifier"
    bl_description = "Apply Lattice on selected objects"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object
        obj_list = [obj for obj in context.selected_objects]
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            
            lattice = False
            for mod in obj.modifiers:
                if mod.type == "LATTICE":
                    lattice = True
            if lattice:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
                
            #Remove Vgroup
            for vgroup in obj.vertex_groups:
                if vgroup.name == "SpeedLattice_Group":
                    obj.vertex_groups.remove(vgroup)
        
        del(obj_list[:])    
        return {"FINISHED"}

#Delete Lattice
class SPEEDSCULPT_OT_delete_lattice(bpy.types.Operator):
    bl_idname = "speedsculpt.delete_lattice"
    bl_label = "Delete Lattice"
    bl_description = "Remove the Lattice"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.object.delete(use_global=False)
        return {"FINISHED"}

#Apply Lattice on all objects
class SPEEDSCULPT_OT_apply_lattice_objects(bpy.types.Operator):
    bl_idname = "speedsculpt.apply_lattice_objects"
    bl_label = "Apply Lattice Objects"
    bl_description = "Apply Lattice on all objects and Delete the Lattice"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        act_obj = context.active_object.name
        active_lattice = context.active_object
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                lattice = False
                for mod in obj.modifiers:
                    if mod.type == "LATTICE":
                        lattice = True
                        
                if lattice :
                    obj.select_set(state=True)
                    context.view_layer.objects.active = obj
                    if act_obj in bpy.context.object.modifiers:    
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier=act_obj)
                        
                        #Remove Vertex Group
                        for vgroup in obj.vertex_groups:
                            if vgroup.name == "SpeedLattice_Group":
                                obj.vertex_groups.remove(vgroup)
                        
        bpy.ops.object.select_all(action='DESELECT')

        active_lattice.select_set(state=True)
        context.view_layer.objects.active = active_lattice
        bpy.ops.object.delete(use_global=False)
 
        
        return {"FINISHED"}

#Remove Lattice on all objects
class SPEEDSCULPT_OT_remove_lattice_objects(bpy.types.Operator):
    bl_idname = "speedsculpt.remove_lattice_objects"
    bl_label = "Remove Lattice Objects"
    bl_description = "Remove Lattice on all objects and Delete the Lattice"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        act_obj = context.active_object.name
        active_lattice = context.active_object
        
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:                
            if obj.type == 'MESH':                  
                lattice = False
                for mod in obj.modifiers:
                    if mod.type == "LATTICE":
                        lattice = True
                if lattice :
                    obj.select_set(state=True)
                    context.view_layer.objects.active = obj
                    if act_obj in bpy.context.object.modifiers: 
                        bpy.ops.object.modifier_remove(modifier=act_obj)  
                        
                        for vgroup in obj.vertex_groups:
                            if vgroup.name == "SpeedLattice_Group":
                                obj.vertex_groups.remove(vgroup)
                                
                                
        bpy.ops.object.select_all(action='DESELECT')

        active_lattice.select_set(state=True)
        context.view_layer.objects.active = active_lattice
        bpy.ops.object.delete(use_global=False)
 
        
        return {"FINISHED"}                

#Connect Object To Lattice
class SPEEDSCULPT_OT_connect_lattice(bpy.types.Operator):
    bl_idname = "speedsculpt.connect_lattice"
    bl_label = "Connect Object To Lattice"
    bl_description = "Connect Objects to selected Lattice"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        actObj = context.active_object        
        for selObj in context.selected_objects:
            if selObj != context.active_object and(selObj.type == "MESH"):
                if not "Lattice" in selObj.modifiers:
                    newMod = selObj.modifiers.new(actObj.name, 'LATTICE')
                    newMod.object = actObj

                context.view_layer.objects.active = selObj
                # bpy.context.scene.objects.active = selObj
                bpy.ops.object.select_all(action='DESELECT')
                
            selObj.select_set(state=True)
            for vgroup in selObj.vertex_groups:
                if vgroup.name == "SpeedLattice_Group":
                    for mod in bpy.context.active_object.modifiers:
                        mod.vertex_group = "SpeedLattice_Group"
                      
                        
        return {"FINISHED"}
        
        
        
#Interpolation
def LatticeInterpolation(self, context):
    WM = bpy.context.window_manager
    
    context.object.data.interpolation_type_u = WM.lattice_interp
    context.object.data.interpolation_type_v = WM.lattice_interp
    context.object.data.interpolation_type_w = WM.lattice_interp
    

                