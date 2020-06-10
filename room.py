import matplotlib.pyplot as plt
from shapely import geometry
import chunk

class Room:
	def __init__(self, position, size):
		x = position[0]
		y = position[1]
		self.position = position
		self.size = size
		self.square = geometry.Polygon([(x, y), (x + size[0], y), (x + size[0], y + size[1]), (x, y + size[1])])

		self.chunk = chunk.get_chunk(position)
	
	# check to see if we overlap with another room
	def overlaps(self, room):
		return self.square.intersects(room.square)
	
	def plot(self, plotter=plt, alpha=1):
		plotter.fill(*self.square.exterior.xy, alpha=alpha)