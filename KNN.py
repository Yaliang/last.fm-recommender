# Use K-Nearest Neighbor to train and classify.
import math, operator
import numpy as np
import matplotlib.pyplot as plt


class KNN:
	""" K-Nearest Neighbor"""
	def __init__(self, k):
		# node in Nodes:
		# node is a dictionary: 
		# key: id
		# value: feature vector, where vector is a dictionary
		self.Nodes = {}
		self.K = k

	def training(self, userManager, artistManager):
		""" parse feature vector of user instance in userManager"""
		for userID,user in userManager.iteritems():
			self.Nodes[userID] = self.getFeature(user, artistManager)

	def getFeature(self, user, artistManager):
		""" get the feature vector of a particular user"""
		artists = user.ArtistList
		feature = {}
		for artistID, listenTimes in artists.iteritems():
			# print artistID
			# print artistManager[artistID]
			taginfo = artistManager[artistID].TagNormalized
			
			for tagID,weight in taginfo.iteritems():
				if not feature.has_key(tagID):
					feature[tagID] = weight * listenTimes
				else:
					feature[tagID] += weight * listenTimes

		weightSum = 0
		for tagID, weight in feature.iteritems():
			# used to normalized the feature vector
			weightSum += feature[tagID]

		for tagID, weight in feature.iteritems():
			feature[tagID] = 1.0*weight/weightSum

		return feature


	def testing(self, testUser, userManager, artistManager, removeKnownArtist = False, animate = False):
		""" calculate the distance between test user and trained nodes
			find out the k nearest neighbors
			return ID of a best matched artist"""	
		#get the feature vector of current testUser
		curFeature = self.getFeature(testUser, artistManager)

		# nodes in knn:
		# key: nodeID, value: distance between node and testUser
		# knn is ordered by ascending distance 
		knn = [{-1: float("Inf")} for i in range(self.K)]
		
		for userID, feature in self.Nodes.iteritems(): 
			# calculate the distance between node and testUser
			# distance use Euclidean distance
			distance = 0
			for tagID, weight in curFeature.iteritems():
				# combine feature of node and curfeature
				if not feature.has_key(tagID):
					feature[tagID] = -weight
				else:
					feature[tagID] -= weight

			for tagID, weight in feature.iteritems():
				distance += weight**2

			distance = math.sqrt(distance)

			for index in range(self.K-1, -1, -1):
				# loop knn from self.K-1 to 1 
				if knn[index].values()[0] > distance:
					if index < self.K-1:
						knn[index+1] = knn[index]
					knn[index] = {userID: distance}
				else:
					break

		match = {}
		gd = [0]
		mf = [0]
		wig = [0]
		dgr = [0]

		disttt = []
		for node in knn:
			disttt.append(node.values()[0])
		maxdistance = max(disttt)
		maxGDistance = 1.0* math.exp(-maxdistance**2 / 0.004)
		axislim = [-2*maxGDistance, 2*maxGDistance]


		for node in knn:
			# get userId
			userID = node.keys()[0]
			# get distance
			distance = node.values()[0]
			# G is a gaussian function: G(x) = a exp (- x^2 / (2 * c^2))
			# use a = 1, c^2 = 0.004 
			GDistance = 1.0* math.exp(-distance**2 / 0.004)
			# get artist list of user with userId
			user = userManager[userID]
			artistList = user.ArtistList
			# Matching(testuser-artist) = sum [G(distance(testuser-user)) * listenTime(user-artiest)]
			for artistID, listenTime in artistList.iteritems():
				if match.has_key(artistID):
					match[artistID] += GDistance*listenTime
				else:
					match[artistID] = GDistance*listenTime
			
			if animate:
				# if we don't want to recommand an artist in the testuser's listen record
				# just remove the artists in its match dictionary
				testUserArts = testUser.ArtistList
				if removeKnownArtist:
					for artistID in testUserArts:
						if match.has_key(artistID):
							del match[artistID]

				sortedMatch = sorted(match.items(), key=operator.itemgetter(1))
				bestMatchArtistID = sortedMatch[-1][0]

				mf[0] = bestMatchArtistID
				wig[0] = 3.14*match[bestMatchArtistID]


				gd.append(GDistance)
				favDic = userManager[userID].getMostFav()
				favID = favDic.keys()[0]
				mf.append(favID)
				lt = userManager[userID].ArtistList[favID]
				wig.append(lt)
				dgr.append(np.random.rand()*np.pi*2 - np.pi) 
				# plot 
				di = np.array(gd)
				degree = np.array(dgr)
				x = np.sin(degree)*di
				y = np.cos(degree)*di
				labels = np.array(mf)
				area = np.array(wig)**2
				# save
				fig = plt.scatter(x,y,s=10000*area, c=labels)
				plt.axis('off')
				plt.xlim(axislim)
				plt.ylim(axislim)
				plt.savefig(str(len(gd))+"plot.png")

		# if we don't want to recommand an artist in the testuser's listen record
		# just remove the artists in its match dictionary
		testUserArts = testUser.ArtistList
		if removeKnownArtist:
			for artistID in testUserArts:
				if match.has_key(artistID):
					del match[artistID]

		sortedMatch = sorted(match.items(), key=operator.itemgetter(1))
		bestMatchArtistID = sortedMatch[-1][0]

		return bestMatchArtistID, knn


			
	def testingTimeBased(self, testUser, userManager, artistManager):
		""" calculate the distance between test user and trained nodes
			find out the k nearest neighbors
			return ID of a best matched artist"""	
		#get the feature vector of current testUser
		curFeature = self.Nodes[testUser.ID]

		# nodes in knn:
		# key: nodeID, value: distance between node and testUser
		# knn is ordered by ascending distance 
		knn = [{-1: float("Inf")} for i in range(self.K)]
		
		for userID, feature in self.Nodes.iteritems(): 
			# calculate the distance between node and testUser
			# distance use Euclidean distance

			valid = userManager[userID].hasArtistInRecord(testUser.ArtistList.keys())
			if not valid or testUser.ID == userID:
				continue

			distance = 0
			for tagID, weight in curFeature.iteritems():
				# combine feature of node and curfeature
				if not feature.has_key(tagID):
					feature[tagID] = -weight
				else:
					feature[tagID] -= weight

			for tagID, weight in feature.iteritems():
				distance += weight**2

			distance = math.sqrt(distance)

			for index in range(self.K-1, -1, -1):
				# loop knn from self.K-1 to 1 
				if knn[index].values()[0] > distance:
					if index < self.K-1:
						knn[index+1] = knn[index]
					knn[index] = {userID: distance}
				else:
					break

		match = {}
		for artistID in testUser.ArtistList:
			match[artistID] = 0

		for node in knn:
			# get userId
			userID = node.keys()[0]
			# get distance
			distance = node.values()[0]
			# G is a gaussian function: G(x) = a exp (- x^2 / (2 * c^2))
			# use a = 1, c^2 = 0.004 
			GDistance = 1.0* math.exp(-distance**2 / 0.004)
			# get artist list of user with userId
			user = userManager[userID]
			artistList = user.ArtistList
			# Matching(testuser-artist) = sum [G(distance(testuser-user)) * listenTime(user-artiest)]
			for artistID, listenTime in artistList.iteritems():
				if match.has_key(artistID):
					match[artistID] += GDistance*listenTime
				else:
					continue


		# if we don't want to recommand an artist in the testuser's listen record
		# just remove the artists in its match dictionary

		sortedMatch = sorted(match.items(), key=operator.itemgetter(1))
		bestMatchArtistID = sortedMatch[-1][0]

		return bestMatchArtistID, knn











