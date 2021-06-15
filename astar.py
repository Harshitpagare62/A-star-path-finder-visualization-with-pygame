import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col 

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		# this draws a square on the window at the given position for the spot object called by 
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	# looping over the spots which we came from to change their color to highlight the path
	while current in came_from:
		# getting the spot from the spots we came from 
		current = came_from[current]

		# changing the color of current spot and spot which we came from
		current.make_path()

		# undating the screen with the color changed spot 
		draw()



def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))

	# to store the spots we travelled or came from
	came_from = {}

	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	# this function creates a 2D list and appends  a spot object as element for each and every indices
	grid = []

	# this is for the size of square or Spot
	size_of_spot = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, size_of_spot, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	# this function divides display into a grid of given length and width 
	size_of_spot = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * size_of_spot), (width, i * size_of_spot))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * size_of_spot, 0), (j * size_of_spot, width))


def draw(win, grid, rows, width):
	#first filling the screen with white background
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			# creating a Square or rect object for each spot on screen
			spot.draw(win)

	#displaying the grid with horizontal and vertical lines creating each square		
	draw_grid(win, rows, width)
	
	#updaing the display or screeen
	pygame.display.update()




def main(win, width):
	ROWS = 50

	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			#if the left mouse button is pressed somewhere in the grid on a spot then 		
			if pygame.mouse.get_pressed()[0]: 
				#getting the postion where the button is clicked
				pos = pygame.mouse.get_pos()

				# getting the the position of the box in the grid
				row, col = get_clicked_pos(pos, ROWS, width)

				# getting the spot on that position in the grid
				spot = grid[row][col]

				#if there is not start yet and that spot is also not the end
				if not start and spot != end:
					#then assigning that spot as start
					start = spot
					#changing its color property
					start.make_start()

				#if there is not end yet and spot is not start then	
				elif not end and spot != start:
					end = spot

					#make the spot end and change the color
					end.make_end()

				#if the spot is not start and spot is not end 
				elif spot != end and spot != start:
					# make the spot barrier and change the color
					spot.make_barrier()

			# if the right mouse button is pressed in the grid then			
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				# change the color to the earlier one
				spot.reset()

				# Reset the values of start and end to None
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:

				#if there is start and end spots choosen and space bar is pressed in keyboard then
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							# then updating the neighbours for all the spots
							spot.update_neighbors(grid)
							
					# then starting the algotithum		
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
