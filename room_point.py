from room_type import RoomType
from simplified_object import SimplifiedObject

##
# A class that will store a point in space, the classification of the room
# that the point is in and the objects that are visible from this point.
##
class RoomPoint:

  ##
  # Class variables for keeping track of all kitchen_points, bedroom_points, bathroom_points and living rooms
  ##
  kitchen_points = []
  living_room_points = []
  bathroom_points = []
  bedroom_points = []

  # All visible objects by room type -- simplified format an full
  visible_objects_in_kitchen_smpl = set()
  visible_objects_in_living_room_smpl = set()
  visible_objects_in_bathroom_smpl = set()
  visible_objects_in_bedroom_smpl = set()

  visible_objects_in_kitchen = {}
  visible_objects_in_living_room = {}
  visible_objects_in_bathroom = {}
  visible_objects_in_bedroom = {}

  # And visible objects names room type
  visible_object_names_in_kitchen = set()
  visible_object_names_in_living_room = set()
  visible_object_names_in_bathroom_points = set()
  visible_object_names_in_bedroom = set()

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
        RoomPoint.living_room_points.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            #print(obj)
            RoomPoint.visible_objects_in_living_room_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_living_room[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_living_room.add(obj['objectType'])
    elif (room_type == RoomType.KITCHEN):
        RoomPoint.kitchen_points.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_kitchen_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_kitchen[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_kitchen.add(obj['objectType'])
    elif (room_type == RoomType.BEDROOM):
        RoomPoint.bedroom_points.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_bedroom_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_bedroom[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_bedroom.add(obj['objectType'])
    elif (room_type == RoomType.BATHROOM):
        RoomPoint.bathroom_points.append(self)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            RoomPoint.visible_objects_in_bathroom_smpl.add(SimplifiedObject(obj))
            RoomPoint.visible_objects_in_bathroom[obj['objectId']] = obj
            RoomPoint.visible_object_names_in_bathroom_points.add(obj['objectType'])

  #######################################################################################

  def getPose(self):
      return self.point_pose

  def getRoomType(self):
      return self.room_type

  def getAllVisibleObjectsAtThisPoint(self):
      return self.visible_objects_at_this_point

  def isObjectVisibleAtThisPoint(self, strObject):
      return strObject in self.visible_object_names

  # get all kitchen_points
  @classmethod
  def getAllkitchen_points(cls):
      return RoomPoint.kitchen_points

  # get all living rooms
  @classmethod
  def getAllLivingRooms(cls):
      return RoomPoint.living_room_points

  # get all bathroom_points
  @classmethod
  def getAllbathroom_points(cls):
      return RoomPoint.bathroom_points

  # get all bedroom_points
  @classmethod
  def getAllbedroom_points(cls):
      return RoomPoint.bedroom_points

  # get all visible objects in all kitchen_points
  @classmethod
  def getAllVisibleObjectsInAllkitchen_points(cls):
      return RoomPoint.visible_objects_in_kitchen

  # get all visible objects in all living rooms
  @classmethod
  def getAllVisibleObjectsInAllLivingRooms(cls):
      return RoomPoint.visible_objects_in_living_room

  # get all visible objects in all bathroom_points
  @classmethod
  def getAllVisibleObjectsInAllbathroom_points(cls):
      return RoomPoint.visible_objects_in_bathroom

  # get all visible objects in all bedroom_points
  @classmethod
  def getAllVisibleObjectsInAllbedroom_points(cls):
      return RoomPoint.visible_objects_in_bedroom

  # get all visible objects in all kitchen_points
  @classmethod
  def getAllVisibleObjectsInAllkitchen_points_smpl(cls):
      return RoomPoint.visible_objects_in_kitchen_smpl

  # get all visible objects in all living rooms
  @classmethod
  def getAllVisibleObjectsInAllLivingRooms_smpl(cls):
      return RoomPoint.visible_objects_in_living_room_smpl

  # get all visible objects in all bathroom_points
  @classmethod
  def getAllVisibleObjectsInAllbathroom_points_smpl(cls):
      return RoomPoint.visible_objects_in_bathroom_smpl

  # get all visible objects in all bedroom_points
  @classmethod
  def getAllVisibleObjectsInAllbedroom_points_smpl(cls):
      return RoomPoint.visible_objects_in_bedroom_smpl

  # get all visible object names in all kitchen_points
  @classmethod
  def getAllVisibleObjectNamesInAllkitchen_points(cls):
      return RoomPoint.visible_object_names_in_kitchen

  # get all visible object names in all living rooms
  @classmethod
  def getAllVisibleObjectNamesInAllLivingRooms(cls):
      return RoomPoint.visible_object_names_in_living_room

  # get all visible object names in all bathroom_points
  @classmethod
  def getAllVisibleObjectNamesInAllbathroom_points(cls):
      return RoomPoint.visible_object_names_in_bathroom_points

  # get all visible object names in all kitchen_points
  @classmethod
  def getAllVisibleObjectNamesInAllbedroom_points(cls):
      return RoomPoint.visible_object_names_in_bedroom
