import bpy
l0 = bpy.context.user_preferences.system.solid_lights[0]
l1 = bpy.context.user_preferences.system.solid_lights[1]
l2 = bpy.context.user_preferences.system.solid_lights[2]

l0.use = True
l0.diffuse_color = (0.6096379160881042, 0.6096379160881042, 0.6096379160881042)
l0.specular_color = (0.0, 0.0, 0.0)
l0.direction = (-0.4528301954269409, 0.30188679695129395, 0.8389333486557007)
l1.use = True
l1.diffuse_color = (0.6243075728416443, 0.6243075728416443, 0.6243075728416443)
l1.specular_color = (0.0, 0.0, 0.0)
l1.direction = (0.7547169923782349, 0.46226415038108826, 0.46552565693855286)
l2.use = True
l2.diffuse_color = (0.17659585177898407, 0.17659585177898407, 0.17659585177898407)
l2.specular_color = (0.0, 0.0, 0.0)
l2.direction = (-0.1320754736661911, 0.6226415038108826, 0.7712805271148682)
