from word_grid import *
import argparse

parser = argparse.ArgumentParser(description="Generates a word search puzzle")

parser.add_argument("-c", "--cheated", action="store_true", help="Hightlight words")
parser.add_argument("-f", "--file", type=str, default="words.txt", help="Path to a custom words file. One word per line.")
parser.add_argument("-s", "--size", type=int, default=20, help="Sets a custom grid size (Default: 20)")
parser.add_argument('-u', '--upper', action="store_true", help="All upper-case")
parser.add_argument('-l', '--lower', action="store_true", help="All lower-case")
parser.add_argument('-n', '--number', type=int, default=10, help="Number of words to hide")
parser.add_argument('-b', '--borders', action="store_true", help="Add border")
parser.add_argument('--header', action="store_true", help="Print header")
parser.add_argument('--wordslocalized', type=str, default="Wörter", help="Words in your language, default: Wörter (German)")

args = parser.parse_args()

def main(cheated=False, words_file=None, size=20, n=10, header=False, borders=False, upper=False, lower=False):

	if upper and lower:
		print("Cannot do both upper and lower")
		return

	# generating words from file
	with open(words_file, 'r') as file:
		lines = file.readlines()

	def word_map(w:str):
		w = w.strip()
		if upper:
			return w.upper()
		if lower:
			return w.lower()
		return w

	words = list(map(word_map, random.sample(lines, n)))

	# creating the word grid
	grid = WordGrid(size, upper=upper, lower=lower)

	if header:
		print("┌────────────────────┐")
		print("│ Word Search Puzzle │")
		print("└────────────────────┘")

	grid.cheated = cheated

	grid.add_words(words)

	# printing the words to find
	print(args.wordslocalized)
	for count, word in enumerate(words):
		print(f"{count}. {word}", end=" | ")
	print()
	grid.print(borders)


if __name__ == "__main__":
	main(cheated=args.cheated, words_file=args.file, size=args.size, n=args.number, header=args.header, borders=args.borders, upper=args.upper, lower=args.lower)
