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

def splitTrainSet(userManager, testUserID):
	"""split the train set by percentage, to """
	#testUserIDList = random.sample(userManager, int(len(userManager)*percentage))
	testUserIDList = [testUserID]
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




if __name__ == "__main__":
	# filepath = "test-data/"
	filepath = "hetrec2011-lastfm-2k/"
	filelist = ["artists.dat", "tags.dat", "user_artists.dat", "user_friends.dat", "user_taggedartists.dat"]
	data = readFile(filepath, filelist)

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



	# print UserManager
	theSameNum = 0
	inListenNum = 0
	users = UserManager.keys()
	for user in users:
		testUserSet, testUserIDList, testUserMostFavourite = splitTrainSet(UserManager, user)
		knn = KNN(2)
		knn.training(UserManager, ArtistManager)
		
		for i in range(len(testUserIDList)):
			favOfOne = knn.testing(testUserSet[testUserIDList[i]],UserManager, ArtistManager)
			if favOfOne == testUserMostFavourite[testUserIDList[i]].keys()[0]:
				theSameNum += 1
			if testUserSet[testUserIDList[i]].ArtistList.has_key(favOfOne):
				inListenNum += 1
			UserManager[testUserIDList[i]]=testUserSet[testUserIDList[i]]
			key = testUserMostFavourite[testUserIDList[i]].keys()[0]
			value = testUserMostFavourite[testUserIDList[i]].values()[0]
			UserManager[testUserIDList[i]].insertArt(key,value)

			# print testUserSet[testUserIDList[i]]
			# print testUserMostFavourite[testUserIDList[i]], favOfOne, testUserSet[testUserIDList[i]].ArtistList.pop(favOfOne, "cannot match any one")
		print str(user)

	print theSameNum/len(UserManager)
	print inListenNum/len(UserManager)

	# print favOfOne













