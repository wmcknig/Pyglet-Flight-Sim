from plane_sim import *

waypoints1 = [Waypoint([200, 300]), Waypoint([300, 300]), Waypoint([200, 100])]
plane_list = [Plane(1, [100, 100], 0, waypoints=waypoints1),
		Plane(1, [100, 200], -pi/6),
		Plane(1, [400, 300], pi),
		Plane(1, [450, 300], -pi)]
update_plane_lists(plane_list)
