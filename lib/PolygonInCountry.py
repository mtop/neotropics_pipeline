#!/usr/bin/env python
# -*- coding: utf-8 -*-

###   Copyright (C) 2012 Mats Töpel.

###   This program is free software: you can redistribute it and/or modify
###   it under the terms of the GNU General Public License as published by
###   the Free Software Foundation, either version 3 of the License, or
###   (at your option) any later version.
###   
###   This program is distributed in the hope that it will be useful,
###   but WITHOUT ANY WARRANTY; without even the implied warranty of
###   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###   GNU General Public License for more details at
###   http://www.gnu.org/licenses/.


# Determine if a country is fully, partially or not at all part of a user defined polygon
# Usage: ./CountryInPolygon.py <ISO2_code>


import MySQLdb as mdb
from PointInPolygon import pip
import UserInput

uim = UserInput.MySQL()
uid = UserInput.Data()

def pic(user_polygon):		# pic = "Polygon in country"
	for code in get_iso():
##		T = 0
##		F = 0
		t = run_test(user_polygon, code)
		if t != None:
			return t[0]
			break


# Extract the ISO2 country codes from the database
def get_iso():
	con = mdb.connect(uim.host, uim.user, uim.password, uim.db)
	with con:
		cur = con.cursor()
		sql_string = "SELECT ISO2 FROM country_polygons"
		cur.execute(sql_string)
		ISO2_code = list(cur.fetchall())
		return ISO2_code


# Retreive the country polygons from the database, and 
# then test each node in the user polygon using the 
# "Point in Polygon" algorith
def pic(user_polygon):      # pic = "Polygon in country"
    for iso_code in get_iso():
# def run_test(user_polygon, iso_code):
		con = mdb.connect(uim.host, uim.user, uim.password, uim.db)
		with con:
			cur = con.cursor()
			sql_string = "SELECT polygons FROM country_polygons WHERE ISO2='%s'" % iso_code
			cur.execute(sql_string)
			country_polygon = list(cur.fetchall()[0])[0]
#			T = 0
#			F = 0
			# The contry polygon may be made up of several polygons separated by ':'.
			for poly in country_polygon.split(':'):
				T = 0
				F = 0
				for node in user_polygon.split(' '):
					x = float(node.split(',')[0])
					y = float(node.split(',')[1])
					test = pip(poly, x, y)
					if test == True:
						T = 1
					elif test == False:
						F = 1
				# Polygon in country (Country is only one polygon)
				if T == 1 and F == 0:
					return iso_code[0]
#			# Polygon not in country
#			if T == 0 and F == 1:
#				print "no"
#				# Polygon in one of the country polygons (Country has many polygons)
#				if T == 1 and F == 1:
#					return iso_code


if __name__ == '__main__':
	import ConfigParser
	config = ConfigParser.RawConfigParser()
	config.read('neotropis.cfg')
	host = config.get('MySQL', 'host')
	db = config.get('MySQL', 'db')
	user = config.get('MySQL', 'user')	
	password = config.get('MySQL', 'password')
	user_polygon = config.get('Polygons', 'part_of_sweden')
	print pic(user_polygon)
