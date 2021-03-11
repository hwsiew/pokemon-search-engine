import unittest
from unittest.mock import patch
from io import StringIO 
import os

import main

class TestMain(unittest.TestCase):
	"""Simple test file to validate various input"""
	empty_input = ''
	valid_input = '1'
	invalid_input = 'pp'
	exit_input  = '0'

	def __init__(self, *args, **kwargs):
		super(TestMain, self).__init__(*args, **kwargs)
		# remove cache file if any
		if os.path.exists("cache.json"):	
			os.remove("cache.json")

	@patch('builtins.input', side_effect=[ empty_input , exit_input ])
	def test_empty_input(self,mock_input):
		"""Test user empty input"""
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			
			main.main()
			
			expected_output = 'You had entered nothing\n'

			self.assertEqual(fake_out.getvalue(), expected_output) 
		
	@patch('builtins.input', side_effect=[ invalid_input , exit_input ])
	def test_invalid_input(self,mock_input):
		"""Test user invalid input"""
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			
			main.main()
			
			expected_output = 'Loading...\n'
			expected_output += 'Pokemon not found: pp\n'
			
			self.assertEqual(fake_out.getvalue(), expected_output) 

	@patch('builtins.input', side_effect=[ valid_input , exit_input ])
	def test_valid_input(self,mock_input):
		"""Test user valid input"""
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			
			main.main()
			
			expected_output = 'Loading...\n' # only show this if query is not cache
			expected_output += 'ID: 1\n'
			expected_output += 'Name: bulbasaur\n'
			expected_output += "Types: ['grass', 'poison']\n"
			expected_output += "Stats [name(base_stat)]: ['hp(45)', 'attack(49)', 'defense(49)', 'special-attack(65)', 'special-defense(65)', 'speed(45)']\n"
			expected_output += "Locations: -\n"

			self.assertEqual(fake_out.getvalue(), expected_output)

	@patch('builtins.input', side_effect=[ valid_input , exit_input ])
	def test_valid_input_cached(self,mock_input):
		"""Test user cached input"""
		with patch('sys.stdout', new = StringIO()) as fake_out: 
			
			main.main()
			
			expected_output = 'ID: 1\n'
			expected_output += 'Name: bulbasaur\n'
			expected_output += "Types: ['grass', 'poison']\n"
			expected_output += "Stats [name(base_stat)]: ['hp(45)', 'attack(49)', 'defense(49)', 'special-attack(65)', 'special-defense(65)', 'speed(45)']\n"
			expected_output += "Locations: -\n"

			self.assertEqual(fake_out.getvalue(), expected_output) 

if __name__ == '__main__':
    unittest.main()