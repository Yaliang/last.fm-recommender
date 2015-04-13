# This is a class defination of the artist in the dataset

class Artist:
	""" The class of artist """
	def __init__(self, data, tagData):
		"""Initialize the Artist object"""
		self.ID = data[0]
		self.Name = data[1]
		self.Tag = {}
		for tagItem in tagData:
			if tagItem[1] == self.ID:
				tagId = tagItem[2]
				if self.Tag.has_key(tagId):
					self.Tag[tagId] += 1
				else:
					self.Tag[tagId] = 1

	def __repr__(self):
		ret = "Artiest: " + self.ID + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag)

		return ret

	def __str__(self):
		ret = "Artiest: " + self.ID + "\t"
		ret = ret + self.Name + "\n"
		ret = ret + str(self.Tag)

		return ret