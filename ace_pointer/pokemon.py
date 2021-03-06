import requests
from typing import List, Dict
from datetime import datetime, timedelta  

class PokemonError(Exception):
	"""
	A class to represent errors in the app
	...
	Attributes
	----------
	message : str
		error message to display

	Methods
	-------

	"""
	
	def __init__(self, message:str):
		self.message 	= message

	@property
	def message(self):
		"""Get or set error message to display"""
		return self.__message

	@message.setter
	def message(self, value:str) -> None:
		self.__message = value

class Pokemon():
	"""
	A class to represent Pokemon entity
	...
	Attributes
	----------
	API_HOST : str
		remote api host 
	ENDPOINTS : Dict[str,str]
		supported endpoints to query related to pokemon data
	raw : dict
		serializable data of pokemon

	Methods
	-------
	query(id_or_name:str) -> Pokemon
		query a pokemon by id or name

	build_request(endpoint:str, id_or_name:str) -> requests.models.Response
		constucts and send a remote GET request to query a pokemon by id or name

	serialize() -> dict
		return serializable data of pokemon	
	"""

	API_HOST 	= 'https://pokeapi.co/api/v2/'
	ENDPOINTS 	= {
		'pokemon' 						: 'pokemon/%s',
		'pokemon_enconter_locations'	: 'pokemon/%s/encounters'
	}

	def __init__(self, pid:str, name:str, types:List[dict], location_area_encounters:List[dict], stats:List[dict], ttl:float = None) -> None:
		"""
		Initialize a pokemon instance

		Parameters
		----------
		pid : str
			id of the pokemon
		name : str
			name of the pokemon
		types : List[dict]
			types of a pokemon
		location_area_encounters : List[dict]
			area of location to encounter the pokemon
		stats : List[dict]
			stats  of the pokemon
		ttl : float = None
			time to live (timestamp) of the data of pokemon
			invalidate pokemon data when now > ttl
		Returns
		-------
		None
		"""

		self.id 	= pid
		self.name 	= name
		self.types 	= types
		self.location_area_encounters = location_area_encounters
		self.stats 	= stats
		self.ttl	= ttl

		# ttl (time to live) is not available when pokemon is created from remote host query
		# then set the ttl from now + 7 days
		if not ttl:
			now 		= datetime.now()
			expire 		= now + timedelta(days=7)
			timestamp 	= datetime.timestamp(expire)
			self.ttl    = timestamp

		self.raw 	= {
			'id' 	: pid,
			'name' 	: name,
			'types'	: types,
			'stats' : stats,
			'location_area_encounters' : location_area_encounters,
			'ttl'	: self.ttl
		}

	@classmethod
	def query(cls, id_or_name:str) -> 'Pokemon':
		"""
		Returns a pokemon by its name or id

		Parameters
		----------
		id_or_name : str
			id or name of a pokemon

		Raises
        ------
		PokemonError
			if pokemon is not found by its id or name
			
		Returns
		-------
		pokemon : Pokemon
			an instance of Pokemon with respective details
		"""
		response = cls.build_request( 'pokemon' , id_or_name )

		if response.status_code != 200:
			raise PokemonError('Pokemon not found: %s'%(id_or_name))

		data  	 = response.json()

		response = cls.build_request( 'pokemon_enconter_locations' , id_or_name )
		location_area_encounters  	 = response.json()

		pokemon  = cls( str(data['id']) , data['name'], data['types'], location_area_encounters, data['stats'])

		return pokemon

	@staticmethod
	def build_request(endpoint:str, id_or_name:str) -> 'requests.models.Response':
		"""
		Constucts and send a remote GET request to query a pokemon by id or name

		Parameters
		----------
		id_or_name : str
			id or name of a pokemon 

		Returns
		-------
		response : requests.models.Response
			the response object for the GET request
		"""
		if endpoint not in Pokemon.ENDPOINTS:
			raise PokemonError('Unsupported API enpoint: %s'%(endpoint))

		url 	 = Pokemon.API_HOST + Pokemon.ENDPOINTS[endpoint]%(id_or_name)
		response = requests.get(url)

		return response

	@property
	def id(self) -> str:
		"""Get or set the id of a pokemon"""
		return self.__id

	@id.setter
	def id(self, value:str) -> None:
		self.__id = value

	@property
	def name(self) -> str:
		"""Get or set the name of a pokemon"""
		return self.__name

	@name.setter
	def name(self, value:str) -> None:
		self.__name = value

	@property
	def types(self) -> List[str]:
		"""Get or set the tyeps of a pokemon
		
		Returns
		-------
		types : List[str]
		"""
		types = []
		for t in self.__types:
			types.append(t['type']['name'])

		return types

	@types.setter
	def types(self,value:List[Dict]) -> None:
		self.__types = value

	@property
	def location_area_encounters(self) -> List[str]:
		"""Get or set the location area of encounters of a pokemon in kanto only
		
		Returns
		-------
		types : List[str]
		"""
		locations = []
		for l in self.__location_area_encounters:
			name = l['location_area']['name']
			# filter only location in kanto
			if name[0:len('kanto')] == 'kanto':
				locations.append(name)

		# if there are no encounter location in Kanto, display '-' 
		if len(locations) == 0:
			return '-'

		return locations

	@location_area_encounters.setter
	def location_area_encounters(self,value:List[Dict]) -> None:
		self.__location_area_encounters = value

	@property
	def stats(self) -> List[str]:
		"""Get or set the stats of a pokemon
		
		Returns
		-------
		types : List[str]
		"""
		stats = []
		for s in self.__stats:
			stats.append( s['stat']['name'] + '(%s)'%(str(s['base_stat'])) )
			
		return stats

	@stats.setter
	def stats(self, value:List[Dict]) -> None:
		self.__stats = value

	@property
	def ttl(self) -> float:
		return self.__ttl

	@ttl.setter
	def ttl(self, value:float):
		self.__ttl = value

	def serialize(self) -> Dict:
		"""
		return serializable data of pokemon	

		Returns
		-------
		raw : Dict
		"""
		return self.raw