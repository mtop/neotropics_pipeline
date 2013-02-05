#!/usr/bin/env python

#
# Input:	See the example files.
#

from optparse import OptionParser

# Figure out the options and arguments
def input(option, opt_str, value, parser):
	assert value is None
	value = []
	for arg in parser.rargs:
		# Stop on --foo like option
		if arg[:2] == "--" and len(arg) > 2:
			break
		# Stop on -a
		if arg[:1] == "-" and len(arg) > 1:
			break
		value.append(arg)
	del parser.rargs[:len(value)]
	setattr(parser.values, option.dest, value)

usage = "\n  %prog -p [Polygon_file] -l [Locality_data_file] -o [Optional_output_file]"
opts=OptionParser(usage=usage, version="%prog v.0.1")

opts.add_option("--polygons", "-p", dest="polygons", action="callback",
callback=input, help="Path to file containing polygon coordinates")

opts.add_option("--localities", "-l", dest="localities", action="callback",
callback=input, help="Path to file containig species locality data")

opts.add_option("--out", "-o", dest="output", action="callback",
callback=input, default=[None], help="Name of optional outputfile. Output is otherwise sent to STDOUT by default")

options, arguments = opts.parse_args()


class Polygons(object):
	# Object that contains the polygons
	def __init__(self):
		self.polygonFile = options.polygons[0]

	def getPolygons(self):
		f = open(self.polygonFile)
		lines = f.readlines()
		for line in lines:
			if not line:
				break
			splitline = line.split(':')
			name = splitline[0]
			polygon = self.prepare_poly(splitline[1])
			yield name, polygon

	def prepare_poly(self, poly):
		poly = poly.split(' ')
		poly_2 = []
		for node in list(poly):
			if not node:
				pass
			else:
				mod = ('%s') % node
				poly_2.append(mod)
		return poly_2
									


class Localities(object):
	# Objec that contains the locality data,
	def __init__(self):
		self.localityFile = options.localities[0]

	def getLocalities(self):
		f = open(self.localityFile)
		lines = f.readlines()
		for line in lines:
			if not line:
				break
			# Skip comments in the file
			if line[0] == "#":
				continue
			splitline = line.split()
			numbers = splitline[0]
			species = splitline[1] + ' ' + splitline[2]
			longitude = splitline[3]
			latitude = splitline[4]
			yield numbers, species, longitude, latitude


def pointInPolygon(poly, x, y):
	# Returns "True" if a point is inside a given polygon. 
	# Othewise returns "False". The polygon is a list of 
	# Longitude/Latitude (x,y) pairs.
	# Code modified from  http://www.ariel.com.au/a/python-point-int-poly.html

	x = float(x)
#	print x     		# Devel.
	y = float(y)
#	poly = prepare_poly(poly)
#	print poly			# Devel.
#	print poly[0]		# Devel.
	n = len(poly)
	inside = False
	p1x = float('%s' % poly.split(',')[0])
#	print type(p1x)     # Devel.
	print p1x           # Devel.
	print poly.split(',')[1]	# Devel.
	p1y = float('%s' % poly.split(',')[1])
#   print type(p1y)     # Devel.
#   print p1y           # Devel.
	for i in range(n+1):
		p2x = float('%s' % poly[i % n].split(',')[0])
#       print type(p2x) # Devel.
#       print p2x       # Devel.
		p2y = float('%s' % poly[i % n].split(',')[1])
#       print type(p2y) # Devel.
#       print p2y       # Devel.
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y
	return inside

def prepare_poly(poly):
	poly = poly.split(' ')
	poly_2 = []
	for node in list(poly):
		mod = ('%s') % node
		poly_2.append(mod)
	return poly_2

def main():
	# Read the locality data and test if the coordinates 
	# are located in any of the polygons.
	polygons = Polygons()
	localities = Localities()
	for polygon in polygons.getPolygons():
#		print polygon[1]
		for locality in localities.getLocalities():
			print pointInPolygon(polygon[1], locality[2], locality[3])


if __name__ == "__main__":
	main()
#	polygons = Polygons()
#	for i in polygons.getPolygons():
#		print i
	


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
#	import SpeciesList
#	import UserInput
#	import QueryGBIF
#	import PointInPolygon
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


#	potentilla = regionCoding()
#	my_analysis = Results()
#	print potentilla.raw_speciesList		# Ok!
#	print potentilla.getSpecieslist()		# Ok!
#	print potentilla.getPolygons()			# Ok!
#	print potentilla.getPolyNames()			# Ok!
#	print potentilla.getSpeciesDict()		# Ok!
#	print potentilla.getCoordinates()
#	print my_analysis.getResultDict()
#	potentilla.__main__()

