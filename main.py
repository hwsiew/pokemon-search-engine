#!/usr/bin/env python 

import json
from ace_pointer.myapp import PokemonSearchEngine

def main():
	"""The entry point of the program"""

	# initialize pokemon search engine
	engine = PokemonSearchEngine()

	# promt for user input
	id_or_name = input('Please enter Pokemon Name or ID follows by enter: ')

	# loop to continue pokemon search until '0' is entered
	while id_or_name != '0':
		
		if id_or_name != '':
			engine.query(id_or_name)
		else:
			print('You had entered nothing')

		#print() # empty line to separate query

		id_or_name = input('Search more or enter 0 to quit: ')

if __name__ == '__main__':

	# banner to display at the beginning of program 
	banner = """
~ Welcome to Ace pointer Pokemon Search Enginee ~
To query a pokemon, please type an id or name follows by enter
To quit the program, please type 0 
 	"""
	 
	print(banner)

	main()