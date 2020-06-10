import matplotlib.pyplot as plt
from room import Room
import chunk

room1 = Room((0, 0), (2, 2))
room2 = Room((15, 15), (2, 2))

chunk.get_chunk((0, 0)).overlap(room2)

plt.show()