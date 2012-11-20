#!/usr/bin/env python

import MySQLdb as mdb
import UserInput

class speciesDict(object):
# The speciesDict object contains a dictionary 
# of species names as keys, and a list of their 
# respective synonymous names as values. 
# The taxonomy is retreived from a local installation
# of the Catalogue of Life database.


	def __init__(self, speciesList):
		# Input: List of species names.
		self.speciesList = speciesList

	def getNameList(self):
		# Returns the original species list
		return self.speciesList

	def getDict(self):
		# Input: List of species names
		# Output: Dictionary of synonymous names. Correct name as key.
		nameDict = {}
		for taxonName in self.speciesList:
			# Test if name has a taxon_id (or a synonym_id instead)
			if self.getTaxonId(taxonName):
				# Some names have several taxonIds. Only use the first one
				taxonId = self.getTaxonId(taxonName)[0]
				synonymes = self.getSynNames(taxonId)		# "synonymes" contains synonymous names.
				# Test if names in speciesList are accepted
				if self.getStatus(taxonId) == 'accepted name':
					nameDict[taxonName] = self.uniqeNames(synonymes, taxonName)
			# elif the name is a synonym
			elif not self.getTaxonId(taxonName):
				taxonIds = self.getSynTaxonId(taxonName)
				# If several accepted names are associated with the synonyme 
				# (I suppose this will happen if two subspecies of the synonym 
				# are recogniced as individual species. Try with "Argentina anserina"
				# that will return the two accepted names "Potentilla anserina" and 
				# "Anserina groenlandica".
				for taxonId in taxonIds:
					taxonName = self.getTaxonName(taxonId)
					synonymes = self.getSynNames(taxonId)
					# Remove accepted name from synonyme list
					nameDict[taxonName] = self.uniqeNames(synonymes, taxonName)
		return nameDict

	
	def uniqeNames(self, nameList, taxonName):
		# Input: "nameList" = List of duplicated synonymous names that also may include the accepted name.
		#		 "taxonName" = A taxon name that should be removed from "nameList".	
		# Output: List of unique names
		keys = {}
		for name in nameList:
			if name == taxonName:
				continue
			else:
				keys[name] = 1
		return keys.keys()


	def getStatus(self, speciesId):
		# Imput: species id
		# Output: String declaring the taxonomic status 
		# for the species name (e.g. 'accepted name' or 
		# 'provisionally accepted name')
		db = UserInput.MySQL()
		con = mdb.connect(db.host, db.user, db.password, db.col_db)
		with con:
			cur = con.cursor()
			sql_string = "select name_status from scientific_name_status where id = (select scientific_name_status_id from taxon_detail where taxon_id = '%s')" % speciesId
			cur.execute(sql_string)
			status = cur.fetchall()
			return status[0][0]


	def queryDb(self, sql_string):
		db = UserInput.MySQL()
		con = mdb.connect(db.host, db.user, db.password, db.col_db)
		with con:
			cur = con.cursor()
			cur.execute(sql_string)
			output = cur.fetchall()
			return output 


	def getTaxonName(self, taxonId):
		db = UserInput.MySQL()
		con = mdb.connect(db.host, db.user, db.password, db.col_db)
		with con:
			cur = con.cursor()
			sql_string_genus = "select name_element from scientific_name_element where id = (select scientific_name_element_id from taxon_name_element where taxon_id = (select parent_id from taxon_name_element where taxon_id='%s'))" % taxonId
			sql_string_species = "select name_element from scientific_name_element where id = (select scientific_name_element_id from taxon_name_element where taxon_id='%s')" % taxonId
			cur.execute(sql_string_genus)
			genus = cur.fetchall()
			cur.execute(sql_string_species)
			species = cur.fetchall()
			species_name = genus[0][0].capitalize() + ' ' + species[0][0]
			return species_name
			
	def getSynNames(self, speciesId):
		# Input: Species id
		# Output: List of synonymous names
		db = UserInput.MySQL()
		con = mdb.connect(db.host, db.user, db.password, db.col_db)
		with con:
			cur = con.cursor()
			sql_string = "select id from synonym where taxon_id ='%s'" % speciesId
			cur.execute(sql_string)
			synIds = cur.fetchall()
			synNames = []
			for i in synIds:
				sql_string_genus = "select name_element from scientific_name_element where id = (select scientific_name_element_id from synonym_name_element where taxonomic_rank_id = '20' and synonym_id = '%s')" % i[0]
				sql_string_species = "select name_element from scientific_name_element where id = (select scientific_name_element_id from synonym_name_element where taxonomic_rank_id = '83' and synonym_id = '%s')" % i[0]
				genus = self.queryDb(sql_string_genus)
				species = self.queryDb(sql_string_species)
				synName = genus[0][0].capitalize() + ' ' + species[0][0]
				synNames.append(synName)
			return synNames


	def getTaxonId(self, name):
		# Input: A species name like 'Potentilla alba'
		# Output: A list of taxon id's of synonymous names
		genus = name.split()[0]
		species = name.split()[1]
		db = UserInput.MySQL()
		con = mdb.connect(db.host, db.user, db.password, db.col_db) # Host, user name, password, database name
		with con:
			cur = con.cursor()
			sql_string = "SELECT taxon_id FROM taxon_name_element WHERE (scientific_name_element_id=(select id from scientific_name_element where name_element='%s')) AND parent_id=any(select taxon_id from taxon_name_element where scientific_name_element_id=(select id from scientific_name_element where name_element='%s'))" % (species, genus)
			cur.execute(sql_string)
			species_id = cur.fetchall()
			idList = []
			for i in species_id:
				idList.append(i[0])
			return idList


	def getSynTaxonId(self, name):
		# Input: Synonymous species name
		# Output: List of taxon id's of accepted name
		genus = name.split()[0]
		species = name.split()[1]
		sql_string_synId = "SELECT synonym_id FROM synonym_name_element WHERE taxonomic_rank_id ='20' and scientific_name_element_id = (SELECT id FROM scientific_name_element WHERE name_element='%s') and synonym_id in (SELECT synonym_id FROM synonym_name_element WHERE taxonomic_rank_id ='83' and scientific_name_element_id = (SELECT id FROM scientific_name_element WHERE name_element='%s'))" % (genus, species)
		synIds = self.queryDb(sql_string_synId)
		taxonIdList = []
		for synId in synIds:
			sql_string_taxonId = "SELECT taxon_id from synonym where id = '%s'" % synId
			taxonId = self.queryDb(sql_string_taxonId)
			for i in taxonId:
				if int(i[0]) not in taxonIdList:
					taxonIdList.append(int(i[0]))
				else:
					continue	
		return taxonIdList


if __name__ == "__main__":
	names = speciesDict(['Potentilla alba', 'Argentina anserina'])
	longList = ['Argentina anserina', 'Argentina anserina', 'Potentilla anserina', 'Potentilla egedii', 'Potentilla yukonensis']
	taxonName = 'Potentilla anserina'
	taxonId_1 = '7209247'   # Potentilla anserina
	taxonId_2 = '7167046'   # Potentilla alba
	taxonId_3 = '7197490'   # Anserina groenlandica
	synId_1 = '7211961'     # Argentina anserina
	genus = 'Potentilla'
	species = 'alba'
	taxonName_1 = 'Potentilla anserina'
	taxonName_2 = 'Potentilla alba'
	taxonName_3 = 'Anserina groenlandica'
	sql_string_1 = "select name_status from scientific_name_status where id = (select scientific_name_status_id from taxon_detail where taxon_id = '%s')" % taxonId_1
	sql_string_2 = "SELECT taxon_id from synonym where id = '%s'" % synId_1
	sql_string_3 = "SELECT taxon_id FROM taxon_name_element WHERE (scientific_name_element_id=(select id from scientific_name_element where name_element='%s')) AND parent_id=any(select taxon_id from taxon_name_element where scientific_name_element_id=(select id from scientific_name_element where name_element='%s'))" % (species, genus)
#	print names.queryDb(sql_string_1)
#	print names.getSynTaxonId(taxonName_1)
#	print names.getSynTaxonId(taxonName_2)
#	print names.getSynTaxonId(taxonName_3)
#	print names.getTaxonId(taxonName_1)
#	print names.getTaxonId(taxonName_2)
#	print names.getTaxonId(taxonName_3)
#	print names.queryDb(sql_string_3)
#	print names.uniqeNames(longList, taxonName)
#	names = speciesDict(['Dasiphora alba'])
#	names = speciesDict(['Dasiphora alba', 'Potentilla alba'])
#	names = speciesDict(['Potentilla alba', 'Argentina anserina', 'Duchesnea indica', 'Potentilla indica'])
#	names = speciesDict(['Argentina anserina'])
#	print names.getTaxonName('7197490')
#	print names.getStatus('7209247')
#	print names.getTaxonName('7197490')
#	print names.getStatus('7209247')
#	print names.getStatus('7167046')
#	print names.getStatus('7197490')
#	print names.getSynTaxonId('Dasiphora alba')
#	print names.getSynTaxonId('Argentina anserina')
#	print names.getSynNames(taxonId_1)
#	print names.getSynNames(taxonId_2)
#	print names.getSynNames(taxonId_3)
#	print names.synNames('7215711')
#	print names.synNames('7216263')
#	print names.synNames('7222278')
#	print names.getNameList()
#	print names.getDict()
#	print names.getStatus('7197490')
#	print name.getList(['Potentilla alba'])
#	print name.getList(['Potentilla alba'])
