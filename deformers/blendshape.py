from maya import cmds
from maya.api import OpenMaya


class Blendshape(object):
    def __init__(self, name):
        self.name = name


    def __str__(self):
        return self.name



    def exists(self):
        if cmds.objExists(self.name):
            if cmds.nodeType(self.name)=="blendShape":
                return True
            else:
                return False
        else:
            return False

    @property
    def envelope(self):
        if self.exists():
            cmds.blendShape(self, q=True, en=True)

    @envelope.setter
    def envelope(self, value):
        if self.exists():
            cmds.blendShape(self,e=True, en = value)
    @property
    def geometryIndices(self):
        if self.exists():
            return cmds.blendShape(self, q=True, gi=True )


    @property
    def geometry(self):
        if self.exists():
            return cmds.blendShape(self,q=True,g=True )


    def create(self, base, targets =[]):
        targets.append(base)
        blendShape = cmds.blendShape(targets , name = self.name)
        self.name = blendShape[0]
    @property
    def targets(self):
        return cmds.aliasAttr(self,q=True)




class targets(object):
    def __init__(self, blendshape, id):
        pass
