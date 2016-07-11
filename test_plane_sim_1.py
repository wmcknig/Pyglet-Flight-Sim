from plane_sim import *

plane1 = Plane(1, [0, 0], 0, apf=lambda r, theta: (0, 0))
plane2 = Plane(1, [1, 1], pi/2, apf=lambda r, theta: (0, 0))
plane_list = [plane1, plane2]

update_plane_lists(plane_list)

print(plane1.plane_list)
print(plane_list)
print(plane2.plane_list)
print(plane_list)
print('')

print(plane1.position)
print(plane2.position)
print(plane1.heading)
print(plane2.heading)
print(plane1.collisions)
print(plane2.collisions)
print(plane1.current_collisions)
print(plane2.current_collisions)
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
print(plane1.current_collisions)
print(plane2.current_collisions)
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
print(plane1.current_collisions)
print(plane2.current_collisions)
