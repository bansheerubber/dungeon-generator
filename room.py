import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collection import Collection
from hallway import Hallway
import chunk
import math
import random

HALLWAY_MAX_DIST = 7

class Room:
	def __init__(self, position, room_type, generator):
		x = position[0]
		y = position[1]
		self.position = position
		self.size = room_type.size
		self.hallways = set()
		self.connected_rooms = set()
		self.hallway_map = {}
		self.chunk = None
		self.index = None
		self.difficulty = -1

		self.overwrite_color = None

		self.is_destroyed = False

		self.generator = generator

		self.room_type = room_type
		self.tile_collection = room_type.collection_prefab.clone_into_owner(self)
		room_type.add_room(self)

		self.set_chunk()

		self.generator.rooms.add(self)
		self.collection = None

		if room_type.force_place == False:
			self.settle()
		else: # re-settle rooms that are in our way
			for x in range(self.position[0] - 1, self.position[0] + self.size[0] + 1):
				for y in range(self.position[1] - 1, self.position[1] + self.size[1] + 1):
					position = (x, y)
					if position in self.generator.room_map:
						self.generator.room_map[position].settle()
			self.settle()

		# determine difficulty from y-position
		for difficulty in generator.difficulties:
			if self.position[1] > difficulty[0] and self.position[1] <= difficulty[1]:
				self.difficulty = generator.difficulties_map[difficulty]

				if generator.color_by_difficulty:
					if difficulty not in generator.difficulty_colors:
						generator.difficulty_colors[difficulty] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
					
					self.overwrite_color = generator.difficulty_colors[difficulty]
	
	def serialize(self, file):
		file.write(self.generator.room_types.index(self.room_type), 2)
		file.write(self.difficulty, 2)
		file.write(self.position[0], 2)
		file.write(self.position[1], 2)

		file.write_break()
	
	def set_chunk(self):
		if self.chunk != None:
			self.chunk.remove_room(self)
		
		self.chunk = self.generator.get_chunk(self.position)
		self.chunk.add_room(self)
	
	# check to see if we overlap with another room
	def overlaps(self, room):
		if(
			self.position[0] <= (room.position[0] + room.size[0])
			and (self.position[0] + self.size[0]) >= room.position[0]
			and self.position[1] <= (room.position[1] + room.size[1])
			and (self.position[1] + self.size[1]) >= room.position[1]
		):
			return True
		else:
			return False
	
	def overlapping_rooms(self):
		overlapping_room = self.chunk.overlaps(self)
		while overlapping_room != None:
			yield overlapping_room
			overlapping_room = self.chunk.overlaps(self)
	
	# makes sure the room does not overlap any other rooms
	def settle(self):
		for x in range(self.position[0], self.position[0] + self.size[0]):
			for y in range(self.position[1], self.position[1] + self.size[1]):
				position = (x, y)
				if position in self.generator.room_map and self.generator.room_map[position] == self:
					self.generator.room_map.pop(position)
		
		for overlapping_room in self.overlapping_rooms():
			y_offset = abs((self.size[1] + 1) - (self.position[1] - overlapping_room.position[1]))

			if y_offset == 0:
				y_offset = y_offset + 1

			self.position = (self.position[0], self.position[1] + y_offset)
			self.set_chunk()

		for x in range(self.position[0], self.position[0] + self.size[0]):
			for y in range(self.position[1], self.position[1] + self.size[1]):
				self.generator.room_map[(x, y)] = self
	
	def draw(self, image):
		color = self.room_type.color
		if self.overwrite_color != None and color == (0, 0, 0):
			color = self.overwrite_color

		if self.tile_collection != None:
			self.tile_collection.draw(image, color)
		else:
			for x in range(self.position[0], self.position[0] + self.size[0]):
				for y in range(self.position[1], self.position[1] + self.size[1]):
					image.putpixel((x + 5, y + 5), color)
	
	def _hallway_positions(self):
		for x in range(self.position[0], self.position[0] + self.size[0]):
			position = (x, self.position[1])
			yield position
		
		for x in range(self.position[0], self.position[0] + self.size[0]):
			position = (x, self.position[1] + self.size[1])
			yield position
		
		for y in range(self.position[1], self.position[1] + self.size[1]):
			position = (self.position[0], y)
			yield position
		
		for y in range(self.position[1], self.position[1] + self.size[1]):
			position = (self.position[0] + self.size[0], y)
			yield position
	
	def _hallway_rooms(self):
		for room in self.chunk.all_rooms():
			bigger_room = self
			smaller_room = room
			if room.size[1] > self.size[1]:
				bigger_room = room
				smaller_room = self
			
			# y-axis check
			if(
				room != self
				and ((
						smaller_room.position[1] > bigger_room.position[1]
						and smaller_room.position[1] < (bigger_room.position[1] + bigger_room.size[1])
					)
					or (
						(smaller_room.position[1] + smaller_room.size[1]) > bigger_room.position[1]
						and (smaller_room.position[1] + smaller_room.size[1]) < (bigger_room.position[1] + bigger_room.size[1])
					)
					or (
						smaller_room.position[1] == bigger_room.position[1]
						and (smaller_room.position[1] + smaller_room.size[1]) == (bigger_room.position[1] + bigger_room.size[1])
					)
				)
			):
				yield (False, room)
			
			bigger_room = self
			smaller_room = room
			if room.size[0] > self.size[0]:
				bigger_room = room
				smaller_room = self

			# x-axis check
			if(
				room != self
				and ((
						smaller_room.position[0] > bigger_room.position[0]
						and smaller_room.position[0] < (bigger_room.position[0] + bigger_room.size[0])
					)
					or (
						(smaller_room.position[0] + smaller_room.size[0]) > bigger_room.position[0]
						and (smaller_room.position[0] + smaller_room.size[0]) < (bigger_room.position[0] + bigger_room.size[0])
					)
					or (
						smaller_room.position[0] == bigger_room.position[0]
						and (smaller_room.position[0] + smaller_room.size[0]) == (bigger_room.position[0] + bigger_room.size[0])
					)
				)
			):
				yield (True, room)
	
	# checks if a point is on the same x-axis as us
	def _is_point_on_x(self, point):
		if(
			point[0] >= self.position[0]
			and point[0] < (self.position[0] + self.size[0])
		):
			return True
		else:
			return False
	
	# checks if a point is on the same y-axis as us
	def _is_point_on_y(self, point):
		if(
			point[1] >= self.position[1]
			and point[1] < (self.position[1] + self.size[1])
		):
			return True
		else:
			return False

	# finds a suitable start location for a hallway along the x-axis of the room
	def _find_x_hallway(self, room, max_dist=HALLWAY_MAX_DIST):
		closest_y = self.position[1]
		closest_y2 = room.position[1] + room.size[1] - 1
		if abs(room.position[1] - self.position[1] + self.size[1] - 1) > abs(room.position[1] - self.position[1]):
			closest_y = self.position[1] + self.size[1] - 1
			closest_y2 = room.position[1]
		
		if abs(closest_y - closest_y2) < max_dist:
			collection = set()
			for x in range(self.position[0], self.position[0] + self.size[0]):
				point = (x, closest_y)
				if(
					room._is_point_on_x(point)
					and (x - 1, closest_y) not in self.hallway_map # make sure there aren't adjacent hallways
					and (x + 1, closest_y) not in self.hallway_map
					and (x - 1, closest_y2) not in room.hallway_map
					and (x + 1, closest_y2) not in room.hallway_map
					and (x, closest_y) not in room.hallway_map
					and (x, closest_y2) not in room.hallway_map
				):
					collection.add(point)
			
			if len(collection) > 0:
				point1 = random.sample(collection, 1)[0]
				point2 = (point1[0], closest_y2)
				
				if point1 in self.generator.hallway_map or point2 in self.generator.hallway_map:
					return None

				# don't make a hallway if our hallway intersects another room or hallway
				iteration = range(point1[1] + 1, point2[1])
				if point1[1] > point2[1]:
					iteration = range(point2[1] + 1, point1[1])
				
				for y in iteration:
					point = (point1[0], y)
					if point in self.generator.room_map or point in self.generator.hallway_map:
						return None
				
				return (point1, point2)
			else:
				return None
		else:
			return None
	
	# finds a suitable start location for a hallway along the y-axis of the room
	def _find_y_hallway(self, room, max_dist=HALLWAY_MAX_DIST):
		closest_x = self.position[0]
		closest_x2 = room.position[0] + room.size[0] - 1
		if abs(room.position[0] - self.position[0] + self.size[0] - 1) > abs(room.position[0] - self.position[0]):
			closest_x = self.position[0] + self.size[0] - 1
			closest_x2 = room.position[0]
		
		if abs(closest_x - closest_x2) < max_dist:
			collection = set()
			for y in range(self.position[1], self.position[1] + self.size[1]):
				point = (closest_x, y)
				if(
					room._is_point_on_y(point)
					and (closest_x, y - 1) not in self.hallway_map # make sure there aren't adjacent hallways
					and (closest_x, y + 1) not in self.hallway_map
					and (closest_x2, y - 1) not in room.hallway_map
					and (closest_x2, y + 1) not in room.hallway_map
					and (closest_x, y) not in room.hallway_map
					and (closest_x2, y) not in room.hallway_map
				):
					collection.add(point)
			
			if len(collection) > 0:
				point1 = random.sample(collection, 1)[0]
				point2 = (closest_x2, point1[1])

				if point1 in self.generator.hallway_map or point2 in self.generator.hallway_map:
					return None

				# don't make a hallway if our hallway intersects another room or hallway
				iteration = range(point1[0] + 1, point2[0])
				if point1[0] > point2[0]:
					iteration = range(point2[0] + 1, point1[0])
				
				for x in iteration:
					point = (x, point1[1])
					if point in self.generator.room_map or point in self.generator.hallway_map:
						return None
				
				return (point1, point2)
			else:
				return None
		else:
			return None
	
	def _add_hallway_from_points(self, room, points):
		hallway = Hallway(points[0], points[1], self.generator)
		self.hallways.add(hallway)
		room.hallways.add(hallway)

		self.connected_rooms.add(room)
		room.connected_rooms.add(self)

		self.hallway_map[points[0]] = hallway
		room.hallway_map[points[1]] = hallway

		self.hallway_map[room] = hallway
		room.hallway_map[self] = hallway

		if self.collection == None and room.collection == None:
			self.collection = Collection(self.generator).add_room(self).add_room(room)
		elif self.collection != None and room.collection == None:
			self.collection.add_room(room)
		elif self.collection == None and room.collection != None:
			room.collection.add_room(self)
		elif self.collection != room.collection:
			self.collection.merge(room.collection)

	def place_hallways(self, max_dist=HALLWAY_MAX_DIST):
		for (is_xaxis, room) in self._hallway_rooms():
			if room not in self.connected_rooms:
				points = self._find_x_hallway(room, max_dist=max_dist)
				if points != None:
					self._add_hallway_from_points(room, points)

				points = self._find_y_hallway(room, max_dist=max_dist)
				if points != None:
					self._add_hallway_from_points(room, points)
	
	def destroy(self):
		self.chunk.remove_room(self)
		self.room_type.remove_room(self)
		
		self.generator.rooms.remove(self)
		self.is_destroyed = True
		if self.collection != None:
			self.collection.remove_room(self)
		
		for neighbor in self.connected_rooms:
			neighbor.connected_rooms.discard(self)
		
		for hallway in self.hallways:
			hallway.destroy()
		
		for x in range(self.position[0], self.position[0] + self.size[0]):
			for y in range(self.position[1], self.position[1] + self.size[1]):
				position = (x, y)
				if position in self.generator.room_map:
					self.generator.room_map.pop(position)
		
		self.position = None