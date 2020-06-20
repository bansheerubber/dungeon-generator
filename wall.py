class RoomWall:
	def __init__(self, normal, tile):
		self.normal = normal # normal points into the room
		self.tile = tile
		self.is_door = False
		self.adjacents = set() # the walls that are connected to this wall
	
	def add_adjacent(self, adjacent):
		self.adjacents.add(adjacent)

		if len(self.adjacents) > 2:
			raise Exception("Wall has too many adjacents")
	
	# whether or not we're on a corner tile
	def is_corner(self):
		for adjacent in self.adjacents:
			if adjacent.normal != self.normal:
				return True
		return False