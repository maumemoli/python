import bpy
import math
import mathutils
from mathutils import Vector
from mathutils import Matrix
from .functions import *

class SPEEDSCULPT_OT_create_envelope(bpy.types.Operator):
    bl_idname = 'speedsculpt.create_envelope'
    bl_label = "Create Envelope"
    bl_description = "Experimental Feature"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        WM = context.window_manager

        if context.object is not None :
            bpy.ops.object.mode_set(mode = 'OBJECT')

        if not WM.origin:
            bpy.ops.view3d.cursor3d('INVOKE_DEFAULT')
            bpy.ops.object.armature_add(align='WORLD', enter_editmode=False)

        else:
            bpy.ops.object.armature_add(align='WORlD', enter_editmode=False, location=(0, 0, 0))

        envelope = context.active_object
        envelope.name = "Envelope"
        context.object.data.display_type = 'ENVELOPE'

        # envelope.data.draw_type = 'ENVELOPE'
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_more()

        if not WM.origin:
            bpy.ops.transform.translate('INVOKE_DEFAULT')

        return {'FINISHED'}


class SPEEDSCULPT_OT_enveloppe_symmetrize(bpy.types.Operator):
    bl_idname = 'speedsculpt.enveloppe_symmetrize'
    bl_label = "Symmetrize"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.armature.autoside_names(type='XAXIS')
        bpy.ops.armature.symmetrize()
        bpy.context.object.data.use_mirror_x = True
        bpy.ops.armature.select_all(action='DESELECT')

        return {'FINISHED'}


class SPEEDSCULPT_OT_convert_armature(bpy.types.Operator): # Code from Pentan https://gist.github.com/Pentan/3455286
    bl_idname = 'speedsculpt.convert_armature'
    bl_label = "Convert Armature"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        if context.object is not None :
            bpy.ops.object.mode_set(mode = 'OBJECT')

        for selobj in context.selected_objects:
            if selobj.type == 'ARMATURE':
                arm = selobj.data
                if len(arm.bones) <= 0:
                    print("Armature {} has no bones. skip it.".format(arm.name))
                    continue

                verts = []
                faces = []
                vgroups = []
                for abone in arm.bones:
                    head_r = abone.head_radius
                    tail_r = abone.tail_radius
                    bone_len = abone.length
                    tmpverts = [
                        Vector((-head_r, -head_r, head_r)),
                        Vector((head_r, -head_r, head_r)),
                        Vector((head_r, -head_r, -head_r)),
                        Vector((-head_r, -head_r, -head_r)),

                        Vector((-head_r, head_r, head_r)),
                        Vector((head_r, head_r, head_r)),
                        Vector((head_r, head_r, -head_r)),
                        Vector((-head_r, head_r, -head_r)),

                        Vector((-tail_r, bone_len - tail_r, tail_r)),
                        Vector((tail_r, bone_len - tail_r, tail_r)),
                        Vector((tail_r, bone_len - tail_r, -tail_r)),
                        Vector((-tail_r, bone_len - tail_r, -tail_r)),

                        Vector((-tail_r, bone_len + tail_r, tail_r)),
                        Vector((tail_r, bone_len + tail_r, tail_r)),
                        Vector((tail_r, bone_len + tail_r, -tail_r)),
                        Vector((-tail_r, bone_len + tail_r, -tail_r))
                    ]
                    tmpfaces = [
                        (3, 2, 1, 0),

                        (0, 1, 5, 4),
                        (1, 2, 6, 5),
                        (2, 3, 7, 6),
                        (3, 0, 4, 7),

                        (4, 5, 9, 8),
                        (5, 6, 10, 9),
                        (6, 7, 11, 10),
                        (7, 4, 8, 11),

                        (8, 9, 13, 12),
                        (9, 10, 14, 13),
                        (10, 11, 15, 14),
                        (11, 8, 12, 15),

                        (12, 13, 14, 15)
                    ]
                    voffset = len(verts)
                    tmpvgrp = {'name': abone.name, 'verts': []}
                    for i, v in enumerate(tmpverts):
                        verts.append(abone.matrix_local @ v)
                        tmpvgrp['verts'].append(i + voffset)
                    vgroups.append(tmpvgrp)
                    for f in tmpfaces:
                        faces.append((f[0] + voffset, f[1] + voffset, f[2] + voffset, f[3] + voffset))

                # create meshes
                newname = arm.name + "_mesh"
                newmesh = bpy.data.meshes.new(newname)
                newobj = bpy.data.objects.new(newname, newmesh)
                newobj.matrix_world = selobj.matrix_world

                # context.scene.objects.link(newobj)
                context.scene.collection.objects.link(newobj)


                newmesh.from_pydata(verts, [], faces)
                newmesh.update(calc_edges=True)

                for vg in vgroups:
                    newvg = newobj.vertex_groups.new(name=vg['name'])
                    for vid in vg['verts']:
                        newvg.add([vid], 1.0, 'REPLACE')

                submod = newobj.modifiers.new('Subsurf', 'SUBSURF')
                submod.levels = 3

                # bpy.context.object.hide = True
                bpy.ops.object.hide_view_set(unselected=False)

                selobj.select_set(state=False)
                newobj.select_set(state=True)
                context.view_layer.objects.active = newobj

                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subsurf")

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')
        selection = context.selected_objects

        bpy.ops.object.update_dyntopo()

        for obj in selection:
            obj.select_set(state=True)
            context.view_layer.objects.active = obj

        bpy.ops.object.boolean_sculpt_union_difference(operation_type='UNION')

        return {'FINISHED'}



