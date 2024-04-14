import os
import pickle

from gemma_room_classifier import LLMRoomClassifier
from room_type import RoomType
from scene_description import SceneDescription

##
# This class will analyze harvested scene data and ask LLM:
# 1) In which room is the best chance to find the requested object?
# 2) Near which object should we look first?
#
# Based on the answers we then plan a path to the best choice room, best choice
# object.
##
class SemanticPathPlanner:
    def __init__(self):
        scene_descr_fname = "pkl/scene_descriptions_llm.pkl"
        if os.path.isfile(scene_descr_fname):
            file = open(scene_descr_fname,'rb')
            self.scene_descriptions = pickle.load(file)
            file.close()

            print("Loaded : " + str(len(self.scene_descriptions)) + " scenes")
        else:
            # if no scenes' data, then nothing to do
            raise Exception("No scenes data file found. Nothing to do.")

        self.lrc = LLMRoomClassifier()


    ##
    # Asking LLM to tell us where to look for a bottle of beer
    ##
    def bring_me_a_bottle_of_beer(self, scene_id):
        work_scene = self.scene_descriptions[scene_id]

        room_to_look_in = self.lrc.where_to_find_this("A bottle of beer")

        object_names_to_look_at = work_scene.getAllVisibleObjectNamesInThisRoom(room_to_look_in)

        print(object_names_to_look_at)

        object_to_look_at = self.lrc.where_to_look_first("A fresh, cold, unopened bottle of beer", object_names_to_look_at)

if __name__ == "__main__":
    spp = SemanticPathPlanner()
    spp.bring_me_a_bottle_of_beer(2)
