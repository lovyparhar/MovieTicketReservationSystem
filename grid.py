import os
import csv

def isleapyear(y):
	if(y % 100 == 0):
		return not(y % 400)
	else:
		return not(y % 4)


def nextdate(sd, sm, sy):
	sd += 1
	if(sm == 1 or sm == 3 or sm == 5 or sm == 7 or sm == 8 or sm == 10 or sm == 12):
		if(sd > 31):
			sd = sd % 31
			sm += 1

	elif(sm == 2):
		if(isleapyear(sy)):
			if(sd > 29):
				sd = sd % 29;
				sm += 1;
		else:
			if(sd > 28):
				sd = sd % 28;
				sm += 1;
	else:
		if(sd > 30):
			sd = sd % 30
			sm += 1

	if(sm > 12):
		sm = sm % 12
		sy += 1

	return [sd, sm, sy]

def twoweekdate(sd):
	l = []
	currd = sd
	l.append(currd)

	for i in range(14):
		currd = nextdate(currd[0], currd[1], currd[2])
		l.append(currd)

	return l


stdate = [28, 10, 2020]
slots = 6

dates = twoweekdate(stdate)

gr = []

def readslots(gr):
with open("slots.csv", "r") as slots:
	file_reader = csv.reader(slots)
	for line in file_reader:
		gr.append(line)


# gr = []
# for i in dates:
# 	row = []
# 	row.append(str(i[0]) + "|" + str(i[1]) + "|" + str(i[2]))
# 	for j in range(slots):
# 		row.append("nb")
# 	gr.append(row)

#user given slot
d = {"29|10|2020":"s4", "1|11|2020":"s3"}

for i in d:
	for j in gr:
		if(j[0] == i):
			j[int(d[i][1])] = 'apni'



def writeslots(gr):
	with open("slots.csv", "w") as slots:
		file_writer = csv.writer(slots)

		for i in gr:
			file_writer.writerow(i)
