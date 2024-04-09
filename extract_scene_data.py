import os
import time
from thortils import (launch_controller,
                      convert_scene_to_grid_map, proper_convert_scene_to_grid_map, proper_convert_scene_to_grid_map_and_poses)
from thortils.scene import SceneDataset
from thortils.utils.visual import GridMapVisualizer
from thortils.agent import thor_reachable_positions
from thortils.grid_map import GridMap

import prior

from gemma_room_classifier import LLMRoomClassifier # LLM room classifier
from room_classifier import RoomClassifier # SVC room classifier
from scene_description import SceneDescription
import pickle

class DataSceneExtractor:
    def __init__(self):
        self.dataset = None
        # If our point only has these common objects visible, then there's little point
        # to classify, because these are common.
        self.common_objs = {'Wall', 'Doorway', 'Window', 'Floor', 'Doorframe'}

        self.lrc = LLMRoomClassifier()
        self.src = RoomClassifier()

    def get_visible_objects_from_collection(self, objects, print_objects = False):
        visible_objects = []

        for obj in objects:
            if obj['visible']:
                if print_objects:
                    print(obj['objectType'] + " : " + str(obj['position']))
                visible_objects.append(obj)

        return visible_objects


    def getDataSet(self):
        if (self.dataset is None):
            self.dataset = prior.load_dataset("procthor-10k", "439193522244720b86d8c81cde2e51e3a4d150cf")
            #print(self.dataset)
        return self.dataset

    def test_data_scene_processing(self, scene_id):
        self.ae_process_proctor_scene(scene_id, self.getDataSet())

    def process_10_data_scenes(self):
        ds = self.getDataSet()
        # scene descriptions. Each of which will contain points of its floorplan
        # that were traversed using the proper_convert_scene_to_grid_map_and_poses
        # method
        # If pickle file for our scene descriptions exists, then load scene
        # descriptions from there, otherwise create an empty collection
        #
        # The number in SVC classified scenes must match the number in LLM classified
        # scenes list.
        scene_descr_llm_fname = "scene_descriptions_llm.pkl"
        scene_descr_svc_fname = "scene_descriptions_svc.pkl"
        if (os.path.isfile(scene_descr_llm_fname) and os.path.isfile(scene_descr_svc_fname)):
            file_llm = open(scene_descr_llm_fname,'rb')
            file_svc = open(scene_descr_svc_fname,'rb')
            scene_descriptions_llm = pickle.load(file_llm)
            scene_descriptions_svc = pickle.load(file_svc)
            file_llm.close()
            file_svc.close()
        else:
            scene_descriptions_llm = []
            scene_descriptions_svc = []

        stored_number_of_scenes = len(scene_descriptions_llm)
        print("Scenes already stored: " + str(stored_number_of_scenes))

        for cnt in range((1 + stored_number_of_scenes), (3 + stored_number_of_scenes)):
            scene_id = "train_" + str(cnt)
            print("Processing " + scene_id)
            (sd_llm, sd_svc) = self.ae_process_proctor_scene(scene_id, ds)
            scene_descriptions_llm.append(sd_llm)
            scene_descriptions_svc.append(sd_svc)

            # store our room points collection into a pickle file. Do it on every
            # scene so that we don't lose anything if stopped prematurely.
            pickle.dump(scene_descriptions_llm, open(scene_descr_llm_fname, "wb"))
            pickle.dump(scene_descriptions_svc, open(scene_descr_svc_fname, "wb"))

    ##
    # Load a PROCTHOR scene specified by the scene_id, build map and classify all
    # visited points belonging to one of the semantic room types. Also build a pkl
    # file with the classification result and the visible objects at that point.
    #
    # The scene_id takes form of <dataset>_<scene_number>, where dataset is one of:
    # train, val, test and scene_number is a number of scene in that set.
    # e.g.: "train_3" or "test_10"
    ##
    def ae_process_proctor_scene(self, scene_id, dataset):
        scene_id_split = scene_id.split("_")
        data_set = scene_id_split[0]
        scene_num = int(scene_id_split[1])
        diffs = []

        print("Loading : " + data_set + "[" + str(scene_num) + "]")

        house = dataset[data_set][scene_num]
        controller = launch_controller({"scene":house})
        #grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)

        keywords = {'num_stops': 100, 'num_rotates': 8, 'sep': 1.25, 'downsample': True}
        (grid_map, observed_pos) = proper_convert_scene_to_grid_map_and_poses(controller,
                                     floor_cut=0.1,
                                     ceiling_cut=1.0,
                                     **keywords)

        # scene description, which will contain points of its floorplan
        # that were traversed using the proper_convert_scene_to_grid_map_and_poses
        # method.
        sd_llm = SceneDescription() # scene description classified with LLM
        sd_svc = SceneDescription() # scene description classified with SVC

        i = 0
        for pos, objs in observed_pos.items():
            print(pos)
            objs_at_this_pos = set()
            for obj in self.get_visible_objects_from_collection(objs):
                objs_at_this_pos.add(obj['objectType'])

            # No point to classify this point if there are no objects
            if (len(objs_at_this_pos) < 1):
                print("Empty set of objects -- skipping")
                continue

            print(objs_at_this_pos)

            if (objs_at_this_pos.issubset(self.common_objs)):
                print("Only common objects -- skipping")
                continue

            rt_llm = self.lrc.classify_room_by_this_object_set(objs_at_this_pos)
            sd_llm.addPoint(pos, rt_llm, objs)

            rt_svc = self.src.classify_room_by_this_object_set(objs_at_this_pos)
            sd_svc.addPoint(pos, rt_svc, objs)

            # If SVC and LLM don't agree to the classification of the room, then
            # tell user and store this difference for reference.
            if (rt_llm != rt_svc):
                print("LLM AND SVC CLASSIFICATIONS DIFFER. LLM :: SVC : " + rt_llm.name + " :: " + rt_svc.name)
                diffs.append({"svc" : rt_svc.name, "llm" : rt_llm.name, "objs" : objs_at_this_pos})

            #i+=1
            #if i > 3:
            #    break

        #print("AE::::::::::::::::::::::;")
        #print(sd.getAllVisibleObjectsInAllLivingRooms_smpl())

        #print(sd.getAllVisibleObjectNamesInAllLivingRooms())

        # store our room points collection into a pickle file
        scene_descr_fname = "scene_descr_llm_" + scene_id + ".pkl"
        pickle.dump(sd_llm, open(scene_descr_fname, "wb"))

        scene_descr_fname = "scene_descr_svc_" + scene_id + ".pkl"
        pickle.dump(sd_svc, open(scene_descr_fname, "wb"))

        diff_fname = "diff_svc_llm_" + scene_id + ".pkl"
        pickle.dump(diffs, open(diff_fname, "wb"))

        #print(len(observed_pos))

        #print(floor_plan)
        for y in range(grid_map.length):
            row = []
            for x in range(grid_map.width):
                if (x,y) in grid_map.free_locations:
                    row.append(".")
                else:
                    #assert (x,y) in grid_map.obstacles
                    if (x,y) in grid_map.obstacles:
                        row.append("x")
                    else:
                        row.append("u")
            print("".join(row))

        return (sd_llm, sd_svc) # return both scene descriptions - classified with LLM and with SVC

    def ae_test(self):
        floor_plan = "FloorPlan22"
        scene_info = SceneDataset.load_single("./scenes", floor_plan)
        controller = launch_controller({"scene":floor_plan})
        grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)

        print(floor_plan)
        for y in range(grid_map.length):
            row = []
            for x in range(grid_map.width):
                if (x,y) in grid_map.free_locations:
                    row.append(".")
                else:
                    assert (x,y) in grid_map.obstacles
                    row.append("x")
            print("".join(row))

    def test_scene_to_grid_map(self):
        floor_plan = "FloorPlan22"
        scene_info = SceneDataset.load_single("./scenes", floor_plan)
        controller = launch_controller({"scene":floor_plan})
        grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)

        print(floor_plan)
        for y in range(grid_map.length):
            row = []
            for x in range(grid_map.width):
                if (x,y) in grid_map.free_locations:
                    row.append(".")
                else:
                    assert (x,y) in grid_map.obstacles
                    row.append("x")
            print("".join(row))

        # Highlight reachable positions
        reachable_positions = thor_reachable_positions(controller)
        highlights = []
        for thor_pos in reachable_positions:
            highlights.append(grid_map.to_grid_pos(*thor_pos))
        viz = GridMapVisualizer(grid_map=grid_map, res=30)
        img = viz.render()
        img = viz.highlight(img, highlights,
                            color=(25, 214, 224), show_progress=True)
        viz.show_img(img)
        time.sleep(10)

    def test_grid_map_save_load(self):
        floor_plan = "FloorPlan1"
        scene_info = SceneDataset.load_single("./scenes", floor_plan)
        controller = launch_controller({"scene":floor_plan})
        grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)
        grid_map.save("temp-grid-map.json")

        grid_map2 = GridMap.load("temp-grid-map.json")

        assert grid_map.free_locations == grid_map2.free_locations
        assert grid_map.width == grid_map2.width
        assert grid_map.length == grid_map2.length
        assert grid_map.grid_size == grid_map2.grid_size

        os.remove("temp-grid-map.json")

if __name__ == "__main__":
    dse = DataSceneExtractor()
    #dse.getDataSet()
    #dse.test_data_scene_processing("val_15")
    dse.process_10_data_scenes()
    #dse.test_scene_to_grid_map()
    #dse.test_grid_map_save_load()
