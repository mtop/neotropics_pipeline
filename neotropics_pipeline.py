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

	""" Create a list of all species found in a 
		user defined polygon """
	raw_species_list = QueryGBIF.qgd(c_all[0])			# Working
	print "raw_species_list contains %s records" % len(raw_species_list)	# Devel.
	print "species_list contains %s records" % len(Filters.occurrence_nr(raw_species_list))		# Devel.

