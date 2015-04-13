f = open("hetrec2011-lastfm-2k/tags.dat",'r')
line = f.readline()
lines = 1
# while line:
line = f.readline()
lines += 1

print lines
if len(line.split( )):
	print "len(line.split( ))"


li = [1,2,3,4,5,6,7,5,4,3,3,3,3]
d = {}
for tag in li:
	if d.has_key(tag):
		d[tag] += 1
	else:
		d[tag] = 1

print d