import random

class Collection:
	def __init__(self, generator):
		self.rooms = set()
		self.generator = generator
		self.generator.collections.append(self)

		self.color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
	
	def add_room(self, room):
		self.rooms.add(room)
		room.collection = self
		return self
	
	def remove_room(self, room):
		self.rooms.remove(room)
		room.collection = None
	
	def merge(self, collection):
		if len(self.rooms) >= len(collection.rooms):
			if self in self.generator.collections:
				self.generator.collections.remove(self)
			
			for room in collection.rooms:
				self.add_room(room)
			
			collection.rooms = set() # clear the set
		else:
			collection.merge(self)