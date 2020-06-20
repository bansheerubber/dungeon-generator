from wall import RoomWall

NORTH = (0, 1)
EAST = (1, 0)
SOUTH = (0, -1)
WEST = (-1, 0)

def direction_to_color(direction):
	if direction == NORTH:
		return (255, 0, 0)
	elif direction == EAST:
		return (0, 255, 0)
	elif direction == SOUTH:
		return (0, 0, 255)
	elif direction == WEST:
		return (255, 0, 255)
	else:
		raise Exception("Invalid direction to color")

def direction_to_index(direction):
	if direction == NORTH:
		return 0
	elif direction == EAST:
		return 1
	elif direction == SOUTH:
		return 2
	elif direction == WEST:
		return 3
	else:
		raise Exception("Invalid direction to index")

def index_to_direction(index):
	if index == 0:
		return NORTH
	elif index == 1:
		return EAST
	elif index == 2:
		return SOUTH
	elif index == 3:
		return WEST
	else:
		raise Exception("Invalid index")

def expect_corners_to_be(direction): # if we're on the same tile, use this to figure out what walls are our corners
	if direction == NORTH or direction == SOUTH:
		return (EAST, WEST)
	elif direction == EAST or direction == WEST:
		return (NORTH, SOUTH)
	else:
		raise Exception("Invalid direction")
	
class RoomTile:
	def __init__(self, position, collection=None):
		self.collection = collection
		self.position = position
		self.walls = [None, None, None, None]
	
	def add_wall(self, index=None, direction=None):
		if index != None:
			direction = index_to_direction(index)
		elif direction != None:
			index = direction_to_index(direction)
		elif direction == None:
			raise Exception("No index or direction")

		new_wall = RoomWall(direction, self)
		self.walls[index] = new_wall
		# search for adjacent walls on this tile (corners)
		for wall in self.walls:
			(direction1, direction2) = expect_corners_to_be(new_wall.normal)
			if wall != None and (wall.normal == direction1 or wall.normal == direction2):
				new_wall.add_adjacent(wall)
		
		# search for adjacent walls on other tiles (straights)
		for index in range(0, 4):
			direction = index_to_direction(index)
			position = (
				self.position[0] + direction[0],
				self.position[1] + direction[1]
			)
			if position in self.collection.tile_map:
				wall = self.collection[position]
				if wall != None and new_wall.normal == wall.normal:
					new_wall.add_adjacent(wall)
		
		return self

# collection of tiles and their walls, can be instansiated without an owner for use in RoomTypes
class RoomTileCollection:
	def __init__(self, room=None):
		self.tiles = set()
		self.tile_map = {} # maps position to tile
		self.room = room
	
	def add_tile(self, position):
		room_position = (0, 0)
		if self.room != None:
			room_position = self.room.position
		
		tile = RoomTile(position, self)
		self.tiles.add(tile)
		return tile

	def clone_into_owner(self, room):
		new_collection = RoomTileCollection(room)
		for tile in self.tiles:
			new_tile = new_collection.add_tile(tile.position)
			for wall in tile.walls:
				if wall != None:
					new_tile.add_wall(direction=wall.normal)
		return new_collection
	
	def draw(self, image, color):
		for tile in self.tiles:
			# used_color = color
			# for wall in tile.walls:
			# 	if wall != None:
			# 		if wall.is_corner():
			# 			used_color = (0, 255, 255)
			# 			break
			# 		else:
			# 			used_color = direction_to_color(wall.normal)
			
			image.putpixel(
				(
					tile.position[0] + 5 + self.room.position[0],
					tile.position[1] + 5 + self.room.position[1],
				),
				color
			)