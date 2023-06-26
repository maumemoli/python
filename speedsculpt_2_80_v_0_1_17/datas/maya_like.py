import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (0.384, 0.384, 0.384)
l0.specular_color = (0.2333, 0.2333, 0.2333)
l0.direction = (-0.028169013559818268, 0.563380241394043, 0.8257173895835876)
l1.use = True
l1.diffuse_color = (0.119, 0.119, 0.119)
l1.specular_color = (0.07, 0.07, 0.07)
l1.direction = (-0.43661969900131226, -0.3661971688270569, 0.8217437267303467)
l2.use = True
l2.diffuse_color = (0.196, 0.196, 0.196)
l2.specular_color = (0.107, 0.107, 0.107)
l2.direction = (-0.2816901206970215, 0.11267605423927307, 0.9528665542602539)
