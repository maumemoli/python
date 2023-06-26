import bpy
from bpy.props import (StringProperty, 
                       BoolProperty, 
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty)

from .primitives import (UpdateMetaballs,
                        ClippingMerge)

from .remesh_decimate import HideRemeshSmooth, Hidedecimate, DecimateRatio, RemeshOctreeDepth, RemeshSmoothRepeat

from .lattice import (HideLattice, 
                      LatticeInterpolation)

# from .operators import Speedsculpt_Set_Material_Color

import os


##------------------------------------------------------  
#
# Funtions
#
##------------------------------------------------------  

def get_addon_preferences():
    addon_key = __package__.split(".")[0]

    return bpy.context.preferences.addons[addon_key].preferences

# def get_addon_preferences():
#     addon_name = os.path.basename(os.path.dirname(os.path.abspath(__file__).split("utils")[0]))
#     user_preferences = bpy.context.preferences
#     # addon_prefs = user_preferences.addons[addon_name].preferences
#     addon_prefs = bpy.context.preferences.addons[__name__].preferences
#
#     return addon_prefs
#------------------------------------------------------------------------------------------
# Object ref mirror
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.ref_obj =StringProperty(description='Object reference for the Mirror')

#------------------------------------------------------------------------------------------
# Options 
#------------------------------------------------------------------------------------------

            
bpy.types.WindowManager.detail_size =FloatProperty(min = 0.01, max = 300, default = 20)

#------------------------------------------------------------------------------------------
# Shading
#------------------------------------------------------------------------------------------
# bpy.types.WindowManager.speedsculpt_set_material_color : FloatVectorProperty(
#                 name="Set Material Color",
#                 default=(0.214041, 0.214041, 0.214041),
#                 min=0, max=1,
#                 precision=3,
#                 size=3,
#                 subtype='COLOR',
#                 update = Speedsculpt_Set_Material_Color
#                 )


#------------------------------------------------------------------------------------------
# Extract Mask
#------------------------------------------------------------------------------------------
# bpy.types.WindowManager.extract_cut_delete = EnumProperty(
#         items=(('extract', "Extract", "Extract"),
#                ('cut', "Cut", "Cut"),
#                ('duplicate', "Duplicate", "Duplicate"),
#                ('flatten', "Flatten", "Flatten"),
#                ('hook', "Hook", "Hook"),
#                ('remove', "Remove", "Remove")
#                ),
#                default='extract'
#                )

bpy.types.WindowManager.extract_cut_delete = EnumProperty(
        items=(('extract', "Extract", "Extract"),
               ('cut', "Cut", "Cut"),
               ('duplicate', "Duplicate", "Duplicate"),
               ('flatten', "Flatten", "Flatten"),
               ('hook', "Hook", "Hook")),
               default='extract'
               )

               
bpy.types.WindowManager.add_solidify = BoolProperty(
    name="Add Solidify",
    description="Add Solidify to the extracted object",
    default=True)

bpy.types.WindowManager.comeback_in_sculpt_mode = BoolProperty(
    name="Comme Back in Sculpt mode",
    description="Comme Back in Sculpt mode",
    default=True)
    
bpy.types.WindowManager.apply_solidify = BoolProperty(
        default=True,
        description="Apply Solidify"
        )    

bpy.types.WindowManager.update_dyntopo = BoolProperty(
        default=True,
        description="Update Dyntopo"
        ) 
                
bpy.types.WindowManager.rim_only = BoolProperty(
    name="Rim Only",
    description="Rim Only",
    default=False) 
    
bpy.types.WindowManager.solidify_thickness = FloatProperty(min = 0.01, max = 300, default = 0.1)

bpy.types.WindowManager.solidify_offset = FloatProperty(min = -1, max = 1, default = 0)


#------------------------------------------------------------------------------------------
# GP Lines
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.gp_solidify_thickness = FloatProperty(min = 0.01, max = 300, default = 0.1)

bpy.types.WindowManager.gp_solidify_offset = FloatProperty(min = -1, max = 1, default = 0.5)

bpy.types.WindowManager.use_clipping = BoolProperty(
        default=False,
        description="Use Clipping/Merger for the mirror modifier",
        update = ClippingMerge
        ) 
  
#------------------------------------------------------------------------------------------
# Quick Pose
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.use_mask = BoolProperty(
    name="Use Mask",
    description="Use Mask",
    default=True) 
#------------------------------------------------------------------------------------------
# BBOX
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.bbox_bevel = FloatProperty(min = 0, max = 100, default = 0.1)
bpy.types.WindowManager.bbox_depth = FloatProperty(min = 0, max = 100, default = 1)
bpy.types.WindowManager.bbox_offset = FloatProperty(min = -100, max = 100, default = -0.1)


bpy.types.WindowManager.bbox_apply_solidify = BoolProperty(
        default=True,
        description="Apply solidify"
        ) 
        
bpy.types.WindowManager.bbox_convert = BoolProperty(
        default=False,
        description="Convert to Dyntopo"
        )  

bpy.types.WindowManager.smooth_result = BoolProperty(
        default=False,
        description="Smooth the object"
        )                 
#------------------------------------------------------------------------------------------
# Primitives
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.origin = BoolProperty(
        default=False,
        description="Place the object at the origin of the Scene"
        )      

bpy.types.WindowManager.add_mirror = BoolProperty(
        default=False,
        description="Add Mirror"
        )    

bpy.types.WindowManager.primitives_parenting = BoolProperty(
        default=False,
        description="Make the new object children to the active object"
        )  
#------------------------------------------------------------------------------------------
# Metaballs
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.metaballs_pos_neg = EnumProperty(
        items = (('positive', "Positive", ""),
                 ('negative', "Negative", "")),
                 default = 'positive',
                 update = UpdateMetaballs
                 )   
              
#------------------------------------------------------------------------------------------
# Curves
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.bbox = BoolProperty(
        default=False,
        description="Add Solidify"
        ) 

bpy.types.WindowManager.direct_cut = BoolProperty(
        default=False,
        description="Cut Directly the mesh"
        ) 

bpy.types.WindowManager.direct_rebool = BoolProperty(
        default=False,
        description="Directly Rebool"
        ) 

bpy.types.WindowManager.create_lathe = BoolProperty(
        default=False,
        description="Create Lathe"
        ) 
        
bpy.types.Scene.obj1 = StringProperty()
                        

#------------------------------------------------------------------------------------------
# Skin
#------------------------------------------------------------------------------------------

        
bpy.types.WindowManager.skin_mirror = BoolProperty(
        default=False,
        description="Add Mirror"
        ) 
        
#------------------------------------------------------------------------------------------
# Remesh
#------------------------------------------------------------------------------------------
# bpy.types.WindowManager.add_remesh= BoolProperty(
#         default=True,
#         description="Add Remesh and smooth"
#         )
        
bpy.types.WindowManager.hide_remesh_smooth = BoolProperty(
        default=True,
        description="Hide Remesh and smooth",
        update = HideRemeshSmooth
        ) 

bpy.types.WindowManager.apply_remesh = BoolProperty(
        default=False,
        description="Apply Remesh"
        )

# bpy.types.WindowManager.remesh_octree_depth = IntProperty(
#                                             min = 0,
#                                             max = 15,
#                                             default = 6,
#                                             update = RemeshOctreeDepth)

bpy.types.WindowManager.remesh_smooth_repeat = IntProperty(
                                            min = 0,
                                            max = 100,
                                            default = 10,
                                            update = RemeshSmoothRepeat)
#------------------------------------------------------------------------------------------
# Decimate
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.hide_decimate = BoolProperty(
        default=True,
        description="Hide Decimate",
        update = Hidedecimate
        )

bpy.types.WindowManager.decimate_ratio = FloatProperty(
                                            min = 0,
                                            max = 1,
                                            default = 1,
                                            update = DecimateRatio)
#------------------------------------------------------------------------------------------
# Lattice
#------------------------------------------------------------------------------------------         
bpy.types.WindowManager.copy_orientation = BoolProperty(
    name="Copy orientation",
    description="Copy the orientation of the active Object",
    default=False)

bpy.types.WindowManager.hide_lattice = BoolProperty(
        default=True,
        description="Hide Lattice on selected objects",
        update = HideLattice
        )  
           
bpy.types.WindowManager.lattice_u = IntProperty(min = 2, max = 100, default = 2)
bpy.types.WindowManager.lattice_v = IntProperty(min = 2, max = 100, default = 2)
bpy.types.WindowManager.lattice_w = IntProperty(min = 2, max = 100, default = 2)

bpy.types.WindowManager.lattice_interp = EnumProperty(
        items = (('KEY_LINEAR', 'linear', ""),
                ('KEY_BSPLINE', 'bspline', ""),
                ('KEY_CATMULL_ROM', 'catmull_rom', ""),
                ('KEY_CARDINAL', 'cardinal', "")),
                default = 'KEY_BSPLINE',
                update = LatticeInterpolation
                )
            
#------------------------------------------------------------------------------------------
# Show/Hide
#------------------------------------------------------------------------------------------
bpy.types.WindowManager.show_shading  = BoolProperty(
        default=False,
        description="Show/Hide Shading Tools"
        )

bpy.types.WindowManager.show_primitives = BoolProperty(
        default=True,
        description="Show/Hide Primitives"
        )  

bpy.types.WindowManager.show_extract = BoolProperty(
        default=False,
        description="Show/Hide Extract"
        )  
 
bpy.types.WindowManager.show_symmetrize  = BoolProperty(
        default=False,
        description="Show/Hide Symmetrize Tools"
        )  
       
bpy.types.WindowManager.show_remesh = BoolProperty(
        name="Add Solidify",
        description="Add Solidify to the extracted object",
        default=False)              

bpy.types.WindowManager.show_lattice = BoolProperty(
        name="Add Lattice",
        description="Add Lattice to selected objects",
        default=False)              

bpy.types.WindowManager.show_quickpose = BoolProperty(
        name="Quick Pose",
        description="Show/Hide Quick Pose Tools",
        default=False)  