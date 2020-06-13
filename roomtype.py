import random
import chunk
from dist import dist

def add_room_type(room_type):
	room_types.append(room_type)
	return room_type

class Condition:
	def __init__(self, rarity=100, avoid_type=None, avoid_radius=0, min_distance=-50, max_distance=5000000):
		self.rarity = rarity
		self.avoid_type = avoid_type
		self.avoid_radius = avoid_radius
		self.min_distance = min_distance
		self.max_distance = max_distance

class RoomType:
	def __init__(self, size, force_place=False, name="", is_special=False):
		self.chunk_map = {}
		self.size = size
		self.conditions = set()
		self.rooms = set()
		self.color = (0, 0, 0)
		self.force_place = force_place
		self.name = name
		self.is_special = is_special
	
	def serialize(self, file):
		file.write(self.size[0], 1)
		file.write(self.size[1], 1)
	
	# adds a room to our room chunks
	def add_room(self, room):
		chunk.get_chunk(room.position, self.chunk_map).add_room(room)
		self.rooms.add(room)
	
	def remove_room(self, room):
		chunk.get_chunk(room.position, self.chunk_map).remove_room(room)
		self.rooms.discard(room)
	
	def add_rarity_condition(self, rarity):
		self.conditions.add(Condition(
			rarity=rarity
		))
		return self
	
	def add_avoid_condition(self, radius, room_type=None):
		if room_type == None:
			room_type = self
		
		self.conditions.add(Condition(
			avoid_type=room_type,
			avoid_radius=radius,
		))
		return self
	
	# distance on y-axis from 0
	def add_min_distance_condition(self, distance):
		self.conditions.add(Condition(
			min_distance=distance
		))
		return self

	# distance on y-axis from 0
	def add_max_distance_condition(self, distance):
		self.conditions.add(Condition(
			max_distance=distance
		))
		return self
	
	def add_color(self, color):
		self.color = color
		return self
	
	def can_place(self, position):
		for condition in self.conditions:
			if condition.rarity < random.uniform(0, 100):
				return False
			
			if condition.avoid_type != None:
				for room in condition.avoid_type.rooms:
					if dist(room.position, position) < condition.avoid_radius:
						return False
			
			if position[1] < condition.min_distance:
				return False
			
			if position[1] > condition.max_distance:
				return False

		return True