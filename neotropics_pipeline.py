#!/usr/bin/env python

import UserInput
import Countries
import QueryGBIF
import Filters

uid = UserInput.Data()

"""     For each user defined polygon, Identify 
		countries from where all species should 
		be included in downstream analyses,
		and countries where only some species 
		should be included.
"""
for polygon in uid.user_polygons.split(':'):
	c_all = Countries.all_species(polygon)				# Working
	c_some = Countries.some_species(c_all[1])			# Working
	#print c_all[0]										# Devel.
	#print c_some										# Devel.

	#c_all = ['IS']										# Devel.
	""" Create a list of all species found in a 
		user defined polygon """
	raw_species_list = QueryGBIF.qgd(c_all[0])			# Working
#	print str(raw_species_list)							# Devel.
#	print raw_species_list.count(2038894)				# Devel. 
	print "raw_species_list contains %s records" % len(raw_species_list)
#	Filters.occurrence_nr(raw_species_list)				# Working	
	print "species_list contains %s records" % len(Filters.occurrence_nr(raw_species_list))		# Devel.


	#code = 'IS'										# Devel.
	#print QueryGBIF.qgd(code)								# Devel.
	#print QueryGBIF.raw_species_list(code)			# Devel.

	#print c[0]	# Devel
	#print c[1]	# Devel
	#print Countries.some_species(c[1])	# Devel


