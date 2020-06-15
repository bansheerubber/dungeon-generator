import math

CHUNK_SIZE = 15

# small area containing a bunch of rooms
class Chunk:	
	def __init__(self, position, chunk_map):
		self.position = position # top left of chunk
		self.rooms = set()
		self.chunk_map = chunk_map
		self.adjacent_chunks = set()
	
	def adjacents(self):
		if len(self.adjacent_chunks) == 0:
			for x in range(-1, 2): # go to 2 since range is exclusive
				for y in range(-1, 2):
					position = (self.position[0] + x, self.position[1] + y)
					if position != self.position:
						if position not in self.chunk_map:
							self.chunk_map[position] = Chunk(position, self.chunk_map)
						self.adjacent_chunks.add(self.chunk_map[position])
		
		return self.adjacent_chunks
	
	def all_rooms(self):
		for room in self.rooms:
			yield room
		
		for chunk in self.adjacents():
			for room in chunk.rooms:
				yield room

	# checks if a room overlaps in this chunk or any adjacent chunks
	def overlaps(self, room):
		for test_room in self.all_rooms():
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
			elif size > -60: # lol idk
				force = True

			if size > CHUNK_SIZE or force == True:
				for adjacent in self.adjacents():
					adjacent.add_room(room, size - CHUNK_SIZE)
	
	def remove_room(self, room):
		self.rooms.discard(room)

# gets a chunk at a position. if there isn't one, then create one
def get_chunk(position, chunk_map):
	normalized_position = (
		math.floor(position[0] / CHUNK_SIZE),
		math.floor(position[1] / CHUNK_SIZE)
	)

	if normalized_position not in chunk_map:
		chunk_map[normalized_position] = Chunk(normalized_position, chunk_map)
	
	return chunk_map[normalized_position]