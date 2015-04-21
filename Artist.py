# This is a class defination of the artist in the dataset

class Artist:
	""" The class of artist """
	def __init__(self, artistID, artistName):
		"""Initialize the Artist object"""
		#tagData is the tags.dat file
		self.ID = artistID
		self.Name = artistName
		self.Tag = {}
		

	def __repr__(self):
		ret = "Artiest: " + self.ID + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag)

		return ret

	def __str__(self):
		"""convert the object to string"""
		ret = "Artiest: " + self.ID + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag)

		return ret

	def insertTag(self, tagID):
		"""insert a tag in Tag"""
		if self.Tag.has_key(tagID):
			self.Tag[tagID] += 1
		else:
			self.Tag[tagID] = 1