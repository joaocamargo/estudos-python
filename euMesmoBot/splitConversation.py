import re

filenames = ['amorChat']
folderTalkings = 'conversas/'

conversasDeA = []
conversasDeJ = []

for names in filenames:
    nameFile = folderTalkings + names + ".txt"
    nameFileOut = folderTalkings +names + "_out.txt"
    file_handle = open(nameFile, encoding='utf8')
    print(nameFile + " opened")
    f = open(nameFileOut,'w')
    for line in file_handle:        
             #print(line[20:].replace('❤️','').replace('😜',';P').replace('🥺',':(')) #take the timespan out         
        noDateLine = line[20:].replace('❤️','').replace('ç','c').replace(' Andressa Preguicinha','Andressa Preguicinha').replace('🥴',':S').replace('🤯','=,)').replace('🤣','kkkk').replace('🥗','')
        noDateLine = noDateLine.replace('😒','...').replace('😁','hahaha').replace('😜',':P').replace('🙁',':(').replace('😥','snif..').replace('😶','').replace('❤','Amoo').replace('🥺','')
        noDateLine = noDateLine.replace('🤬','grrr').replace('😦','').replace('💔','coracao partido').replace('🙋🏼‍','eu!!!').replace('♀','').replace('🙋','eu!!!').replace('😔',':(')
        noDateLine = noDateLine.replace('😣','grrr').replace('😫',':,O').replace('🙄','de olho..').replace('😬','').replace('♾','').replace('😍','_olhos coracao_').replace('😭','snif snif snif')
        noDateLine = noDateLine.replace('🎷','').replace('🎼','').replace('🧐','').replace('🥳','').replace('🙏🏼','').replace('💗','').replace('👍🏼','').replace('😳','').replace('😉',';)')
        noDateLine = noDateLine.replace('💪','').replace('🏽','').replace('😷','').replace('😡','').replace('🤢','').replace('😟','').replace('🥰','').replace('🥶','').replace('🤵','')
        noDateLine = noDateLine.replace('🏻','').replace('😈','').replace('‍🏼','').replace('🤷','').replace('🏼‍','').replace('🤭','').replace('👏','').replace('👏🏼','').replace('🏼','')
        noDateLine = noDateLine.replace('👁','').replace(' 😘','').replace('😴','zzzz').replace('😘','').replace('🤗','').replace('😑','').replace('💆','').replace('☺','')
        noDateLine = noDateLine.replace('🙈','').replace('🤔','').replace('😱',':O').replace('😮',':O').replace('😢','snif').replace('😞','snif').replace('💎','')
        noDateLine = noDateLine.replace('💕','').replace('📐','').replace('📝','').replace('👑','').replace('🤩','').replace('😚','').replace('😇','').replace('🧳','').replace('😂','kkkk')
        noDateLine = noDateLine.replace('🚗','').replace('👍','ok').replace('☝','').replace('👀','').replace('😕','').replace('😰','').replace('😓','').replace('�','').replace('🤨','kkkk')
        noDateLine = noDateLine.replace('😅','').replace('💦','ok').replace('🇨🇦','').replace('🔥','').replace('😠','').replace('‍♂','').replace('🐱','').replace('🐠','').replace('⚽','').replace(' ️ ','')
        noDateLine = noDateLine.replace('💩','').replace('👎','ok').replace('🙃','').replace('🙏','').replace('‍💻','').replace('‍👨‍','').replace('👨','').replace('😽','')
        noDateLine = noDateLine.replace('😑','').replace('🙂',':)').replace('👇','').replace('👧','').replace('🤒','').replace('‍🤐‍','').replace(' 🤐','').replace('✌','')
        

        if(noDateLine.find('omitted') != -1):
            #print(noDateLine)
            noDateLine = noDateLine.split(':')[0]+': omitido\n'
            #print(noDateLine)

        if(noDateLine.find('Location') != -1):
            #print(noDateLine)
            noDateLine = noDateLine.split(':')[0]+': Location\n'

        if(noDateLine.find('deleted') != -1):
            #print(noDateLine)
            noDateLine = noDateLine.split(':')[0]+': mensagem deletada\n'

        if(noDateLine.find('Missed voice call') != -1):
                #print(noDateLine)
            noDateLine = noDateLine.split(':')[0]+': ligação perdida\n'
                

        if(noDateLine.find('Andressa Preguicinha :') != -1):                
            conversasDeA.append(noDateLine)                
        else:
            conversasDeA.append('|\n')
        
        if(noDateLine.find('Jpcn:') != -1):                
            conversasDeJ.append(noDateLine)                             
        else:
            conversasDeJ.append('|\n')
    
    faw = open(folderTalkings + names + "_ConvA.txt",'w', encoding='utf8')
    faw.writelines(conversasDeA)
    fbw = open(folderTalkings + names + "_ConvJ.txt",'w', encoding='utf8')
    fbw.writelines(conversasDeJ)






        #temp = re.sub(r'*-','-',line)
        #print(temp)
