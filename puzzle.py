import argparse
import random
import numpy as np


parser = argparse.ArgumentParser(description="Generates a word search puzzle")

parser.add_argument("-s", "--solution", action="store_true", help="Hightlight words")
parser.add_argument("-f", "--file", type=str, default="words.txt", help="Path to a custom words file. One word per line.")
parser.add_argument("-w", "--width", type=int, default=20, help="Sets a custom grid width (Default: 20)")
parser.add_argument("--height", type=int, default=20, help="Sets a custom grid height (Default: width)")
parser.add_argument('-u', '--upper', action="store_true", help="All upper-case")
parser.add_argument('-l', '--lower', action="store_true", help="All lower-case")
parser.add_argument('-n', '--number', type=int, default=10, help="Number of words to hide")
parser.add_argument('-d', '--dirs', type=int, default=7, help="Allow directions, bit vector: 1*horizontal + 2*vertical + 4*diagonal")
parser.add_argument('-b', '--borders', action="store_true", help="Print borders")
parser.add_argument('--wordslocalized', type=str, default="Wörter", help="Words in your language, default: Wörter (German)")
parser.add_argument('--spacer', type=str, default=" ", help="Spacer between letters")

args = parser.parse_args()

def main(solution=False, words_file=None, width=20, height=20, n=10, borders=False, upper=False, lower=False, directions=7, spacer=" "):

	if upper and lower:
		print("Cannot do both upper and lower")
		return

	# generating words from file
	word_filter = lambda x: len(x) <= min(width, height)
	with open(words_file, 'r') as file:
		lines = list(filter(word_filter, map(lambda x: x.strip(), file.readlines())))

	def word_map(w:str):
		if upper:
			return w.upper()
		if lower:
			return w.lower()
		return w
	words = list(map(word_map, random.sample(lines, n)))

	# creating the word grid
	grid = WordGrid(width, height, upper=upper, lower=lower)

	words = grid.add_words(words, solution=solution, directions=directions)

	grid.print(borders, spacer)
	print()
	# printing the words to find
	print(args.wordslocalized)
	for count, word in enumerate(words):
		print(f"{count + 1}. {word}", end=" | ")
	print()


alphabet = 'abcdefghijklmnopqrstuvwxyz'


class WordGrid:
	def __init__(self, width=20, height=None, upper=False, lower=False) -> None:
		if height is None:
			height = width
		self.grid = np.zeros([height, width], dtype='U1')
		self.available = np.ones([height, width], dtype='bool')
		self.width = width
		self.height = height
		self.solution = False
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

	def add_words(self, words:list, solution=False, directions=7):
		self.solution = solution
		remove_list = []

		available_dirs = []
		for i in range(3):
			if directions%2:
				available_dirs.append(i+1)
			directions //= 2

		for word in words:
			placed = False
			rem_dirs = set()
			if len(word) > self.height:
				rem_dirs = rem_dirs.union([2, 3])
			if len(word) > self.width:
				rem_dirs = rem_dirs.union([1, 3])
			dirs = list(set(available_dirs) - rem_dirs)
			if not dirs:
				print("warning: no dirs left")
				continue

			for _ in range(100):
				# chooses a random direction
				dir = random.choice(dirs)	# 1: HORIZONTAL, 2: VERTICAL, 3: DIAGONAL
				x_offset = dir % 2
				y_offset = dir // 2

				# random x and y positions of the first letter of the current word
				x = random.randint(0, self.width - 1 - (len(word)-1)*x_offset)
				y = random.randint(0, self.height - 1 - (len(word)-1)*y_offset)
				if self._is_placeable(word, x, y, x_offset, y_offset):
					self._place_word(word, x, y, x_offset, y_offset)
					placed = True
					break

			if not placed:
				print(f"Warning: Could not place {word}")
				remove_list.append(word)
		
		for w in remove_list:
			words.remove(w)
		return words
					
	

	# sets a word in a position and with a particular direction
	def _place_word(self, word, x, y, x_offset, y_offset):
		for i, w in enumerate(word):
			this_x, this_y = x + i*x_offset, y + i*y_offset
			self.grid[this_y, this_x] = w
			self.available[this_y, this_x] = False
	
	# checks if a word can be placed in a position and with a particular direction
	def _is_placeable(self, word, x, y, x_offset, y_offset):
		for i, w in enumerate(word):
			this_x, this_y = x + i*x_offset, y + i*y_offset
			if not self.available[this_y, this_x] and not self.grid[this_y, this_x] == w:
				return False

		return True


	# prints the grid on the terminal
	def print(self, border=False, spacer=" "):

		if border:
			print(f"{bcolors.BEG}┌" + ("─"*(2*(self.width)+1)) + f"┐{bcolors.ENDC}" )
		for y in range(self.height):
			if border:
				print(f"{bcolors.BEG}│{bcolors.ENDC}", end=spacer)
			for x in range(self.width):
				self._print_letter(x, y, spacer=spacer)
			if border:
				print(f"{bcolors.BEG}│{bcolors.ENDC}", end="")
			print()
		if border:
			print(f"{bcolors.BEG}└" + ("─"*(2*(self.width)+1)) + f"┘{bcolors.ENDC}" )


	def _print_letter(self, x, y, spacer=" "):
		if self.available[y, x] or not self.solution:
			print(self.grid[y, x], end=spacer)
		else:
			print(f"{bcolors.BEG}{self.grid[y, x]}{bcolors.ENDC}", end=spacer)


class bcolors:
    BEG = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == "__main__":
	main(solution=args.solution, words_file=args.file, width=args.width, height=args.height, n=args.number, borders=args.borders, upper=args.upper, lower=args.lower, directions=args.dirs, spacer=args.spacer)
