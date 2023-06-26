'''
Copyright (C) 2016 CEDRIC LEPILLER
pitiwazou@gmail.com

Created by CEDRIC LEPILLER

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "SpeedSculpt",
    "description": "Create models for sculpt and manage Dyntopo sculpt",
    "author": "pitiwazou",
    "version": (0, 1, 17),
    "blender": (2, 80, 0),
    "location": "View3D",
    "wiki_url": "",
    "category": "3D View" }


import bpy
from bpy.types import Menu, Operator
from bpy.props import PointerProperty, StringProperty, BoolProperty, \
    EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, \
    CollectionProperty, BoolVectorProperty

from .ui import *
from . import auto_load
from .icon.icons import load_icons


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

########################################
# UPDATE
########################################
import requests
import json

# def get_last_version(user):
#     r = requests.get('https://api.github.com/users/%s/repos' % user)
#     repos = json.loads(r.content)
#
#     for repo in repos:
#         if repo['name'] != "sculpt_update":
#             continue
#         r = requests.get(repo['url'] + "/commits")
#         commits = json.loads(r.content)
#         return commits[0]["commit"]["message"]
#
# def sculpt_check_update():
#     prefs = bpy.context.preferences.addons[__name__].preferences
#
#     if prefs.check_for_updates:
#         previous_version = str(bl_info['version'])
#         last_version = get_last_version("pitiwazou").split("version_")[-1]
#         # print(f"previous version{previous_version}, lastversion{last_version}")
#         if previous_version != last_version:
#             prefs.sculpt_update_check = True
#             prefs.sculpt_update_new_version = last_version
#             # print("An Update is Available!")
#             # print("Please, Update your Addon")
###########################################

##------------------------------------------------------  
#
# Preferences
#
##------------------------------------------------------  

# def SC_update_panel_position(self, context):
#     try:
#         bpy.utils.unregister_class(SpeedSculptMenu)
#         bpy.utils.unregister_class(SpeedSculptMenuUI)
#     except:
#         pass
#
#     try:
#         bpy.utils.unregister_class(SpeedSculptMenuUI)
#     except:
#         pass
#
#     if context.preferences.addons[__name__].preferences.Speedsculpt_tab_location == 'tools':
#         SpeedSculptMenu.bl_category = context.preferences.addons[__name__].preferences.category
#         bpy.utils.register_class(SpeedSculptMenu)
#
#     else:
#         bpy.utils.register_class(SpeedSculptMenuUI)


# Addons Preferences Update Panel
def SC_update_panel(self, context):
    prefs = context.preferences.addons[__name__].preferences

    if hasattr(bpy.types, 'SPEEDSCULPT_PT_panel'):
        try:
            bpy.utils.unregister_class(bpy.types.SPEEDSCULPT_PT_panel)
        except:
            pass

    SPEEDSCULPT_PT_panel.bl_category = prefs.category
    bpy.utils.register_class(SPEEDSCULPT_PT_panel)


    
class SCPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
        
    prefs_tabs : EnumProperty(
        items=(('info', "Info", "Info"),
               ('options', "Options", "Options"),
               # ('doc', "Doc", "Doc"),
               ('tutorials', "Tutorials", "Tutorials"),
               ('addons', "Addons", "Addons"),
               ('links', "Links", "Links"),),
               default='info'
               )

    sculpt_update_check: BoolProperty(
        name="",
        default=False,
        description="Check For Updates")

    # check_for_updates: BoolProperty(
    #     name="",
    #     default=False,
    #     description="Check for updates of the addon",
    #     update = 'sculpt_check_update')

    # sculpt_update_new_version: StringProperty(
    #     description="Updates Version"
    # )
    category : bpy.props.StringProperty(
            name="Category",
            description="Choose a name for the category of the panel",
            default="Tools",
            update=SC_update_panel)
    
    show_help : BoolProperty(
            name="",
            default=True,
            description="Show the help on the Addon"
            )     
    
    auto_save : BoolProperty(
            name="",
            default=True,
            description="Auto save the scene when updating a mesh or making booleans"
            )

    smooth_mesh : BoolProperty(
        name="",
        default=True,
        description="Smooth the mesh when updating a mesh or making booleans"
    )

    fill_holes_dyntopo : BoolProperty(
        name="",
        default=False,
        description="Close holes on the mesh when updating a mesh or making booleans"
    )

    update_detail_flood_fill : BoolProperty(
        name="",
        default=True,
        description="Update Detail Flood Fill when updating a mesh or making booleans"
    )

    flat_shading : BoolProperty(
        name="",
        default=False,
        description="Use Flat shading"
    )

    add_remesh : BoolProperty(
        name="",
        default=False,
        description="Add Remesh to cut object"
    )

    remesh_value : bpy.props.IntProperty(
        min=0,
        max=15,
        default=6,
        description="Remesh Value",
        update=RemeshOctreeDepth)

    # # SOLO
    # sc_solo_color : FloatVectorProperty(
    #     name="Solo Color:",
    #     default=(0.15, 1, 0.2),
    #     min=0, max=1,
    #     subtype='COLOR'
    # )
    #
    # sc_solo_alpha : FloatProperty(
    #     default=0.3,
    #     min=0, max=1,
    #     precision=3
    # )

    # speedsculpt_dyntopo_value = FloatProperty(
    #     name="Dyntopo Value",
    #     default=10,
    #     min=0, max=100,
    #     precision=3,
    #     update=DyntopoValue
    # )

    #Tab Location           
    # Speedsculpt_tab_location = EnumProperty(
    #     name = 'Panel Location',
    #     description = 'The 3D view shelf to use. (Save user settings and restart Blender)',
    #     items=(('tools', 'Tool Shelf', 'Places the Asset Management panel in the tool shelf'),
    #            ('ui', 'Property Shelf', 'Places the Asset Management panel in the property shelf.')),
    #            default='tools',
    #            update = SC_update_panel_position,
    #            )
                                    
    def draw(self, context):
            layout = self.layout
            wm = bpy.context.window_manager

            # box = layout.box()
            # row = box.row(align=True)
            # row.label(text="Check For Updates")
            # row.prop(self, "check_for_updates", text="      ")
            #
            # if self.check_for_updates:
            #     if self.sculpt_update_check:
            #         icons = load_icons()
            #
            #         box = layout.box()
            #         box.label(text="Speedsculpt have been updated", icon='ERROR')
            #         box.label(text="Please download the last version and intall it")
            #         box.label(text=f"NEW VERSION: {self.sculpt_update_new_version}", icon='ERROR')
            #
            #         row = box.row()
            #         icon = icons.get("icon_gumroad")
            #         row.operator("wm.url_open", text="GUMROAD",
            #                      icon_value=icon.icon_id).url = "https://gumroad.com/l/SpeedSculpt"
            #         icon = icons.get("icon_market")
            #         row.operator("wm.url_open", text="BLENDER MARKET",
            #                      icon_value=icon.icon_id).url = "https://blendermarket.com/products/speedsculpt"
            #         icon = icons.get("icon_artstation")
            #         row.operator("wm.url_open", text="ARTSTATION",
            #                      icon_value=icon.icon_id).url = "https://www.artstation.com/pitiwazou/store/JmKn/speedsculpt"
            #         box.separator()
            #         box.label(text="HOW TO UPDATE:", icon='FILE_REFRESH')
            #         box.label(text="- Uninstall previous version with the REMOVE Button")
            #         box.label(text="- Click on INSTALL FROM FILE")
            #         box.label(text="- Select the Zip")
            #         box.label(text="- Click OK")
            #         box.label(text="- Activate it")
            #         box.label(text="- Click on SAVE PREFERENCES")
            #         box.label(text="- Restart Blender")
            
            row= layout.row(align=True)
            row.prop(self, "prefs_tabs", expand=True)
            if self.prefs_tabs == 'info':
                layout = self.layout
                layout.label(text="Welcome to SpeedSculpt, this addon allows you to create objects for sculpting")
                layout.label(text="You can make booleans, adjust the Detail Size etc")
                layout.operator("wm.url_open",
                                text="Blender Artist Post").url = "https://blenderartists.org/forum/showthread.php?405035-Addon-SpeedSculpt"

            if self.prefs_tabs == 'options':
                layout = self.layout

                box = layout.box()
                box.label(text="Panel Location: ")
                
                # row= box.row(align=True)
                # row.prop(self, 'Speedsculpt_tab_location', expand=True)
                # row = box.row()
                # if self.Speedsculpt_tab_location == 'tools':
                split = box.split()
                col = split.column()
                col.label(text="Change Category:")
                col = split.column(align=True)
                col.prop(self, "category", text="")

                box = layout.box()
                split = box.split()
                col = split.column()
                col.label(text="Show Help")
                col = split.column(align=True)  
                col.prop(self, "show_help") 
                
                split = box.split()
                col = split.column()
                col.label(text="Auto Save Scene")
                col = split.column(align=True)  
                col.prop(self, "auto_save")

                box = layout.box()
                split = box.split()
                col = split.column()
                col.label(text="UPDATE MESH:")

                split = box.split()
                col = split.column()
                col.label(text="Smooth the Mesh")
                col = split.column(align=True)
                col.prop(self, "smooth_mesh")

                split = box.split()
                col = split.column()
                col.label(text="Update the Mesh")
                col = split.column(align=True)
                col.prop(self, "update_detail_flood_fill")

                split = box.split()
                col = split.column()
                col.label(text="Fill Holes")
                col = split.column(align=True)
                col.prop(self, "fill_holes_dyntopo")

                split = box.split()
                col = split.column()
                col.label(text="Flat Shading")
                col = split.column(align=True)
                col.prop(self, "flat_shading")

                split = box.split()
                col = split.column()
                col.label(text="Add Remesh to cut object")
                col = split.column(align=True)
                col.prop(self, "add_remesh")

                split = box.split()
                col = split.column()
                col.label(text="Remesh Value:")
                col = split.column(align=True)
                col.prop(self, "remesh_value", text="")

                # box = layout.box()
                # split = box.split()
                # col = split.column()
                # col.label(text="SHADING:")
                # split = box.split()
                # col = split.column()
                # col.label(text="Solo Color:")
                # col = split.column(align=True)
                # col.prop(self, "sc_solo_color", text="")


                # split = box.split()
                # col = split.column()
                # col.label(text="Solo Alpha:")
                # col = split.column(align=True)
                # col.prop(self, "sc_solo_alpha", text="")

            # ------TUTORIALS
            if self.prefs_tabs == 'tutorials':
                box = layout.box()
                box.label(text="Free Tutorials:", icon='COMMUNITY')
                box.operator("wm.url_open", text="Youtube Channel").url = "https://www.youtube.com/user/pitiwazou"
                box.label(text="Paid Tutorials:", icon='HAND')
                box.operator("wm.url_open",
                             text="Non - Destructive Workflow Tutorial 1").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_1"
                box.operator("wm.url_open",
                             text="Non - Destructive Workflow Tutorial 2").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_2"
                box.operator("wm.url_open",
                             text="Non - Destructive Workflow Tutorial 3").url = "https://gumroad.com/l/Non-Destructive_Workflow_Tutorial_3"
                box.operator("wm.url_open",
                             text="Hydrant Modeling Tutorial").url = "https://gumroad.com/l/hydrant_modeling_tutorial"
                box.operator("wm.url_open",
                             text="Hydrant Unwrapping Tutorial").url = "https://gumroad.com/l/hydrant_unwrapping_tutorial"
                box.operator("wm.url_open",
                             text="Furry Warfare Plane Modeling Tutorial").url = "https://gumroad.com/l/furry_warfare_plane_modeling_tutorial"

            # Addons
            if self.prefs_tabs == 'addons':
                box = layout.box()
                box.operator("wm.url_open", text="Addon's Discord").url = "https://discord.gg/ctQAdbY"
                box.separator()
                box.operator("wm.url_open", text="Asset Management").url = "https://gumroad.com/l/asset_management"
                box.operator("wm.url_open", text="Speedflow").url = "https://gumroad.com/l/speedflow"
                box.operator("wm.url_open", text="SpeedSculpt").url = "https://gumroad.com/l/SpeedSculpt"
                box.operator("wm.url_open", text="SpeedRetopo").url = "https://gumroad.com/l/speedretopo"
                box.operator("wm.url_open", text="Easyref").url = "https://gumroad.com/l/easyref"
                box.operator("wm.url_open", text="RMB Pie Menu").url = "https://gumroad.com/l/wazou_rmb_pie_menu_v2"
                box.operator("wm.url_open", text="Wazou's Pie Menu").url = "https://gumroad.com/l/wazou_pie_menus"
                box.operator("wm.url_open", text="Smart Cursor").url = "https://gumroad.com/l/smart_cursor"
                box.operator("wm.url_open",
                             text="My 2.79 Theme").url = "https://www.dropbox.com/s/x6vcip7n11j5w4e/wazou_2_79_001.xml?dl=0"

            if self.prefs_tabs == 'links':
                box = layout.box()
                box.label(text="Support me:", icon='HAND')
                box.operator("wm.url_open", text="Patreon").url = "https://www.patreon.com/pitiwazou"
                box.operator("wm.url_open", text="Tipeee").url = "https://www.tipeee.com/blenderlounge"
                box.separator()
                box.label(text="Archipack", icon='BLENDER')
                box.operator("wm.url_open", text="Archi Pack").url = "https://blender-archipack.org"

                box.separator()
                box.label(text="Web:", icon='WORLD')
                box.operator("wm.url_open", text="Pitiwazou.com").url = "http://www.pitiwazou.com/"
                box.separator()
                box.label(text="Youtube:", icon='SEQUENCE')
                box.operator("wm.url_open",
                             text="Youtube - Pitiwazou").url = "https://www.youtube.com/user/pitiwazou"
                box.operator("wm.url_open",
                             text="Youtube - Blenderlounge").url = "https://www.youtube.com/channel/UCaA3_WSE5A0H6YrS1SDfAQw/videos"
                box.separator()
                box.label(text="Social:", icon='USER')
                box.operator("wm.url_open", text="Artstation").url = "https://www.artstation.com/artist/pitiwazou"
                box.operator("wm.url_open", text="Twitter").url = "https://twitter.com/#!/pitiwazou"
                box.operator("wm.url_open",
                             text="Facebook").url = "https://www.facebook.com/Pitiwazou-C%C3%A9dric-Lepiller-120591657966584/"
                box.operator("wm.url_open",
                             text="Google+").url = "https://plus.google.com/u/0/116916824325428422972"
                box.operator("wm.url_open", text="Blenderlounge's Discord").url = "https://discord.gg/MBDphac"







##################################
# register
##################################
from .preview_collection import *
import traceback


auto_load.init()
def register():
    bpy.utils.register_class(SCPreferences)
    auto_load.register()

    # Check the addon version on Github
    # sculpt_check_update()


# def register():
#     try: bpy.utils.register_module(__name__)
#     except: traceback.print_exc()

    # print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

    # Panels
    # SC_update_panel(None, bpy.context)
    # SC_update_panel_position(None, bpy.context)

    SC_update_panel(None, bpy.context)

    # Material Color
    # bpy.types.WindowManager.speedsculpt_set_material_color : FloatVectorProperty(
    #     name="Set Material Color",
    #     default=(0.214041, 0.214041, 0.214041),
    #     min=0, max=1,
    #     precision=3,
    #     size=3,
    #     subtype='COLOR',
    #     update=Speedsculpt_Set_Material_Color
    # )

    # Setup OGL
    # ui.register()
    # preview_collection.register()

def unregister():
    bpy.utils.unregister_class(SCPreferences)
    auto_load.unregister()

# def unregister():
#     try: bpy.utils.unregister_module(__name__)
#     except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))

    # Setup OGL
    # ui.unregister()
    # preview_collection.unregister()
