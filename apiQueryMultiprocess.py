import urllib2
import urllib
import random
import json
import math
import os
from multiprocessing import Pool
from time import sleep

def getData(options):
	keys = options.keys()
	url = "http://ws.audioscrobbler.com/2.0/?api_key=01966bc783793c8d9fede104bdaeff31&format=json"
	for key in keys:
		value = options[key]
		url += "&"+urllib.quote_plus(key)+"="+urllib.quote_plus(value.encode('utf8'))
	# print url
	success = False
	time = 1
	while (not success) and (time<10):
		try:
			connection = urllib2.urlopen(url)
			dataJSON = connection.read()
			dataObj = json.loads(dataJSON)
			success = True
		except:
			# print url
			# print "timeout happened."+str(time)+" s"
			sleep(1.0*random.randrange(time*100)/100)
			time += 1
			dataObj = {}

	return dataObj

def getWeeklyChartList(userName):
	# get the chart list of users
	options = {"method":"user.getweeklychartlist","user":userName}
	chartListObj = getData(options)
	return chartListObj

def getWeeklyArtistChart(args):
	# enumerate each weekly artist chart
	userName = args[0]
	chart = args[1]
	options = {"method":"user.getweeklyartistchart", "from":chart['from'], "to":chart['to'], "user":userName}
	listenObj = getData(options)
	return listenObj

def getArtistUserTag(args):
	userName = args[0]
	artistName = args[1]
	options = {"method":"artist.getTags", "artist":artistName, "user":userName}
	tagObj = getData(options)
	return tagObj

def getArtistTopTag(artistName):
	options = {"method":"artist.gettoptags","artist":artistName}
	tagObj = getData(options)
	return tagObj

def getUserArtistRecord(pool, userName, chartList):
	listLength = len(chartList)
	splitTime = 1431864000 - 3600*24*7*12
	wholeListenArtist = {}
	BaseListenArtist = {}
	args = [[userName, chartList[i]] for i in range(listLength)]
	listenObjList = pool.map(getWeeklyArtistChart, args)
	for chartIndex in range(len(listenObjList)):
		listenObj = listenObjList[chartIndex]
		weeklychartFrom = chartList[chartIndex]['from']
		weeklychartTo = chartList[chartIndex]['to']
		if type(listenObj) == unicode:
			print userName, weeklychartFrom, weeklychartTo, listenObj.encode('utf8')
			continue
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
				if int(weeklychartFrom) < splitTime:
					# add listen record into user's base data
					if not BaseListenArtist.has_key(artistName):
						BaseListenArtist[artistName] = int(artist['playcount'])
					else:
						BaseListenArtist[artistName] += int(artist['playcount'])
				# add listen record into user's data
				if not wholeListenArtist.has_key(artistName):
					wholeListenArtist[artistName] = int(artist['playcount'])
				else:
					wholeListenArtist[artistName] += int(artist['playcount'])
	return wholeListenArtist, BaseListenArtist

def getArtistTags(pool, artistName, userNames):
	# get the tag of artist from the user in our library
	tags = {}
	args = [[userNames[i], artistName] for i in range(len(userNames))]
	# print "ready to call multiprocessing"
	# print args
	tagObjList = pool.map(getArtistUserTag, args)
	# print "multiprocessing finished"
	for i in range(len(tagObjList)):
		tagObj = tagObjList[i]
		if not tagObj["tags"].has_key("tag"):
			continue
		else:
			tagList = tagObj["tags"]["tag"]
			if type(tagList) is dict:
				tagList = [tagList]
			for tag in tagList:
				tagName = tag["name"]
				# count tag to artist
				if not tags.has_key(tagName):
					tags[tagName] = 1
				else:
					tags[tagName] += 1

	return tags


if __name__ == '__main__':
	groupUserList = {}	# user library 
	groupArtistList = {}	# artist library
	groupTagList = {} 	# tag library

	# get the list of user in a group: I+Still+Buy+CDs
	for pageIndex in range(2,3):
		options = {"method":"group.getmembers","group":"I Still Buy CDs","limit":"100","page":str(pageIndex)}
		memberObj = getData(options)
		userListlenth = len(memberObj['members']['user'])
		for userIndex in range(userListlenth):
			groupUserList[str(memberObj['members']['user'][userIndex]['name'])] = {}

	# fetch the user name list 
	userNames = groupUserList.keys()
	print "Total User Number:",len(groupUserList)

	# get the chart list of users
	pool = Pool(processes=100)
	chartListObjList = pool.map(getWeeklyChartList, userNames)
	for userIndex in range(len(userNames)):
		userName = userNames[userIndex]
		groupUserList[userName]['chart'] = chartListObjList[userIndex]['weeklychartlist']['chart']


	# get the listen history of users
	for userIndex in range(len(userNames)):
		print userIndex
		userName = userNames[userIndex]
		listenArtist, BaseListenArtist= getUserArtistRecord(pool, userName, groupUserList[userName]['chart'])
		groupUserList[userName]['artist'] = listenArtist
		groupUserList[userName]['artistBase'] = BaseListenArtist
		# print len(groupUserList[userName]['artistBase'])
		# add artists into artist library
		artists = listenArtist.keys()
		for artistName in artists:
			groupArtistList[artistName] = {}


	# remove user without any record
	for userName in userNames:
		if len(groupUserList[userName]['artist']) == 0:
			groupUserList.pop(userName, None)

	# get new userNames
	userNames = groupUserList.keys()

	print "Total User Number:",len(groupUserList)

	# fetch the list of artist name
	artistNames = groupArtistList.keys()

	print "Total Artist Number:",len(groupArtistList)

	# get the tag of artist from the user in our library
	# for artistIndex in range(len(artistNames)):
	# 	print artistIndex
	# 	artistName = artistNames[artistIndex]
	# 	artistMBID = groupArtistList[artistName]['mbid']
	# 	tags = getArtistTags(pool, artistName, userNames)
	# 	groupArtistList[artistName]["tags"] = tags
	# 	# add tags into tag library
	# 	tagList = tags.keys()
	# 	for tagName in tagList:
	# 		if not groupTagList.has_key(tagName):
	# 			groupTagList[tagName] = {}

	# get the normalized tag of artist from the user in our library
	tagObjList = pool.map(getArtistTopTag, artistNames)
	for i in range(len(tagObjList)):
		print i
		tagObj = tagObjList[i]
		artistName = artistNames[i]
		groupArtistList[artistName]["tags"] = {}
		if not tagObj["toptags"].has_key("tag"):
			continue
		else:
			tagList = tagObj["toptags"]["tag"]
			if type(tagList) is dict:
				tagList = [tagList]
			for tag in tagList:
				tagName = tag["name"]
				tagCount = tag["count"]
				groupArtistList[artistName]["tags"][tagName] = tagCount
				groupTagList[tagName] = {}

	# fetch tagName list
	tagNames = groupTagList.keys()

	# save Artist.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\Artist.data","w")
	output = "<ArtistID>\t<ArtistName>\n".encode('utf8')

	for artistID in range(len(artistNames)):
		line = str(artistID)+"\t"+artistNames[artistID]+"\n"
		f.write(line.encode('utf8'))
	f.close()

	# save ArtistTags.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\ArtistTags.data","w")
	output = "<ArtistID>\t<TagID>\t<Count>\n".encode('utf8')
	for artistID in range(len(artistNames)):
		artistName = artistNames[artistID]
		for tagID in range(len(tagNames)):
			tagName = tagNames[tagID]
			if not groupArtistList[artistName]["tags"].has_key(tagName):
				continue
			line = str(artistID)+"\t"+str(tagID)+"\t"+str(groupArtistList[artistName]["tags"][tagName])+"\n"
			output += line.encode('utf8')

	f.write(output)
	f.close()

	# save UserArtist.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\UserArtist.data","w")
	output = "<UserID>\t<ArtistID>\t<Count>\n".encode('utf8')
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
			output += line.encode('utf8')
	
	f.write(output)
	f.close()

	# save Tag.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\Tag.data","w")
	output = "<TagID>\t<TagName>\n".encode('utf8')
	for tagID in range(len(tagNames)):
		line = str(tagID)+"\t"+tagNames[tagID]+"\n"
		output += line.encode('utf8')
	
	f.write(output)
	f.close()

	# save TestUser.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\TestUser.data","w")
	output = "<UserID>\t<ArtistID>\t<Count>\n".encode('utf8')
	for userID in range(len(userNames)):
		userName = userNames[userID]
		print userName
		if not groupUserList[userName].has_key('artistBase'):
			continue
		listenArtistNames = groupUserList[userName]['artistBase'].keys()
		print len(listenArtistNames)
		for i in range(len(listenArtistNames)):
			artistName = listenArtistNames[i]
			artistID = artistNames.index(artistName)
			artistCount = groupUserList[userName]['artistBase'][artistName]
			line = str(userID)+"\t"+str(artistID)+"\t"+str(artistCount)+"\n"
			output += line.encode('utf8')
	f.write(output)
	f.close()

	# save User.data
	f = open(os.path.dirname(os.path.realpath(__file__))+"\lastfm-API-data\User.data","w")
	output = "<UserID>\t<UserName>\n".encode('utf8')
	for userID in range(len(userNames)):
		line = str(userID)+"\t"+userNames[userID]+"\n"
		output += line.encode('utf8')

	f.write(output)
	f.close()
	