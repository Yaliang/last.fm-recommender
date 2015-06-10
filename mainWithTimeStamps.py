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
	filepath = "lastfm-API-data/"
	filelist = ["Artist.data", "ArtistTags.data", "UserArtist.data", "Tag.data", "Tag.data","TestUser.data","User.data"]
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
			if tag[1] == "" or tag[2] == "":
				continue
			ArtistManager[int(tag[0])].insertTag(int(tag[1]), int(tag[2]))

	for artistID, artist in ArtistManager.iteritems():
		artist.tagNormalize()


	# print ArtistManager[3]

	#create User Manager
	UserManager = {}
	for user in data[5]:
		# data[5]: TestUser.data
		# user = [userID	artistID	count]
		if not UserManager.has_key(int(user[0])):
			UserManager[int(user[0])] = User(int(user[0]))
			
		UserManager[int(user[0])].insertArt(int(user[1]),int(user[2]))
	
	TestUserManager = {}
	for user in data[2]:
		#data[2]: UserArtist.data
		#user = [userID	artistID count]
		userID = int(user[0])
		artistID = int(user[1])
		if UserManager.has_key(userID) and not UserManager[userID].ArtistList.has_key(artistID):
			if not TestUserManager.has_key(userID):
				TestUserManager[userID] = User(userID)
			TestUserManager[userID].insertArt(artistID,int(user[2]))



	# for friend in data[4]:
	# 	# data[3]: UserFriends.data
	# 	# friend = [userID	friendID]
	# 	if UserManager.has_key(int(friend[0])):
	# 		UserManager[int(friend[0])].insertFriend(int(friend[1]))

	# for tag in data[4]:		
	# 	# data[4]: user_taggedartists.dat 
	# 	# tag = [userID	artistID	tagID	day	month	year]
	# 	if UserManager.has_key(int(tag[0])):
	# 		UserManager[int(tag[0])].insertTag(int(tag[1]),int(tag[2]))



	#train with UserManager, test with TestUserManager
	# counter = 0
	# for userID,user in TestUserManager.iteritems():
	# 	if len(user.ArtistList) == 0:

	# 		counter += 1
	# 	# print userID, len(user.ArtistList)
	# print counter, len(TestUserManager)
	knn = KNN(30)
	knn.training(UserManager, ArtistManager)

	theSameNum = 0
	for userID in TestUserManager:
		favOfOne, neighbors = knn.testingTimeBased(TestUserManager[userID],UserManager, ArtistManager)
		favTruth = TestUserManager[userID].getMostFav().keys()[0]
		if favOfOne == favTruth:
			theSameNum += 1
		print userID, theSameNum, favOfOne

	print 1.0*theSameNum/len(TestUserManager)

	# print favOfOne













