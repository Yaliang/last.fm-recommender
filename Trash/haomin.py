
import operator

# method of User class
def getArtistRank(self, artistID):
	"""get the rank of the input artist of the user"""
	"""if the artist is not in self.ArtistList return -1"""
	sorted_ArtistList = sorted(self.ArtistList.items(), key = operator.itemgetter(1))
	for i in range(len(sorted_ArtistList)):
		if sorted_ArtistList[i][0] == artistID:
			return i
	return -1



#test code 1
# train with records with all the time
# test every user in TestUserManager (records without the latest few monthes)
# write the output to another file in format
# userID recommendedArtistID Rank

#function in main

def test_case_1(TestUserManager, UserManager, ArtistManager):
	""" train KNN with UserManager & ArtistManager, test every user in TestUserManager"""
	""" output txt format: userID recommendedArtistID Rank"""
	# set the k of KNN
	knn = KNN(2)
	knn.training(TestUserManager, ArtistManager)
	output_file = open("Output_1.txt", "w")
	output_file.write("userID\trecommendedArtistID\tRank\n")

	for key, ele in TestUserManager.items():
		favOfOne = knn.testing(ele, TestUserManager, ArtistManager)
		rank = UserManager[key].getArtistRank(favOfOne)
		output_file.write(str(key)+'\t'+str(favOfOne)+'\t'+str(rank)+'\n')

	output_file.close()

def calcAccuracy(filepath, numOfTestUser, percentage):
	""" according to percentage calculate the accuracy of output data"""
	""" if rank < numOfTestUser * percentage, take it as accurate recommdation"""
	accurateNum = 0
	f = open(filepath, "r")
	line = f.readline()
	while line:
		line = f.readline()
		linedata = line.replace('\n','').split('\t')
		if len(linedata) == 3 && float(linedata[2]) < percentage * numOfTestUser:
			accurateNum += 1
	return 1.0*accurateNum/numOfTestUser

