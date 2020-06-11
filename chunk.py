import math

CHUNK_SIZE = 10
global chunk_map # [index: Position]: Chunk
chunk_map = {}

# small area containing a bunch of rooms
class Chunk:	
	def __init__(self, position, chunk_map=chunk_map):
		self.position = position # top left of chunk
		self.rooms = set()
		self.chunk_map = chunk_map
	
	def adjacents(self):
		for x in range(-1, 2): # go to 2 since range is exclusive
			for y in range(-1, 2):
				position = (self.position[0] + x, self.position[1] + y)
				if position != self.position:
					if position not in self.chunk_map:
						self.chunk_map[position] = Chunk(position)
					yield self.chunk_map[position]
	
	def all_rooms(self):
		for room in self.rooms:
			yield room
		
		for chunk in self.adjacents():
			for room in chunk.rooms:
				yield room

	# checks if a room overlaps in this chunk or any adjacent chunks
	def overlaps(self, room):
		for test_room in self.rooms:
			if test_room != room and room.overlaps(test_room):
				return test_room

		# iterate through adjacent chunks
		for chunk in self.adjacents():
			for test_room in chunk.rooms:
				if test_room != room and room.overlaps(test_room):
					return test_room
		
		return None
	
	def add_room(self, room, size=None):
		if room not in self.rooms:
			self.rooms.add(room)

			force = False
			if size == None:
				if room.size[0] > room.size[1]:
					size = room.size[0]
				else:
					size = room.size[1]
			elif size > -20:
				force = True

			if size > CHUNK_SIZE or force == True:
				for adjacent in self.adjacents():
					adjacent.add_room(room, size - CHUNK_SIZE)
	
	def remove_room(self, room):
		self.rooms.discard(room)

# gets a chunk at a position. if there isn't one, then create one
def get_chunk(position, chunk_map=chunk_map):
	normalized_position = (
		math.floor(position[0] / CHUNK_SIZE),
		math.floor(position[1] / CHUNK_SIZE)
	)

	if normalized_position not in chunk_map:
		chunk_map[normalized_position] = Chunk(normalized_position)
	
	return chunk_map[normalized_position]