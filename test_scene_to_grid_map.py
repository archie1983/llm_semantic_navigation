# Copyright 2022 Kaiyu Zheng
#
# Usage of this file is licensed under the MIT License.

import os
import time
from thortils import (launch_controller,
                      convert_scene_to_grid_map, proper_convert_scene_to_grid_map, proper_convert_scene_to_grid_map_and_poses)
from thortils.scene import SceneDataset
from thortils.utils.visual import GridMapVisualizer
from thortils.agent import thor_reachable_positions
from thortils.grid_map import GridMap

import prior

from gemma_room_classifier import LLMRoomClassifier

def get_visible_objects_from_collection(objects, print_objects = False):
    visible_objects = []

    for obj in objects:
        if obj['visible']:
            if print_objects:
                print(obj['objectType'] + " : " + str(obj['position']))
            visible_objects.append(obj)

    return visible_objects

def ae_test_proctor():
    dataset = prior.load_dataset("procthor-10k")
    #dataset
    floor_plan = "FloorPlan22"
    #scene_info = SceneDataset.load_single("./scenes", floor_plan)
    #controller = launch_controller({"scene":dataset})
    #grid_map = convert_scene_to_grid_map(controller, dataset, 0.25)

    #controller = launch_controller({"scene":floor_plan})
    #grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)

    house = dataset["train"][3]
    #controller = Controller(scene=house)
    #print(house)
    controller = launch_controller({"scene":house})
    #grid_map = convert_scene_to_grid_map(controller, floor_plan, 0.25)
    (grid_map, observed_pos) = proper_convert_scene_to_grid_map_and_poses(controller)

    lrc = LLMRoomClassifier()

    for pos, objs in observed_pos.items():
        print(pos)
        objs_at_this_pos = set()
        for obj in get_visible_objects_from_collection(objs):
            objs_at_this_pos.add(obj['objectType'])

        print(objs_at_this_pos)
        lrc.classify_room_by_this_object_set(objs_at_this_pos)

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

def ae_test():
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

def test_scene_to_grid_map():
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

def test_grid_map_save_load():
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
    ae_test_proctor()
    #test_scene_to_grid_map()
    #test_grid_map_save_load()
