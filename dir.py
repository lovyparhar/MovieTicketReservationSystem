import os
import csv


#MAKING FOLDERS FROM DICTIONARY
def writecsv(movs):
	curdir = os.getcwd()

	if not os.path.isdir(os.path.join(curdir, "Movies")):
		os.mkdir("Movies")

	moviedir = os.path.join(curdir, "Movies")
	os.chdir(moviedir)

	for i in movs:
		if not os.path.isdir(os.path.join(os.getcwd(), i)):
			os.mkdir(i)
		datedir = os.path.join(os.getcwd(), i)
		os.chdir(datedir)

		for j in movs[i]:
			if not os.path.isdir(os.path.join(os.getcwd(), j)):
				os.mkdir(j)

			timedir = os.path.join(os.getcwd(), j)
			os.chdir(timedir)

			for k in movs[i][j]:
				if not os.path.isdir(os.path.join(os.getcwd(), k)):
					os.mkdir(k)
				seatsdir = os.path.join(os.getcwd(), k)
				os.chdir(seatsdir)

				if movs[i][j][k]:
					with open("seats.csv", 'w') as seatmap:
						writingob = csv.writer(seatmap)
						for n in movs[i][j][k]:
							writingob.writerow([n])

				if(os.path.exists('seats.csv') and (len(movs[i][j][k])==0)):
					os.remove('seats.csv')

				os.chdir(timedir)

			os.chdir(datedir)

		os.chdir(moviedir)

	os.chdir(curdir)




#MAKING DICTIONARY OUT OF DIRECTORIES

#IF YOU ADD MOVIES BY SLOT THEN IT WILL SURELY MAKE DICTIONARY
def readcsv():
	movs = dict()

	curdir = os.getcwd()

	moviedir = os.path.join(curdir, "Movies")
	os.chdir(moviedir)

	movies = os.listdir(os.getcwd())

	for i in movies:
		movs[i] = dict()

		datedir = os.path.join(os.getcwd(), i)
		os.chdir(datedir)

		dates = os.listdir(os.getcwd())
		for j in dates:
			movs[i][j] = dict()

			timedir = os.path.join(os.getcwd(), j)
			os.chdir(timedir)

			times = os.listdir(os.getcwd())
			for k in times:
				movs[i][j][k] = []

				seatdir = os.path.join(os.getcwd(), k)
				os.chdir(seatdir)

				if(os.path.exists("seats.csv")):
					with open("seats.csv", "r") as readfile:
						file_reader = csv.reader(readfile)

						for line in file_reader:
							movs[i][j][k].extend(line)
				os.chdir(timedir)

			os.chdir(datedir)

		os.chdir(moviedir)

	os.chdir(curdir)

	return movs
