from math import pi, sin, cos, sqrt, atan2
from apf import *

class Plane():
	"""
	Represents a plane, contains the functionality of moving the plane, obtaining a
	force vector on the plane based on APF's and processing it, and detecting plane
	collisions.  A plane object contains a list of other plane objects (a global list can
	be passed, each object will remove itself from its own plane object list).  Each plane object
	specifies an APF it projects onto other planes for its collision avoidance, 
	being a	function of r and theta.
	A boundary is also assigned, specifying the extent of the APF for each angle.
	"""
	#note: turning radius is a function of turn rate and velocity
	def __init__(self, speed=1, position=[0, 0], heading=0, waypoints=[], apf=lambda r, theta: (r**2, theta), boundary=lambda theta: 20, max_turn_rate=pi/300):
		self.speed = speed
		self.position = position
		self.heading = self.heading_corrector(heading)
		self.max_turn_rate = max_turn_rate
		self.turn_rate = 0
		self.collision_margin = 2
		self.current_collisions = []
		self.collisions = 0
		self.waypoints = waypoints
		self.plane_list = []
		self.relative_locations = []
		self.apf = apf
		self.new_collision = False
		self.boundary = boundary
		self.force_vector = (0, 0)
		self.min_radius = (self.speed / self.max_turn_rate) + .5 #the added .5 just adds a little safety margin

	def chord_length(self, waypoint):
		"""
		Based on the relative location of the waypoint, determines the chord to the intersection
		of the "waypoint line" and a circle the plane would follow if it turned constantly at
		its maximum rate.
		"""
		return 2 * self.min_radius * sin(abs(waypoint[1]))

	def detect_collision(self, plane):
		"""
		Detects if the plane is colliding with another plane, based on if it
		is within the radius of the other planes speed.
		Update: Resets the new_collision flag to its default position (False).
		"""
		self.new_collision = False
		return self.get_relative_position(plane)[0] <= (plane.speed * self.collision_margin)

	def generate_force_vector(self):
		"""
		Generates the force vector on the plane based on current object attributes.
		"""
		if len(self.waypoints) == 0:
			waypoint, apf_waypoint = None, None
		else:
			apf_waypoint = self.waypoints[0].field
			waypoint = self.get_relative_position(self.waypoints[0])
		self.force_vector = apf_force_vector(self.apf, self.boundary, apf_waypoint, waypoint, self.relative_locations, self.heading)

	def get_plane_list(self, plane_list):
		"""
		Accepts a global list of plane objects in the simulator and makes an internal version that
		excludes the calling plane object.
		"""
		self.plane_list = plane_list
		self.plane_list.remove(self)

	def get_plane_positions(self):
		"""
		Updates a list of the relative locations of other planes, each element in
		the form (r, theta, heading).
		"""
		self.relative_locations = []
		for i in self.plane_list:
			self.relative_locations.append(self.get_relative_position(i))

	def get_relative_position(self, plane):
		"""
		Takes the absolute position of a plane, and its heading, and returns a
		tuple of its position relative to the calling plane object.  Can also be used to get
		the position of a waypoint relative to your plane; waypoint objects work the same
		as plane objects for this method.
		"""
		x_delta = plane.position[0] - self.position[0]
		y_delta = plane.position[1] - self.position[1]
		r = sqrt(x_delta ** 2 + y_delta ** 2)
		theta_north = atan2(-x_delta, y_delta) #angle to other plane if your plane heading is north; note that by our convention, the "y" direction is negative x
		theta = theta_north - self.heading #adjusts for actual heading
		return (r, theta, plane.heading)

	def heading_corrector(self, heading):
		"""
		Corrects a heading to ensure it's between -pi and  pi; this varies from
		the angle correction in the apf file due to different considerations in
		defining polar coordinates versus desired force vector coordinates.
		"""
		heading = heading % (2 * pi)
		if heading < 0:
			return heading + 2 * pi
		return heading

	def record_collision(self):
		"""
		Checks if this plane has collided with another specified plane, and that
		it is a new collision (i.e. it isn't the next "frame" of an earlier
		collision).  If it's a new collision, record it as a current collision
		and increase the collision count.  If there isn't a collision with the
		other plane and said plane is on the current collision list, remove the
		plane from the list.
		Update: controls a flag indicating if a new collision just occurred.
		"""
		for i in self.plane_list:
			if self.detect_collision(i) and i not in self.current_collisions:
				self.current_collisions.append(i)
				self.collisions += 1
				self.new_collision = True
			if not self.detect_collision(i) and i in self.current_collisions:
				self.current_collisions.remove(i)

	def update_position(self):
		"""
		Changes the plane heading by the current turning rate, and then moves the
		plane straightforward by its speed.
		"""
		self.heading += self.turn_rate
		self.position[0] += -sin(self.heading) * self.speed
		self.position[1] += cos(self.heading) * self.speed
	
	def within_waypoint(self):
		"""
		Detects if the plane is within the radius of the current waypoint.  If so, deletes the
		waypoint.
		Update: Checks the chord length along the waypoint line and changes the APF of the
		waypoint if the waypoint is closer than the chord length.
		"""
		if len(self.waypoints) == 0:
			return None
		waypoint_location = self.get_relative_position(self.waypoints[0])
		if self.chord_length(waypoint_location) > waypoint_location[0] and not self.waypoints[0].flipped:
			self.waypoints[0].flip_fields()
		elif self.chord_length(waypoint_location) < waypoint_location[0] and self.waypoints[0].flipped:
			self.waypoints[0].flip_fields()
		if waypoint_location[0] < self.waypoints[0].margin:
			del(self.waypoints[0])


	def yaw(self):
		"""
		Based on the objects polar force vector, determines the instant turning rate of the
		plane.
		"""
		if self.force_vector[1] > self.max_turn_rate:
			self.turn_rate = self.max_turn_rate
		elif self.force_vector[1] < -self.max_turn_rate:
			self.turn_rate = -self.max_turn_rate
		else:
			self.turn_rate = self.force_vector[1]

class Waypoint():
	"""
	Represents a waypoint, defined by a cartesian 2D position, a heading (the reference
	angle for the field), and an artificial potential field.  Also specifies a margin,
	the radius within which a plane is considered to have reached the waypoint.
	"""
	def __init__(self, position=[0, 0], heading=0, field=lambda r, theta: (1, theta + pi),
			alternate_field=lambda r, theta: (1, theta), margin=1):
		self.position = position
		self.heading = heading
		self.field = field
		self.alternate_field = alternate_field
		self.margin = margin
		self.flipped = False

	def flip_fields(self):
		"""
		Switches the values of self.field and self.alternate_field.  Intended
		functionality is to allow for an alternate waypoint field if the waypoint
		is determined to be currently unreachable.
		"""
		self.field, self.alternate_field = self.alternate_field, self.field
		self.flipped = not self.flipped
