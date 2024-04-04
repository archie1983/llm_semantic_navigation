# Importing the necessary libraries for AI2-THOR to run

#!pip install --upgrade ai2thor ai2thor-colab &> /dev/null
import ai2thor
import ai2thor_colab
import time
import math
from typing import Dict, List

from ai2thor.controller import Controller
from ai2thor_colab import (
    plot_frames,
    show_objects_table,
    side_by_side,
    overlay,
    show_video
)

import prior

# Class for controlling robot navigation. This is where we will have all the navigation commands.
# This has NOT yet got the LLM connected, but merely a set of tools to move the robot and to interact
# with the simulation environment.
class RobotNavigationControl:
    is_DEBUG = False

    def start_procthor(self):
        dataset = prior.load_dataset("procthor-10k")
        #dataset
        house = dataset["train"][0]
        type(house), house.keys(), house

        controller = Controller(scene=house)

    # Starts server
    def start_ai2_thor(self):
        ai2thor_colab.start_xserver()
        "AI2-THOR Version: " + ai2thor.__version__

    # Initialises controller
    def initialise_controller(self):
        self.controller = Controller(
            agentMode="default",
            visibilityDistance=3,
            scene="FloorPlan209",
            # image modalities
            #renderDepthImage=False,
            #renderInstanceSegmentation=False,
            # camera properties
            width=400,
            height=400,
            fieldOfView=120,
            # step sizes
            gridSize=0.25,
            snapToGrid=True,
            #rotateStepDegrees=15,
        )

        # If debug is enabled, then print scene name and a few other things.
        if (self.is_DEBUG):
            event = self.controller.step(action="RotateRight")
            metadata = event.metadata
            print(event, event.metadata.keys())
            print("sceneName : " + self.controller.last_event.metadata["sceneName"])
            print("agent_pos : " + str(self.controller.last_event.metadata["agent"]["position"]))
            print("agent_rtn : " + str(self.controller.last_event.metadata["agent"]["rotation"]))
            #print("actionReturn : " + controller.last_event.metadata["actionReturn"])


        event = self.controller.step(
            action="AddThirdPartyCamera",
            position=dict(x=-4.25, y=2, z=-2.5),
            rotation=dict(x=90, y=0, z=0),
            fieldOfView=120
        )

    # Get robot's current position and rotation in format that Thortils use
    def get_agent_pos_and_rotation(self):

        pos = (self.controller.last_event.metadata["agent"]["position"]["x"], self.controller.last_event.metadata["agent"]["position"]["y"], self.controller.last_event.metadata["agent"]["position"]["z"])
        rtn = (self.controller.last_event.metadata["agent"]["rotation"]["x"], self.controller.last_event.metadata["agent"]["rotation"]["y"], self.controller.last_event.metadata["agent"]["rotation"]["z"])

        return (pos, rtn)

    # Exposing plot_frames function from AI2-THOR
    def show_current_robot_view(self, ev):
        plot_frames(ev.third_party_camera_frames[0])

    # Return current controller
    def get_current_controller(self):
        return self.controller

    # Return 1st object ID of the required object type specified by name
    def get_obj_id(self, obj_name):
        obj_of_interest = self.validate_object_in_collection(obj_name, self.get_visible_objects())
        #print(obj_of_interest)
        return obj_of_interest['objectId']

    # Purely for debug - shows where the robot is, where the target is and the list of available positions
    # that can be navigated to.
    def print_world_state(self, target_name):
        obj_navigate_to = self.validate_object_in_collection(target_name, self.get_visible_objects())

        print("target pos : " + str(obj_navigate_to['position']))
        print("agent pos : " + str(self.controller.last_event.metadata["agent"]["position"]))

        #reachable_positions = self.controller.step(action="GetReachablePositions").metadata["actionReturn"]
        #print("reachable cells : " + str(reachable_positions))
        rc = self.get_reachable_cells_2d()
        print("reachable cells : " + str(rc))

    # Takes the list of available positions to navigate to, throws out the vertical dimension of each of them
    # (key: y) and creates a new list of these cells containing only 2d information.
    def get_reachable_cells_2d(self):
        reachable_positions = self.controller.step(action="GetReachablePositions").metadata["actionReturn"]

        positions_2d = []

        for pos in reachable_positions:
            positions_2d.append((pos["x"], pos["z"]))

        return positions_2d

    # Print a table of all objects in the scene
    def show_all_objects(self):
        show_objects_table(self.controller.last_event.metadata['objects'])
        print(self.controller.last_event.metadata['objects'])

    # Rotate left by given number of degrees degrees
    def rotate_left(self, deg):
        frames = []
        for _ in range(int(deg) // 5):
            frames.append(self.controller.step(action="RotateLeft", degrees=5).frame)
            time.sleep(0.05)

    # Rotate right by given number of degrees degrees
    def rotate_right(self, deg):
        frames = []
        for _ in range(int(deg) // 5):
            frames.append(self.controller.step(action="RotateRight", degrees=5).frame)
            time.sleep(0.05)

    # Rotate right or left depending on the degree (positive degree- right, negative - left)
    def rotate_by_degree(self, deg):
        if (deg < 0):
            self.rotate_left(abs(deg))
        else:
            self.rotate_right(abs(deg))

    # Store visible objects in the self.visible_objects collection and print them out if needed
    def get_visible_objects(self, print_objects = False):
        objects = self.controller.last_event.metadata['objects']
        visible_objects = []

        for obj in objects:
            if obj['visible']:
                if print_objects:
                    print(obj['objectType'] + " : " + str(obj['position']))
                visible_objects.append(obj)

        return visible_objects

    # Find the closest positon from the given reachable positions to the given object position using
    # Pythagorean theorem.
    def closest_position(self, object_position: Dict[str, float], reachable_positions: List[Dict[str, float]]) -> Dict[str, float]:
        out = reachable_positions[0]
        min_distance = float('inf')
        for pos in reachable_positions:
            # NOTE: y is the vertical direction, so only care about the x/z ground positions
            dist = sum([(pos[key] - object_position[key]) ** 2 for key in ["x", "z"]])
            if dist < min_distance:
                min_distance = dist
                out = pos
        return out

    # Finds the given object name in the given collection of objects and if found, returns the actual object
    def validate_object_in_collection(self, obj_name, obj_collection):
        obj_names = sorted([obj["objectType"] for obj in obj_collection])

        try:
            assert obj_name in obj_names
        except AssertionError:
            print(obj_name + " is not visible!!!!!!!!!!!!!!!!")
            return None

        obj_of_interest = next(obj for obj in obj_collection if obj["objectType"] == obj_name)
        return obj_of_interest

    # Navigate to object defined by the name in the input
    def navigate_to_object(self, obj_name):
        #plot_frames(self.controller.last_event)
        obj_navigate_to = self.validate_object_in_collection(obj_name, self.get_visible_objects())

        # Can't navigate to an unknown object
        if (obj_navigate_to is None):
            return

        reachable_positions = self.controller.step(action="GetReachablePositions").metadata["actionReturn"]

        pos_navigate_to = self.closest_position(obj_navigate_to['position'], reachable_positions)

        #print(pos_navigate_to)

        self.controller.step(action="Teleport", **pos_navigate_to)
        #plot_frames(self.controller.last_event)

    def execute_action_plan(self, plan):
        for act in plan:
            self.controller.step(action=act[0])
            time.sleep(0.2)

    # Print pose of the object defined by the name in the input
    def print_pose_of_object(self, obj_name):
        obj_of_interest = self.validate_object_in_collection(obj_name, self.controller.last_event.metadata['objects'])

        # Unknown object
        if (obj_of_interest is None):
            return

        print("position of " + obj_name + " : " + str(obj_of_interest["position"]))
        print("rotation of " + obj_name + " : " + str(obj_of_interest["rotation"]))

    # Print current pose of robot
    def print_current_pose_of_robot(self):
        print("agent_pos : " + str(self.controller.last_event.metadata["agent"]["position"]))
        print("agent_rtn : " + str(self.controller.last_event.metadata["agent"]["rotation"]))

    # Calculate angle from the target that we need to rotate by to face the target
    def get_angle_offset_from_target(self, obj_name):
        obj_of_interest = self.validate_object_in_collection(obj_name, self.controller.last_event.metadata['objects'])

        # Unknown object
        if (obj_of_interest is None):
            return None

        robot_position = self.controller.last_event.metadata["agent"]["position"]

        # Using formula tg(alpha) = a/b to find relative angle from robot to object
        #tg_alpha = (robot_position["z"] - obj_of_interest["position"]["z"]) / (robot_position["x"] - obj_of_interest["position"]["x"])
        z_diff = (robot_position["z"] - obj_of_interest["position"]["z"])
        x_diff = (robot_position["x"] - obj_of_interest["position"]["x"])
        #print(math.degrees(math.atan2(z_diff, x_diff)))
        return math.degrees(math.atan2(z_diff, x_diff))

    # Rotate to face the selected target
    def rotate_to_face_target(self, obj_name):
        angle_to_target = self.get_angle_offset_from_target(obj_name)

        if (angle_to_target is None):
            print(obj_name + " not visibile")
            return

        current_robot_yaw = self.controller.last_event.metadata["agent"]["rotation"]["y"]

        self.rotate_by_degree(angle_to_target - current_robot_yaw)
        #print("rotating by: " + str(angle_to_target - current_robot_yaw) + " " + str(angle_to_target) + " " + str(current_robot_yaw))

    # Get ceiling camera image -- can try using this if you don't like the 3rd camera set up earlier.
    def get_ceiling_image(self):
        # puts the camera in the ceiling, then puts it back with the robot
        event = self.controller.step('ToggleMapView')
        self.controller.step('ToggleMapView')
        return event.frame
