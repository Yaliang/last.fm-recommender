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
	for userID in testUserIDList:
		artists = userManager[userID].ArtistList
		mostFavourite = {-1:0}
		for artistID, listenTime in artists.iteritems():
			if listenTime > mostFavourite.values()[0]:
				mostFavourite = {artistID: listenTime}
		testUserMostFavourite[userID] = mostFavourite
		del userManager[userID].ArtistList[mostFavourite.keys()[0]]

	return testUserIDList, testUserMostFavourite




if __name__ == "__main__":
	filepath = "test-data/"
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


	print ArtistManager[3]

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



	print UserManager
	testUserIDList, testUserMostFavourite = splitTrainSet(UserManager, 0.5)
	knn = KNN(2)
	knn.training(UserManager, ArtistManager)
	favOfOne = knn.testing(UserManager[testUserIDList[0]],UserManager, ArtistManager)
	print UserManager
	print favOfOne













