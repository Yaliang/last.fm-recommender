#This is a class defination of the user in the dataset

class User:
	"""The class of user"""
	def __init__(self, userID):
		"""Initialize the User object"""
		self.ID = userID
		self.ArtistList = {}
		self.FriendList = []
		self.TagList = {}

	def __repr__(self):
		ret = "User: " + self.ID + "\n"
		ret = ret + "ArtistList: " + str(self.ArtistList) + "\n"  
		ret = ret + "FriendList: " + str(self.FriendList) + "\n"
		ret = ret + "TagList: " + str(self.TagList) + "\n"

		return ret

	def __str__(self):
		"""convert the object to string"""
		ret = "User: " + self.ID + "\n"
		ret = ret + "ArtistList: " + str(self.ArtistList) + "\n"  
		ret = ret + "FriendList: " + str(self.FriendList) + "\n"
		ret = ret + "TagList: " + str(self.TagList) + "\n"

		return ret

	def insertArt(self, artistID, weight):
		"""insert a Artist in ArtistList"""
		self.ArtistList[artistID] = weight


	def insertFriend(self, friendID):
		"""insert a friend in FriendList """
		self.FriendList.append(friendID)

	def insertTag(self, artistID, tagID):
		"""insert a tag in TagList"""
		if self.TagList.has_key(artistID):
			self.TagList[artistID].append(tagID)
		else:
			self.TagList[artistID] = [tagID]







