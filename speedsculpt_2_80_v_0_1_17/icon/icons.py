'''
Copyright (C) 2015 Pistiwique, Pitiwazou
 
Created by Pistiwique, Pitiwazou
 
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


import os
import bpy
import bpy.utils.previews

speedsculpt_icon_collections = {}
speedsculpt_icons_loaded = False


def load_icons():
    global speedsculpt_icon_collections
    global speedsculpt_icons_loaded

    if speedsculpt_icons_loaded: return speedsculpt_icon_collections["main"]

    custom_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__))

    # modals
    custom_icons.load("icon_market", os.path.join(icons_dir, "market.png"), 'IMAGE')
    custom_icons.load("icon_artstation", os.path.join(icons_dir, "artstation.png"), 'IMAGE')
    custom_icons.load("icon_gumroad", os.path.join(icons_dir, "gumroad.png"), 'IMAGE')

    speedsculpt_icon_collections["main"] = custom_icons
    speedsculpt_icons_loaded = True

    return speedsculpt_icon_collections["main"]


def speedsculpt_clear_icons():
    global speedsculpt_icons_loaded
    for icon in speedsculpt_icon_collections.values():
        bpy.utils.previews.remove(icon)
    speedsculpt_icon_collections.clear()
    speedsculptt_icons_loaded = False