from room_type import RoomType
from simplified_object import SimplifiedObject

##
# A class that will store points that have been explored in the given scene
# along with the classification of each of those points and objects visible
# from them.
##
class SceneDescription:
  def __init__(self):
    ##
    # Variables for keeping track of all kitchen_points, bedroom_points, bathroom_points and living rooms
    ##
    self.kitchen_points = []
    self.living_room_points = []
    self.bathroom_points = []
    self.bedroom_points = []

    # All visible objects by room type -- simplified format an full
    self.visible_objects_in_kitchen_smpl = set()
    self.visible_objects_in_living_room_smpl = set()
    self.visible_objects_in_bathroom_smpl = set()
    self.visible_objects_in_bedroom_smpl = set()

    self.visible_objects_in_kitchen = {}
    self.visible_objects_in_living_room = {}
    self.visible_objects_in_bathroom = {}
    self.visible_objects_in_bedroom = {}

    # And visible objects names room type
    self.visible_object_names_in_kitchen = set()
    self.visible_object_names_in_living_room = set()
    self.visible_object_names_in_bathroom = set()
    self.visible_object_names_in_bedroom = set()

    # Points of this scene
    self.points_of_scene = []

  def addPoint(self, point_pose, room_type, visible_objects_at_this_point):
    # we don't want to store points where no objects are visible.
    # Those are useless as we can't use them for semantic navigation.
    if (len(visible_objects_at_this_point) < 1):
        return

    new_point = {
        "point_pose" : point_pose,
        "room_type" : room_type,
        "visible_objects_at_this_point" : visible_objects_at_this_point,
        "visible_object_names" : set()
    }

    # store names of the objects visible from this point
    for obj in visible_objects_at_this_point:
        new_point["visible_object_names"].add(obj['objectType'])

    # store the new point in our class collection of points
    self.points_of_scene.append(new_point)

    # store the collections of the room types
    if (room_type == RoomType.LIVING_ROOM):
        self.living_room_points.append(new_point)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            #print(obj)
            self.visible_objects_in_living_room_smpl.add(SimplifiedObject(obj))
            self.visible_objects_in_living_room[obj['objectId']] = obj
            self.visible_object_names_in_living_room.add(obj['objectType'])
    elif (room_type == RoomType.KITCHEN):
        self.kitchen_points.append(new_point)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            self.visible_objects_in_kitchen_smpl.add(SimplifiedObject(obj))
            self.visible_objects_in_kitchen[obj['objectId']] = obj
            self.visible_object_names_in_kitchen.add(obj['objectType'])
    elif (room_type == RoomType.BEDROOM):
        self.bedroom_points.append(new_point)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            self.visible_objects_in_bedroom_smpl.add(SimplifiedObject(obj))
            self.visible_objects_in_bedroom[obj['objectId']] = obj
            self.visible_object_names_in_bedroom.add(obj['objectType'])
    elif (room_type == RoomType.BATHROOM):
        self.bathroom_points.append(new_point)
        # store names of the objects and objects themselves visible from this point
        # by each room type
        for obj in visible_objects_at_this_point:
            #self.visible_object_names.add(obj['objectType'])
            self.visible_objects_in_bathroom_smpl.add(SimplifiedObject(obj))
            self.visible_objects_in_bathroom[obj['objectId']] = obj
            self.visible_object_names_in_bathroom.add(obj['objectType'])

  #######################################################################################

  # Do we have all 4 rooms- Kitchen, bedroom, living room and bathroom?
  def isFullHouse(self):
      return len(self.living_room_points) > 0 and len(self.kitchen_points) > 0 and len(self.bedroom_points) > 0 and len(self.bathroom_points) > 0

  def getAllVisibleObjectsAtThisPoint(self):
      return self.visible_objects_at_this_point

  def isObjectVisibleAtThisPoint(self, strObject, point):
      return strObject in point["visible_object_names"]

  # get all kitchen_points
  def getAllkitchen_points(self):
      return self.kitchen_points

  # get all living rooms
  def getAllLivingRooms(self):
      return self.living_room_points

  # get all bathroom_points
  def getAllbathroom_points(self):
      return self.bathroom_points

  # get all bedroom_points
  def getAllbedroom_points(self):
      return self.bedroom_points

  # get all visible objects in all kitchen_points
  def getAllVisibleObjectsInAllkitchen_points(self):
      return self.visible_objects_in_kitchen

  # get all visible objects in all living rooms
  def getAllVisibleObjectsInAllLivingRooms(self):
      return self.visible_objects_in_living_room

  # get all visible objects in all bathroom_points
  def getAllVisibleObjectsInAllbathroom_points(self):
      return self.visible_objects_in_bathroom

  # get all visible objects in all bedroom_points
  def getAllVisibleObjectsInAllbedroom_points(self):
      return self.visible_objects_in_bedroom

  # get all visible objects in all kitchen_points
  def getAllVisibleObjectsInAllkitchen_points_smpl(self):
      return self.visible_objects_in_kitchen_smpl

  # get all visible objects in all living rooms
  def getAllVisibleObjectsInAllLivingRooms_smpl(self):
      return self.visible_objects_in_living_room_smpl

  # get all visible objects in all bathroom_points
  def getAllVisibleObjectsInAllbathroom_points_smpl(self):
      return self.visible_objects_in_bathroom_smpl

  # get all visible objects in all bedroom_points
  def getAllVisibleObjectsInAllbedroom_points_smpl(self):
      return self.visible_objects_in_bedroom_smpl

  # get all visible object names in all kitchen_points
  def getAllVisibleObjectNamesInAllkitchen_points(self):
      return self.visible_object_names_in_kitchen

  # get all visible object names in all living rooms
  def getAllVisibleObjectNamesInAllLivingRoom_points(self):
      return self.visible_object_names_in_living_room

  # get all visible object names in all bathroom_points
  def getAllVisibleObjectNamesInAllbathroom_points(self):
      return self.visible_object_names_in_bathroom

  # get all visible object names in all kitchen_points
  def getAllVisibleObjectNamesInAllbedroom_points(self):
      return self.visible_object_names_in_bedroom

  ##
  # Gets the names of visible objects in the room specified by room type.
  ##
  def getAllVisibleObjectNamesInThisRoom(self, room_type):
      if RoomType.KITCHEN == room_type:
          return self.getAllVisibleObjectNamesInAllkitchen_points()
      elif RoomType.LIVING_ROOM == room_type:
          return self.getAllVisibleObjectNamesInAllLivingRoom_points()
      elif RoomType.BATHROOM == room_type:
          return self.getAllVisibleObjectNamesInAllbathroom_points()
      elif RoomType.BEDROOM == room_type:
          return self.getAllVisibleObjectNamesInAllbedroom_points()
