class Hallway:
	def __init__(self, start, end, generator):
		self.is_horizontal = start[1] == end[1]
		self.generator = generator
		self.is_destroyed = False

		if self.is_horizontal:
			if start[0] < end[0]:
				self.start = start
				self.end = end
			else:
				self.start = end
				self.end = start
			
			for x in range(self.start[0], self.end[0] + 1):
				self.generator.hallway_map[(x, self.start[1])] = self
		else:
			if start[1] < end[1]:
				self.start = start
				self.end = end
			else:
				self.start = end
				self.end = start
			
			for y in range(self.start[1], self.end[1] + 1):
				self.generator.hallway_map[(self.start[0], y)] = self
		
		self.generator.hallways.add(self)
	
	def draw(self, image):
		if self.is_horizontal:
			for x in range(self.start[0] + 1, self.end[0]):
				image.putpixel((x + 10, self.start[1] + 10), (0, 0, 0))
		else:
			for y in range(self.start[1] + 1, self.end[1]):
				image.putpixel((self.start[0] + 10, y + 10), (0, 0, 0))
	
	def destroy(self):
		self.generator.hallways.discard(self)
		self.is_destroyed = True

		if self.is_horizontal:
			for x in range(self.start[0], self.end[0] + 1):
				position = (x, self.start[1])
				if position in self.generator.hallway_map and self.generator.hallway_map[position] == self:
					self.generator.hallway_map.pop(position)
		else:
			for y in range(self.start[1], self.end[1] + 1):
				position = (self.start[0], y)
				if position in self.generator.hallway_map and self.generator.hallway_map[position] == self:
					self.generator.hallway_map.pop(position)