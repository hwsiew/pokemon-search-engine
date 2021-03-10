from .pokemon import Pokemon, PokemonError

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
		pass

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

			pokemon = Pokemon.query(id_or_name)

			print('ID: %s'%(pokemon.id))
			print('Name: %s'%(pokemon.name))
			print('Types: %s'%(str(pokemon.types)))
			print('Stats [name(base_stat)]: %s'%(str(pokemon.stats)))
			print('Locations: %s'%(str(pokemon.location_area_encounters)))

		except PokemonError as error:
			print(error.message)

		