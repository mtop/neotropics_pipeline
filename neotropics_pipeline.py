#!/usr/bin/env python

import UserInput
import Countries
import QueryGBIF
import Filters
import SpeciesInPolygon as sip

uid = UserInput.Data()

def generate_country_lists():
""" For each user defined polygon, Identify 
	countries from where all species should 
	be included in downstream analyses,
	and countries where only some species 
	should be included."""
	for polygon in uid.user_polygons.split(':'):
		c_all = Countries.all_species(polygon)				# Working # Includes all species from these countries 
		c_some = Countries.some_species(c_all[1])			# Working # Includes some species from these countries
		print c_all[0]										# Devel.
		return c_all, c_some
		#print c_some										# Devel.


def generate_species_list(c_all, c_some):
""" Create a list of all species found in a 
	user defined polygon.""" 
	raw_species_list_plants, raw_species_list_animals, raw_species_list_fungi = QueryGBIF.qgd(c_all)
#	raw_species_list = QueryGBIF.qgd(c_all)
#	raw_species_list = QueryGBIF.qgd(c_all[0])				# Working
	species_list_plants = Filters.occurrence_nr(raw_species_list_plants)
	print species_list_plants		# Devel.
	species_list_animals = Filters.occurrence_nr(raw_species_list_animals)
	species_list_fungi = Filters.occurrence_nr(raw_species_list_fungi)
#	species_list = Filters.occurrence_nr(raw_species_list)
	return species_list_plants, species_list_animals, species_list_fungi


def numbers_to_names(species_list, sufix):
""" Convert the numerical species list 
	to a list containing species names.""" 
	filtered_species_list =[]
	for number in species_list:
		name = QueryGBIF.species_name(number)
		species_name = str(name[0])+" "+str(name[1])
		print species_name		# Devel.
		if species_name not in filtered_species_list and species_name is not 'None None': # 'None None' is not working yet
			filtered_species_list.append(species_name)
	write_output_file(filtered_species_list, sufix)


def write_output_file(filtered_species_list, sufix):
"""	Write species list to file."""		
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

def write_output_file(species_list, sufix):
    output = open('species_list_%s.txt' % sufix, "w")
    output.write(species_list)
    output.close()

	
#	print "raw_species_list contains %s records" % len(raw_species_list)	# Devel.
#	print "species_list contains %s records" % len(Filters.occurrence_nr(raw_species_list))		# Devel.
#	sip.additional_species(c_some, species_list, raw_species_list, polygon)
"""

if __name__ == '__main__':
	c_all = ['AD']
	c_some = ['NO']
#	c_all = ['AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'IS', 'NO']
#	generate_country_lists()
#	generate_species_list(c_all, c_some)
	species_list_plants, species_list_animals, species_list_fungi = generate_species_list(c_all, c_some)
	numbers_to_names(species_list_plants, 'plants')
	numbers_to_names(species_list_animals, 'animals')
	numbers_to_names(species_list_fungi, 'fungi')
