import time
import random
import math
from file import File
from roomtype import RoomType
from PIL import Image
from room import Room
from chunk import get_chunk
from a_star import a_star

class Generator:
	def __init__(self):
		self.room_types = []
		self.reset()
	
	def get_chunk(self, position):
		return get_chunk(position, chunk_map=self.chunk_map)
	
	def add_room_type(self, roomtype):
		self.room_types.append(roomtype)
		return roomtype
	
	def reset(self):
		self.chunk_map = {}
		self.rooms = set()
		self.room_map = {}
		self.hallways = set()
		self.hallway_map = {}
		self.collections = []
	
	def generate(self, width, rows):
		self.reset()

		# place row of rooms
		y = 0
		max_y = 0
		start = time.time()
		room_index = 0
		for row in range(0, rows):
			percent = 0.5
			y = math.floor((y * percent) + (max_y * (1 - percent)))
			max_y = 0
			for x in range(0, width):
				position = (int(x + random.randint(-5, 5) + 5), int(y + random.randint(-5, 5) + 5))

				room_type = random.sample(self.room_types, 1)[0]
				while room_type.can_place(position) == False:
					room_type = random.sample(self.room_types, 1)[0]

				room = Room(position, room_type, self)

				if room.position[1] > max_y:
					max_y = room.position[1]
		
		# try to create tendrils at the end of the dungeon
		# for x in range(0, width, 20):
		# 	new_y = y
		# 	for i in range(0, random.randint(5, 70)):
		# 		position = (int(x + random.randint(-5, 5) + 5), int(y))
		# 		test_position = (int(x + random.randint(-5, 5) + 5), int(new_y))

		# 		room_type = random.sample(self.room_types, 1)[0]
		# 		while room_type.can_place(position) == False:
		# 			room_type = random.sample(self.room_types, 1)[0]

		# 		room = Room(position, room_type, self)

		# 		new_y = room.position[1]

		print(f"Created {len(self.rooms)} rooms in {int((time.time() - start) * 1000)}ms")

		start = time.time()
		for room in self.rooms:
			room.place_hallways()

		print(f"Created {len(self.hallways)} hallways in {int((time.time() - start) * 1000)}ms")

		start = time.time()
		# repair rooms
		largest_collection_count = 0
		largest_collection = None
		for collection in self.collections:
			if len(collection.rooms) > largest_collection_count:
				largest_collection_count = len(collection.rooms)
				largest_collection = collection

		deleted_rooms = set()
		fixed_rooms = 0
		for room in self.rooms:
			if room.collection != largest_collection:
				room.place_hallways(max_dist=15)

				if room.collection != None and len(room.collection.rooms) >= largest_collection_count:
					largest_collection = room.collection
					largest_collection_count = len(room.collection.rooms)
				
				if room.collection == largest_collection:
					fixed_rooms = fixed_rooms + 1

		# final pruning
		for room in self.rooms:
			if room.collection != largest_collection:
				deleted_rooms.add(room)

		for room in deleted_rooms:
			room.destroy()

		print(f"Deleted {len(deleted_rooms)} rooms and fixed {fixed_rooms} in {int((time.time() - start) * 1000)}ms")

		# find the room furthest down and create the boss room there
		Boss = self.add_room_type(
			RoomType(
				(10, 10),
				name="Final Boss",
				is_special=True,
			)
			.add_color((255, 0, 0))
		)

		furthest_y = 0
		furthest_y_room = None
		for room in self.rooms:
			if room.position[1] + room.size[1] > furthest_y:
				furthest_y = room.position[1] + room.size[1]
				furthest_y_room = room
		
		room = Room((furthest_y_room.position[0] + random.randint(-2, 2), furthest_y + 2), Boss, self)
		room.place_hallways(max_dist=50)
	
		# give rooms indices, used for file saving
		room_index = 0
		for room in self.rooms:
			room.index = room_index
			room_index = room_index + 1

		if len(room.hallways) == 0:
			print("FINAL BOSS HAS NO CONNECTIONS")

		for room_type in self.room_types:
			print(f"{room_type.name}: {len(room_type.rooms)}")
		
		return self
	
	def save(self, file_name, blockland=False):
		file = File()

		for room_type in self.room_types:
			room_type.serialize(file)
		file.write_section()

		rooms = list(self.rooms)
		rooms.sort(key=lambda room: room.index)

		for room in rooms:
			room.serialize(file)
		file.write_section()

		for hallway in self.hallways:
			hallway.serialize(file)
		file.write_section()

		# write room connections
		for room in rooms:
			for neighbor in room.connected_rooms:
				file.write(neighbor.index, 4)
			file.write_break()
		file.write_section()

		if blockland == False:
			file.save(file_name)
		else:
			file.save_blockland(file_name)
		
		return self
	
	def save_image(self, file_name):
		image_x = 0
		image_y = 0
		for room in self.rooms:
			if room.position[0] + room.size[0] > image_x:
				image_x = room.position[0] + room.size[0]

			if room.position[1] + room.size[1] > image_y:
				image_y = room.position[1] + room.size[1]
		
		image = Image.new("RGB", (image_x + 10, image_y + 10), color=(255,255,255,0))
		for room in self.rooms:
			room.draw(image)

		for hallway in self.hallways:
			hallway.draw(image)

		image.save(file_name)

		return self
	
	def _color_path(self, path):
		for index in range(1, len(path)):
			previous_room = path[index - 1]
			room = path[index]

			room.overwrite_color = (255, 100, 0)
			if previous_room in room.hallway_map:
				room.hallway_map[previous_room].overwrite_color = (255, 100, 0)
	
	# tries to path from spawn to the boss room
	def shortest_path(self):
		# find the boss room
		boss = None
		for room in self.rooms:
			if room.room_type.name == "Final Boss":
				boss = room
				break
		
		# find the spawn room
		spawn = None
		for room in self.rooms:
			if room.room_type.name == "Spawn":
				spawn = room
				break
		
		path = a_star(spawn, boss)
		if path != None:
			self._color_path(path)
			
			print(f"Path traverses {len(path)} rooms")
		else:
			print("Path not found")
		
		return self
	
	# tries to path to every single occurance of this room type on its way to the boss
	def path_to_all_room_types(self, room_types):
		rooms = []
		chances = {}
		for (room_type, chance) in room_types:
			rooms = rooms + list(room_type.rooms)
			chances[room_type] = chance
		
		rooms.sort(key=lambda room: room.position[1])

		# remove random rooms
		for room in rooms:
			if room.room_type in chances and chances[room.room_type] < random.randint(0, 100):
				rooms.remove(room)

		# find the spawn room
		spawn = None
		for room in self.rooms:
			if room.room_type.name == "Spawn":
				spawn = room
				break
		rooms.insert(0, spawn)

		# find the boss room
		boss = None
		for room in self.rooms:
			if room.room_type.name == "Final Boss":
				boss = room
				break
		rooms.append(boss)

		total_path = []
		last_room = rooms[0]
		for index in range(1, len(rooms)):
			room = rooms[index]

			if room not in total_path:
				path = a_star(last_room, room)
				if path != None:
					total_path = total_path + path
				last_room = room
		
		print(f"Path traverses {len(total_path)} rooms")
		
		self._color_path(total_path)
		
		return self