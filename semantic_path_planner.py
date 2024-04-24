import os
import pickle
import prior

from llm_room_classifier import LLMRoomClassifier, LLMType
from room_type import RoomType
from scene_description import SceneDescription, ClassifierType

from thortils import (launch_controller,
                      convert_scene_to_grid_map, proper_convert_scene_to_grid_map, proper_convert_scene_to_grid_map_and_poses)

from thortils.navigation import get_shortest_path_to_object_type
from ae_robot_simulation_control import RobotNavigationControl

##
# This class will analyze harvested scene data and ask LLM:
# 1) In which room is the best chance to find the requested object?
# 2) Near which object should we look first?
#
# Based on the answers we then plan a path to the best choice room, best choice
# object.
##
class SemanticPathPlanner:
    def __init__(self, scene_id):
        scene_descr_fname = "experiment_data/pkl_llama/scene_descr_" + scene_id + ".pkl"
        if os.path.isfile(scene_descr_fname):
            file = open(scene_descr_fname,'rb')
            self.scene_description = pickle.load(file)
            file.close()

            print("Loaded : " + scene_descr_fname + " scene")
        else:
            # if no scenes' data, then nothing to do
            raise Exception("No scenes data file found. Nothing to do.")

        self.scene_id = scene_id
        self.lrc = LLMRoomClassifier(LLMType.LLAMA)
        self.dataset = None
        self.controller = None
        self.rnc = RobotNavigationControl()

        self.ae_load_proctor_scene(self.scene_id)

    def getDataSet(self):
        if (self.dataset is None):
            self.dataset = prior.load_dataset("procthor-10k", "439193522244720b86d8c81cde2e51e3a4d150cf")
            #print(self.dataset)
        return self.dataset

    def ae_load_proctor_scene(self, scene_id):
        dataset = self.getDataSet()

        scene_id_split = scene_id.split("_")
        data_set = scene_id_split[0]
        scene_num = int(scene_id_split[1])
        time_records = []  # List to store time records for each position

        print("Loading : " + data_set + "[" + str(scene_num) + "]")

        house = dataset[data_set][scene_num]

        self.controller = launch_controller({"scene": house, "VISIBILITY_DISTANCE": 3.0})

        self.rnc.set_controller(self.controller)

    def get_path_to(self, object_type):
        #return get_shortest_path_to_object_type(controller, object_id, start_position, start_rotation, **{"return_plan": return_plan})
        (start_position, start_rotation) = self.rnc.get_agent_pos_and_rotation()
        return get_shortest_path_to_object_type(self.controller, object_type, start_position, start_rotation)

    ##
    # Asking LLM to tell us where to look for a bottle of beer
    ##
    def bring_me_a_bottle_of_beer(self, scene_id):
        work_scene = self.scene_description

        #room_to_look_in = self.lrc.where_to_find_this("A bottle of beer")

        #object_names_to_look_at = work_scene.getAllVisibleObjectNamesInThisRoom(ClassifierType.LLM, room_to_look_in)

        #print(object_names_to_look_at)

        #object_to_look_at = self.lrc.where_to_look_first("A fresh, cold, unopened bottle of beer", object_names_to_look_at)

        #path = self.get_path_to(object_to_look_at)
        path = self.get_path_to("Fridge")

        print(str(path))

if __name__ == "__main__":
    spp = SemanticPathPlanner("train_55")
    spp.bring_me_a_bottle_of_beer(2)
