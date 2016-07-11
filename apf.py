from math import pi, sqrt, sin, cos, atan2

def add_polar_vector(vector_1, vector_2):
	"""
	Adds two 2D polar vectors together.
	"""
	x1, y1 = vector_1[0] * sin(vector_1[1]), vector_1[0] * cos(vector_1[1])
	x2, y2 = vector_2[0] * sin(vector_2[1]), vector_2[0] * cos(vector_2[1])
	r = sqrt((x1 + x2) ** 2 + (y1 + y2) ** 2)
	theta = atan2((x1 + x2), (y1 + y2))
	return (r, radian_angle_corrector(theta))

def vector_reference_shift(vector, other_heading, your_heading):
	"""
	Takes a vector whose angle is defined relative to a particular heading
	and changes it to be relative to the heading specified in your_heading.
	"""
	return (vector[0], radian_angle_corrector(vector[1] + heading_converter(other_heading, your_heading)))

def field_boundary(theta): #this particular function is an example
	"""
	Defines the boundary containing an artificial potential field, in
	polar coordinates (radians).  For each angle (with 0 radians as the
	front of the APF-providing aircraft), there is a distance r in that
	angle direction where the boundary is.  The positive anglular
	direction is counter-clockwise.  Theta is the location of your
	aircraft relative to the other aircraft.  Returns the distance
	from the plane to the field boundary in that direction.
	"""
	return .5

def potential_field(r, theta): #this particular function is an example
	"""
	Specifies a 2D artificial potential field, based on the location
	relative to the plane creating the APF (specified in polar coordinates).
	Returns the force vector in the APF at the specified point, relative
	to the plane creating the APF.
	"""
	return ((1 / (r ** 2)), theta)

def waypoint_field(r, theta): #this is an example function
	"""
	Specifies the APF of a waypoint, in polar coordinates relative to the
	waypoint center.  0 degrees is north.
	"""
	return (1, theta + pi)

def radian_angle_corrector(angle):
	"""
	Accepts a radian value and translates it into a radian value from
	-pi to pi radians.
	"""
	angle = angle % (2 * pi)
	if angle > pi:
		return angle - (2 * pi)
	if angle < -pi:
		return angle + (2 * pi)
	return angle

def heading_converter(other_heading, reference_heading):
	"""
	Takes the absolute heading of two aircraft, returns the difference in
	heading angle relative to the latter.
	"""
	return radian_angle_corrector(other_heading - reference_heading)

def angle_reference_conversion(other_plane, your_heading):
	"""
	Takes the angle location of another aircraft relative to yours and
	its absolute heading, returns the location of your aircraft, in polar
	coordinates, relative to it.  other_plane is a tuple from the sequence
	of other detected planes.  Note that the returned tuple does NOT
	account for heading; that is irrelevant for how this function is used
	in this software.
	"""
	return (other_plane[0], radian_angle_corrector((other_plane[1]+pi) + heading_converter(your_heading, other_plane[2])))

def apf_force_vector(apf_function, apf_boundary, apf_waypoint, waypoint, other_planes, your_heading):
	"""
	Returns a 2D force vector, defined in polar coordinates relative to
	your plane (0 radians is the direction your plane is facing).
	Note: APF functions and boundaries should be defined over the theta domain -pi to pi.
	"""
	if waypoint is None or apf_waypoint is None:
		force_vector = (0, 0)
	else:
		relative_to_waypoint = angle_reference_conversion(waypoint, your_heading)
		force_vector = apf_waypoint(relative_to_waypoint[0], relative_to_waypoint[1])
		force_vector = vector_reference_shift(force_vector, waypoint[2], your_heading)
	for i in other_planes:
		relative_to_other = angle_reference_conversion(i, your_heading)
		if relative_to_other[0] > apf_boundary(relative_to_other[1]):
			continue
		force_relative_to_other = apf_function(relative_to_other[0], relative_to_other[1])
		force_relative_to_you = vector_reference_shift(force_relative_to_other, i[2], your_heading)
		force_vector = add_polar_vector(force_vector, force_relative_to_you)
	return force_vector

#next_waypoint = (500, 0, 0) #sample location of next waypoint, relative to your plane; note that waypoints have headings, this one is north
#other_planes = [(5, -pi/4, pi/2), (3, 0, -pi/4), (.5, 3*pi/4, pi), (.5, 5*pi/4, 0)] #first element in each tuple is distance, second is angle from your plane, third is absolute heading

#print(apf_force_vector(potential_field, field_boundary, waypoint_field, next_waypoint, [], 0)) #debug
