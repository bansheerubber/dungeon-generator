from generator import Generator
from roomtype import RoomType

generator = Generator()

# create standard room types
for width in range(3, 6):
	for height in range(3, 6):
		generator.add_room_type(
			RoomType(
				(width, height),
				name=f"{width}x{height}"
			)
		)

# add special megarooms
for width in range(8, 10):
	for height in range(8, 10):
		generator.add_room_type(
			RoomType(
				(width, height),
				name=f"Big {width}x{height}"
			)
			.add_rarity_condition(1)
			.add_min_distance_condition(30)
		)

Shop = generator.add_room_type(
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

Boss = generator.add_room_type(
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

Spawn = generator.add_room_type(
	RoomType(
		(1, 1),
		force_place=True,
		name="Spawn"
	)
	.add_max_distance_condition(45)
	.add_color((255, 0, 255))
)

Puzzle = generator.add_room_type(
	RoomType(
		(3, 3),
		name="Puzzle"
	)
	.add_rarity_condition(50)
	.add_avoid_condition(15)
	.add_min_distance_condition(25)
	.add_color((25, 230, 25))
)

Maze = generator.add_room_type(
	RoomType(
		(14, 14),
		name="Maze",
		force_place=True,
	)
	.add_avoid_condition(200)
	.add_min_distance_condition(100)
	.add_color((25, 230, 25))
)

MegaMaze = generator.add_room_type(
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

BowlingAlley = generator.add_room_type(
	RoomType(
		(3, 15),
		name="Bowling Alley",
		force_place=True,
	)
	.add_rarity_condition(0.5)
	.add_min_distance_condition(200)
	.add_color((25, 25, 230))
)

generator.generate(100, 50).save_image("egg.png")