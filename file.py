import zlib

class File:
	def __init__(self):
		self.bytes = bytearray()
	
	def write(self, number, count):
		byte = number.to_bytes(count, byteorder='big')
		self.bytes += byte

	def save(self, file_name):
		file = open(file_name, "wb")
		file.write(zlib.compress(self.bytes, 9))