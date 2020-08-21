from PIL import Image
from generator import Generator
from roomtype import RoomType
from room import Room

from tile import RoomTileCollection, NORTH, EAST, SOUTH, WEST

# image = Image.new("RGB", (50, 50), color=(255,255,255,0))
# test = RoomTileCollection()
# test.add_tile((0, 0)).add_wall(direction=SOUTH).add_wall(direction=EAST)
# test.add_tile((1, 0)).add_wall(direction=SOUTH).add_wall(direction=WEST)
# test.add_tile((0, 1)).add_wall(direction=EAST).add_wall(direction=NORTH)
# test.add_tile((1, 1)).add_wall(direction=WEST).add_wall(direction=NORTH)
# test.draw(image)
# image.save("egg.png")

generator = Generator()

generator.add_difficulty((-100, 75), 0)

for i in range(1, 10):
	generator.add_difficulty((75 * i, 75 + 75 * i), i)

# create standard room types
standard_rooms = {}
for width in range(3, 6):
	for height in range(3, 6):
		if (width, height) not in standard_rooms:
			standard_rooms[(width, height)] = generator.add_room_type(
				RoomType(
					(width, height),
					name=f"{width}x{height}"
				)
			)
			print((width, height))

# # add special megarooms
# mega_rooms = {}
# for width in range(8, 10):
# 	for height in range(8, 10):
# 		mega_rooms[(width, height)] = generator.add_room_type(
# 			RoomType(
# 				(width, height),
# 				name=f"Big {width}x{height}"
# 			)
# 			.add_rarity_condition(1)
# 			.add_min_distance_condition(30)
# 		)

Shop = generator.add_room_type(
	RoomType(
		(2, 2),
		force_place=True,
		name="Shop",
		is_special=True,
	)
	#.add_rarity_condition(1)
	.add_avoid_condition(50)
	.add_min_distance_condition(30)
	.add_color((230, 230, 25))
)

# Boss = generator.add_room_type(
# 	RoomType(
# 		(8, 8),
# 		force_place=True,
# 		name="Boss",
# 		is_special=True,
# 	)
# 	#.add_rarity_condition(1)
# 	.add_avoid_condition(200)
# 	.add_min_distance_condition(100)
# 	.add_color((255, 0, 0))
# )

Spawn = generator.add_room_type(
	RoomType(
		(1, 1),
		force_place=True,
		name="Spawn",
		is_special=True,
	)
	.add_avoid_condition(5)
	.add_max_distance_condition(45)
	.add_color((255, 0, 255))
)

# Puzzle = generator.add_room_type(
# 	RoomType(
# 		(3, 3),
# 		name="Puzzle",
# 		is_special=True,
# 	)
# 	.add_rarity_condition(50)
# 	.add_avoid_condition(15)
# 	.add_min_distance_condition(25)
# 	.add_color((25, 230, 25))
# )

# Maze = generator.add_room_type(
# 	RoomType(
# 		(14, 14),
# 		name="Maze",
# 		force_place=True,
# 		is_special=True,
# 	)
# 	.add_avoid_condition(200)
# 	.add_min_distance_condition(100)
# 	.add_color((25, 230, 25))
# )

# MegaMaze = generator.add_room_type(
# 	RoomType(
# 		(25, 25),
# 		name="Super Maze",
# 		force_place=True,
# 		is_special=True,
# 	)
# 	.add_rarity_condition(1)
# 	.add_avoid_condition(300)
# 	.add_min_distance_condition(200)
# 	.add_color((25, 230, 25))
# )

# BowlingAlley = generator.add_room_type(
# 	RoomType(
# 		(3, 15),
# 		name="Bowling Alley",
# 		force_place=True,
# 		is_special=True,
# 	)
# 	.add_rarity_condition(0.5)
# 	.add_min_distance_condition(200)
# 	.add_color((25, 25, 230))
# )

# width, height
generator.generate(45, 15).shortest_path().save_image("egg.png").save("test.dungeon", blockland=True)