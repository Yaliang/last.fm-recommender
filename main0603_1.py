from Artist import *
from User import *
from KNN import *
import random
import time

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

def splitTrainSet(userManager, percentage, userList = []):
	"""split the train set by percentage, to """
	if len(userList) == 0:
		testUserIDList = random.sample(userManager, int(len(userManager)*percentage))
	else:
		testUserIDList = userList
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
		# UserManager[userID] = testUser
		

	return testUserSet, testUserIDList, testUserMostFavourite

def splitTrainSetWithoutRemoving(userManager, percentage, userList = []):
	"""split the train set by percentage, to """
	if len(userList) == 0:
		testUserIDList = random.sample(userManager, int(len(userManager)*percentage))
	else:
		testUserIDList = userList
	testUserSet = {}
	for userID in testUserIDList:
		testUser = userManager.pop(userID)
		testUserSet[userID] = testUser

	return testUserSet, testUserIDList

def removeMostFav(userManager):
	newUserManager = {}
	for userID in userManager:
		user = userManager[userID]
		newUser = User(userID, user.ArtistList, user.FriendList, user.TagList, user.totalListenTime)
		mostFavourite = user.getMostFav()
		del newUser.ArtistList[mostFavourite.keys()[0]]
		newUserManager[userID] = newUser

	return newUserManager

def crossvalidation(userManager, artistManager, folders):
	"""split data into folders and validate the performance"""
	userIDs = userManager.keys()
	userFolders = {}
	for i in range(folders):
		userFolders[i] = []
	for userID in userIDs:
		i = random.randrange(folders)
		userFolders[i].append(userID)
	for f in range(folders):
		testUserSet, testUserIDList, testUserMostFavourite = splitTrainSet(userManager, 1.0/folders, userFolders[f])
		knn = KNN(6)
		knn.training(userManager, artistManager)
		rightNum = 0
		totalNum = len(testUserIDList)
		for i in range(len(testUserIDList)):
			print i, totalNum,
			favOfOne = knn.testing(testUserSet[testUserIDList[i]], userManager, artistManager)
			print testUserIDList[i], testUserMostFavourite[testUserIDList[i]].keys()[0], favOfOne
			if favOfOne == testUserMostFavourite[testUserIDList[i]].keys()[0]:
				rightNum += 1
		print "Folder", f, ":"
		print "Total:", totalNum
		print float(rightNum)/len(testUserIDList)
		for i in range(len(testUserIDList)):
			userManager[testUserIDList[i]] = testUserSet[testUserIDList[i]]


if __name__ == "__main__":
	# filepath = "test-data/"
	filepath = "hetrec2011-lastfm-2k/"
	filelist = ["artists.dat", "tags.dat", "user_artists.dat", "user_friends.dat", "user_taggedartists.dat"]
	data = readFile(filepath, filelist)
	RemoveListened = True

	#create Artist Manager
	ArtistManager = {}
	for artist in data[0]:
		# data[0]: artists.dat
		# artist = [id	name  url	pictureURL]
		ArtistManager[int(artist[0])] = Artist(int(artist[0]),artist[1])

	for tag in data[4]:
		# data[4]: user_taggedartists.dat
		# tag = [userID	artistID	tagID	day	month	year]
		if ArtistManager.has_key(int(tag[1])):
			ArtistManager[int(tag[1])].insertTag(int(tag[2]))

	for artistID, artist in ArtistManager.iteritems():
		artist.tagNormalize()


	# print ArtistManager[3]

	#create User Manager
	UserManager = {}
	for user in data[2]:
		# data[2]: user_artists.dat
		# user = [userID	artistID	weight]
		if not UserManager.has_key(int(user[0])):
			UserManager[int(user[0])] = User(int(user[0]))
			
		UserManager[int(user[0])].insertArt(int(user[1]),int(user[2]))
			


	for friend in data[3]:
		# data[3]: user_friends.dat
		# friend = [userID	friendID]
		if UserManager.has_key(int(friend[0])):
			UserManager[int(friend[0])].insertFriend(int(friend[1]))

	for tag in data[4]:		
		# data[4]: user_taggedartists.dat 
		# tag = [userID	artistID	tagID	day	month	year]
		if UserManager.has_key(int(tag[0])):
			UserManager[int(tag[0])].insertTag(int(tag[1]),int(tag[2]))

	# normalize the listen count
	for userID, user in UserManager.iteritems():
		user.normalizeListenRecord()

	# remove most fav of all, return a new userManager for train
	TrainUserManager = removeMostFav(UserManager)


	# 10 cross validation
	# crossvalidation(UserManager, ArtistManager, 10)


	# print UserManager
	theSameNum = 0
	inListenNum = 0
	users = UserManager.keys()
	for user in users:
		# testUserSet, testUserIDList, testUserMostFavourite = splitTrainSet(UserManager, 0, [user])
		testUserSet, testUserIDList = splitTrainSetWithoutRemoving(TrainUserManager, 0, [user])
		knn = KNN(2)
		knn.training(TrainUserManager, ArtistManager)
		
		for i in range(len(testUserIDList)):
			testUserID = testUserIDList[i]
			favOfOne = knn.testing(testUserSet[testUserID], UserManager, ArtistManager, RemoveListened)
			realfavOfOne = UserManager[testUserID].getMostFav().keys()[0]
			if favOfOne == realfavOfOne:
				theSameNum += 1
			if testUserSet[testUserID].ArtistList.has_key(favOfOne):
				inListenNum += 1
			# recovery modified TrainUserManager
			TrainUserManager[testUserID]=testUserSet[testUserID]

			# print testUserSet[testUserIDList[i]]
			# print testUserMostFavourite[testUserIDList[i]], favOfOne, testUserSet[testUserIDList[i]].ArtistList.pop(favOfOne, "cannot match any one")
			print str(user), theSameNum, inListenNum, favOfOne

	print theSameNum/len(UserManager)
	print inListenNum/len(UserManager)

	# print favOfOne













