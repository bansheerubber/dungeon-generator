from PIL import Image
from PIL import ImageOps
import math

def ceil_to_number(input, round):
	return math.ceil(input / round) * round

def slice(image, start, dimensions):
	area = (start[0], start[1], start[0] + dimensions[0], start[1] + dimensions[1])
	output = image.crop(area)
	return output

image_name = "egg"
image = Image.open(f"{image_name}.png")
width, height = image.size
size = 128

x_loss = ceil_to_number(width, size) - width
y_loss = ceil_to_number(height, size) - height
loss = x_loss
if y_loss > x_loss:
	loss = y_loss

image = ImageOps.expand(image, border=loss, fill=(255, 255, 255))

x_index = 0
y_index = 0
for x in range(0, ceil_to_number(width, size), size):
	y_index = 0
	for y in range(0, ceil_to_number(height, size), size):
		slice(image, (x + loss, y + loss), (size, size)).save(f"./tiles/{image_name}_{x_index}_{y_index}.png")
		y_index = y_index + 1
	x_index = x_index + 1

print(int(ceil_to_number(width, size) / size - 1), int(ceil_to_number(height, size) / size - 1))

file = open("./tiles/tile_data", "w")
file.write(f"{image_name}\n")
file.write(f"{int(ceil_to_number(width, size) / size - 1)} {int(ceil_to_number(height, size) / size - 1)}\n")
file.write(f"{width} {height}\n")
file.write(f"{size}\n")
file.close()