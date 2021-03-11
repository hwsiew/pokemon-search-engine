from os import path
import json
from typing import List, Optional
from .pokemon import Pokemon
from datetime import datetime

class SimpleCache():
	"""
	A class to repesents simple in-memory cache and offers persistancy by saving to file
	...
	Attributes
	----------
	file : str = 'cache.json'
		cache file location
	cache : dict
		in-memory cache reference to all pokemon reference
		key is either name or id, value is a pokemon reference
		this enable O(1) lookup for pokemon by name or id
	Methods
	-------
	load() -> None
		load pokemon data from cache file is one exists
	
	save() -> None
		Save in-memory cache to persistent file

	get(key:str) -> Pokemon | None
		get pokemon instance by key either name or id
	
	put(keys:List[str],value:Pokemon) -> None
		add pokemon references to in memory cahce and save to cache file for persistency
	"""
	def __init__(self, file:str = 'cache.json'):
		self.file  = file
		self.cache = {}

		self.load()

	def load(self) -> None:
		"""Load pokemon data from cache file is one exists"""
		if not path.exists(self.file): 
			return

		with open(self.file) as f:
  			data = json.load(f)

		# load saved information to in memory cache
		saved = []
		for d in data:
			pid 	= d['id']
			name 	= d['name']
			types 	= d['types']
			stats	= d['stats']
			location_area_encounters = d['location_area_encounters']
			ttl		= d['ttl']
			pokemon = Pokemon( pid, name, types, location_area_encounters, stats, ttl )

			# insert cache key for both name and id and reference to same pokemon
			self.cache[pid]  = pokemon
			self.cache[name] = pokemon

	def save(self) -> None:
		"""Save in-memory cache to persistent file"""
		data  = []
		saved = [] # to keep track which keys had been saved 
		for key in self.cache:
			if key in saved: 
				continue
			
			pokemon = self.cache[key]
			data.append(pokemon.serialize())
			# id and name key in cache both point to the same Pokemon
			# so saved only once
			saved.append(self.cache[key].id)
			saved.append(self.cache[key].name)

		with open(self.file, 'w') as outfile:
  			json.dump(data, outfile)

	def get(self,key:str) -> Optional['Pokemon']:
		"""
		get pokemon instance by key either name or id

		Parameters
		----------
		key : str
			name or id of pokemon to 
		
		Returns
		-------
		pokemon : Pokemon | None
			pokemon instance if one is found
		"""
		if key not in self.cache: 
			return None

		pokemon = self.cache[key]

		now 	= datetime.timestamp(datetime.now())
		
		# data has expired > 7 days apart from first query
		if now > pokemon.ttl:
			del self.cache[pokemon.id]
			del self.cache[pokemon.name]
			self.save()
			return None

		return pokemon

	def put(self,keys:List[str],value:Pokemon) -> None:
		"""
		add pokemon references to in memory cahce and save to cache file for persistency

		Parameters
		----------
		keys : List[str]
			keys of pokemon which are name and id of pokemon
		value : Pokemon
			a reference to Pokemon instance

		Returns
		-------
		None
		"""
		for key in keys:
			self.cache[key] = value

		self.save()
