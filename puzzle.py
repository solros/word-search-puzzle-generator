from word_grid import *
import argparse

parser = argparse.ArgumentParser(description="Generates a word search puzzle")

parser.add_argument("-c", "--cheated", action="store_true", help="Hightlight words")
parser.add_argument("-f", "--file", type=str, default="words.txt", help="Path to a custom words file. One word per line.")
parser.add_argument("-w", "--width", type=int, default=20, help="Sets a custom grid width (Default: 20)")
parser.add_argument("--height", type=int, default=20, help="Sets a custom grid height (Default: width)")
parser.add_argument('-u', '--upper', action="store_true", help="All upper-case")
parser.add_argument('-l', '--lower', action="store_true", help="All lower-case")
parser.add_argument('-n', '--number', type=int, default=10, help="Number of words to hide")
parser.add_argument('-b', '--borders', action="store_true", help="Print borders")
parser.add_argument('--header', action="store_true", help="Print header")
parser.add_argument('--wordslocalized', type=str, default="Wörter", help="Words in your language, default: Wörter (German)")
parser.add_argument('--spacer', type=str, default=" ", help="Spacer between letters")

args = parser.parse_args()

def main(cheated=False, words_file=None, width=20, height=20, n=10, header=False, borders=False, upper=False, lower=False, spacer=" "):

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

	if header:
		print("┌────────────────────┐")
		print("│ Word Search Puzzle │")
		print("└────────────────────┘")

	grid.cheated = cheated

	words = grid.add_words(words)

	# printing the words to find
	print(args.wordslocalized)

	for count, word in enumerate(words):
		print(f"{count + 1}. {word}", end=" | ")
	print()

	grid.print(borders, spacer)


if __name__ == "__main__":
	main(cheated=args.cheated, words_file=args.file, width=args.width, height=args.height, n=args.number, header=args.header, borders=args.borders, upper=args.upper, lower=args.lower, spacer=args.spacer)
