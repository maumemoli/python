from .functions import *


# Solo
def SC_Create_Transparent_Shader():
    prefs = get_addon_preferences()
    sc_solo_color = prefs.sc_solo_color
    sc_solo_alpha = prefs.sc_solo_alpha


    material = bpy.data.materials.new(name="Transparent_shader")
    material.use_nodes = True

    material_output = material.node_tree.nodes.get('Material Output')
    shader = material.node_tree.nodes['Diffuse BSDF']

    material.node_tree.links.new(material_output.inputs[0], shader.outputs[0])

    material.alpha = sc_solo_alpha
    material.diffuse_color = sc_solo_color

def SC_Add_Solo(obj, context):
    prefs = get_addon_preferences()
    sc_solo_alpha = prefs.sc_solo_alpha

    context.space_data.viewport_shade = 'SOLID'

    sculpt = False
    if context.object.mode == "SCULPT":
        sculpt = True

    if bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode='OBJECT')

    context.preferences.edit.use_duplicate_material = False
    context.space_data.show_backface_culling = True
    context.object.show_transparent = False

    # on recup la selection et l'objet actif
    act_obj_list = [obj for obj in context.selected_objects]

    # On selectionne les objets visible de la scene
    bpy.ops.object.select_grouped(type='LAYER')

    # On deselectionne les objets selectionnes
    for obj in act_obj_list:
        obj.select_set(state=True)

    # On cree une liste avec les objets restants
    obj_list = [obj for obj in context.selected_objects]

    # On check si le shader existe dans la scene
    if not bpy.data.materials.get('Transparent_shader'):
        SC_Create_Transparent_Shader()

    # On sélectionne les objets de la liste et on leur attribue le transparent shader, la transparence et l'alpha
    for obj in obj_list:

        context.scene.objects.active = obj
        if hasattr(obj.data, "materials") and not obj.type == 'EMPTY_IMAGE':
            obj.show_transparent = True

            if obj.material_slots:
                mats = [mat.name for mat in obj.material_slots]
                if not 'Transparent_shader' in mats:

                    bpy.ops.object.material_slot_add()
                    obj.material_slots[-1].material = bpy.data.materials['Transparent_shader']
                    for f in obj.data.polygons:
                        f.material_index = 1
            else:
                obj.active_material = bpy.data.materials['Transparent_shader']

            obj.active_material.alpha = sc_solo_alpha

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    for obj in act_obj_list:
        context.view_layer.objects.active = obj
        obj.select_set(state=True)
        if hasattr(obj.data, "materials"):
            mats = [mat.name for mat in obj.material_slots]
            if 'Transparent_shader' in mats:
                obj.data.materials.pop(mats.index('Transparent_shader'), update_data=True)

    if sculpt:
        bpy.ops.object.mode_set(mode='SCULPT')

# Add Solo On Selection
def SC_Add_Solo_On_Selection(obj, context):
    prefs = get_addon_preferences()
    sc_solo_alpha = prefs.sc_solo_alpha
    bpy.context.preferences.edit.use_duplicate_material = False

    for obj in context.selected_objects:
        context.view_layer.objects.active = obj
        if hasattr(obj.data, "materials") and not obj.type == 'EMPTY_IMAGE':
            obj.show_transparent = True
            # On check si le shader existe dans la scene
            if not bpy.data.materials.get('Transparent_shader'):
                context.space_data.show_backface_culling = True
                SC_Create_Transparent_Shader()

            if obj.material_slots:
                mats = [mat.name for mat in obj.material_slots]
                if not 'Transparent_shader' in mats:

                    bpy.ops.object.material_slot_add()
                    obj.material_slots[1].material = bpy.data.materials['Transparent_shader']
                    for f in obj.data.polygons:
                        f.material_index = 1

            else:
                obj.active_material = bpy.data.materials['Transparent_shader']

            obj.active_material.alpha = sc_solo_alpha

#Remove Transparent Shader
def SC_Remove_Transparent_shader(obj):
    if hasattr(obj.data, "materials"):

        mats = [mat.name for mat in obj.material_slots]
        if 'Transparent_shader' in mats:

            obj.data.materials.pop(mats.index('Transparent_shader'), update_data=True)
            obj.show_transparent = False

        else:
            if obj.data.materials:
                obj.active_material.alpha = 1
            obj.show_transparent = False

#Remove_Solo
class SC_Stop_Solo(bpy.types.Operator):
    bl_idname = 'object.sc_stop_solo'
    bl_label = "Stop Solo"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        obj = context.active_object
        SC_Remove_Solo(obj)

        return {'FINISHED'}


def SC_Remove_Solo(obj, context):
    duplicate_material = context.preferences.edit.use_duplicate_material

    if bpy.data.materials.get('Transparent_shader'):
        context.space_data.show_backface_culling = False
        for obj in context.visible_objects:
            if hasattr(obj.data, "materials"):
                SC_Remove_Transparent_shader(obj)

            obj.hide_select = False

        bpy.data.materials.remove(bpy.data.materials['Transparent_shader'], do_unlink=True)

    context.preferences.edit.use_duplicate_material = duplicate_material

#Remove Solo From Selection
def SC_Remove_Solo_From_Selection(obj, context):
    duplicate_material = bpy.context.preferences.edit.use_duplicate_material
    if hasattr(obj.data, "materials"):
        SC_Remove_Transparent_shader(obj)

    else:
        context.space_data.show_backface_culling = False
        for obj in context.visible_objects:
            if hasattr(obj.data, "materials"):
                SC_Remove_Transparent_shader(obj)
        bpy.data.materials.remove(bpy.data.materials['Transparent_shader'], do_unlink=True)

    context.preferences.edit.use_duplicate_material = duplicate_material

class SC_Make_Solo(bpy.types.Operator):
    """    SOLO

    CLICK - Solo the selection
    SHIFT - Add Selection to Transparency
    CTRL  - Remove Selection from Transparency
    ALT    - UnSolo"""

    bl_idname = 'object.sc_make_solo'
    bl_label = "Make Solo"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        obj = context.active_object

        if context.object is not None and hasattr(context.object.data, "materials"):

            if event.shift:
                SC_Add_Solo_On_Selection(obj)

            elif event.ctrl:
                SC_Remove_Solo_From_Selection(obj)

            elif event.alt:
                SC_Remove_Solo(obj)

            else:
                SC_Add_Solo(obj)
        return {'FINISHED'}