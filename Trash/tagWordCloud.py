filepath = "hetrec2011-lastfm-2k/"
f = open(filepath+"/tags.dat",'r')

tagdict={}
# read the first line 
line = f.readline()
# read the data of file
while line:
	line = f.readline()
	linedata = line.replace('\n','').split('\t')
	if len(linedata) > 1:
		tagID = linedata[0]
		tagWord = linedata[1]
		tagdict[tagID] = tagWord

f.close()

f = open(filepath+"/user_taggedartists.dat",'r')
fo = open("wordClound.txt",'w')

# read the first line 
line = f.readline()
# read the data of file
while line:
	line = f.readline()
	linedata = line.replace('\n','').split('\t')
	if len(linedata) > 1:
		tagID = linedata[2]
		fo.write(tagdict[tagID]+"\n")

f.close()
fo.close()


