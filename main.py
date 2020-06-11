import matplotlib.pyplot as plt
from room import Room
from room import rooms
from room import collections
from hallway import hallways
import roomtype
from roomtype import RoomType
import chunk
import random
import math
import time
from PIL import Image

image_x = 0
image_y = 0

# create standard room types
for width in range(3, 6):
	for height in range(3, 6):
		roomtype.add_room_type(
			RoomType(
				(width, height),
				name=f"{width}x{height}"
			)
		)

# add special megarooms
for width in range(8, 10):
	for height in range(8, 10):
		roomtype.add_room_type(
			RoomType(
				(width, height),
				name=f"Big {width}x{height}"
			)
			.add_rarity_condition(1)
			.add_min_distance_condition(30)
		)

Shop = roomtype.add_room_type(
	RoomType(
		(3, 3),
		force_place=True,
		name="Shop"
	)
	#.add_rarity_condition(1)
	.add_avoid_condition(50)
	.add_min_distance_condition(30)
	.add_color((230, 230, 25))
)

Boss = roomtype.add_room_type(
	RoomType(
		(8, 8),
		force_place=True,
		name="Boss"
	)
	#.add_rarity_condition(1)
	.add_avoid_condition(200)
	.add_min_distance_condition(100)
	.add_color((255, 0, 0))
)

Spawn = roomtype.add_room_type(
	RoomType(
		(1, 1),
		force_place=True,
		name="Spawn"
	)
	.add_max_distance_condition(45)
	.add_color((255, 0, 255))
)

Puzzle = roomtype.add_room_type(
	RoomType(
		(3, 3),
		name="Puzzle"
	)
	.add_rarity_condition(50)
	.add_avoid_condition(15)
	.add_min_distance_condition(25)
	.add_color((25, 230, 25))
)

Maze = roomtype.add_room_type(
	RoomType(
		(14, 14),
		name="Maze",
		force_place=True,
	)
	.add_avoid_condition(200)
	.add_min_distance_condition(100)
	.add_color((25, 230, 25))
)

MegaMaze = roomtype.add_room_type(
	RoomType(
		(25, 25),
		name="Super Maze",
		force_place=True,
	)
	.add_rarity_condition(1)
	.add_avoid_condition(300)
	.add_min_distance_condition(200)
	.add_color((25, 230, 25))
)

# place row of rooms
y = 0
max_y = 0
start = time.time()
for row in range(0, 50):
	y = math.floor((max_y + y) / 2)
	max_y = 0
	for x in range(0, 1000):
		position = (x + random.randint(-5, 5), y + random.randint(-5, 5))

		room_type = random.sample(roomtype.room_types, 1)[0]
		while room_type.can_place(position) == False:
			room_type = random.sample(roomtype.room_types, 1)[0]

		size = room_type.size
		room = Room(position, size, room_type)

		if room.position[0] + size[0] > image_x:
			image_x = room.position[0] + size[0]

		if room.position[1] + size[1] > image_y:
			image_y = room.position[1] + size[1]

		if room.position[1] > max_y:
			max_y = room.position[1]

print(f"Created {len(rooms)} rooms in {int((time.time() - start) * 1000)}ms")

start = time.time()
for room in rooms:
	room.place_hallways()

print(f"Created {len(hallways)} hallways in {int((time.time() - start) * 1000)}ms")

start = time.time()
# repair rooms
largest_collection_count = 0
largest_collection = None
for collection in collections:
	if len(collection) > largest_collection_count:
		largest_collection_count = len(collection)
		largest_collection = collection

deleted_rooms = set()
fixed_rooms = 0
for room in rooms:
	if room.all_connected_rooms != largest_collection:
		room.place_hallways(max_dist=15)
		
		if room.all_connected_rooms != largest_collection:
			# remove the room if its broken
			deleted_rooms.add(room)
		else:
			fixed_rooms = fixed_rooms + 1

# final pruning
for room in rooms:
	if len(room.hallways) == 0:
		deleted_rooms.add(room)

for room in deleted_rooms:
	room.destroy()

print(f"Deleted {len(deleted_rooms)} rooms and fixed {fixed_rooms} in {int((time.time() - start) * 1000)}ms")

for room_type in roomtype.room_types:
	print(f"{room_type.name}: {len(room_type.rooms)}")

image = Image.new("RGB", (image_x + 20, image_y + 20), color=(255,255,255,0))
for room in rooms:
	room.draw(image)

for hallway in hallways:
	hallway.draw(image)

# image.show()
image.save("egg.png")

# plt.axis((0, 100, 0, 100))
# plt.show()