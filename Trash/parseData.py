import urllib2
import json
import math
import os

def getData(options):
	keys = options.keys()
	url = "http://ws.audioscrobbler.com/2.0/?api_key=01966bc783793c8d9fede104bdaeff31&format=json"
	for key in keys:
		value = options[key]
		url += "&"+key+"="+value
	print url
	dataJSON = urllib2.urlopen(url).read()
	dataObj = json.loads(dataJSON)
	return dataObj



groupUserList = {}	# user library 
groupArtistList = {}	# artist library
groupTagList = {} 	# tag library
trainWeeks = 100
testWeeks = 5

# get the list of user in a group: I+Still+Buy+CDs
for pageIndex in range(1,2):
	options = {"method":"group.getmembers","group":"I+Still+Buy+CDs","limit":"10","page":str(pageIndex)}
	memberObj = getData(options)
	userListlenth = len(memberObj['members']['user'])
	for userIndex in range(userListlenth):
		groupUserList[str(memberObj['members']['user'][userIndex]['name'])] = {}

	print len(groupUserList)

# fetch the user name list 
userNames = groupUserList.keys()

# get the chart list of users
for userIndex in range(len(userNames)):
	userName = userNames[userIndex]
	options = {"method":"user.getweeklychartlist","user":userName}
	chartListObj = getData(options)
	groupUserList[userName]['chart'] = chartListObj['weeklychartlist']['chart']


# get the listen history of users
for userIndex in range(len(userNames)):
	# method=user.getweeklyartistchart&from=1249819200&to=1413720000&user=przemyslanka90
	userName = userNames[userIndex]
	chartNum = len(groupUserList[userName]['chart'])
	groupUserList[userName]['artist'] = {}
	groupUserList[userName]['test'] = {}
	groupUserList[userName]['test']['artist'] = {}
	for chartIndex in range(chartNum-trainWeeks-1, chartNum):
		# enumerate each weekly artist chart
		chart = groupUserList[userName]['chart'][chartIndex]
		options = {"method":"user.getweeklyartistchart", "from":chart['from'], "to":chart['to'], "user":userName}
		listenObj = getData(options)
		if not listenObj.has_key('weeklyartistchart'):
			continue
		if not listenObj['weeklyartistchart'].has_key('artist'):
			# not record in this week
			continue
		else:
			# add each artist's to user's data
			artistList = listenObj['weeklyartistchart']['artist']
			if type(artistList) is dict:
				artistList = [artistList]
			for artist in artistList:
				artistName = artist['name']
				# add artist into library
				if not groupArtistList.has_key(artistName):
					groupArtistList[artistName] = {}
				# add listen record into user's data
				if not groupUserList[userName]['artist'].has_key(artistName):
					groupUserList[userName]['artist'][artistName] = int(artist['playcount'])
				else:
					groupUserList[userName]['artist'][artistName] += int(artist['playcount'])
				# if the record period is outside the predict period, add it to the test data
				if chartIndex < chartNum-testWeeks:
					if not groupUserList[userName]['test']['artist'].has_key(artistName):
						groupUserList[userName]['test']['artist'][artistName] = int(artist['playcount'])
					else:
						groupUserList[userName]['test']['artist'][artistName] += int(artist['playcount'])

# remove user without any record in test
for userName in userNames:
	if len(groupUserList[userName]['test']['artist']) == 0:
		groupUserList.pop(userName, None)

# get new userNames
userNames = groupUserList.keys()
	
# print number of all artist
print len(groupArtistList.keys())

# fetch the list of artist name
artistNames = groupArtistList.keys()

# get the tag of artist from the user in our library
for artistID in range(len(artistNames)):
	artistName = artistNames[artistID]
	groupArtistList[artistName]['tags'] = {}
	for userID in range(len(userNames)):
		userName = userNames[userID]
		options = {"method":"artist.getTags", "artist":artistName, "user":userName}
		tagObj = getData(options)
		if not tagObj["tags"].has_key("tag"):
			continue
		else:
			tags = tagObj["tags"]["tag"]
			if type(tags) is dict:
				tags = [tags]
			for tag in tags:
				tagName = tag["name"]
				# store to tag library
				if not groupTagList.has_key(tagName):
					groupTagList[tagName] = {}
				# count tag to artist
				if not groupArtistList[artistName]["tags"].has_key(tagName):
					groupArtistList[artistName]["tags"][tagName] = 1
				else:
					groupArtistList[artistName]["tags"][tagName] += 1

# fetch tagName list
tagNames = groupTagList.keys()

# save Artist.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\Artist.data","w")
f.write("<ArtistID>\t<ArtistName>\n".encode('utf8'))
for artistID in range(len(artistNames)):
	line = str(artistID)+"\t"+artistNames[artistID]+"\n"
	f.write(line.encode('utf8'))
f.close()

# save ArtistTags.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\ArtistTags.data","w")
f.write("<ArtistID>\t<TagID>\t<Count>\n".encode('utf8'))
for artistID in range(len(artistNames)):
	artistName = artistNames[artistID]
	for tagID in range(len(tagNames)):
		tagName = tagNames[tagID]
		if not groupArtistList[artistName]["tags"].has_key(tagName):
			continue
		line = str(artistName)+"\t"+str(tagID)+"\t"+str(groupArtistList[artistName]["tags"][tagName])+"\n"
		f.write(line.encode('utf8'))
f.close()

# save UserArtist.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\UserArtist.data","w")
f.write("<UserID>\t<ArtistID>\t<Count>\n".encode('utf8'))
for userID in range(len(userNames)):
	userName = userNames[userID]
	if not groupUserList[userName].has_key('artist'):
		continue
	listenArtistNames = groupUserList[userName]['artist'].keys()
	for i in range(len(listenArtistNames)):
		artistName = listenArtistNames[i]
		artistID = artistNames.index(artistName)
		artistCount = groupUserList[userName]['artist'][artistName]
		line = str(userID)+"\t"+str(artistID)+"\t"+str(artistCount)+"\n"
		f.write(line.encode('utf8'))
f.close()

# save Tag.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\Tag.data","w")
f.write("<TagID>\t<TagName>\n".encode('utf8'))
for tagID in range(len(tagNames)):
	line = str(tagID)+"\t"+tagNames[tagID]+"\n"
	f.write(line.encode('utf8'))
f.close()

# save TestUser.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\TestUser.data","w")
f.write("<UserID>\t<ArtistID>\t<Count>\n".encode('utf8'))
for userID in range(len(userNames)):
	userName = userNames[userID]
	if not groupUserList[userName]["test"].has_key('artist'):
		continue
	listenArtistNames = groupUserList[userName]["test"]['artist'].keys()
	for i in range(len(listenArtistNames)):
		artistName = listenArtistNames[i]
		artistID = artistNames.index(artistName)
		artistCount = groupUserList[userName]["test"]['artist'][artistName]
		line = str(userID)+"\t"+str(artistID)+"\t"+str(artistCount)+"\n"
		f.write(line.encode('utf8'))
f.close()

# save User.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\User.data","w")
f.write("<UserID>\t<UserName>\n".encode('utf8'))
for userID in range(len(userNames)):
	line = str(userID)+"\t"+userNames[userID]+"\n"
	f.write(line.encode('utf8'))
f.close()

# save TestUser.data
f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\TestUser.data","w")
f.write("<UserID>\t<ArtistID>\t<Count>\n".encode('utf8'))
for userID in range(len(userNames)):
	userName = userNames[userID]
	if not groupUserList[userName].has_key('test'):
		continue
	listenArtistNames = groupUserList[userName]['test']['artist'].keys()
	for i in range(len(listenArtistNames)):
		artistName = listenArtistNames[i]
		artistID = artistNames.index(artistName)
		artistCount = groupUserList[userName]['test']['artist'][artistName]
		line = str(userID)+"\t"+str(artistID)+"\t"+str(artistCount)+"\n"
		f.write(line.encode('utf8'))
f.close()





