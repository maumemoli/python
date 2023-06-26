# import bpy, os
# from os import remove, rename, listdir, makedirs
#
#
# def sc_get_data_path():
#     addon_path = os.path.dirname(__file__)
#     return os.path.join(addon_path, "datas")
#
# def sc_get_filepath(image_name):
#     data_path = sc_get_data_path()
#     file_name = "{}.py".format(image_name.rsplit(".", 1)[0])
#     return os.path.join(data_path, file_name)
#
#
# def sc_setup_opengl_lights(self, context):
#     exec(compile(open(self.sc_my_previews).read(), self.sc_my_previews, 'exec'))
#
# def sc_enum_previews_from_directory_items(self, context):
#     """EnumProperty callback"""
#     enum_items = []
#
#     if context is None:
#         return enum_items
#
#     wm = context.window_manager
#     directory = wm.sc_my_previews_dir = sc_get_data_path()
#
#     pcoll = sc_preview_collections["main"]
#
#     if directory == pcoll.sc_my_previews_dir:
#         return pcoll.sc_my_previews
#
#     print("Scanning directory: %s" % directory)
#
#     if directory and os.path.exists(directory):
#         image_paths = []
#         for fn in os.listdir(directory):
#             if fn.lower().endswith(".png"):
#                 image_paths.append(fn)
#
#         for i, name in enumerate(image_paths):
#             # generates a thumbnail preview for a file.
#             image_path = os.path.join(directory, name)
#             thumb = pcoll.load(image_path, image_path, 'IMAGE')
#             filepath = sc_get_filepath(name)
#             enum_items.append((filepath, name.split(".png")[0], name.split(".png")[0],
#                                thumb.icon_id, i))
#
#     pcoll.sc_my_previews = enum_items
#     pcoll.sc_my_previews_dir = directory
#     return pcoll.sc_my_previews
#
# sc_preview_collections = {}
#
#
#
#
# class NextAsset(bpy.types.Operator):
#     """ Display the next asset """
#     bl_idname = "object.sc_next_asset"
#     bl_label = "Next Asset"
#     bl_options = {"REGISTER"}
#
#     selection = bpy.props.IntProperty(
#             default=0
#             )
#
#     def get_next_asset(self, selection):
#         """ Return the next asset to draw in the preview """
#
#         WM = bpy.context.window_manager
#         current_asset = WM.sc_my_previews.split(".py")[0]
#         data_path = os.path.join(os.path.dirname(__file__), "datas")
#
#         thumb_list = [os.path.join(data_path, thumb.split(".png")[0]) for thumb
#                       in os.listdir(data_path) if thumb.endswith(".png")]
#
#         current_index = thumb_list.index(current_asset)
#         max_index = len(thumb_list) - 1
#         asset = thumb_list[
#             current_index + selection] if current_index + selection <= max_index else \
#             thumb_list[0]
#
#         return asset + ".py"
#
#     def execute(self, context):
#         bpy.context.window_manager.sc_my_previews = self.get_next_asset(
#             self.selection)
#
#         return {"FINISHED"}
#
#
# def register():
#     from bpy.types import WindowManager
#     from bpy.props import (
#             StringProperty,
#             EnumProperty,
#             )
#
#     WindowManager.sc_my_previews_dir = StringProperty(
#             name="Folder Path",
#             subtype='DIR_PATH',
#             default=""
#             )
#
#     WindowManager.sc_my_previews = EnumProperty(
#             items=sc_enum_previews_from_directory_items,
#             update=sc_setup_opengl_lights
#             )
#
#     import bpy.utils.previews
#     pcoll = bpy.utils.previews.new()
#     pcoll.sc_my_previews_dir = ""
#     pcoll.sc_my_previews = ()
#
#     sc_preview_collections["main"] = pcoll
#
#
# def unregister():
#     from bpy.types import WindowManager
#
#     del WindowManager.sc_my_previews
#
#     for pcoll in sc_preview_collections.values():
#         bpy.utils.previews.remove(pcoll)
#     sc_preview_collections.clear()
#
