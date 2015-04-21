from Artist import *
from User import *

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


if __name__ == "__main__":
	filepath = "hetrec2011-lastfm-2k/"
	filelist = ["artists.dat", "tags.dat", "user_artists.dat", "user_friends.dat", "user_taggedartists.dat"]
	data = readFile(filepath, filelist)

	#create Artist Manager
	ArtistManager = {}
	for artist in data[0]:
		# data[0]: artists.dat
		# artist = [id	name  url	pictureURL]
		ArtistManager[int(artist[0])] = Artist(artist[0],artist[1])

	for tag in data[4]:
		# data[4]: user_taggedartists.dat
		# tag = [userID	artistID	tagID	day	month	year]
		if ArtistManager.has_key(int(tag[1])):
			ArtistManager[int(tag[1])].insertTag(tag[2])

	#create User Manager
	UserManager = {}
	for user in data[2]:
		# data[2]: user_artists.dat
		# user = [userID	artistID	weight]
		if UserManager.has_key(int(user[0])):
			UserManager[int(user[0])].insertArt(user[1],user[2])
		else:
			UserManager[int(user[0])] = User(user[0])

	for friend in data[3]:
		# data[3]: user_friends.dat
		# friend = [userID	friendID]
		UserManager[int(friend[0])].insertFriend(friend[1])

	for tag in data[4]:		
		# data[4]: user_taggedartists.dat 
		# tag = [userID	artistID	tagID	day	month	year]
		UserManager[int(tag[0])].insertTag(tag[1],tag[2])



	print UserManager[2]
	print ArtistManager[2]












