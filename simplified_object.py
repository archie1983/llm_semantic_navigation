##
# AI2-THOR objects contain dictionaries, so can't be added to dictionaries or
# sets themselves. If we strip out the offending dictionaries and sets, then
# we can store the information that actually matters to us. This is what we'll
# do here- the stripping part.
##
class SimplifiedObject:
    def __init__(self, ai2_thor_object):
        self.name = ai2_thor_object['name']
        self.objectId = ai2_thor_object['objectId']
        self.objectType = ai2_thor_object['objectType']
        self.x = ai2_thor_object['position']['x']
        self.y = ai2_thor_object['position']['y']
        self.z = ai2_thor_object['position']['z']
        self.rx = ai2_thor_object['rotation']['x']
        self.ry = ai2_thor_object['rotation']['y']
        self.rz = ai2_thor_object['rotation']['z']

    def getName(self):
        return self.name

    def getObjectId(self):
        return self.objectId

    def getObjectType(self):
        return self.objectType

    def getPosX(self):
        return self.x

    def getPosY(self):
        return self.y

    def getPosZ(self):
        return self.z

    def getRotationX(self):
        return self.rx

    def getRotationY(self):
        return self.ry

    def getRotationZ(self):
        return self.rz
