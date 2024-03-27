import os
import time
from thortils import (launch_controller,
                      convert_scene_to_grid_map)
from thortils.scene import SceneDataset
from thortils.utils.visual import GridMapVisualizer
from thortils.agent import thor_reachable_positions
from thortils.grid_map import GridMap

from thortils.navigation import get_shortest_path_to_object

def get_path(controller, object_id, start_position, start_rotation, return_plan):
    return get_shortest_path_to_object(controller, object_id, start_position, start_rotation, **{"return_plan": return_plan})

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

if __name__ == "__main__":
    test_scene_to_grid_map()
    test_grid_map_save_load()
