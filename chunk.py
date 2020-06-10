import math

CHUNK_SIZE = 10
global chunk_map # [index: Position]: Chunk
chunk_map = {}

# small area containing a bunch of rooms
class Chunk:	
	def __init__(self, position):
		self.position = position # top left of chunk
		self.rooms = []
	
	def adjacents(self):
		for x in range(-1, 1):
			for y in range(-1, 1):
				position = (self.position[0] + x, self.position[1] + y)
				if position in chunk_map:
					yield chunk_map[position]

	# checks if a room overlaps in this chunk or any adjacent chunks
	def overlap(self, room):
		for test_room in self.rooms:
			if room.overlaps(test_room):
				return True

		# iterate through adjacent chunks
		for chunk in self.adjacents():
			for test_room in chunk.rooms:
				if room.overlaps(test_room):
					return True
		return False

# gets a chunk at a position. if there isn't one, then create one
def get_chunk(position):
	normalized_position = (
		math.floor(position[0] / CHUNK_SIZE),
		math.floor(position[1] / CHUNK_SIZE)
	)

	if normalized_position not in chunk_map:
		chunk_map[normalized_position] = Chunk(normalized_position)
	
	return chunk_map[normalized_position]