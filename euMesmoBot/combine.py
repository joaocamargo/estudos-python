import re

filenames = ['amorChat_ConvA','amorChat_ConvJ']
folderTalkings = 'conversas/'

cwcounter = 0
othercounter = 0
stringstore = ""

f = open("myside.txt", 'w')
fother = open("otherside.txt", 'w')
#column 0 and column 1, 0 Chunside 1 Ohter Side, row 0++
for names in filenames:
	cwfile = open(folderTalkings+"amorChat_ConvJ_nonames_OK.txt")
	otherfile = open(folderTalkings+"amorChat_ConvA_nonames_OK.txt")

	print(names + ".txt QnA pair has been opened")
	for line in cwfile:
		if(line.startswith("|")):
			#s1.write(cwcounter, 0, stringstore)
			f.write(stringstore)
			cwcounter += 1
			stringstore = "\n"
		else:
			stringstore += " " + line.rstrip()
			#print(stringstore)
			
	for oline in otherfile:
		if(oline.startswith("|")):
			#s1.write(othercounter, 1, stringstore)
			fother.write(stringstore)
			othercounter += 1
			stringstore = "\n"
		else:
			stringstore += " " + oline.rstrip()
			#print(stringstore)
print("Me:" + str(cwcounter) + " Other" + str(othercounter))






        #temp = re.sub(r'*-','-',line)
        #print(temp)
