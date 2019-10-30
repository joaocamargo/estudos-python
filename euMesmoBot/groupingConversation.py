import re

filenames = ['amorChat_ConvA','amorChat_ConvJ']
folderTalkings = 'conversas/'

conversasDeA = []
conversasDeJ = []

for names in filenames:
    file_handle = open(folderTalkings+names+ ".txt", encoding='utf-8')
    print(folderTalkings+names + ".txt has been opened")
    f = open(folderTalkings+names + "_nonames_OK.txt",'w')
    i=0
    for line in file_handle:        
        if(line.startswith("|")):
                f.write(line)
                i = i +1;
        else:
                i = i +1;                
                #temp = re.sub(r'.*:', ':', line)
                temp = line.split(':')[1]                
                #line1 = temp.encode('ascii','ignore')     
                print(temp)            
                f.write(str(temp))
			    
            #print(line)			
            #f.write(line)

file_handle.close()






        #temp = re.sub(r'*-','-',line)
        #print(temp)
