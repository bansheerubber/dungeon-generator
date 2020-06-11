class Line:
	def set_points(self, start, end):
		self.is_horizontal = start[1] == end[1]

		if self.is_horizontal:
			if start[0] < end[0]:
				self.start = start
				self.end = end
			else:
				self.start = end
				self.end = start
		else:
			if start[1] < end[1]:
				self.start = start
				self.end = end
			else:
				self.start = end
				self.end = start
		
		return self

	# check if this line intersects another line
	def intersects(self, line):
		# if the lines are parallel, they cannot intersect
		if (line.is_horizontal == True and self.is_horizontal == True) or (line.is_horizontal == False and self.is_horizontal == False):
			return False
		
		if self.is_horizontal:
			# see if the intersection is within our line
			if(
				self.start[0] < line.start[0] and line.start[0] < self.end[0]
				and line.start[1] < self.start[1] and self.start[1] < line.end[1] 
			):
				return True
		else:
			return line.intersects(self)
		
		return False