#This is a class defination of the user in the dataset
from copy import deepcopy

class User:
	"""The class of user"""
	def __init__(self, userID, artistList = {}, friendList = [], tagList = {}, totalListenTime = 0):
		"""Initialize the User object"""
		self.ID = userID
		self.ArtistList = deepcopy(artistList) # key = artistID, value = listenTimes
		self.FriendList = deepcopy(friendList)
		self.TagList = deepcopy(tagList)
		self.totalListenTime = totalListenTime

	def __repr__(self):
		ret = "User: " + str(self.ID) + "\n"
		ret = ret + "ArtistList: " + str(self.ArtistList) + "\n"  
		ret = ret + "FriendList: " + str(self.FriendList) + "\n"
		ret = ret + "TagList: " + str(self.TagList) + "\n"

		return ret

	def __str__(self):
		"""convert the object to string"""
		ret = "User: " + str(self.ID) + "\n"
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

	def normalizeListenRecord(self):
		"""normalize the count of listening record"""
		artistIDs = self.ArtistList.keys()
		self.totalListenTime = 0
		for artistID in artistIDs:
			self.totalListenTime += self.ArtistList[artistID]
		for artistID in artistIDs:
			self.ArtistList[artistID] = float(self.ArtistList[artistID]) / self.totalListenTime

	def getMostFav(self):
		"""return the most favorite artist"""
		mostFavourite = {-1:0}
		artists = self.ArtistList
		for artistID, listenTime in artists.iteritems():
			if listenTime > mostFavourite.values()[0]:
				mostFavourite = {artistID: listenTime}

		return mostFavourite






