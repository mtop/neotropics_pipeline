class MySQL:
	def __init__(self):
		import ConfigParser
		config = ConfigParser.RawConfigParser()
		config.read('neotropis.cfg')
	
		self.gbif_db = config.get('MySQL', 'gbif_db')
		self.col_db = config.get('MySQL', 'col_db')
		self.db = config.get('MySQL', 'db')
		self.host = config.get('MySQL', 'host')
		self.user = config.get('MySQL', 'user')
		self.password = config.get('MySQL', 'password')
		

class Data:
	def __init__(self):
		import ConfigParser
		config = ConfigParser.RawConfigParser()
		config.read('neotropis.cfg')

		self.user_polygons = config.get('Polygons', 'user_polygons')
		self.occurrence_nr = config.get('Filters', 'occurrence_nr')
