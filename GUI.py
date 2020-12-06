import time
import sys
import argparse
import math
import numpy as np
import gym
from gym_duckietown.envs import DuckietownEnv

parser = argparse.ArgumentParser()
parser.add_argument("--env-name", default=None)
parser.add_argument("--map-name", default="udem1")
parser.add_argument("--no-pause", action="store_true", help="don't pause on failure")
args = parser.parse_args()

if args.env_name is None:
    env = DuckietownEnv(map_name=args.map_name, domain_rand=False, draw_bbox=False)
else:
    env = gym.make(args.env_name)

obs = env.reset()
env.render()

total_recompense = 0

last_dist = 0
last_angel = 0

start_time = time.time()

last_time = 0


class GUI:
    def __init__(self):
        pass

    def game_loop(self, last_dist=0, last_time=0, total_recompense=0, last_angel=0):
        while True:
            lane_pose = env.get_lane_pos2(env.cur_pos, env.cur_angle)
            distance_to_road_center = lane_pose.dist
            angle_from_straight_in_rads = lane_pose.angle_rad

            k_p = 10
            k_p_1 = 5
            k_d = 1
            k_d_1 = 0.5

            # La vitesse est une valeur entre 0 et 1 (correspond à une vitesse réelle de 0 à 1,2m/s)

            vitesse = 0.2  # You should overwrite this value
            timer = time.time() - last_time

            braquage = (
                    k_p * distance_to_road_center + k_d * angle_from_straight_in_rads + k_p_1 * (
                        distance_to_road_center - last_dist) / timer + k_d_1 * (
                                angle_from_straight_in_rads - last_angel) / timer
            )  # You should overwrite this value

            last_time = time.time()

            last_dist = distance_to_road_center
            last_angel = angle_from_straight_in_rads

            ###### Fini à remplir le code ici

            obs, recompense, fini, info = env.step([vitesse, braquage])
            total_recompense += recompense

            print(
                "étape = %s, recompense instantanée=%.3f, recompense totale=%.3f"
                % (env.step_count, recompense, total_recompense)
            )

            env.render()

            if fini:
                if recompense < 0:
                    print("*** CRASHED ***")
                print("recompense finale = %.3f" % total_recompense)
                break

gui = GUI()
gui.game_loop()
