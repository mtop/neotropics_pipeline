#!/usr/bin/env python

class Results(object):
	
#	def __init__(self):
#		self.regionCoding = regionCoding()
#		self.speciesDict = self.regionCoding.getSpeciesDict()
#		self.polyDict =  self.regionCoding.getPolygons()
#		self.uid = self.UserInput.Data()
#		self.raw_speciesList = self.uid.specieslist()
#		self.speciesDictionary = self.SpeciesList.speciesDict(self.raw_speciesList)
#		self.speciesDict = self.speciesDictionary.getDict()

	def getResultDict(self, polyDict, speciesDict):
#		print self.speciesDict
#		print self.polyDict
		resultDict = {}
		polyList = []
		# polyList holds the absent (0), pressent (1) information 
		# for each species and polygon. Absent is the initial value.
		for key in polyDict:
			polyList.append(0)
		for name in speciesDict:
#			print "name :", name				# Devel.
			resultDict[name] = polyList[:]
#		print "In Result(): ", resultDict
		return resultDict


class regionCoding(object):
	import SpeciesList
	import UserInput
	import QueryGBIF
	import PointInPolygon
#import Countries
#import Filters
#import SpeciesInPolygon as sip

	def __init__(self):
		self.uid = self.UserInput.Data()
		self.raw_speciesList = self.uid.specieslist()
		self.speciesDictionary = self.SpeciesList.speciesDict(self.raw_speciesList)
#		self.speciesDictionary = self.SpeciesList.speciesDict(self.uid.specieslist)
		# create an object with accepted names and respective synonyms 
		self.speciesDict = self.speciesDictionary.getDict()
		# create an object with the userdefined species list
		self.specieslist = self.speciesDictionary.getNameList()
		# create an object with the userdefined polygons
		self.user_polygons = self.uid.user_polygons()
		self.polygon_names = self.uid.polygon_names
		self.gbif = self.QueryGBIF.gbif()
		# Create an object to store the results in
		my_analysis = Results()
		self.result = my_analysis.getResultDict(self.getPolygons(), self.getSpeciesDict())

	def getSpecieslist(self):
		# Output: Raw species list provided by 
		# 	      the user and read from config file
		return self.specieslist

	def getPolygons(self):
		# Returns a dictionary. Keys are numbers and 
		# values are a string of polygon coordinates.
		polyDict = {}
		key = 0 
		for poly in self.user_polygons:
			polyDict[key] = poly
			key += 1
		return polyDict

	def getPolyNames(self):
		raw_names = self.polygon_names
		name_list = raw_names.split(' ')
		polyNameDict = {}
		key = 0
		for name in name_list:
			polyNameDict[key] = name
			key += 1
		return polyNameDict

	def getSpeciesDict(self):
		return self.speciesDict

	def __main__(self):
		for speciesName in self.speciesDict:
#			print "### speciesName: ", speciesName, '###'						# Devel.
			# Query GBIF using the key taxon name
			# and retreive a list of GBIF taxon id's.
#			gbifIds = self.gbif.getGbifIds(speciesName)		
			self.getSpeciesCoord(speciesName)
			self. getSynCoord(speciesName)
		self.printNexus()


	def getSpeciesCoord(self, speciesName):
#	def getSpeciesCoord(self, gbifIds, speciesName): 
		gbifIds = self.gbif.getGbifIds(speciesName)
		# Get location data for each GBIF taxon id.
		done = False
		for speciesId in gbifIds:
			# Break out of the loop and continue 
			# with next species name if found in 
			# all polygons
			if done:
				break
#			print "GBIF speciesId: ", speciesId					# Devel.
			coordinates = self.gbif.getLocations(speciesId)
			self.testCoord(coordinates, speciesName, speciesId)
#			# For each lat/long pair, check if it falls 
#			# within one of the user polygons.
#			for pair in coordinates:
#				print "Coord. pair: ", pair						# Devel.
#				# Test if coordinate pair is found in any polygon.
#				# But first test if taxon with this species name 
#				# has been found in all polygons already.
#				if sum(self.result[speciesName]) < len(self.result[speciesName]):
#					self.isPointInPoly(pair, speciesName, speciesId)
#				else:
#					done = True
#					print "I'm done with %s" % speciesName
#					break


	def getSynCoord(self, speciesName):
		done = False
		# Also test the synonymous names
		for value in self.speciesDict[speciesName]:
			if done:
				break
#			print "Testin synonyms for %s" % speciesName				# Devel.
			# Query GBIF using the value taxon names
			# and retreive a list of GBIF taxon id's.
			gbifIds = self.gbif.getGbifIds(value)
			# Get location data for each GBIF taxon id.
			for speciesId in gbifIds:
				if done:
					break
				coordinates = self.gbif.getLocations(speciesId)
				self.testCoord(coordinates, speciesName, speciesId)


	def testCoord(self, coordinates, speciesName, speciesId):
		for pair in coordinates:
			# Test if coordinate pair is found in any polygon.
			# But first test if taxon with this species name
			# has been found in all polygons already.
			if sum(self.result[speciesName]) < len(self.result[speciesName]):
				self.isPointInPoly(pair, speciesName, speciesId)
			else:
				done = True
				return done

	def isPointInPoly(self, coordinate, speciesName, GBIFspeciesId):
		polygons = self.getPolygons()
#		result = []
		for poly in polygons:
			# Check if this species already has 
			# been found in this polygon. 
			# If so, move on to the next polygon.
#			print self.result
			if self.result[speciesName][poly] != 0:
				continue
			else:
#				print "Testing %s in poly nr: " % speciesName, poly				# Devel.
				longitude = coordinate[0]
				latitude =  coordinate[1]
				self.pip = self.PointInPolygon.pointInPolygon() # pip(polygon, longitude, latitude)
				if self.pip.evaluate(polygons[poly], longitude, latitude) == True:
#					print speciesName, ' ', poly
					self.result[speciesName][poly] = 1
#					print "I found %s in polygon nr. %s" % (speciesName, poly)		# Devel.


	def printNexus(self):
		# Print the results to stdOut in NEXUS format.
		# Use a redirect to store in file.
		print "#NEXUS\n"
		print "Begin data;"
		print "\tDimensions ntax=%s nchar=%s;" % (len(self.getSpecieslist()), len(self.getPolyNames()))
		print "\tFormat datatype=standard symbols=\"01\" gap=-;"
		print "\tCHARSTATELABELS"
		# Print the names of the polygons
		for i in range(len(self.getPolyNames())):
			if i+1 < len(self.getPolyNames()):
				print "\t%s %s"	% (i+1, self.getPolyNames()[i]) + ','
			if i+1 == len(self.getPolyNames()):
				print "\t%s %s" % (i+1, self.getPolyNames()[i]) + ';'
		print "\n"
		print "\tMatrix"
		# Print the species names and character matrix
		for name in self.result:
			print name.replace(" ","_"), '\t', self.resultToStr(self.result[name])
		print '\t;'
		print 'End;'


	def resultToStr(self, resultList):
		string = ''
		for i in resultList:
			string += str(i)
		return string
		

		


# write the content of result object to output file


if __name__ == '__main__':
	potentilla = regionCoding()
	my_analysis = Results()
#	print potentilla.raw_speciesList		# Ok!
#	print potentilla.getSpecieslist()		# Ok!
#	print potentilla.getPolygons()			# Ok!
#	print potentilla.getPolyNames()			# Ok!
#	print potentilla.getSpeciesDict()		# Ok!
#	print potentilla.getCoordinates()
#	print my_analysis.getResultDict()
	potentilla.__main__()

"""
def generate_country_list():
	# For each user defined polygon, Identify 
	# countries from where all species should 
	# be included in downstream analyses,
	# and countries where only some species 
	# should be included.

	c_all, c_some = Countries.all_species(polygon)
	print "1. In __main__: c_all  = ", c_all				# Devel.
	print "1. In __main__: c_some = ", c_some				# Devel.
	c_some = Countries.some_species(c_some)					# Why "c_some" as variable???
	print "2. In __main__: c_all  = ", c_all				# Devel.
	print "2. In __main__: c_some = ", c_some				# Devel.
	return c_all, c_some


def generate_species_lists(c_all, c_some, polygon):
	# Create a list of all species found in a 
	# user defined polygon.
	# Start with species from countries fully
	# enclosed by the user defined polygon
	if uid.taxon:
		print "Applying taxon filter."							# Devel.	
		rank = uid.taxon.split()[0]
		taxon_name = uid.taxon.split()[1]
		raw_species_list_plants, raw_species_list_animals, raw_species_list_fungi = QueryGBIF.qgd(c_all, c_some, polygon, rank, taxon_name)
	else:
		print "No taxon filtering required."					# Devel.
		raw_species_list_plants, raw_species_list_animals, raw_species_list_fungi = QueryGBIF.qgd(c_all, c_some, polygon)
#	print "In __main__: raw_species_list_plants = ", raw_species_list_plants		# Devel.
#	print "In __main__: It is time for filtering!"				# Devel.


#	raw_species_list = QueryGBIF.qgd(c_all)
#	raw_species_list = QueryGBIF.qgd(c_all[0])					# Working
	species_list_plants = Filters.occurrence_nr(raw_species_list_plants)
#	print species_list_plants									# Devel.
	species_list_animals = Filters.occurrence_nr(raw_species_list_animals)
	species_list_fungi = Filters.occurrence_nr(raw_species_list_fungi)
#	species_list = Filters.occurrence_nr(raw_species_list)		# Devel.
	return species_list_plants, species_list_animals, species_list_fungi


def numbers_to_names(species_list, sufix):
	# Convert the numerical species list 
	# to a list containing species names.
	# THIS FUNCTION IS NOT REQUIRED ANYMORE 
	# SINCE "raw_occurrence_record_<ISO>" 
	# RETURNS CLEAR TEXT SPECIES NAMES.
	filtered_species_list =[]
	for number in species_list:
		name = QueryGBIF.species_name(number)
		species_name = str(name[0])+" "+str(name[1])
		print species_name		# Devel.
		if species_name not in filtered_species_list and species_name is not 'None None': # 'None None' is not working yet
			filtered_species_list.append(species_name)
	write_output_file(filtered_species_list, sufix)


def write_output_file(filtered_species_list, sufix):
	# Write species list to file.
	for name in filtered_species_list:
#		print str(species_name[0]), str(species_name[1])
#		name = str(species_name[0]), str(species_name[1])	# Remove ????
#		print name								# Devel.
		output = open('species_list_%s.txt' % sufix, "a")
		output.write(str(name))
#		output.write(str(species_name[0]))
#		output.write(" ")
#		output.write(str(species_name[1]))
		output.write("\n")
		output.close()
#		write_output_file(str(species_name))
		"""

#def write_output_file(species_list, sufix):
 #   output = open('species_list_%s.txt' % sufix, "w")
 #   output.write(species_list)
 #   output.close()

	
#	print "raw_species_list contains %s records" % len(raw_species_list)	# Devel.
#	print "species_list contains %s records" % len(Filters.occurrence_nr(raw_species_list))		# Devel.
#	sip.additional_species(c_some, species_list, raw_species_list, polygon)
"""
"""
	
#	c_all = ['AD']
#	c_some = ['NO']
#	c_all = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'IS', 'NO']
#	generate_country_list()
#	generate_species_list(c_all, c_some)
#	species_list_plants, species_list_animals, species_list_fungi = generate_species_list(c_all, c_some)
#	numbers_to_names(species_list_plants, 'plants')
#	numbers_to_names(species_list_animals, 'animals')
#	numbers_to_names(species_list_fungi, 'fungi')

#	for polygon in uid.user_polygons.split(':'):
#		c_all, c_some = generate_country_list()
#		species_list_plants, species_list_animals, species_list_fungi = generate_species_lists(c_all, c_some, polygon)
#		print "In __main__ species_list_plants = ", species_list_plants		# Devel
#		write_output_file(species_list_plants, sufix)

# Examples:
# For each user defined polygon, generate separate lists of species per kingdom (Plantae, Animalia and Fungi):
# for polygon in uid.user_polygons.split(':'):
# 	generate_species_lists(generate_country_list())		
