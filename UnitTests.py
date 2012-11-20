#!/usr/bin/env python

import unittest
import SpeciesList

class Test_SpeciesList(unittest.TestCase):
	names_1 = SpeciesList.speciesDict(['Potentilla alba', 'Argentina anserina'])
	taxonId_1 = '7209247'	# Potentilla anserina
	taxonId_2 = '7167046'	# Potentilla alba
	taxonId_3 = '7197490'	# Anserina groenlandica
	synId_1 = '7211961'		# Argentina anserina
	genus_1  = 'Potentilla'
	species_1 = 'alba'
	taxonName_1 = 'Potentilla anserina'
	taxonName_2 = 'Potentilla alba'
	taxonName_3 = 'Anserina groenlandica'
	longOutput_1 = {'Potentilla alba': ['Potentilla caulescens', 'Fragariastrum album', 'Trichothalamus albus', 'Potentilla cordata', 'Potentilla nitida', 'Dasiphora alba'], 'Anserina groenlandica': ['Potentilla anserina', 'Potentilla egedii', 'Argentina egedii', 'Argentina anserina'], 'Potentilla anserina': ['Potentilla egedii', 'Potentilla yukonensis', 'Argentina anserina']}
	longOutput_2 = ['Argentina anserina', 'Argentina anserina', 'Potentilla anserina', 'Potentilla egedii', 'Potentilla yukonensis']
	longOutput_3 = ['Dasiphora alba', 'Fragariastrum album', 'Potentilla caulescens', 'Potentilla cordata', 'Potentilla nitida', 'Trichothalamus albus']
	longOutput_4 = ['Argentina anserina', 'Argentina anserina', 'Argentina egedii', 'Potentilla anserina', 'Potentilla anserina', 'Potentilla anserina', 'Potentilla egedii', 'Potentilla egedii']
	longInput_1 = ['Argentina anserina', 'Argentina anserina', 'Potentilla anserina', 'Potentilla egedii', 'Potentilla yukonensis']
	sql_string_1 = "select name_status from scientific_name_status where id = (select scientific_name_status_id from taxon_detail where taxon_id = '%s')" % taxonId_1
	sql_string_2 = "SELECT taxon_id from synonym where id = '%s'" % synId_1
	sql_string_3 = "SELECT taxon_id FROM taxon_name_element WHERE (scientific_name_element_id=(select id from scientific_name_element where name_element='%s')) AND parent_id=any(select taxon_id from taxon_name_element where scientific_name_element_id=(select id from scientific_name_element where name_element='%s'))" % (species_1, genus_1)

	def test_getTaxonName(self):
		self.assertEqual(self.names_1.getTaxonName(self.taxonId_1), "Potentilla anserina", "getTaxonName failed to find the name 'Potentilla anserina' for taxon id 7209247")
		self.assertEqual(self.names_1.getTaxonName(self.taxonId_2), "Potentilla alba", "getTaxonName failed to find the name 'Potentilla alba' for taxon id 7167046")
		self.assertEqual(self.names_1.getTaxonName(self.taxonId_3), "Anserina groenlandica", "getTaxonName failed to find the name 'Anserina groenlandica' for taxon id 7197490")


	def test_getNameList(self):
		self.assertEqual(self.names_1.getNameList(),['Potentilla alba', 'Argentina anserina'], "getNameList failed to return the list ['Potentilla alba', 'Argentina anserina']") 


	def test_getDict(self):
		self.assertEqual(self.names_1.getDict(), self.longOutput_1, "getDict failed to return the dictionary of synonymous names for 'Potentilla alba' and 'Argentina anserina'")


	def test_uniqeNames(self):
		self.assertEqual(self.names_1.uniqeNames(self.longInput_1, self.taxonName_1) ,['Potentilla egedii', 'Potentilla yukonensis', 'Argentina anserina'], "uniqeNames failed to produce the correct output for 'Potentilla anserina'")

	def test_getStatus(self):
		self.assertEqual(self.names_1.getStatus(self.taxonId_1), "accepted name", "getStatus failed to identify the correct taxonomic status for the name Potentilla anserina")
		self.assertEqual(self.names_1.getStatus(self.taxonId_2), "accepted name", "getStatus failed to identify the correct taxonomic status for the name Potentilla alba")
		self.assertEqual(self.names_1.getStatus(self.taxonId_3), "accepted name", "getStatus failed to identify the correct taxonomic status for the name Anserina groenlandica")

	def test_queryDb(self):
		self.assertEqual(self.names_1.queryDb(self.sql_string_1), (('accepted name',),), "queryDb failed to produce the correct output for sql_string_1")
		self.assertEqual(self.names_1.queryDb(self.sql_string_2), ((7209247L,),), "queryDb failed to produce the correct output for sql_string_1")
		self.assertEqual(self.names_1.queryDb(self.sql_string_3), ((7167046L,), (7193078L,)), "queryDb failed to produce the correct output for sql_string_1")

	def test_getSynNames(self):
		self.assertEqual(self.names_1.getSynNames(self.taxonId_1), self.longOutput_2, "getSynNames failed to produce the correct output for Potentilla anserina")
		self.assertEqual(self.names_1.getSynNames(self.taxonId_2), self.longOutput_3, "getSynNames failed to produce the correct output for Potentilla alba")
		self.assertEqual(self.names_1.getSynNames(self.taxonId_3), self.longOutput_4, "getSynNames failed to produce the correct output for Anserina groenlandica")

	def test_getTaxonId(self):
		self.assertEqual(self.names_1.getTaxonId(self.taxonName_1), [7183990L, 7209247L], "getTaxonId failed to produce the correct output for Potentilla anserina")
		self.assertEqual(self.names_1.getTaxonId(self.taxonName_2), [7167046L, 7193078L], "getTaxonId failed to produce the     correct output for Potentilla alba")
		self.assertEqual(self.names_1.getTaxonId(self.taxonName_3), [7197490L], "getTaxonId failed to produce the     correct output for Anserina groenlandica")

	def test_getSynTaxonId(self):
		self.assertEqual(self.names_1.getSynTaxonId(self.taxonName_1), [7197490, 7197529, 7199122, 7209247], "getSynTaxonId failed to produce the correct output for Potentilla anserina")
		self.assertEqual(self.names_1.getSynTaxonId(self.taxonName_2), [7210899, 7197819, 7211089], "getSynTaxonId     failed to produce the correct output for Potentilla alba")
		self.assertEqual(self.names_1.getSynTaxonId(self.taxonName_3), [], "getSynTaxonId     failed to produce the correct output for Anserina groenlandica")

if __name__ == '__main__':
	unittest.main()
#	suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
#	suite = unittest.TestSuite()
#	unittest.TextTestRunner(verbosity=2).run(suite)	
