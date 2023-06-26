import bpy
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

from .functions import *
from .operators import *
from .lattice import *
from .curves import *
from bpy.types import Curve, SurfaceCurve, TextCurve

import os
from os.path import isfile, join
from os import remove, listdir
# from .preview_collection import *

##------------------------------------------------------  
#
# UI
#
##------------------------------------------------------ 

# -----------------------------------------------------------------------------
#    Help
# ----------------------------------------------------------------------------- 
class SC_HELP_MT_shading(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_shading"
    bl_label = "Help Shading"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Random Colors")
        layout.label(text="> Create Materials with Random Colors on selection")
        layout.separator()
        layout.label(text="Solo")
        layout.label(text="> Make non selected objects transparent")
        layout.separator()
        layout.label(text="OpenGL")
        layout.label(text="> Change the OpenGL Lighting for better results")


class SC_HELP_MT_primitives(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_primitives"
    bl_label = "Help Primitives"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create primitives for booleans")
        layout.label(text="You can combine Mesh and Metaballs")
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Add And combine primitives").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/primitives.gif"
        
        
class SC_HELP_MT_skin(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_skin"
    bl_label = "Help Skin"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create objects with skin Modifier")
        layout.label(text="Create Fast Character with Skin, Origin + Mirror On")
        layout.separator()  
        layout.label(text="Examples :")
        layout.operator("wm.url_open", text="Add Skin and combine").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/skin_simple.gif"
        layout.operator("wm.url_open", text="Create a character with Skin").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/skin_character.gif"

class SC_HELP_MT_envelope(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_envelope"
    bl_label = "Help Envelope"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create Armature to make your character")
        layout.label(text="You can use the origin option from primitives to place it at the center of the grid")
        layout.separator()
        layout.label(text="You can select and symmetrize bones")
        layout.label(text="And use the X-Axis Mirror to tweak both sides")
        layout.separator()
        layout.label(text="Change the Dyntopo Value with Smooth Options/Update and Click on the Convert button")
        
                     
class SC_HELP_MT_curves(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_curves"
    bl_label = "Help Curves"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Need Blender 2.79", icon='ERROR')
        layout.separator()  
        layout.label(text="Create Curve and use BBox to make surface")
        layout.label(text="Create Curve and convert it to skin Modifier")
        layout.label(text="Slice Objects with curves, make holes etc")
        layout.separator()  
        layout.label(text="Examples :")
        layout.operator("wm.url_open", text="Convert Curve to skin").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/convert_curve.gif" 
        layout.operator("wm.url_open", text="Slice/Cut/Rebool objects with curves").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/curves_slice.gif" 
        
class SC_HELP_MT_gpLine1(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_gpLine1"
    bl_label = "How to Use Gpline"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create surfaces with Bsurface")
        layout.separator() 
        layout.label(text="1 - Draw Grease Pencil Lines")
        layout.label(text="2 - Press Add Bsurface to create surface")
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Add surface with Bsurface").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/gp_lines.gif" 

class SC_HELP_MT_gpLine2(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_gpLine2"
    bl_label = "How to Use Gpline"

    def draw(self, context):
        layout = self.layout
        layout.label(text="1 - Press D and Draw Grease Pencil Lines")
        layout.label(text="2 - Press Space to exit Grease Pencil")
        layout.label(text="3 - Press Add Bsurface to create surface")
        
class SC_HELP_MT_lattice(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_lattice"
    bl_label = "Help Lattice"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Create Lattice and deform objects")
        layout.label(text="Create Lattice from mask in Sculpt mode and deform your mesh")
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Add Lattice and deform objects").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/lattices.gif" 
               
        
class SC_HELP_MT_symmetrize(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_symmetrize"
    bl_label = "Help Symmetrize"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Symmetrize your mesh in object, Sculpt and Dyntopo")
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Symmetrize mesh in Sculpt/Object/Dyntopo").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/symmetrize.gif" 

class SC_HELP_MT_remesh(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_remesh"
    bl_label = "Help Remesh"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Remesh - Add Remesh Modifier to make 3D printed objetcs")
        layout.label(text="Decimate - Simplify your mesh or use mask to simplify a part of it")
        layout.separator()  
        layout.label(text="Examples :")
        layout.operator("wm.url_open", text="Remesh object").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/remesh.gif" 
        layout.operator("wm.url_open", text="Decimate mesh with mask").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/decimate.gif" 

class SC_HELP_MT_extractmask(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_extractmask"
    bl_label = "Help Extract Mask"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Extract new mesh from Sculpt mask")
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Extract mesh with mask").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/extract_mask.gif" 

class SC_HELP_MT_quickpose(bpy.types.Menu):
    bl_idname = "SC_HELP_MT_quickpose"
    bl_label = "Help Quick Pose"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Make a quick pose of your model")
        layout.label(text="You can use mask to pose only a part")
        layout.separator() 
        layout.label(text="Direct Pose :")
        layout.label(text="Click on Create Bones, place the vertice, extrude it")
        layout.label(text="Click on the Pose button and make your pose")
        layout.separator() 
        layout.label(text="Mask Pose :")
        layout.label(text="Click on Use Mask and Add Mask")
        layout.label(text="Paint your mask")
        layout.label(text="Click on Create Bones, place the vertice, extrude it")
        layout.label(text="Click on the Pose button and make your pose")
        layout.separator() 
        layout.label(text="You can Edit and smooth your mask")
        layout.separator() 
        layout.label(text="The creation of the Armature don't work in Local View", icon='ERROR')
        
        layout.separator()  
        layout.label(text="Example :")
        layout.operator("wm.url_open", text="Quick Pose with mask").url = "http://www.pitiwazou.com/wp-content/uploads/2016/08/quick_pose_mask.gif"

# -----------------------------------------------------------------------------
#    Options
# -----------------------------------------------------------------------------
def Options(self, context):
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    prefs = get_addon_preferences()
    add_remesh = prefs.add_remesh

    row = layout.row(align=True)
    row.prop(prefs, "smooth_mesh", text="Smooth")
    row.prop(prefs, "update_detail_flood_fill", text="Update")
    row = layout.row(align=True)
    row.prop(prefs, "flat_shading", text="Flat")
    row.prop(prefs, "fill_holes_dyntopo", text="Fill Holes")
    row = layout.row(align=True)
    row.prop(prefs, "add_remesh", text="Remesh")
    if add_remesh:
        # row = layout.row(align=True)
        row.prop(prefs, "remesh_value", text="Value")

    if context.object is not None:
        remesh = False
        for mod in bpy.context.active_object.modifiers:
            if mod.type == "REMESH":
                remesh = True
        if remesh:
            layout.prop(WM, "apply_remesh", text="Apply Remesh")
                 
# -----------------------------------------------------------------------------
#    Add Primitives
# ----------------------------------------------------------------------------- 
def AddPrimitives(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    obj = context.active_object
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help
    
        
    # Add Primitives
    
    row = layout.row(align=True)
    row.prop(WM, "show_primitives", text="Add Primitives", icon='TRIA_UP' if WM.show_primitives else 'TRIA_DOWN')
    if self.show_help :    
        row.menu("SC_HELP_MT_primitives",text="", icon='TRIA_RIGHT')
    if WM.show_primitives:
        box = layout.box()
        split = box.split()
        box = split.column(align=True) 
        row = box.row(align=True)
        row.prop(WM, "origin",text="Origin")
        if context.object is not None :
            if obj.type == 'MESH':
                row.prop(WM, "primitives_parenting", text ="Parent")
        
        row.prop(WM, "add_mirror", text ="Mirror")
        
        if WM.add_mirror :
            box.label(text="Mirror Object:")
            box.prop_search(WM, "ref_obj", bpy.data, 'objects', text="")
        
        row = box.row(align=True)
        row.scale_x = 2
        row.operator("speedsculpt.add_custom_primitives", text = "", icon = 'MATSPHERE').primitive = "sphere"
        row.operator("speedsculpt.add_custom_primitives",text="", icon ='MESH_CYLINDER').primitive = "cylinder"
        row.operator("speedsculpt.add_custom_primitives",text="", icon ='MESH_CUBE').primitive = "cube"
        row.operator("speedsculpt.add_custom_primitives",text="", icon ='MESH_CONE').primitive = "cone"
        row.operator("speedsculpt.add_custom_primitives",text="", icon ='MESH_TORUS').primitive = "torus"
        
        # Metaballs
        row = box.row(align=True)
        row.scale_x = 2
        row.operator("speedsculpt.add_custom_metaballs", text = "", icon = 'META_BALL').metaballs = "ball"
        row.operator("speedsculpt.add_custom_metaballs",text="", icon ='META_CAPSULE').metaballs = "capsule"
        row.operator("speedsculpt.add_custom_metaballs",text="", icon ='META_CUBE').metaballs = "cube"
        row.operator("speedsculpt.add_custom_metaballs",text="", icon ='META_ELLIPSOID').metaballs = "hellipsoid"
        row.operator("speedsculpt.add_custom_metaballs",text="", icon ='META_PLANE').metaballs = "plane"
           
        if len([obj for obj in context.selected_objects if obj.type == 'META']) >= 1:
            split = box.split()
            col = split.column(align=True)
            col.label(text="Metaballs Options:")
            row = col.row(align=True)
            row.prop(bpy.context.object.data, "resolution", text="Resolution")
            row = col.row(align=True)
            row.prop(bpy.context.object.data, "threshold", text="Threshold")
            row = col.row(align=True)
            row.prop(WM, "metaballs_pos_neg", expand=True)
            
            if len([obj for obj in context.selected_objects if obj.type == 'META' and obj.mode == "EDIT"]) == 1:
                col.prop(bpy.context.object.data.elements.active, "stiffness", text="Stiffness")
                col.prop(bpy.context.object.data.elements.active, "hide", text="Hide")
        
        # Envelope
        box = layout.box()
        split = box.split()
        box = split.column(align=True)

        row.scale_y = 1.2
        row = box.row(align=True)
        row.operator("speedsculpt.create_envelope",text="Add Envelope", icon ='OUTLINER_OB_ARMATURE')
        if self.show_help :
           row.menu("SC_HELP_MT_envelope",text="", icon='TRIA_RIGHT')

        if context.object is not None and obj.type == 'ARMATURE' and obj.name.startswith("Envelope"):
            # if bpy.context.object.mode == 'OBJECT':
            row = box.row(align=True)
            # row.operator("object.ssculpt_convert_armature",text="Convert", icon ='OUTLINER_OB_META')
            if bpy.context.object.mode == "EDIT":
                row = box.row(align=True)
                row.operator("speedsculpt.enveloppe_symmetrize",text="Symmetrize", icon ='UV_EDGESEL')
                arm = context.active_object.data
                row = box.row(align=True)
                row.prop(arm, "use_mirror_x")

            row = box.row(align=True)
            row.scale_y = 4
            row.operator("speedsculpt.convert_armature", text="Convert Armature", icon='OUTLINER_OB_META')


        # Skin
        box = layout.box()
        split = box.split()
        box = split.column(align=True) 
        
        row.scale_y = 1.2
        row = box.row(align=True)
        row.operator("speedsculpt.add_skin",text="Add Skin", icon ='MOD_SKIN')
        if self.show_help :
            row.menu("SC_HELP_MT_skin",text="", icon='TRIA_RIGHT')
        
        if context.object is not None :
            mirror = False
            skin = False  
            bevel = False  
            for mod in bpy.context.active_object.modifiers:
                if mod.type == "SKIN" and bpy.context.object.mode == "EDIT":
                    skin = True
                if mod.type == "MIRROR":
                    mirror = True
                if mod.type == "BEVEL":
                    bevel = True  
                         
            if skin:    
                box.operator("object.skin_root_mark", text='Mark Root', icon='PIVOT_CURSOR')
                row = box.row(align=True) 
                row.operator("object.skin_loose_mark_clear", text='Mark Loose').action='MARK'
                row.operator("object.skin_loose_mark_clear", text='Clear Loose').action='CLEAR'
                row = box.row(align=True) 
                row.operator("object.skin_radii_equalize", text="Equalize Radii")
            
                split = box.split()
                col = split.column(align=True)
                #Mirror 
                if mirror:
                    row = col.row(align=True)
                    if "Mirror_Skin" in obj.modifiers:
                        row = col.row(align=True)
                        row.prop(bpy.context.active_object.modifiers["Mirror_Skin"], "show_viewport", text="Hide Mirror") 
                        row.prop(WM, "use_clipping", text = "", icon='UV_EDGESEL')   
                        row.operator("speedsculpt.remove_mirror", text = "", icon='X')
                        
                        
                    elif "Mirror" in obj.modifiers:
                        row = col.row(align=True)
                        row.prop(bpy.context.active_object.modifiers["Mirror"], "show_viewport", text="Hide Mirror") 
                        row.prop(WM, "use_clipping", text = "", icon='UV_EDGESEL') 
                        row.operator("speedsculpt.remove_mirror", text = "", icon='X')
                        
                
                #Bevel
                if bevel:
                    row = col.row(align=True)
                    row.prop(context.active_object.modifiers["Bevel"], "width", text="Bevel Width")
                    row.prop(context.active_object.modifiers["Bevel"], "show_viewport", text="")
                    row.operator("speedsculpt.remove_bevel", text="", icon='X')
                    row = col.row(align=True)
                    row.prop(context.active_object.modifiers["Bevel"], "angle_limit", text="Bevel Angle")
                    
                
                
                #Smooth Skin
                if "Smooth_skin" in obj.modifiers:
                    row = col.row(align=True)
                    row.prop(context.active_object.modifiers["Smooth_skin"], "levels", text="Smooth Level")
                    row.prop(context.active_object.modifiers["Smooth_skin"], "show_viewport", text="")
                    row.operator("speedsculpt.remove_smooth_skin", text="", icon='X')
                
                split = box.split()
                col = split.column(align=True)       
                if not bevel: 
                    row = col.row(align=True)
                    row.operator("speedsculpt.add_gp_bevel", text="Add Bevel", icon='MOD_BEVEL')
                    
                if not mirror: 
                    row = col.row(align=True)
                    row.operator("speedsculpt.add_mirror", text="Add Mirror", icon='MOD_MIRROR')
                
                if not "Smooth_skin" in obj.modifiers:
                    row = col.row(align=True)
                    row.operator("speedsculpt.add_smooth_skin", text="Add Smooth", icon='MOD_SUBSURF')
                


        box = layout.box()
        split = box.split()
        col = split.column(align=True)

        row = col.row(align=True)
        row.operator("speedsculpt.create_lathe", text="Lathe", icon='MOD_MULTIRES')
        row.operator("speedsculpt.create_curve", text="Curve", icon='LINE_DATA')

        
        if self.show_help : 
            row.menu("SC_HELP_MT_curves",text="", icon='TRIA_RIGHT')

        if context.object is not None:
            screw = False
            for mod in bpy.context.active_object.modifiers:
                if mod.type == "SCREW":
                    screw = True


            if not screw :
                if len(context.selected_objects) == 1:
                    obj1 = context.active_object
                    if obj1.type == 'CURVE' :
                        row = col.row(align=True)
                        row.prop(context.object.data,"resolution_u", text="Resolution")
                        row = col.row(align=True)
                        row.operator("speedsculpt.convert_curve_to_skin", text="Convert To Skin", icon='MOD_SKIN')


                if len(context.selected_objects) >= 2:
                    obj1 = context.active_object
                    obj2 = context.selected_objects[1] if bpy.context.selected_objects[0] == obj1 else bpy.context.selected_objects[0]

                    if obj1.type == 'MESH' and obj2.type == 'CURVE':
                        # row = col.row(align=True)
                        # row.prop(WM, "direct_cut",text="Slice")
                        row = col.row(align=True)
                        row.operator("speedsculpt.cut_boolean", text="Cut", icon='MOD_BOOLEAN')
                        row.operator("speedsculpt.cut_boolean_rebool", text="Rebool")



                # Bbox
                if len(context.selected_objects) == 1:
                    obj1 = context.active_object
                    if obj1.type == 'CURVE' :

                        box = layout.box()
                        split = box.split()
                        col = split.column(align=True)
                        row = col.row(align=True)


                        if context.object.data.bevel_depth == 0 :
                            row = col.row(align=True)
                            row.prop(WM, "bbox_bevel", text="Bevel")
                            row = col.row(align=True)
                            row.prop(WM, "bbox_offset", text="Offset")
                            row = col.row(align=True)
                            row.prop(WM, "bbox_depth", text="Depth")

                        elif context.object.data.bevel_depth > 0 :
                            row = col.row(align=True)
                            row.prop(context.object.data,"bevel_depth", text="Bevel")
                            row = col.row(align=True)
                            row.prop(context.object.data,"offset", text="Offset")
                            row = col.row(align=True)
                            row.prop(context.object.data,"extrude", text="Depth")

                        else:
                            pass
                        row = col.row()
                        row.prop(WM, "bbox_convert", text="Stay in curve Mode")
                        row = col.row()
                        row.prop(WM, "smooth_result", text="Smooth the mesh")
                        row = col.row()
                        row.operator("speedsculpt.bbox", text="BBox", icon='MOD_DYNAMICPAINT')

            else :
                row = col.row(align=True)
                row.scale_x=0.5
                row.prop(context.active_object.modifiers["Screw"], "axis", text="Axis")
                row = col.row(align=True)
                row.prop(context.active_object.modifiers["Screw"], "steps", text="Steps")
                row = col.row(align=True)
                row.prop(context.active_object.modifiers["Screw"], "use_normal_flip", text="Flip Normals")


                if len([obj for obj in context.selected_objects if context.object is not None if obj.type == 'CURVE']) == 1:
                    row = col.row(align=True)
                    row.operator("speedsculpt.create_empty", text="Add empty", icon='OUTLINER_OB_EMPTY')
                
        # # GP Lines
        # if context.object is not None and context.object.mode == "EDIT":
        #     if "Solidify" in obj.modifiers:
        #         solidify = False
        #         mirror = False
        #         shrinkwrap = False
        #         bevel = False
        #         for mod in context.active_object.modifiers:
        #             if mod.type == "SOLIDIFY":
        #                 solidify = True
        #             if mod.type == "MIRROR":
        #                 mirror = True
        #             if mod.type == "SHRINKWRAP":
        #                 shrinkwrap = True
        #             if mod.type == "BEVEL":
        #                 bevel = True
        #
        #         box = layout.box()
        #         split = box.split()
        #         col = split.column(align=True)
        #         row = col.row(align=True)
        #         row.scale_y = 1.5
        #         row.operator("gpencil.surfsk_add_surface", text="Add BSurface", icon='MOD_DYNAMICPAINT')
        #         if self.show_help :
        #             row.menu("SC_HELP_MT_gpLine2", text="", icon='TRIA_RIGHT')
        #
        #
        #         col.separator()
        #
        #         #Solidify
        #         if solidify:
        #             row = col.row(align=True)
        #             row.scale_y = 1
        #             row = col.row(align=True)
        #             row.prop(context.active_object.modifiers["Solidify"], "thickness", text="Thickness")
        #             row.prop(context.active_object.modifiers["Solidify"], "show_viewport", text="")
        #             row = col.row(align=True)
        #             col.prop(context.active_object.modifiers["Solidify"], "offset", text="Offset")
        #
        #         if shrinkwrap:
        #             row = col.row(align=True)
        #             row.prop(context.active_object.modifiers["Shrinkwrap"], "show_viewport", text="Hide Shrinkwrap")
        #             row.operator("speedsculpt.remove_shrinkwrap", text = "", icon='X')
        #
        #         if mirror:
        #             row = col.row(align=True)
        #             if "Mirror_Skin" in obj.modifiers:
        #                 row = col.row(align=True)
        #                 row.prop(context.active_object.modifiers["Mirror_Skin"], "show_viewport", text="Hide Mirror")
        #                 row.prop(WM, "use_clipping", text = "", icon='UV_EDGESEL')
        #                 row.operator("speedsculpt.remove_mirror", text = "", icon='X')
        #
        #             elif "Mirror" in obj.modifiers:
        #                 row = col.row(align=True)
        #                 row.prop(context.active_object.modifiers["Mirror"], "show_viewport", text="Hide Mirror")
        #                 row.prop(WM, "use_clipping", text = "", icon='UV_EDGESEL')
        #                 row.operator("speedsculpt.remove_mirror", text = "", icon='X')
        #
        #
        #         if bevel:
        #             row = col.row(align=True)
        #             row.prop(context.active_object.modifiers["Bevel"], "width", text="Bevel Width")
        #             row.prop(context.active_object.modifiers["Bevel"], "show_viewport", text="")
        #             row.operator("speedsculpt.remove_bevel", text="", icon='X')
        #
        #
        #         #Mirror
        #         if not mirror:
        #             row = col.row(align=True)
        #             row.operator("speedsculpt.add_mirror", text="Add Mirror", icon='MOD_MIRROR')
        #
        #         #Bevel
        #         if not bevel:
        #             row = col.row(align=True)
        #             row.operator("speedsculpt.add_gp_bevel", text="Add Bevel", icon='MOD_BEVEL')
        #
        # else:
        #     box = layout.box()
        #     split = box.split()
        #     col = split.column(align=True)
        #     if "mesh_bsurfaces" in bpy.context.preferences.addons:
        #         row = col.row(align=True)
        #         row.operator("speedsculpt.create_gp_line", text="Create GP Lines", icon='MOD_DYNAMICPAINT')
        #         if self.show_help :
        #             row.menu("SC_HELP_MT_gpLine1", text="", icon='TRIA_RIGHT')
        #     else :
        #         col.label(text="    Activate Bsurface", icon='ERROR')
        #         row = col.row(align=True)
        #         col.operator("screen.userpref_show",text="Open User Prefs", icon='PREFERENCES')
                     
# -----------------------------------------------------------------------------
#    Lattice
# -----------------------------------------------------------------------------                
def Lattice(self, context):
    """ Sub panel for the adding assets """
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help
    WM = context.window_manager
    obj = context.active_object

    layout = self.layout
    if len([obj for obj in context.selected_objects if context.object is not None if obj.type in ['MESH', 'LATTICE'] ]) >= 1:
        row = layout.row(align=True)
        row.prop(WM, "show_lattice", text="Lattice", icon='TRIA_UP' if WM.show_lattice else 'TRIA_DOWN')
        if self.show_help : 
            row.menu("SC_HELP_MT_lattice",text="", icon='TRIA_RIGHT')
        if WM.show_lattice:
            if context.object is not None and obj.type == 'MESH' :
                lattice = False
                for mod in obj.modifiers:
                    if mod.type == "LATTICE":
                        lattice = True
                if not lattice:
                    box = layout.box()
                    split = box.split()
                    col = split.column(align=True)
                    row = col.row(align=True)
                    row.prop(WM, "copy_orientation", text="Don't Copy Orientation")
                    row = col.row(align=True)
                    row.prop(WM, "lattice_u", text="U:")
                    row = col.row(align=True)
                    row.prop(WM, "lattice_v", text="V:")
                    row = col.row(align=True)
                    row.prop(WM, "lattice_w", text="W:")
                    if context.object.mode == "SCULPT":
                        row = col.row(align=True)
                        row.scale_y = 1.2
                        row.operator("speedsculpt.add_lattice", text="Add Lattice From Mask", icon='BRUSH_MASK')
                    else :
                        row = col.row(align=True)
                        row.scale_y = 1.2
                        row.operator("speedsculpt.add_lattice", icon='OUTLINER_OB_LATTICE')
                            
                else :
                    box = layout.box()
                    split = box.split()
                    box = split.column(align=True)
                    row = box.row(align=True)
                    row.operator("speedsculpt.apply_lattice_modifier", text="Apply Lattice", icon='FILE_TICK')
                    row.prop(WM, "hide_lattice", text="", icon='RESTRICT_VIEW_OFF' if WM.hide_lattice else 'RESTRICT_VIEW_ON')
                    row.operator("speedsculpt.remove_lattice_modifier", text="", icon='X')
                    
                    if context.object.mode == "OBJECT":
                        if context.object.vertex_groups:
                            for vgroup in obj.vertex_groups:
                                if vgroup.name.startswith("S"):
                                    if len(context.selected_objects) == 1:
                                        row = box.row(align=True)
                                        row.operator("speedsculpt.lattice_add_mask", text="Edit Mask", icon='BRUSH_MASK')
                                        row = box.row(align=True)
                                        row.operator("speedsculpt.lattice_smooth_mask", text="Smooth Mask", icon='BRUSH_MASK')
                    
                        else :
                            if len(context.selected_objects) == 1:
                                row = box.row(align=True)
                                row.operator("speedsculpt.lattice_add_mask", text="Add Mask", icon='BRUSH_MASK')
                                
                    if context.object.mode == "SCULPT":
                        
                            row = box.row(align=True)
                            row.operator("speedsculpt.valid_lattice_mask", text="Valid Mask", icon='FILE_TICK')
                        
                        
            elif len([obj for obj in context.selected_objects]) >= 2:
                box = layout.box()
                split = box.split()
                box = split.column(align=True)
                box.operator("speedsculpt.connect_lattice", text="Connect To Lattice", icon='OUTLINER_OB_LATTICE')
               

            elif len([obj for obj in context.selected_objects if obj.type == 'LATTICE' ]) == 1:
                box = layout.box()
                split = box.split()
                col = split.column(align=True)
                row = col.row(align=True)
                row.operator("speedsculpt.apply_lattice_objects", text="Apply Lattice", icon='FILE_TICK')
                row.operator("speedsculpt.remove_lattice_objects", text="", icon='X')
                row = col.row(align=True)
                row.prop(context.object.data, "points_u")
                row = col.row(align=True)
                row.prop(context.object.data, "points_v")
                row = col.row(align=True)
                row.prop(context.object.data, "points_w")  
                
                
                row = col.row(align=True)
                row.prop(WM, "lattice_interp", text="")
                
                
# -----------------------------------------------------------------------------
#    Symmetrize
# -----------------------------------------------------------------------------
def Symmetrize(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help
                    
    # Symmetrize
    if len([obj for obj in context.selected_objects if context.object is not None if obj.type == 'MESH' if context.object.mode in ["OBJECT","SCULPT"] ]) >= 1:
        
        row = layout.row(align=True)
        row.prop(WM, "show_symmetrize", text="Symmetrize", icon='TRIA_UP' if WM.show_symmetrize else 'TRIA_DOWN')
        if self.show_help : 
            row.menu("SC_HELP_MT_symmetrize",text="", icon='TRIA_RIGHT')
        if WM.show_symmetrize:
            box = layout.box()
            split = box.split()
            box = split.column(align=True)
            row = box.row(align=True)
            row.operator("speedsculpt.symmetrize", text = "+X to -X").symmetrize_axis = "positive_x"
            row.operator("speedsculpt.symmetrize", text = "-X to +X").symmetrize_axis = "negative_x"
            row = box.row(align=True)
            row.operator("speedsculpt.symmetrize", text = "+Y to -Y").symmetrize_axis = "positive_y"
            row.operator("speedsculpt.symmetrize", text = "-Y to +Y").symmetrize_axis = "negative_y"
            row = box.row(align=True)
            row.operator("speedsculpt.symmetrize", text = "+Z to -Z").symmetrize_axis = "positive_z"
            row.operator("speedsculpt.symmetrize", text = "-Z to +Z").symmetrize_axis = "negative_z"
# -----------------------------------------------------------------------------
#    Remesh/Decimate
# ----------------------------------------------------------------------------- 
def Remesh(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    obj = context.active_object
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help
    remesh_value = prefs.remesh_value
    
    # Remesh
    if len([obj for obj in context.selected_objects if context.object is not None if obj.type == 'MESH' if context.object.mode in ["OBJECT","SCULPT"]]) >= 1:
        row = layout.row(align=True)
        row.prop(WM, "show_remesh", text="Remesh/Decimate", icon='TRIA_UP' if WM.show_remesh else 'TRIA_DOWN')
        if self.show_help : 
            row.menu("SC_HELP_MT_remesh",text="", icon='TRIA_RIGHT')
        if WM.show_remesh:
            
            # Remesh
            remesh = False
            smooth = False
            for mod in context.active_object.modifiers:
                if mod.type == "REMESH":
                    remesh = True
                if mod.type == "SMOOTH":
                    smooth = True  
            if not remesh :
                if context.object.mode == "OBJECT":
                    box = layout.box()
                    split = box.split()
                    box = split.column(align=True)
                    box.operator("speedsculpt.remesh", text="Remesh", icon='MOD_REMESH')
                      
            if remesh and smooth :
                box = layout.box()
                split = box.split()
                col = split.column(align=True)
                row = col.row(align=True)
                row.operator("speedsculpt.apply_remesh_smooth", text="Apply Remesh", icon='FILE_TICK')
                row.prop(WM, "hide_remesh_smooth", text="", icon='RESTRICT_VIEW_OFF' if WM.hide_remesh_smooth else 'RESTRICT_VIEW_ON')
                row.operator("speedsculpt.remove_remesh_smooth", text="", icon='X')
   
            if remesh:  
                row = col.row(align=True)
                prefs = get_addon_preferences()
                row.prop(prefs, "remesh_value", text="Remesh Depth:")
                # row.prop(WM, "remesh_octree_depth", text="Remesh Depth:")
                # row.prop(context.active_object.modifiers["R_Remesh"], "octree_depth", text="Remesh Depth")
              
            if smooth:
                row = col.row(align=True)
                row.prop(WM, "remesh_smooth_repeat", text="Smooth Repeat:")
                # row.prop(context.active_object.modifiers["R_Smooth"], "iterations", text="Smooth Repeat")
                
        
            # Decimate
            decimate = False
            for mod in context.active_object.modifiers:
                if mod.type == "DECIMATE":
                    decimate = True
                    
            if not decimate :
                if context.object.mode == "SCULPT":
                    box = layout.box()
                    split = box.split()
                    box = split.column(align=True)
                    box.operator("speedsculpt.decimate_mask", text="Mask Decimate", icon='MOD_DECIM')
            
                elif context.object.mode == "OBJECT":
                    box = layout.box()
                    split = box.split()
                    box = split.column(align=True)
                    box.operator("speedsculpt.decimate", text="Decimate", icon='MOD_DECIM')
                       
            if decimate:
                box = layout.box()
                split = box.split()
                col = split.column(align=True)
                row = col.row(align=True)
                row.operator("speedsculpt.apply_decimate", text="Apply Decimate", icon='FILE_TICK')
                row.prop(WM, "hide_decimate", text="",
                         icon='RESTRICT_VIEW_OFF' if WM.hide_decimate else 'RESTRICT_VIEW_ON')
                row.operator("speedsculpt.remove_decimate", text="", icon='X')
                
                row = col.row(align=True)

                row.prop(WM, "decimate_ratio", text="Ratio:")
                # row.prop(context.active_object.modifiers["Decimate"], "ratio", text="Ratio")

                if len([obj for obj in context.selected_objects if obj.type == 'MESH' if context.object.mode == "OBJECT"]) == 1:
                # if bpy.context.object.mode == "OBJECT":
                    row = col.row(align=True)
                    if not context.object.modifiers["Decimate"].vertex_group :
                        row.operator("speedsculpt.add_mask", text="Add Mask", icon='BRUSH_MASK')
                        
                    else :
                        row.operator("speedsculpt.edit_decimate_mask", text="Edit Mask", icon='BRUSH_MASK')
                        row.prop(bpy.context.active_object.modifiers["Decimate"],"invert_vertex_group", text="", icon='ARROW_LEFTRIGHT') 
                        row.operator("speedsculpt.remove_mask", text="", icon='X')
                    
                elif context.object.mode == "SCULPT":
                    row = col.row(align=True)    
                    row.operator("speedsculpt.valid_decimate_mask", text="Valid Mask", icon='FILE_TICK')


# -----------------------------------------------------------------------------
#    Extract Mask
# -----------------------------------------------------------------------------
def ExtractMask(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    obj = bpy.context.active_object
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help

    # Extract Mask
    if len([obj for obj in context.selected_objects if context.object is not None if obj.type == 'MESH' if bpy.context.object.mode in ["OBJECT", "SCULPT"]]) == 1:
        
        row = layout.row(align=True)
        row.prop(WM, "show_extract", text="Mask Operations", icon='TRIA_UP' if WM.show_extract else 'TRIA_DOWN')
        if self.show_help : 
            row.menu("SC_HELP_MT_extractmask",text="", icon='TRIA_RIGHT')
        if WM.show_extract:
            if bpy.context.object.mode == "SCULPT":
                box = layout.box()
                box.prop(WM, "extract_cut_delete", expand=True)
                
                if WM.extract_cut_delete == 'extract':
                    split = box.split()
                    col = split.column(align=True)  
                    col.prop(WM, "add_solidify", text="Add Solidify")
                    if WM.add_solidify :
                        split = box.split()
                        col = split.column(align=True)
                        col.prop(WM, "solidify_thickness", text="Thickness")
                        col.prop(WM, "solidify_offset", text="Offset")
                        col.prop(WM, "rim_only", text="Rim Only")
                        col.prop(WM, "apply_solidify", text="Apply Solidify")
                    col.prop(WM, "comeback_in_sculpt_mode", text="Go To Sculpt")
                    col.separator()
                    col.operator("speedsculpt.extract_mask", text ="Extract mask", icon ='BRUSH_TEXMASK')
                 
                 
                if WM.extract_cut_delete == 'cut': 
                    split = box.split()
                    col = split.column(align=True)  
                    col.prop(WM, "comeback_in_sculpt_mode", text="Go To Sculpt")
                    col.operator("speedsculpt.cut_by_mask", text="Cut Masked Part")
                    

                if WM.extract_cut_delete == 'duplicate': 
                    split = box.split()
                    col = split.column(align=True)   
                    col.prop(WM, "comeback_in_sculpt_mode", text="Go To Sculpt")  
                    col.operator("speedsculpt.duplicate_by_mask", text="Duplicate Masked Part")
                    
                if WM.extract_cut_delete == 'flatten':
                    split = box.split()
                    col = split.column(align=True)
                    col.prop(WM, "comeback_in_sculpt_mode", text="Go To Sculpt")
                    col.prop(WM, "update_dyntopo", text="Update Dyntopo")
                    col.operator("speedsculpt.flatten_mask", text="Flatten Masked Part")

                if WM.extract_cut_delete == 'hook':
                    split = box.split()
                    col = split.column(align=True)
                    # col.prop(WM, "comeback_in_sculpt_mode", text="Go To Sculpt")
                    # col.prop(WM, "update_dyntopo", text="Update Dyntopo")
                    col.operator("speedsculpt.hook_mask", text="Hook Masked Part")


                # if WM.extract_cut_delete == 'remove':
                #     split = box.split()
                #     col = split.column(align=True)
                #     col.operator("speedsculpt.delete_by_mask", text="Delete Masked Part")


            elif bpy.context.object.mode == "OBJECT":
                box = layout.box()
                split = box.split()
                box = split.column(align=True)
                
                solidify = False
                for mod in context.active_object.modifiers:
                    if mod.type == "SOLIDIFY":
                        solidify = True
                if solidify:  
                    split = box.split()
                    col = split.column(align=True)
                    col.prop(bpy.context.active_object.modifiers["Solidify"], "thickness", text="Thickness")
                    col.prop(bpy.context.active_object.modifiers["Solidify"], "offset", text="Offset")  
                    col.prop(bpy.context.active_object.modifiers["Solidify"], "use_rim_only", text="Only Rim")     

                else:  
                    row = box.row(align=True) 
                    row.operator("speedsculpt.add_extract_mask", text="Add Mask", icon='BRUSH_MASK')


# -----------------------------------------------------------------------------
#    Quick Pose
# ----------------------------------------------------------------------------- 
def QuickPose(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    obj = bpy.context.active_object
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help
    
    
    if len([obj for obj in context.selected_objects if obj.type == 'MESH']) == 1:
        row = layout.row(align=True)
        row.prop(WM, "show_quickpose", text="Quick Pose", icon='TRIA_UP' if WM.show_quickpose else 'TRIA_DOWN')
        if self.show_help : 
            row.menu("SC_HELP_MT_quickpose",text="", icon='TRIA_RIGHT')
        if WM.show_quickpose:
            # Armature
            armature = False
            for mod in bpy.context.active_object.modifiers:
                if mod.type == "ARMATURE":
                    armature = True
                    
            if not armature :
                if bpy.context.object.mode == "SCULPT":
                    box = layout.box()
                    split = box.split()
                    col = split.column(align=True)
                    row = col.row(align=True)
                    row.operator("speedsculpt.quick_pose_add_mask", text="Add Mask", icon='BRUSH_MASK')
                    box.operator("speedsculpt.quick_pose_create_bones", text="Create Bones", icon='POSE_HLT')
                    
                elif bpy.context.object.mode == "OBJECT":
                    box = layout.box()
                    split = box.split()
                    col = split.column(align=True)
                    row = col.row()
                    row.prop(WM, "use_mask", text="Use Mask")
                    row = col.row()
                    if WM.use_mask:
                        row.operator("speedsculpt.quick_pose_add_mask", text="Add Mask", icon='BRUSH_MASK')
                    else :
                        box.operator("speedsculpt.quick_pose_create_bones", text="Create Bones", icon='POSE_HLT')
                 
                elif bpy.context.object.mode == 'EDIT': 
                    
                    bs_vertex = True
                    for obj in bpy.context.selected_objects:
                        if obj.name != "BS_Vertex" :
                            bs_vertex = False
                            break
                    if bs_vertex :    
                        box = layout.box()
                        split = box.split()
                        col = split.column(align=True)
                        row = col.row()
                        box.operator("speedsculpt.quick_pose_convert_bones", text="Pose", icon='ARMATURE_DATA')
                    
                
           
            if armature:
                
                if bpy.context.object.mode == "OBJECT":
                    box = layout.box()
                    split = box.split()
                    col = split.column(align=True)
                    row = col.row(align=True)
                    if not "Armature" in obj.modifiers:    
                        if WM.use_mask:
                            row.operator("speedsculpt.quick_pose_add_mask", text="Add Mask", icon='BRUSH_MASK')
                        else :
                            row.operator("speedsculpt.quick_pose_create_bones", text="Create Bones", icon='POSE_HLT')
                        
                    else :
                        row.prop(bpy.context.active_object.modifiers["Armature"], "show_viewport", text="Hide Armature")

                        row.operator("speedsculpt.apply_quick_pose_modifier", text="", icon='FILE_TICK')
                        row.operator("speedsculpt.remove_quick_pose_modifier", text="", icon='X')
                        
                        
                        if WM.use_mask:
                            row = col.row(align=True)
                            row.operator("speedsculpt.edit_quick_pose_mask", text="Edit Mask", icon='BRUSH_MASK')
                            row = col.row(align=True)
                            row.operator("speedsculpt.quick_pose_smooth_mask", text="Smooth Mask", icon='BRUSH_SMOOTH')
                        
                elif bpy.context.object.mode == "SCULPT":
                    box = layout.box()
                    split = box.split()
                    row = split.row(align=True)   
                    row.operator("speedsculpt.valid_quick_pose_mask", text="Valid Mask", icon='FILE_TICK')

# -----------------------------------------------------------------------------
#    Shading
# -----------------------------------------------------------------------------
def Speedsculpt_Shading(self, context):
    """ Sub panel for the adding assets """
    layout = self.layout
    WM = context.window_manager
    act_obj = context.active_object
    prefs = get_addon_preferences()
    self.show_help = prefs.show_help

    if len([obj for obj in context.selected_objects if context.object is not None if obj.type in ['MESH','CURVE'] if
            bpy.context.object.mode in ["OBJECT", "SCULPT"]]) >= 1:
        row = layout.row(align=True)
        row.prop(WM, "show_shading", text="Shading",icon='TRIA_UP' if WM.show_shading else 'TRIA_DOWN')

        if self.show_help:
            row.menu("SC_HELP_MT_shading", text="", icon='TRIA_RIGHT')

        if WM.show_shading:
            box = layout.box()
            split = box.split()
            col = split.column(align=True)
            row = col.row(align=True)
            row.label(text="Material")
            row = col.row(align=True)
            row.operator("object.speedsculpt_random_color", text="Add Random Color", icon='COLOR')
            if len(act_obj.material_slots):
                row.operator("object.sc_remove_shaders", text="", icon='X')

                row = col.row(align=True)
                row.prop(WM, "speedsculpt_set_material_color", text="")


            # Solo
            row = col.row(align=True)
            row.label(text="Solo")
            if bpy.context.scene.render.engine == 'CYCLES':
                row = col.row(align=True)
                # row.scale_y = 1.5
                row.operator("object.sc_make_solo", text="Solo", icon="COLOR_GREEN")

                if bpy.data.materials.get('Transparent_shader'):
                    row.operator("object.sc_stop_solo", text="", icon="X")
                    row = col.row(align=True)
                    row.prop(bpy.data.materials['Transparent_shader'], "diffuse_color", text="")
                    row = col.row(align=True)
                    row.prop(bpy.data.materials['Transparent_shader'], "alpha", text="Alpha")


            # OpenGL
            row = col.row(align=True)
            row.label(text="OpenGL")
            row = col.row(align=True)
            sub = row.row()
            sub.scale_y = 6
            sub.operator("object.sc_next_asset", text="", icon='TRIA_LEFT').selection = -1
            row.template_icon_view(WM, "sc_my_previews", show_labels=True, scale=5.0)

            sub = row.row()
            sub.scale_y = 6
            sub.operator("object.sc_next_asset", text="", icon='TRIA_RIGHT').selection = 1
            row = col.row(align=True)
            row.operator("wm.save_userpref", text="Save Prefs", icon='SAVE_PREFS')

# -----------------------------------------------------------------------------
#    UI
# -----------------------------------------------------------------------------
def UI_Menus(self, context):
    layout = self.layout
    WM = context.window_manager
    toolsettings = context.tool_settings
    sculpt = toolsettings.sculpt
    obj = context.active_object

    if context.object is not None and obj.type == 'ARMATURE' and bpy.context.object.mode == 'POSE' and not obj.name.startswith(
            "Envelope"):
        layout.operator("object.symmetrize_bones", text="Symmetrize Bones", icon='OUTLINER_OB_ARMATURE')

    elif context.object is not None and bpy.context.object.mode == 'EDIT' and obj.type == 'ARMATURE' and not obj.name.startswith(
            "Envelope"):
        layout.operator("object.update_armature", text="Update Armature", icon='OUTLINER_OB_ARMATURE')

    else:
        if bpy.context.area.type == 'VIEW_3D':
            col = layout.column()
            sub = col.column(align=True)
            row = sub.row(align=True)
            row.scale_y = 1.5
            row.scale_x = 1.5

            # row.prop(WM, "speedsculpt_dyntopo_value", text="")
            if hasattr(sculpt, "constant_detail"):
                row.prop(sculpt, "constant_detail")
            else:
                row.prop(sculpt, "constant_detail_resolution")

        if context.object is not None and bpy.context.object.mode == 'SCULPT':
            row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')


        if context.object is not None and not bpy.context.object.mode == 'EDIT' and not obj.name.startswith("Envelope"):
            row.scale_y = 1.5
            row.scale_x = 1.5
            row.operator("object.update_dyntopo", text="", icon='FILE_TICK')

            if len([obj for obj in context.selected_objects]) == 1:
                if not bpy.context.object.mode in ["SCULPT", "POSE"]:
                    if obj.modifiers:
                        if "Mirror_primitive" in obj.modifiers:
                            row = sub.row(align=True)
                            row.scale_y = 1.5
                            row.operator("object.boolean_sculpt_union_difference", text="Union/Apply Modifiers",
                                         icon="MOD_BOOLEAN").operation_type = 'UNION'

            meta_objects = False
            no_modifiers = True
            if len(bpy.context.selected_objects) >= 2:
                if not bpy.context.object.mode in ["SCULPT", "POSE"]:
                    for obj in bpy.context.selected_objects:
                        if obj.modifiers:
                            no_modifiers = False
                            break
                        if obj.type == 'META':
                            meta_objects = True

                    if no_modifiers and not meta_objects:
                        row = sub.row(align=True)
                        row.scale_y = 1.5
                        row.operator("object.boolean_sculpt_rebool", text="R  ", icon="MOD_BOOLEAN")
                        row.operator("object.boolean_sculpt_union_difference", text="D  ",
                                     icon="MOD_BOOLEAN").operation_type = 'DIFFERENCE'
                        row.operator("object.boolean_sculpt_union_difference", text="U  ",
                                     icon="MOD_BOOLEAN").operation_type = 'UNION'
                    else:
                        row = sub.row(align=True)
                        row.scale_y = 1.5
                        row.operator("object.boolean_sculpt_union_difference", text="Union",
                                     icon="MOD_BOOLEAN").operation_type = 'UNION'

        Options(self, context)
        # Speedsculpt_Shading(self, context)
        AddPrimitives(self, context)
        Lattice(self, context)
        Symmetrize(self, context)
        Remesh(self, context)
        ExtractMask(self, context)
        QuickPose(self, context)


class SPEEDSCULPT_PT_panel(bpy.types.Panel):
    bl_label = "SpeedSculpt"
    bl_region_type = 'UI'
    bl_space_type = "VIEW_3D"
    bl_category = "Tools"
    def draw(self, context):
        layout = self.layout
        UI_Menus(self, context)


class SPEEDSCULPT_OT_print_path(bpy.types.Operator):
    '''  '''
    bl_idname = 'object.speedsculpt_printpath'
    bl_label = "Print"
    bl_options = {'REGISTER'}

    def execute(self, context):
        print(os.path.dirname(__file__))
        return {'FINISHED'}


