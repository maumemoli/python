import bmesh
import bpy
from mathutils import Vector
import numpy as np
from mathutils.bvhtree import BVHTree
import datetime
'''
MeshData:
    create_mesh_data:
        generate a mesh/or bmesh based on the chosen space (local, world, uvs)
        generate a BVHTree from the bmesh/mesh to receive the casted vertex data

    get_vertex_coordinates:


'''


class MeshData (object):
    def __init__(self, obj, deformed=False, world_space=False, uv_space=False):
        self.obj = obj
        self.mesh = obj.data

        self.bvhtree = None  # bvhtree for point casting
        self.transfer_bmesh = None

        self.vertex_map = {}  # the corrispondance map of the uv_vertices to the mesh vert id

        self.get_mesh_data(deformed=deformed, world_space=world_space , uv_space=uv_space)

    @property
    def shape_keys(self):
        if self.mesh.shape_keys:
            return self.mesh.shape_keys.key_blocks

    @property
    def vertex_groups(self):
        self.obj.vertex_groups

    def get_vertex_groups_names(self):
        if not self.vertex_groups:
            return
        group_names=list()
        for group in self.vertex_groups:
            group_names.append(group.name)
        return group_names


    def set_position_as_shape_key(self, shape_key_name="Data_transfer", co=None, activate=False):
        if not self.shape_keys:
            basis = self.obj.shape_key_add()
            basis.name = "Basis"
        shape_key = self.obj.shape_key_add()
        shape_key.name = shape_key_name
        shape_key.data.foreach_set("co", co.ravel())
        if activate:
            shape_key.value=1.0

    def get_mesh_data(self, deformed=False, world_space=False, uv_space=False):
        """
        Builds a BVHTree with a triangulated version of the mesh
        :param deformed: will sample the deformed mesh
        :param transformed:  will sample the mesh in world space
        :param uv_space: will sample the mesh in UVspace
        """
        # create an empity bmesh
        bm = self.generate_bmesh (deformed=deformed , world_space=world_space)
        bm.verts.ensure_lookup_table ()
        if uv_space:  # this is for the uv space
            # resetting the vertex map
            self.vertex_map = {}
            # get the uv_layer
            uv_layer_name = self.mesh.uv_layers.active.name
            uv_id = 0
            for i , uv in enumerate (self.mesh.uv_layers):
                if uv.name == uv_layer_name:
                    uv_id = i
            uv_layer = bm.loops.layers.uv[uv_id]
            bm.faces.ensure_lookup_table ()

            nFaces = len(bm.faces)
            verts = []
            faces = []

            for fi in range (nFaces):
                face_verts = bm.faces[fi].verts
                face = []
                for i , v in enumerate (face_verts):
                    vert_id = len(verts)
                    uv = bm.faces[fi].loops[i][uv_layer].uv
                    verts_coord = Vector((uv.x, uv.y, 0.0))

                    verts.append(verts_coord)

                    if vert_id not in self.vertex_map.keys():

                        self.vertex_map[vert_id] = [v.index]
                    else:
                        if v.index not in self.vertex_map[vert_id]:
                            self.vertex_map[vert_id].append(v.index)
                    face.append(vert_id)
                faces.append(face)

            mesh = bpy.data.meshes.new('{}_PolyMesh'.format (self.obj.name))
            # print(faces)
            mesh.from_pydata(verts, [], faces)

            self.transfer_bmesh = bmesh.new()
            self.transfer_bmesh.from_mesh(mesh)
            bpy.data.meshes.remove(mesh)
        else:
            for v in bm.verts:
                self.vertex_map[v.index] = [v.index]
                self.transfer_bmesh = bm

        # triangulating the mesh
        bmesh.ops.triangulate(self.transfer_bmesh, faces=self.transfer_bmesh.faces[:])
        # self.transfer_bmesh.to_mesh(mesh)

        self.bvhtree = BVHTree.FromBMesh(self.transfer_bmesh)

    def generate_bmesh(self, deformed=True, world_space=True):
        """
        Create a bmesh from the mesh.
        This will capture the deformers too.
        :param deformed:
        :param transformed:
        :param object:
        :return:
        """
        bm = bmesh.new ()
        if deformed:
            depsgraph = bpy.context.evaluated_depsgraph_get ()
            ob_eval = self.obj.evaluated_get (depsgraph)
            mesh = ob_eval.to_mesh ()
            bm.from_mesh (mesh)
            ob_eval.to_mesh_clear ()
        else:
            mesh = self.obj.to_mesh ()
            bm.from_mesh (mesh)
        if world_space:
            bm.transform (self.obj.matrix_world)
            self.evalued_in_world_coords = True
        else:
            self.evalued_in_world_coords = False
        bm.verts.ensure_lookup_table ()

        return bm

    def get_shape_keys_vert_pos(self):
        if not self.shape_keys:
            return
        shape_arrays = {}
        for sk in self.shape_keys:
            if sk.name == "Basis":
                continue
            array = self.convert_shape_key_to_array(sk)
            shape_arrays[sk.name]=(array)
        return shape_arrays


    def convert_shape_key_to_array(self, shape_key):
        v_count = len (self.mesh.vertices)
        co = np.zeros (v_count * 3, dtype=np.float32)
        shape_key.data.foreach_get("co", co)
        co.shape = (v_count, 3)
        return co

    def get_verts_position(self):
        """
        Get the mesh vertex coordinated
        :return: np.array
        """
        v_count = len (self.mesh.vertices)
        co = np.zeros (v_count * 3, dtype=np.float32)
        self.mesh.vertices.foreach_get("co", co)
        co.shape = (v_count, 3)
        return co

    def set_verts_position(self, co):
        self.mesh.vertices.foreach_set("co", co.ravel())
        self.mesh.update()


class MeshDataTransfer (object):
    def __init__(self, source, target, uv_space=False, deformed_source=False,
                 deformed_target=False, world_space=False, search_method="RAYCAST"):
        self.uv_space = uv_space
        self.world_space = world_space
        self.source = MeshData(source, uv_space=uv_space, deformed=deformed_source , world_space=world_space)
        self.target = MeshData(target, uv_space=uv_space, deformed=deformed_target , world_space=world_space)

        self.missed_projections = None
        self.ray_casted = None
        self.hit_faces = None
        self.related_ids = None  # this will store the indexing between

        self.cast_verts(search_method)
        self.barycentric_coords = self.get_barycentric_coords(self.ray_casted, self.hit_faces)

    def transfer_shape_keys(self):
        shape_keys = self.source.get_shape_keys_vert_pos()
        undeformed_verts = self.target.get_verts_position()
        base_coords = self.source.get_verts_position()
        base_transferred_position = self.get_transferred_vert_coords(base_coords)
        if self.world_space:
            mat = np.array(self.target.obj.matrix_world.inverted()) @  np.array(self.source.obj.matrix_world)
            base_transferred_position = self.transform_vertices_array(base_transferred_position, mat)
        base_transferred_position = np.where (self.missed_projections , undeformed_verts , base_transferred_position)
        for sk in shape_keys:
            sk_points = shape_keys[sk]
            if self.world_space:
                mat =np.array(self.source.obj.matrix_world)
                sk_points = self.transform_vertices_array(sk_points, mat)
            transferred_sk = self.get_transferred_vert_coords(sk_points)
            if self.world_space:
                mat = np.array(self.target.obj.matrix_world.inverted())
                transferred_sk = self.transform_vertices_array (transferred_sk , mat)
            transferred_sk = np.where(self.missed_projections, undeformed_verts, transferred_sk)
            # extracting deltas
            transferred_sk = transferred_sk - base_transferred_position + undeformed_verts

            self.target.set_position_as_shape_key(shape_key_name=sk, co=transferred_sk)


    def transfer_vertex_position(self, as_shape_key=False):

        transfer_coord = self.source.get_verts_position()

        #transferred_position = self.calculate_barycentric_location(sorted_coords, self.barycentric_coords)
        transferred_position = self.get_transferred_vert_coords(transfer_coord)
        if self.world_space: #inverting the matrix
            mat = np.array(self.target.obj.matrix_world.inverted()) @  np.array(self.source.obj.matrix_world)
            transferred_position = self.transform_vertices_array(transferred_position, mat)


        undeformed_verts = self.target.get_verts_position()
        transferred_position = np.where(self.missed_projections, undeformed_verts, transferred_position )

        if as_shape_key:
            shape_key_name = "{}.Transferred".format(self.source.obj.name)
            self.target.set_position_as_shape_key(shape_key_name=shape_key_name,co=transferred_position, activate=True)
        else:
            self.target.set_verts_position(transferred_position)
            self.target.mesh.update()

    def get_transferred_vert_coords(self , transfer_coord):

        indexes = self.related_ids.ravel ()
        # sorting verts coordinates
        sorted_coords = transfer_coord[indexes]
        # reshaping the array
        sorted_coords.shape = self.hit_faces.shape
        transferred_position = self.calculate_barycentric_location (sorted_coords , self.barycentric_coords)

        return transferred_position

    @staticmethod
    def transform_vertices_array(array, mat):
        verts_co_4d = np.ones(shape=(array.shape[0] , 4) , dtype=np.float)
        verts_co_4d[: , :-1] = array  # cos v (x,y,z,1) - point,   v(x,y,z,0)- vector
        local_transferred_position = np.einsum ('ij,aj->ai' , mat , verts_co_4d)
        return local_transferred_position[:, :3]

    def cast_verts(self, search_method="RAYCAST"):

        self.target.transfer_bmesh.verts.ensure_lookup_table ()
        v_count = len (self.target.mesh.vertices)
        # np array with coordinates
        self.ray_casted = np.zeros(v_count * 3, dtype=np.float32)
        self.ray_casted.shape = (v_count, 3)
        # np array with the triangles
        self.hit_faces = np.zeros(v_count * 9, dtype=np.float32)
        self.hit_faces.shape = (v_count, 3, 3)

        # get the ids of the hit vertices
        self.related_ids = np.zeros(v_count * 3, dtype=np.int)
        self.related_ids.shape = (v_count, 3)

        self.source.transfer_bmesh.faces.ensure_lookup_table()

        # np bool array with hit verts
        self.missed_projections = np.ones(v_count * 3, dtype=np.bool)
        self.missed_projections.shape = (v_count, 3)
        v_normal = Vector((0.0,0.0, 1.0))
        for v in self.target.transfer_bmesh.verts:
            v_ids = self.target.vertex_map[v.index]  # gets the correspondent vert to the UV_mesh

            if search_method == "CLOSEST":
                projection = self.source.bvhtree.find_nearest (v.co)
            else:
                if not self.uv_space:
                    v_normal = v.normal
                projection = self.source.bvhtree.ray_cast (v.co , v_normal)
            if projection[0]:
                for v_id in v_ids:
                    self.ray_casted[v_id] = projection[0]
                    self.missed_projections[v_id] = False
                    face = self.source.transfer_bmesh.faces[projection[2]]
                    self.hit_faces[v_id] = (face.verts[0].co , face.verts[1].co , face.verts[2].co)
                    # getting the related vertex ids
                    v1_id, v2_id, v3_id = face.verts[0].index , face.verts[1].index , face.verts[2].index
                    v1_id = self.source.vertex_map[v1_id][0]
                    v2_id = self.source.vertex_map[v2_id][0]
                    v3_id = self.source.vertex_map[v3_id][0]
                    v_array = np.array ([v1_id , v2_id , v3_id])

                    self.related_ids[v_id] = v_array
            else:
                for v_id in v_ids:
                    self.ray_casted[v_id] = v.co
        return self.ray_casted, self.hit_faces, self.related_ids

    @staticmethod
    def get_barycentric_coords(verts_co, triangles):
        """
        Calculate the barycentric coordinates
        :param verts_co:
        :param triangles:
        :return:
        """

        barycentric_coords = verts_co.copy()
        # calculate vectors from point f to vertices p1, p2 and p3:

        vert_to_corners = np.copy(triangles)
        vert_to_corners[:, 0] -= verts_co  # f1 point 1 of the triangle coord
        vert_to_corners[:, 1] -= verts_co  # f2 point 2 of the triangle coord
        vert_to_corners[:, 2] -= verts_co  # f3 point 3 of the triangle coord

        # main triangle area
        main_triangle_areas = np.cross((triangles[:, 0] - triangles[:, 1]),
                                        (triangles[:, 0] - triangles[:, 2]))  # va
        # calculate vert corners areas
        va1 = np.cross (vert_to_corners[:, 1], vert_to_corners[:, 2])  # va1
        va2 = np.cross (vert_to_corners[:, 2], vert_to_corners[:, 0])  # va2
        va3 = np.cross (vert_to_corners[:, 0], vert_to_corners[:, 1])  # va2
        # getting the magnitude of main triangle areas
        a = np.sqrt ((main_triangle_areas * main_triangle_areas).sum (axis=1))
        # magnitude of the vert corners areas
        barycentric_coords[:, 0] = np.sqrt((va1 * va1).sum (axis=1)) / a * np.sign (
            (va1 * main_triangle_areas).sum(1))
        barycentric_coords[:, 1] = np.sqrt((va2 * va2).sum (axis=1)) / a * np.sign (
            (va2 * main_triangle_areas).sum(1))
        barycentric_coords[:, 2] = np.sqrt((va3 * va3).sum (axis=1)) / a * np.sign (
            (va3 * main_triangle_areas).sum(1))
        return (barycentric_coords)

    @staticmethod
    def calculate_barycentric_location(uv_coords , coords):
        """
        Calculate the vertex position based on the coords
        :param uv_coords:
        :param coords:
        :return:
        """

        location = uv_coords[:, 0] * coords[:, 0, None] + \
                   uv_coords[:, 1] * coords[:, 1, None] + \
                   uv_coords[:, 2] * coords[:, 2, None]
        return location

    # ================================================DEBUG=============================================================
    @staticmethod
    def create_debug_mesh(obj, co, name):
        print(co.shape[0])
        copy = obj.data.copy()
        print(len(copy.vertices))
        new_obj = bpy.data.objects.new(name , copy)
        bpy.context.scene.collection.objects.link (new_obj)
        copy.vertices.foreach_set("co", co.ravel())
        obj.data.update()
        return  new_obj





# class MeshTransferData (object):
#     """
#     Handle the mesh UVs
#
#     """
#
#     def __init__(self, obj):
#         self.obj = obj
#         self.mesh = obj.data
#
#         self.reletionship_mesh_data = None #this host another MeshTransferData instance for relationship creation
#
#         self.bvhtree = None  # the uv bvhTree
#         self.direction_map = {}
#         self.vertex_map = {}  # the corrispondance map of the uv_vertices to the mesh vert id
#         self.uv_bmesh = None
#         self.evalued_in_world_coords=False
#
#
#     def generate_bmesh(self , deformed=True , transformed=True):
#         """
#         Create a bmesh from the mesh.
#         This will capture the deformers too.
#         :param object:
#         :return:
#         """
#         bm = bmesh.new ()
#         if deformed:
#             depsgraph = bpy.context.evaluated_depsgraph_get ()
#             ob_eval = self.obj.evaluated_get (depsgraph)
#             mesh = ob_eval.to_mesh ()
#             bm.from_mesh (mesh)
#             ob_eval.to_mesh_clear ()
#         else:
#             mesh = self.obj.to_mesh ()
#             bm.from_mesh (mesh)
#         if transformed:
#             bm.transform (self.obj.matrix_world)
#             self.evalued_in_world_coords = True
#         else:
#             self.evalued_in_world_coords = False
#         bm.verts.ensure_lookup_table()
#
#         return bm
#
#     def get_local_data(self, deformed=False):
#         """
#         Get the local data and store it in a BVHTree
#         :return:
#         """
#         self.get_mesh_data(deformed=deformed, transformed=False, uv_space=False)
#
#     def get_world_data(self, deformed=False):
#         """
#         Get the world data and store it in a BVHTree
#         :return:
#         """
#         self.get_mesh_data(deformed=deformed, transformed=True, uv_space=False)
#
#     def get_uv_data(self):
#         """
#         Get the uv data and store it in a BVHTree
#         """
#         self.get_mesh_data(uv_space=True)
#
#     def get_mesh_data(self, deformed=False, transformed=False, uv_space=False):
#         """
#         Builds a BVHTree with a triangulated version of the mesh
#         :param deformed: will sample the deformed mesh
#         :param transformed:  will sample the mesh in world space
#         :param uv_space: will sample the mesh in UVspace
#         """
#         # create an empity bmesh
#         bm = self.generate_bmesh(deformed=deformed, transformed=transformed)
#
#         # resetting the vertex map
#         self.vertex_map = {}
#         self.direction_map = {}
#         # get the uv_layer
#         uv_layer_name = self.mesh.uv_layers.active.name
#         uv_id = 0
#         for i, uv in enumerate(self.mesh.uv_layers):
#             if uv.name == uv_layer_name:
#                uv_id = i
#         uv_layer = bm.loops.layers.uv[uv_id]
#         bm.verts.ensure_lookup_table ()
#         bm.faces.ensure_lookup_table ()
#
#         nFaces = len(bm.faces)
#         verts = []
#         faces = []
#         vert_id = 0
#
#         for fi in range(nFaces):
#             face_verts = bm.faces[fi].verts
#             face = []
#             for i, v in enumerate (face_verts):
#                 vert_id = len(verts)
#                 if uv_space:
#                     uv = bm.faces[fi].loops[i][uv_layer].uv
#                     verts_coord = Vector((uv.x, uv.y, 0.0))
#                 else:
#                     verts_coord = v.co
#                 if verts_coord not in verts:
#                     verts.append(verts_coord)
#                 else:
#                     vert_id = verts.index(verts_coord)
#                 if vert_id not in self.vertex_map.keys():
#                     self.vertex_map[vert_id] = [v.index]
#                 else:
#                     self.vertex_map[vert_id].append(v.index)
#                 face.append(vert_id)
#
#                 if uv_space:
#                     self.direction_map[vert_id] = Vector((0.0, 0.0, 1.0))
#                 else:
#                     self.direction_map[vert_id] = v.normal
#
#             faces.append(face)
#
#         mesh = bpy.data.meshes.new('{}_PolyMesh'.format(self.obj.name))
#         # print(faces)
#         mesh.from_pydata(verts, [], faces)
#
#         self.transfer_bmesh = bmesh.new ()
#         self.transfer_bmesh.from_mesh(mesh)
#         #triangulating the mesh
#         bmesh.ops.triangulate (self.transfer_bmesh ,faces = self.transfer_bmesh.faces[:])
#         # self.transfer_bmesh.to_mesh(mesh)
#
#         self.bvhtree = BVHTree.FromBMesh(self.transfer_bmesh)
#         bpy.data.meshes.remove(mesh)
#
#     def get_3d_transferred_position(self, source, search_method="CLOSEST"):
#         verts_coords = {}
#         self.transfer_bmesh.verts.ensure_lookup_table ()
#         for v in self.transfer_bmesh.verts:
#             mesh_indexes = self.vertex_map[v.index]
#             if search_method == "CLOSEST":
#                 projection = source.bvhtree.find_nearest(v.co)
#             else:
#                 projection = source.bvhtree.ray_cast(v.co, self.direction_map[v.index])
#             # print(projection)
#             if not projection[0]:
#                 verts_coords.append(v.co)
#                 continue
#             for mesh_index in mesh_indexes:
#                 verts_coords.append(projection[0])
#             return verts_coords
#
#     def transfer_verts_position(self, source, search_method="CLOSEST"):
#         barycentric_coords = {}
#         self.transfer_bmesh.verts.ensure_lookup_table ()
#         for v in self.transfer_bmesh.verts:
#             mesh_indexes = self.vertex_map[v.index]
#             if search_method == "CLOSEST":
#                 projection = source.bvhtree.find_nearest(v.co)
#             else:
#                 projection = source.bvhtree.ray_cast(v.co, self.direction_map[v.index])
#             # print(projection)
#             if not projection[0]:
#                 continue
#             for mesh_index in mesh_indexes:
#                 self.mesh.vertices[mesh_index].co = projection[0]
#         self.mesh.update()
#
#     def get_casted_verts(self, source, search_method="CLOSEST"):
#         v_count=len(self.mesh)
#         # np array with coordinates
#         verts_co = np.zeros(v_count * 3, dtype=np.float32)
#         verts_co.shape = (v_count, 3)
#         # np array with the triangles
#         triangles = np.zeros(v_count * 9, dtype=np.float32)
#         triangles.shape = (v_count, 3, 3)
#
#
#         #np bool array with hit verts
#         hit = np.zero(v_count, dtype=np.bool)
#         self.transfer_bmesh.verts.ensure_lookup_table()
#         for v in self.transfer_bmesh.verts:
#             mesh_indexes = self.vertex_map[v.index] # gets the correspondent vert to the UV_mesh
#             if search_method == "CLOSEST":
#                 projection = source.bvhtree.find_nearest(v.co)
#             else:
#                 projection = source.bvhtree.ray_cast(v.co, self.direction_map[v.index])
#             if projection[0]:
#                 for v_id in mesh_indexes:
#                     verts_co[v_id] = projection[0]
#                     hit[v_id] = True
#                     face = source.transfer_bmesh.faces[projection[2]]
#                     triangles[v_id] = (face.verts[0], face.verts[1], face.verts[2])
#
#     @staticmethod
#     def get_baricentric_coords_arrays(triangles, verts_co):
#         # calculate vectors from point f to vertices p1, p2 and p3:
#         vert_to_corners = triangles
#         vert_to_corners[:, 0] -= verts_co
#         vert_to_corners[:, 1] -= verts_co
#         vert_to_corners[:, 2] -= verts_co
#
#
#         f1 = p1 - f
#         f2 = p2 - f
#         f3 = p3 - f
#
#         # calculate the areas (parameters order is essential in this case):
#         va = (p1 - p2).cross(p1 - p3)  # Vector.Cross(p1-p2, p1-p3); #main triangle cross product
#         va1 = f2.cross(f3)  # Vector3.Cross(f2, f3); // p1's triangle cross product
#         va2 = f3.cross(f1)  # Vector3.Cross(f3, f1); // p2's triangle cross product
#         va3 = f1.cross(f2)  # Vector3.Cross(f1, f2); // p3's triangle cross product
#         a = va.length  # va.magnitude; # main triangle area
#         # calculate barycentric coordinates with sign:
#         a1 = va1.length / a * np.sign (va1.dot (va))
#         a2 = va2.length / a * np.sign (va2.dot (va))  # var a2: float = va2.magnitude/a * Mathf.Sign(Vector3.Dot(va, va2));
#         a3 = va3.length / a * np.sign (va3.dot (va))  # var a3: float = va3.magnitude/a * Mathf.Sign(Vector3.Dot(va, va3));
#         # find the uv corresponding to point f (uv1/uv2/uv3 are associated to p1/p2/p3):
#         return (a1 , a2 , a3)
#         # uv = uv1 * a1 + uv2 * a2 + uv3 * a3
#
#
#
#
#     def get_verts_position(self):
#         v_count = len (self.mesh.vertices)
#         co = np.zeros (v_count * 3 , dtype=np.float32)
#         self.mesh.vertices.foreach_get ("co" , co)
#         co.shape = (v_count , 3)
#         return co
#
#     def transfer_uv_verts_position(self, source,as_shape_key=False, search_method="CLOSEST"):
#
#         barycentric_coords = {}
#         source.transfer_bmesh.faces.ensure_lookup_table ()
#         self.transfer_bmesh.verts.ensure_lookup_table ()
#         for v in self.transfer_bmesh.verts:
#             mesh_indexes = self.vertex_map[v.index]
#             if search_method == "CLOSEST":
#                 projection = source.bvhtree.find_nearest(v.co)
#             else:
#                 projection = source.bvhtree.ray_cast(v.co, self.direction_map[v.index])
#             # print(projection)
#             if not projection[0]:
#                 continue
#
#             face = source.transfer_bmesh.faces[projection[2]] #getting the hit face
#             baricentric_coords = self.get_baricentric_coords(face.verts[0].co, face.verts[1].co, face.verts[2].co, v.co)
#             # getting the points in world space
#             uv1 = source.mesh.vertices[source.vertex_map[face.verts[0].index][0]]
#             uv2 = source.mesh.vertices[source.vertex_map[face.verts[1].index][0]]
#             uv3 = source.mesh.vertices[source.vertex_map[face.verts[2].index][0]]
#
#             location = self.get_baricentric_location(uv1.co, uv2.co, uv3.co, baricentric_coords)
#             for mesh_index in mesh_indexes:
#                 barycentric_coords[mesh_index] = location
#                 self.mesh.vertices[mesh_index].co = location
#         self.mesh.update()
#
#     @staticmethod
#     def get_baricentric_coords(p1 , p2 , p3 , f):
#         # calculate vectors from point f to vertices p1, p2 and p3:
#         f1 = p1 - f
#         f2 = p2 - f
#         f3 = p3 - f
#         # calculate the areas (parameters order is essential in this case):
#         va = (p1 - p2).cross(p1 - p3)  # Vector.Cross(p1-p2, p1-p3); #main triangle cross product
#         va1 = f2.cross(f3)  # Vector3.Cross(f2, f3); // p1's triangle cross product
#         va2 = f3.cross(f1)  # Vector3.Cross(f3, f1); // p2's triangle cross product
#         va3 = f1.cross(f2)  # Vector3.Cross(f1, f2); // p3's triangle cross product
#         a = va.length  # va.magnitude; # main triangle area
#         # calculate barycentric coordinates with sign:
#         a1 = va1.length / a * np.sign (va1.dot (va))
#         a2 = va2.length / a * np.sign (va2.dot (va))  # var a2: float = va2.magnitude/a * Mathf.Sign(Vector3.Dot(va, va2));
#         a3 = va3.length / a * np.sign (va3.dot (va))  # var a3: float = va3.magnitude/a * Mathf.Sign(Vector3.Dot(va, va3));
#         # find the uv corresponding to point f (uv1/uv2/uv3 are associated to p1/p2/p3):
#         return (a1 , a2 , a3)
#         # uv = uv1 * a1 + uv2 * a2 + uv3 * a3
#
#     @staticmethod
#     def get_baricentric_location(uv1 , uv2 , uv3 , coord):
#         location = Vector (uv1 * coord[0] + uv2 * coord[1] + uv3 * coord[2])
#         return location
#
#
# #========================================================================================================
# class ShapeKeysHandler(object):
#     def __init__(self, obj):
#         self.obj = obj
#         self.mesh = self.obj.mesh
#
#
#
#




"""
mesh_a = bpy.data.objects["destination"]
mesh_b = bpy.data.objects["source"]
tree_a = TransferData (mesh_a.data)
tree_b = TransferData (mesh_b.data)

tree_b.get_verts_barycentric_uvs (tree_a)
"""