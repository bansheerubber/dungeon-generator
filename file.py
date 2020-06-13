import zlib

class File:
	def __init__(self):
		self.bytes = bytearray()
		self.numbers = []
	
	def write(self, number, count):
		byte = number.to_bytes(count, byteorder='big')
		self.bytes += byte

		self.numbers.append(number)
	
	def write_break(self):
		self.numbers.append(-1)
	
	def write_section(self):
		self.numbers.append(-2)

	def save(self, file_name):
		file = open(file_name, "wb")
		file.write(zlib.compress(self.bytes, 9))
		file.close()
	
	def save_blockland(self, file_name):
		file = open(file_name, "w")
		buffer = ""
		for number in self.numbers:
			if number == -1:
				file.write(buffer.strip() + "\n")
				buffer = ""
			elif number == -2:
				file.write("\n")
				buffer = ""
			else:
				buffer = buffer + f"{number} "
		
		file.close()