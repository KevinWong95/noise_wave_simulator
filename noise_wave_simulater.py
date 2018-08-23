import sys
import os

#Creating variables for later used
#The boolean variables or switches used to determine specific outcomes, set to false
#Character flag switches character_used when printing
file_name=''
total_flag=False
character_used='*'
has_score_file=False
valid_score_file=True


#Iterate through each of the arguements
#File name arguement found as the string arguement not starting with '-'
#Determine whether the file is valid or if there even was one, change the switch variables
#Flags trigger switch/change character_used for future printing
for a in range (1, len(sys.argv)):
	if sys.argv[a][0]!='-':
		if os.path.isfile(sys.argv[a])==False:
			has_score_file=True
			valid_score_file=False
		else:
			file_name=sys.argv[a]
			has_score_file=True
			valid_score_file=True
	elif sys.argv[a]=='--total':
		total_flag=True
	elif sys.argv[a][0:11]=='--character':
		character_used=sys.argv[a].replace('--character=','')
		character_used=character_used[0]

#Checks boolean switches if a file was given and if it was valid
#Program can end here if either of the switches failed to switch to true
if valid_score_file is False:
	print('Invalid path to score file.')
elif has_score_file is False:
	print('No score file specified.')
else:
	with open(file_name, 'r') as score_file:
	    score_text=score_file.readlines()

	all_amps=[]
	total_amps=[]
	longest_score=0
	instrument_names=[]
	final_print=''

#This loop goes through each line in the score text file
#Names of instruments seperated from score lines in order to open instruments file
	for x in score_text:
		if x[0]!="|":
			repeat_instrument=False
			instrument_names.append(x.replace('\n',''))
			wave_list=[]
			wave_string=""

			#Checks if instrument exists, if not, exits
			if os.path.isfile("instruments/"+x.replace('\n',''))==False:
				print('Unknown source.')
				sys.exit()

			with open("instruments/"+x.replace('\n',''), 'r') as instrument_file:
				instrument_wave=instrument_file.readlines()

			#Create a list of strings for each line in the instrument wave
			for y in instrument_wave:
				if y[0]!="-":
					if y[0]=="0":
						longest_line=len(y)
					wave_list.append(y[2:len(y)-1])
				else:
					wave_list.append(y[3:len(y)-1])

			#Determine a single string representing the wave from the list
			#ie: ---//---\\\\\//--
			for n in range (0,longest_line):
				for m in range (0,len(wave_list)):
					if len(wave_list[m])>n:
						wave_string+=wave_list[m][n]
			wave_string=wave_string.replace(' ','')

		#For lines that start with '|', the line that represents the wave
		else:
			score_string=x
			score_string=score_string.replace('|','')
			score_string=score_string.replace('\n','')
			consecutive=0
			amp_list=[]

			#Create a list of amplitude int values based on "x value" on wave
			for r in range (0,len(score_string)):
				#For *'s
				if score_string[r]=='*':
					if r==0:
						amp_list.append(0)
					else:
						#For waves that loop
						if consecutive==len(wave_string):
							consecutive-=len(wave_string)
						if wave_string[consecutive]=='-':
							if wave_string[consecutive-1]=='-':
								amp_list.append(amp_list[r-1])
							if wave_string[consecutive-1]=='/':
								amp_list.append(amp_list[r-1]+1)
							if wave_string[consecutive-1]=='\\':
								amp_list.append(amp_list[r-1]-1)
						elif wave_string[consecutive]=='/':
							amp_list.append(amp_list[r-1]+1)
						elif wave_string[consecutive]=='\\':
							amp_list.append(amp_list[r-1]-1)
					consecutive+=1
				#For -'s
				if score_string[r]=='-':
					amp_list.append(0)
					consecutive=0

			#Track the longest score value
			if len(amp_list)>longest_score:
				longest_score=len(amp_list)

			#Same instruments are automatically combined, regardless of '--total' flag or not
			if repeat_instrument==False:
				all_amps.append(amp_list)
			else:
				for z in range(0, longest_score):
					if z<len(amp_list) and z<len(all_amps[-1]):
						all_amps[-1][z]+=amp_list[z]
					elif z<len(amp_list):
						all_amps[-1].append(amp_list[z])
			repeat_instrument=True

	#Total amps list created for total amp values
	for t in range(0,longest_score):
	    total_amps.append(0)
	    for s in range(0,len(all_amps)):
	    	if t<len(all_amps[s]):
	    		total_amps[t]+=all_amps[s][t]

	#Printing based on --total switch state
	if total_flag == False:
		#C value for iterating through each index of string
		for c in range (0, len(all_amps)):

			#Add instrument name to string
			final_print+=instrument_names[c]+':\n'
			highest=0
			lowest=0
			print_list=[]
			previous=0

			#Determine highest and lowest amp values
			for d in range (0, len(all_amps[c])):
				if all_amps[c][d]>highest:
					highest = all_amps[c][d]
				elif all_amps[c][d]<lowest:
					lowest = all_amps[c][d]

			#Create list of strings for each line that will be printed
			for g in range (highest, lowest-1, -1):
				if g>-1:
					print_list.append(' '+str(g)+':\t')
				else:
					print_list.append(str(g)+':\t')

			#Iterate through each string's [c] value.
			for v in all_amps[c]:
				#Print stacked *'s for increases increases/decreases greater than 1
				if v-previous>1:
					for q in range(0, len(print_list)):
						if int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))<=v and int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))>previous:
							print_list[q]+=character_used
						else: 
							print_list[q]+=' '
					previous=v
				elif v-previous<-1:
					for q in range(0, len(print_list)):
						if int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))>=v and int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))<previous:
							print_list[q]+=character_used
						else: 
							print_list[q]+=' '
					previous=v
				#Print *'s'
				else:
					for q in range(0, len(print_list)):
						if (print_list[q][0:print_list[q].find(':')]).replace(' ','')==str(v):
							print_list[q]+=character_used
						else:
							print_list[q]+=' '
					previous=v
			#Add all the strings in list to the final string which will be printed.
			for h in print_list:
				final_print+= h+'\n'
	#Case of --total flag being true
	else:
		final_print+="Total:\n"
		highest=0
		lowest=0
		print_list=[]
		previous=0

		#Determine highest and lowest amps to be printed
		for w in total_amps:
			if w>highest:
				highest = w
			elif w<lowest:
				lowest = w

		#Create list of strings for each line that will be used
		for p in range (highest, lowest-1, -1):
			if p>-1:
				print_list.append(' '+str(p)+':\t')
			else:
				print_list.append(str(p)+':\t')

		#Iterate through amp int values
		for v in total_amps:
			#Print stacked *'s for corresponding values
			if v-previous>1:
				for q in range(0, len(print_list)):
					if int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))<=v and int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))>previous:
						print_list[q]+=character_used
					else: 
						print_list[q]+=' '
				previous=v
			elif v-previous<-1:
				for q in range(0, len(print_list)):
					if int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))>=v and int((print_list[q][0:print_list[q].find(':')]).replace(' ',''))<previous:
						print_list[q]+=character_used
					else: 
						print_list[q]+=' '
				previous=v
			#Print *'s'
			else:
				for q in range(0, len(print_list)):
					if (print_list[q][0:print_list[q].find(':')]).replace(' ','')==str(v):
						print_list[q]+=character_used
					else:
						print_list[q]+=' '
				previous=v
		#Add strings from list to final print
		for h in print_list:
			final_print+= h+'\n'

	#Final product
	print(final_print[:-1	])