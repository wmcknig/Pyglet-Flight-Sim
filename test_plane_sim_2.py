from plane_sim import *

"""
Have 2 planes, with the default APF setup, fly directly towards each other,
and observe what occurs.
"""

plane1 = Plane(1, [0, 0], 0, max_turn_rate=pi/15)
plane2 = Plane(1, [0, 4], pi, max_turn_rate=pi/15)
plane_list = [plane1, plane2]
update_plane_lists(plane_list)

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print('')

sim_cycle(plane_list)
move_planes(plane_list)
detect_collisions(plane_list)

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print('')

sim_cycle(plane_list)
move_planes(plane_list)
detect_collisions(plane_list)

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print('')

sim_cycle(plane_list)
move_planes(plane_list)
detect_collisions(plane_list)

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print('')

sim_cycle(plane_list)
move_planes(plane_list)
detect_collisions(plane_list)

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print('')
