from math import sqrt
import random
import os
import numpy as np

HORIZONTAL 	= 0
VERTICAL	= 1

alphabet = 'abcdefghijklmnopqrstuvwxyz'



class WordGrid:
	def __init__(self, width, height=None, upper=False, lower=False) -> None:
		if height is None:
			height = width
		self.grid = np.zeros([height, width], dtype='U1')
		self.available = np.ones([height, width], dtype='bool')
		self.width = width
		self.height = height
		self.cheated = False
		self.upper = upper
		self.lower = lower

		self.fill()

	def fill(self):
		for i in range(self.height):
			for j in range(self.width):
				self.grid[i,j] = self.get_random_letter()

	def get_random_letter(self, upper_prob=0.5):
		l = alphabet[random.randint(0, len(alphabet)-1)]
		if self.lower:
			return l.lower()
		if self.upper or random.random() >= upper_prob:
			return l.upper()
		return l.lower()

	def add_words(self, words):
		for word in words:
			placed = False
			for _ in range(100):
				# chooses a random direction
				dir = random.choice([1, 2, 3])	# 1: HORIZONTAL, 2: VERTICAL, 3: DIAGONAL
				x_offset = dir % 2
				y_offset = dir // 2

				# random x and y positions of the first letter of the current word
				x = random.randint(0, self.width - 1 - len(word)*x_offset)
				y = random.randint(0, self.height - 1 - len(word)*y_offset)

				if self._is_placeable(word, x, y, x_offset, y_offset):
					self._place_word(word, x, y, x_offset, y_offset)
					placed = True
					break

			if not placed:
				print(f"Warning: Could not place {word}")
					
	

	# sets a word in a position and with a particular direction
	def _place_word(self, word, x, y, x_offset, y_offset):
		for i, w in enumerate(word):
			self.grid[x+i*x_offset, y+i*y_offset] = w
			self.available[x+i*x_offset, y+i*y_offset] = False
	
	# checks if a word can be placed in a position and with a particular direction
	def _is_placeable(self, word, x, y, x_offset, y_offset):
		for i, w in enumerate(word):
			this_x, this_y = x + i*x_offset, y + i*y_offset
			if not self.available[this_x, this_y] and not self.grid[this_x, this_y] == w:
				return False

		return True


	# prints the grid on the terminal
	def print(self, border=False):
		if border:
			print(f"{bcolors.BEG}┌" + ("─"*(2*(self.width)+1)) + f"┐{bcolors.ENDC}" )
		for y in range(self.height):
			if border:
				print(f"{bcolors.BEG}│{bcolors.ENDC}", end=" ")
			for x in range(self.width):
				self._print_letter(x, y)
			if border:
				print(f"{bcolors.BEG}│{bcolors.ENDC}", end="")
			print()
		if border:
			print(f"{bcolors.BEG}└" + ("─"*(2*(self.width)+1)) + f"┘{bcolors.ENDC}" )

	def _print_letter(self, x, y):
		if self.available[x,y]:
			print(self.grid[x, y], end=" ")
		else:
			print(f"{bcolors.BEG}{self.grid[x, y]}{bcolors.ENDC}", end=" ")


class bcolors:
    BEG = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'