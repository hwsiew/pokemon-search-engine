from .pokemon import Pokemon, PokemonError
from .cache import SimpleCache

class PokemonSearchEngine():
	"""
	A class to handle pokemon search query
	...
	Attributes
	----------

	Methods
	----------
	query(id_or_name:str) -> None
		print the result of pokemon query by id_or_name
	"""

	def __init__(self):
		# create a simple in memory cache to store result query before 
		self.cache = SimpleCache() 

	def query(self, id_or_name : str) -> None:
		"""
		print the result of pokemon query by id_or_name

		Parameters
		----------
		id_or_name : str
			id or name of a pokemon

		Returns
		-------
		None
		"""
		try:

			# check in memory cache if one is found or not
			pokemon = self.cache.get(id_or_name)
			if not pokemon:
				print('Loading...') # to specify query is fetch from remote host
				pokemon = Pokemon.query(id_or_name)
				self.cache.put( [pokemon.id,pokemon.name], pokemon )

			print('ID: %s'%(pokemon.id))
			print('Name: %s'%(pokemon.name))
			print('Types: %s'%(str(pokemon.types)))
			print('Stats [name(base_stat)]: %s'%(str(pokemon.stats)))
			print('Locations: %s'%(str(pokemon.location_area_encounters)))

		except PokemonError as error:
			print(error.message)

		