from room_type import RoomType
from simplified_object import SimplifiedObject

class ClassifierType(Enum):
    LLM = 1 # LLM classified this
    SVC = 2 # SVC classified this
    GT = 3 # this is ground truth

##
# A class that will store points that have been explored in the given scene
# along with the classification of each of those points and objects visible
# from them.
##
class SceneDescription:
  def __init__(self):
    # All visible objects by room type -- simplified format and full
    self.points_of_scene_smpl = set()

    # Points of this scene
    self.points_of_scene = []

  ##
  # Adding a point to this scene.
  # point_pose - point pose,
  # room_type_llm - LLM assigned class,
  # room_type_svc - SVC assigned class,
  # room_type_gt - Ground Truth class of room,
  # visible_objects_at_this_point,
  # elapsed_time_llm - LLM inference time to classify this point
  # elapsed_time_svc - SVC inference time to classify this point
  ##
  def addPoint(self, point_pose, room_type_llm, room_type_svc, room_type_gt, visible_objects_at_this_point, elapsed_time_llm, elapsed_time_svc):
    # we don't want to store points where no objects are visible.
    # Those are useless as we can't use them for semantic navigation.
    if (len(visible_objects_at_this_point) < 1):
        return

    new_point = {
        "point_pose" : point_pose,
        "room_type_llm" : room_type_llm,
        "room_type_svc" : room_type_svc,
        "room_type_gt" : room_type_gt,
        "visible_objects_at_this_point" : visible_objects_at_this_point,
        "visible_object_names" : set(),
        "elapsed_time_llm": elapsed_time_llm,
        "elapsed_time_svc": elapsed_time_svc
    }

    # store names of the objects visible from this point
    for obj in visible_objects_at_this_point:
        new_point["visible_object_names"].add(obj['objectType'])

    # store the new point in our class collection of points
    self.points_of_scene.append(new_point)
  #######################################################################################

  ##
  # Get all points belonging to the specified class according to the specified classifier.
  # E.g. get_all_points_of_room_type(self, ClassifierType.LLM, RoomType.KITCHEN)
  # would return all kitchen points that were classified as kitchen by LLM
  ##
  def get_all_points_of_room_type(self, classifier_type, rt):
      ret_points = []
      for point in self.points_of_scene:
          if classifier_type == ClassifierType.LLM and point["room_type_llm"] == rt:
              ret_points.append(point)
          elif classifier_type == ClassifierType.SVC and point["room_type_svc"] == rt:
              ret_points.append(point)
          elif classifier_type == ClassifierType.GT and point["room_type_gt"] == rt:
              ret_points.append(point)

      return ret_points

  def getAllVisibleObjectNamesInThisRoom(self, classifier_type, rt):
      points = self.get_all_points_of_room_type(classifier_type, rt)
      ret_set = set()
      for p in points:
          ret_set = ret_set.union(p.visible_object_names)

      return ret_set
