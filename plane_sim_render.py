import pyglet
from resources import *
from math import pi
from plane_sim import *
from sys import argv, path
#import os

path.append("flight paths")
plane_list = __import__(argv[1], fromlist=["plane_list"])
plane_list = plane_list.plane_list

sim_window = pyglet.window.Window(caption="2D APF Flight Sim")
plane_batch = pyglet.graphics.Batch()

for i in plane_list:
	i.sprite = pyglet.sprite.Sprite(
			plane,
			x=int(i.position[0]),
			y=int(i.position[0]),
			batch=plane_batch)
	i.sprite.rotation = int(i.heading * -180 / pi)
	i.sprite.scale = plane_scale


@sim_window.event
def on_draw():
	sim_window.clear()
	plane_batch.draw()

@sim_window.event
def on_close():
	for i in plane_list:
		print(i.collisions)

@sim_window.event
def update(dt):
	sim_cycle(plane_list)
	move_planes(plane_list)
	detect_collisions(plane_list)
	for i in plane_list:
		i.sprite.x = int(i.position[0])
		i.sprite.y = int(i.position[1])
		i.sprite.rotation = int(i.heading * -180 / pi)

if __name__ == "__main__":
	pyglet.clock.schedule_interval(update, 1/30)
	pyglet.app.run()
