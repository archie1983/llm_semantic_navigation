from room_type import RoomType
from simplified_object import SimplifiedObject

##
# A class that will store a point in space, the classification of the room
# that the point is in and the objects that are visible from this point.
##
class RoomPoint:

  ##
  # Class variables for keeping track of all kitchens, bedrooms, bathrooms and living rooms
  ##
  kitchens = []
  living_rooms = []
  bathrooms = []
  bedrooms = []

  # All visible objects by room type -- simplified format an full
  visible_objects_in_kitchens_smpl = set()
  visible_objects_in_living_rooms_smpl = set()
  visible_objects_in_bathrooms_smpl = set()
  visible_objects_in_bedrooms_smpl = set()

  visible_objects_in_kitchens = {}
  visible_objects_in_living_rooms = {}
  visible_objects_in_bathrooms = {}
  visible_objects_in_bedrooms = {}

  # And visible objects names room type
  visible_object_names_in_kitchens = set()
  visible_object_names_in_living_rooms = set()
  visible_object_names_in_bathrooms = set()
  visible_object_names_in_bedrooms = set()

  def __init__(self, point_pose, room_type, visible_objects_at_this_point):
    self.point_pose = point_pose
    self.room_type = room_type
    self.visible_objects_at_this_point = visible_objects_at_this_point
    self.visible_object_names = set()

    # store names of the objects visible from this point
    for obj in visible_objects_at_this_point:
        self.visible_object_names.add(obj['objectType'])

    # store the collections of the room types
    if (room_type == RoomType.LIVING_ROOM):
        RoomPoint.living_rooms.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            #print(obj)
            RoomPoint.visible_objects_in_living_rooms_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_living_rooms[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_living_rooms.add(obj['objectType'])
    elif (room_type == RoomType.KITCHEN):
        RoomPoint.kitchens.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_kitchens_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_kitchens[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_kitchens.add(obj['objectType'])
    elif (room_type == RoomType.BEDROOM):
        RoomPoint.bedrooms.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_bedrooms_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_bedrooms[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_bedrooms.add(obj['objectType'])
    elif (room_type == RoomType.BATHROOM):
        RoomPoint.bathrooms.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_bathrooms_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_bathrooms[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_bathrooms.add(obj['objectType'])

  #######################################################################################

  def getPose(self):
      return self.point_pose

  def getRoomType(self):
      return self.room_type

  def getAllVisibleObjectsAtThisPoint(self):
      return self.visible_objects_at_this_point

  def isObjectVisibleAtThisPoint(self, strObject):
      return strObject in self.visible_object_names

  # get all kitchens
  @classmethod
  def getAllKitchens(cls):
      return RoomPoint.kitchens

  # get all living rooms
  @classmethod
  def getAllLivingRooms(cls):
      return RoomPoint.living_rooms

  # get all bathrooms
  @classmethod
  def getAllBathrooms(cls):
      return RoomPoint.bathrooms

  # get all bedrooms
  @classmethod
  def getAllBedrooms(cls):
      return RoomPoint.bedrooms

  # get all visible objects in all kitchens
  @classmethod
  def getAllVisibleObjectsInAllKitchens(cls):
      return RoomPoint.visible_objects_in_kitchens

  # get all visible objects in all living rooms
  @classmethod
  def getAllVisibleObjectsInAllLivingRooms(cls):
      return RoomPoint.visible_objects_in_living_rooms

  # get all visible objects in all bathrooms
  @classmethod
  def getAllVisibleObjectsInAllBathrooms(cls):
      return RoomPoint.visible_objects_in_bathrooms

  # get all visible objects in all bedrooms
  @classmethod
  def getAllVisibleObjectsInAllBedrooms(cls):
      return RoomPoint.visible_objects_in_bedrooms

  # get all visible objects in all kitchens
  @classmethod
  def getAllVisibleObjectsInAllKitchens_smpl(cls):
      return RoomPoint.visible_objects_in_kitchens_smpl

  # get all visible objects in all living rooms
  @classmethod
  def getAllVisibleObjectsInAllLivingRooms_smpl(cls):
      return RoomPoint.visible_objects_in_living_rooms_smpl

  # get all visible objects in all bathrooms
  @classmethod
  def getAllVisibleObjectsInAllBathrooms_smpl(cls):
      return RoomPoint.visible_objects_in_bathrooms_smpl

  # get all visible objects in all bedrooms
  @classmethod
  def getAllVisibleObjectsInAllBedrooms_smpl(cls):
      return RoomPoint.visible_objects_in_bedrooms_smpl

  # get all visible object names in all kitchens
  @classmethod
  def getAllVisibleObjectNamesInAllKitchens(cls):
      return RoomPoint.visible_object_names_in_kitchens

  # get all visible object names in all living rooms
  @classmethod
  def getAllVisibleObjectNamesInAllLivingRooms(cls):
      return RoomPoint.visible_object_names_in_living_rooms

  # get all visible object names in all bathrooms
  @classmethod
  def getAllVisibleObjectNamesInAllBathrooms(cls):
      return RoomPoint.visible_object_names_in_bathrooms

  # get all visible object names in all kitchens
  @classmethod
  def getAllVisibleObjectNamesInAllBedrooms(cls):
      return RoomPoint.visible_object_names_in_bedrooms
