from plane_sim import *

"""
Flies a single plane through a series of waypoints, checking what happens.
"""

waypoints = [Waypoint([0, 5]), Waypoint([10, 10]), Waypoint([0, 10])]
plane = Plane(1, waypoints=waypoints)
print(plane.speed)
plane_list = [plane]
update_plane_lists(plane_list)

print(plane.position)
print(plane.heading)
print(plane.force_vector)
for i in plane.waypoints:
	print(i)
print('')
while len(waypoints) != 0:
	sim_cycle(plane_list)
	move_planes(plane_list)
	detect_collisions(plane_list)

	print(plane.position)
	print(plane.heading)
	print(plane.force_vector)
	for i in plane.waypoints:
		print(i)
	print('')

for j in range(20):
	sim_cycle(plane_list)
	move_planes(plane_list)
	detect_collisions(plane_list)

	print(plane.position)
	print(plane.heading)
	print(plane.force_vector)
	for i in plane.waypoints:
		print(i)
	print('')
