from plane_class import *
from copy import copy

def detect_collisions(plane_list):
	for i in plane_list:
		i.record_collision()

def move_planes(plane_list):
	for i in plane_list:
		i.update_position()
		i.within_waypoint()

def sim_cycle(plane_list):
	for i in plane_list:
		i.get_plane_positions()
		i.generate_force_vector()
		i.yaw()

def update_plane_lists(plane_list):
	for i in plane_list:
		i.get_plane_list(copy(plane_list))

def main(plane_list):
	update_plane_lists(plane_list)
	while True:
		sim_cycle(plane_list)
		move_planes(plane_list)
		detect_collisions(plane_list)
