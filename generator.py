import time
import random
import math
from PIL import Image
from room import Room
from chunk import get_chunk

class Generator:
	def __init__(self):
		self.room_types = []
		self.reset()
	
	def get_chunk(self, position):
		return get_chunk(position, chunk_map=self.chunk_map)
	
	def add_room_type(self, roomtype):
		self.room_types.append(roomtype)
		return self
	
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
		for row in range(0, rows):
			y = math.floor((max_y + y) / 2)
			max_y = 0
			for x in range(0, width):
				position = (int(x + random.randint(-5, 5)), int(y + random.randint(-5, 5)))

				room_type = random.sample(self.room_types, 1)[0]
				while room_type.can_place(position) == False:
					room_type = random.sample(self.room_types, 1)[0]

				size = room_type.size
				room = Room(position, size, room_type, self)

				if room.position[1] > max_y:
					max_y = room.position[1]
		
		# try to create tendrils at the end of the dungeon
		for x in range(0, width, int(width / 10)):
			for i in range(0, random.randint(5, 50)):
				position = (int(x + random.randint(-5, 5)), int(y))

				room_type = random.sample(self.room_types, 1)[0]
				while room_type.can_place(position) == False:
					room_type = random.sample(self.room_types, 1)[0]

				size = room_type.size
				room = Room(position, size, room_type, self)
				

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
			if len(collection) > largest_collection_count:
				largest_collection_count = len(collection)
				largest_collection = collection

		deleted_rooms = set()
		fixed_rooms = 0
		for room in self.rooms:
			if room.all_connected_rooms != largest_collection:
				room.place_hallways(max_dist=15)
				
				if room.all_connected_rooms != largest_collection:
					# remove the room if its broken
					deleted_rooms.add(room)
				else:
					fixed_rooms = fixed_rooms + 1

		# final pruning
		for room in self.rooms:
			if len(room.hallways) == 0:
				deleted_rooms.add(room)

		for room in deleted_rooms:
			room.destroy()

		print(f"Deleted {len(deleted_rooms)} rooms and fixed {fixed_rooms} in {int((time.time() - start) * 1000)}ms")

		for room_type in self.room_types:
			print(f"{room_type.name}: {len(room_type.rooms)}")
		
		return self
	
	def save_image(self, file_name):
		image_x = 0
		image_y = 0
		for room in self.rooms:
			if room.position[0] + room.size[0] > image_x:
				image_x = room.position[0] + room.size[0]

			if room.position[1] + room.size[1] > image_y:
				image_y = room.position[1] + room.size[1]
		
		image = Image.new("RGB", (image_x + 20, image_y + 20), color=(255,255,255,0))
		for room in self.rooms:
			room.draw(image)

		for hallway in self.hallways:
			hallway.draw(image)

		image.save(file_name)