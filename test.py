import urllib2
import json
import math
import os
import time
from multiprocessing import Pool

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

def getWeeklyChartList(args):
	# get the chart list of users
	userName = args[0]
	i = args[1]
	options = {"method":"user.getweeklychartlist","user":userName}
	chartListObj = getData(options)
	print i
	return chartListObj


# url = "http://cn.last.fm/group/I+Still+Buy+CDs/members?memberspage=2"
# page = urllib2.urlopen(url)
# pageLines = []
# waitLine = 0
# for line in page:
# 	if "<div class=\"userContainer\">" in line:
# 		waitLine = 2
# 	else:
# 		waitLine -= 1
# 		if waitLine == 0:
# 			length = len(line)
# 			spaceIndex = line.rfind(" ")
# 			pageLines.append(line[spaceIndex+1:length-14])
# print pageLines

# url = "http://ws.audioscrobbler.com/2.0/?method=group.getmembers&api_key=01966bc783793c8d9fede104bdaeff31&group=I+Still+Buy+CDs&format=json"
# memberJSON = urllib2.urlopen(url).read()
# memberObj = json.loads(memberJSON)
# print memberObj['members']['user'][0]['name']



if __name__ == '__main__':
	for i in range(100):
		print str(i)+"\r",
		time.sleep(1)

	# groupUserList = {}	# user library 
	# groupArtistList = {}	# artist library
	# groupTagList = {} 	# tag library
	# trainWeeks = 100
	# testWeeks = 5

	# # get the list of user in a group: I+Still+Buy+CDs
	# for pageIndex in range(1,2):
	# 	options = {"method":"group.getmembers","group":"I+Still+Buy+CDs","limit":"20","page":str(pageIndex)}
	# 	memberObj = getData(options)
	# 	userListlenth = len(memberObj['members']['user'])
	# 	for userIndex in range(userListlenth):
	# 		groupUserList[str(memberObj['members']['user'][userIndex]['name'])] = {}

	# 	print len(groupUserList)

	# # fetch the user name list 
	# userNames = groupUserList.keys()

	# args = [[userNames[i],i] for i in range(len(userNames))]
	# pool = Pool(processes=10)
	# chartListObjList = pool.map(getWeeklyChartList, args)

	# print len(chartListObjList)

	# # get the chart list of users
	# for userIndex in range(len(userNames)):
	# 	userName = userNames[userIndex]
	# 	groupUserList[userName]['chart'] = chartListObjList[userIndex]['weeklychartlist']['chart']

	# print groupUserList  