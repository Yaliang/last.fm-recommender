# This is a class defination of the artist in the dataset

class Artist:
	""" The class of artist """
	def __init__(self, artistID, artistName):
		"""Initialize the Artist object"""
		#tagData is the tags.dat file
		self.ID = artistID
		self.Name = artistName
		self.Tag = {}
		self.TagNormalized = {}

	def __repr__(self):
		ret = "Artiest: " + str(self.ID) + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag) + "\n"

		return ret

	def __str__(self):
		"""convert the object to string"""
		ret = "Artiest: " + str(self.ID) + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag) + "\n"

		return ret

	def insertTag(self, tagID, tagCount = 1):
		"""insert a tag in Tag"""
		if self.Tag.has_key(tagID):
			self.Tag[tagID] += tagCount
		else:
			self.Tag[tagID] = tagCount


	def tagNormalize(self):
		"""to normalize the times of tags appears"""

		totalTagNum = 0
		for key, value in self.Tag.iteritems():
			totalTagNum += value
			#totalTagNum: accounting the # of all tags for one artist
		
		self.TagNormalized = {}
		for key, value in self.Tag.iteritems():
			if totalTagNum == 0:
				self.TagNormalized[key] = 0
			else:
				self.TagNormalized[key] = 1.0*value/totalTagNum













