import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (1.0, 0.7875243425369263, 0.1923077404499054)
l0.specular_color = (0.27399998903274536, 0.27399998903274536, 0.27399998903274536)
l0.direction = (-0.13131313025951385, 0.5050504803657532, 0.8530421257019043)
l1.use = True
l1.diffuse_color = (0.491937518119812, 0.3484707474708557, 0.13772933185100555)
l1.specular_color = (0.0, 0.0, 0.0)
l1.direction = (0.34343433380126953, -0.5858585834503174, 0.7340453267097473)
l2.use = True
l2.diffuse_color = (1.0, 1.0, 1.0)
l2.specular_color = (0.0, 0.0, 0.0)
l2.direction = (-0.3915141820907593, 0.3386068642139435, -0.8556062579154968)
