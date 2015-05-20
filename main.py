from Artist import *
from User import *
from KNN import *
import random

def readFile(filepath, filelist):
	""" read the data file from the filepath/filename """
	data = []
	for filename in filelist:
		f = open(filepath+filename,"r")
		filedata = []
		# read the first line 
		line = f.readline()
		# read the data of file
		while line:
			line = f.readline()
			linedata = line.replace('\n','').split('\t')
			if len(linedata) > 1:
				filedata.append(linedata)
		data.append(filedata)

	return data

def splitTrainSet(userManager, percentage):
	"""split the train set by percentage, to """
	testUserIDList = random.sample(userManager, int(len(userManager)*percentage))
	testUserMostFavourite = {}
	testUserSet = {}
	for userID in testUserIDList:
		testUser = userManager.pop(userID)
		testUserSet[userID] = testUser
		artists = testUser.ArtistList
		mostFavourite = {-1:0}
		for artistID, listenTime in artists.iteritems():
			if listenTime > mostFavourite.values()[0]:
				mostFavourite = {artistID: listenTime}
		testUserMostFavourite[userID] = mostFavourite
		del testUser.ArtistList[mostFavourite.keys()[0]]
		testUserSet[userID] = testUser
		

	return testUserSet, testUserIDList, testUserMostFavourite




if __name__ == "__main__":
	# filepath = "test-data/"
	filepath = "hetrec2011-lastfm-2k/"
	filelist = ["Artist.data", "ArtistTags.data", "UserArtist.data", "Tag.data", "UserFriend.data","TestUser.data","User.data"]
	data = readFile(filepath, filelist)

	#create Artist Manager
	ArtistManager = {}
	for artist in data[0]:
		# data[0]: artists.data
		# artist = [id	name]
		ArtistManager[int(artist[0])] = Artist(int(artist[0]),artist[1])

	for tag in data[1]:
		# data[1]: ArtistTags.data
		# artisttag = [artistID	tagID tagCounts]
		if ArtistManager.has_key(int(tag[0])):
			ArtistManager[int(tag[0])].insertTag(int(tag[1]), int(tag[2]))

	for artistID, artist in ArtistManager.iteritems():
		artist.tagNormalize()


	# print ArtistManager[3]

	#create User Manager
	UserManager = {}
	for user in data[2]:
		# data[2]: UserArtists.data
		# user = [userID	artistID	count]
		if not UserManager.has_key(int(user[0])):
			UserManager[int(user[0])] = User(int(user[0]))
			
		UserManager[int(user[0])].insertArt(int(user[1]),int(user[2]))
	
	TestUserManager = {}
	for user in data[5]:
		#data[5]: TestUser.data
		#user = [userID	artistID count]
		if not UserManager.has_key(int(user[0])):
			UserManager[int(user[0])] = User(int(user[0]))
			
		UserManager[int(user[0])].insertArt(int(user[1]),int(user[2]))


	for friend in data[4]:
		# data[3]: UserFriends.data
		# friend = [userID	friendID]
		if UserManager.has_key(int(friend[0])):
			UserManager[int(friend[0])].insertFriend(int(friend[1]))

	# for tag in data[4]:		
	# 	# data[4]: user_taggedartists.dat 
	# 	# tag = [userID	artistID	tagID	day	month	year]
	# 	if UserManager.has_key(int(tag[0])):
	# 		UserManager[int(tag[0])].insertTag(int(tag[1]),int(tag[2]))



	# print UserManager
	testUserSet, testUserIDList, testUserMostFavourite = splitTrainSet(UserManager, 0.001)
	knn = KNN(2)
	knn.training(UserManager, ArtistManager)
	for i in range(len(testUserIDList)):
		favOfOne = knn.testing(testUserSet[testUserIDList[i]],UserManager, ArtistManager)
		print testUserSet[testUserIDList[i]]
		print testUserMostFavourite[testUserIDList[i]], favOfOne, testUserSet[testUserIDList[i]].ArtistList.pop(favOfOne, "cannot match any one")


	# print favOfOne













