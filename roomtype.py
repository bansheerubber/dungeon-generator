import random
import chunk
from dist import dist
from tile import RoomTileCollection, NORTH, EAST, SOUTH, WEST

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

		self.collection_prefab = RoomTileCollection()
		for x in range(0, self.size[0]):
			for y in range(0, self.size[1]):
				tile = self.collection_prefab.add_tile((x, y))
				
				wall_normal1 = None
				wall_normal2 = None
				if y == 0:
					wall_normal1 = SOUTH
					if x == self.size[0] - 1:
						wall_normal2 = EAST
					elif x == 0:
						wall_normal2 = WEST
				elif y == self.size[1] - 1:
					wall_normal1 = NORTH
					if x == self.size[0] - 1:
						wall_normal2 = EAST
					elif x == 0:
						wall_normal2 = WEST

				if wall_normal1 != None:
					tile.add_wall(direction=wall_normal1)
				if wall_normal2 != None:
					tile.add_wall(direction=wall_normal2)
				
				# different if statement block so 1 wide/1 height rooms can be generated
				wall_normal1 = None
				wall_normal2 = None
				if x == 0:
					wall_normal1 = EAST
					if y == self.size[1] - 1:
						wall_normal2 = NORTH
					elif y == 0:
						wall_normal2 = SOUTH
				elif x == self.size[0] - 1:
					wall_normal1 = WEST
					if y == self.size[1] - 1:
						wall_normal2 = NORTH
					elif y == 0:
						wall_normal2 = SOUTH
				
				if wall_normal1 != None:
					tile.add_wall(direction=wall_normal1)
				if wall_normal2 != None:
					tile.add_wall(direction=wall_normal2)

	
	def serialize(self, file):
		file.write(self.size[0], 1)
		file.write(self.size[1], 1)

		file.write_break()
	
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