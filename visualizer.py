import pygame
import random
import math
import time
pygame.init()
class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0,255,0
	RED = 255,0,0
	BACKGROUND_COLOR = BLACK
	YELLOW = 255,255,0
	SPEED = 80
	FONT = pygame.font.SysFont('comicsans', 30)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)
	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height
		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualizer")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Randomize | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.WHITE)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | Q - Quick Sort | M - Merge Sort", 1, draw_info.WHITE)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 90))
	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}):
	lst = draw_info.lst

	clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
	pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.WHITE

		if i in color_positions:
			color = color_positions[i] 
		pygame.draw.rect(draw_info.window, color, (x+2, y, draw_info.block_width-2, draw_info.height))
	pygame.display.update()

def generate_random_list(n, min_val, max_val):
	lst = []
	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)
	return lst
def scanAfterSort(draw_info):
	lst = draw_info.lst
	hash = {}
	for i in range(len(lst)):
		time.sleep(1/draw_info.SPEED)
		hash[i] = draw_info.GREEN
		draw_list(draw_info,hash)

def bubbleSort(draw_info, ascending=True):
	lst = draw_info.lst
	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]
			draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED})
			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				time.sleep(1/draw_info.SPEED)
				draw_list(draw_info, {j: draw_info.RED, j + 1: draw_info.GREEN})
				time.sleep(1/draw_info.SPEED)
				yield True
	scanAfterSort(draw_info)

def selectionSort(draw_info, ascending=True):
	lst = draw_info.lst
	for i in range(len(lst)):
		min_idx = i
		for j in range(i + 1, len(lst)):
            # to sort in descending order, change > to < in this line
            # select the minimum element in each loop
			time.sleep(1/draw_info.SPEED)
			draw_list(draw_info,{i:draw_info.GREEN,j:draw_info.RED})
			if lst[j] < lst[min_idx] and ascending:
				min_idx = j
			if lst[j] > lst[min_idx] and not ascending:
				min_idx = j
			yield True
		time.sleep(1/draw_info.SPEED)
		draw_list(draw_info,{i:draw_info.GREEN,min_idx:draw_info.YELLOW})
		time.sleep(1/draw_info.SPEED)
        # put min at the correct position
		(lst[i], lst[min_idx]) = (lst[min_idx], lst[i])
		draw_list(draw_info,{i:draw_info.YELLOW,min_idx:draw_info.GREEN})
		time.sleep(1/draw_info.SPEED)
	scanAfterSort(draw_info)

def insertionSort(draw_info,ascending=True):
	lst = draw_info.lst
	for i in range(1, len(lst)):
		key = lst[i]
		j = i - 1
        # Compare key with each element on the left of it until an element smaller than it is found
        # For descending order, change key<array[j] to key>array[j].        
		while (j >= 0 and key < lst[j] and ascending) or (j>=0 and key > lst[j] and not ascending):
			lst[j + 1] = lst[j]
			time.sleep(1/draw_info.SPEED)
			draw_list(draw_info,{j+1:draw_info.RED,j:draw_info.GREEN})
			j = j - 1
			yield True
        
        # Place key at after the element just smaller than it.
		lst[j + 1] = key
		time.sleep(1/draw_info.SPEED)
		draw_list(draw_info,{j+1:draw_info.GREEN})
	scanAfterSort(draw_info)


def partition(draw_info, low, high,ascending):
	lst = draw_info.lst
	pivot = lst[high]
	pivotIndex = high
	i = low - 1
	for j in range(low, high):
		draw_list(draw_info,{pivotIndex:draw_info.YELLOW,i:draw_info.GREEN,j:draw_info.RED})
		time.sleep(1/draw_info.SPEED)
		if (lst[j] <= pivot and ascending) or (lst[j]>= pivot and not ascending):
			i = i + 1
			draw_list(draw_info,{pivotIndex:draw_info.YELLOW , i:draw_info.RED,j:draw_info.GREEN})
			(lst[i], lst[j]) = (lst[j], lst[i])
			time.sleep(1/draw_info.SPEED)
			draw_list(draw_info,{pivotIndex:draw_info.YELLOW,i:draw_info.RED,j:draw_info.GREEN})
	(lst[i + 1], lst[high]) = (lst[high], lst[i + 1])
	draw_list(draw_info,{i+1:draw_info.GREEN,i:draw_info.RED})
	return i + 1
def quickSort(draw_info,ascending=True):
	def quick_sort(draw_info,low,high,ascending):
		if low < high:
			pi = partition(draw_info, low, high,ascending)
			quick_sort(draw_info, low, pi - 1,ascending)
			quick_sort(draw_info, pi + 1, high,ascending)
	quick_sort(draw_info,0,len(draw_info.lst)-1,ascending)
	yield True
	scanAfterSort(draw_info)

def mergeSort(draw_info,ascending = True):
	array = draw_info.lst
	def merge_sort(draw_info,low,high,array,ascending):
		if len(array) > 1:
			hash = {}
			for i in range(len(array)):
				hash[low+i] = draw_info.YELLOW
			time.sleep(1/draw_info.SPEED)
			draw_list(draw_info,hash)
			time.sleep(1/draw_info.SPEED)
			mid = (high+low)//2
			L = array[:len(array)//2]
			M = array[len(array)//2:]
			merge_sort(draw_info,low,mid-1,L,ascending)
			merge_sort(draw_info,mid,high,M,ascending)
			i = j = k = 0
			while i < len(L) and j < len(M):
				draw_list(draw_info,{low+k:draw_info.GREEN})
				time.sleep(1/draw_info.SPEED)
				if (L[i] < M[j] and ascending) or (L[i] > M[j] and not ascending):
					array[k] = L[i]
					draw_info.lst[low+k] = L[i]
					draw_list(draw_info,{low + k:draw_info.RED})
					time.sleep(1/draw_info.SPEED)
					i += 1
				else:
					array[k] = M[j]
					draw_info.lst[low+k] = M[j]
					draw_list(draw_info,{low+k:draw_info.RED})
					time.sleep(1/draw_info.SPEED)
					j += 1
				k += 1
			while i < len(L):
				draw_list(draw_info,{low+k:draw_info.GREEN})
				time.sleep(1/draw_info.SPEED)
				array[k] = L[i]
				draw_info.lst[low+k] = L[i]
				draw_list(draw_info,{low+k:draw_info.RED})
				time.sleep(1/draw_info.SPEED)
				i += 1
				k += 1
			while j < len(M):
				draw_list(draw_info,{low+k:draw_info.GREEN})
				time.sleep(1/draw_info.SPEED)
				array[k] = M[j]
				draw_info.lst[low+k] = M[j]
				draw_list(draw_info,{low+k:draw_info.RED})
				time.sleep(1/draw_info.SPEED)
				j += 1
				k += 1
	merge_sort(draw_info,0,len(array)-1,array,ascending)
	yield True
	scanAfterSort(draw_info)

def main():
	run = True
	bars = 60
	min_val = 0
	max_val = 100
	lst = generate_random_list(bars, min_val, max_val)
	draw_info = DrawInformation(1400, 750, lst)
	sorting = False
	ascending = True
	sorting_algorithm = bubbleSort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None
	while run:
		if sorting :
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = True
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_random_list(bars, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertionSort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubbleSort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selectionSort
				sorting_algo_name = "Selection Sort"
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm = quickSort
				sorting_algo_name = "Quick Sort"
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = mergeSort
				sorting_algo_name = "Merge Sort"
	pygame.quit()
if __name__ == "__main__":
	main()