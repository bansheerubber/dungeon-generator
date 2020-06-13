import math
import heapq
import random

def distance(node1, node2):
	return math.sqrt((node1.position[0] - node2.position[0]) ** 2 + (node1.position[1] - node2.position[1]) ** 2)

def calc_g(g_score, node1, node2):
	return g_score[node1] + distance(node1, node2)

def calc_h(node1, goal):
	return distance(node1, goal)

def a_star(start, goal):
	open_set = []
	heapq.heappush(open_set, (calc_h(start, goal), id(start), start)) # min-heap is correlation between node and its f-score

	close_set = []

	came_from = {}

	g_score = {}
	g_score[start] = 0

	f_score = {}
	f_score[start] = calc_h(start, goal)

	while len(open_set) > 0:
		current = heapq.heappop(open_set)[2]
		if current == goal:
			return reconstruct_path(came_from, current)
		
		close_set.append(current)

		for neighbor in current.connected_rooms:
			temp_g_score = calc_g(g_score, current, neighbor)
			if neighbor not in g_score or temp_g_score < g_score[neighbor]:
				if neighbor not in came_from:
					came_from[neighbor] = current
				
				g_score[neighbor] = calc_g(g_score, current, neighbor)
				f_score[neighbor] = g_score[neighbor] + calc_h(neighbor, goal)
				if neighbor not in close_set:
					heapq.heappush(open_set, (f_score[neighbor], id(neighbor), neighbor))
	
	return None

def reconstruct_path(came_from, current):
	total_path = [current]
	while current in came_from:
		current = came_from[current]
		total_path.insert(0, current)
	return total_path