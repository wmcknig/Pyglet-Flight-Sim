from plane_sim import *

waypoints1 = [Waypoint([100, 200]), Waypoint([300, 300]), Waypoint([300, 500])]
waypoints2 = [Waypoint([200, 100]), Waypoint([300, 300])]
plane_list = [Plane(1, [100, 100], waypoints=waypoints1), Plane(1, [100, 200], pi, waypoints=waypoints2), Plane(1, [500, 500], 4*pi/3)]
update_plane_lists(plane_list)
