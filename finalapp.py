from flask import Flask, render_template, request, url_for,flash,redirect, session
import csv
import os
import secrets
from forms import signupform, loginform, admloginform, validadm

from dir import writecsv, readcsv
from dirslot import readslots, writeslots, makefol, delfol, spacetoscore, scoretospace
from use import User, Booker
import string

#Functons for interacting with user material
class user_ops:

    # users is a static attribute of this class
    # It stores the users during the running of server
    users = []

    #gets users from file to list
    def extractusers():
        if(os.path.exists('users.csv')):

            with open('users.csv', 'r') as readfile:
                file_reader = csv.reader(readfile)

                for line in file_reader:
                    uob = User(line[0], line[1], line[2], line[3])
                    user_ops.users.append(uob)


    #writes users to the file
    def writeusers():
        with open('users.csv', 'w') as writefile:
            file_writer = csv.writer(writefile)

            for i in user_ops.users:
                file_writer.writerow([i.name, i.email, i.mnum, i.password])


#Functios for interacting with bookings
class bookings:

    # This list will store the bookings
    bookinglist = []

    def extractbooking():
        if(os.path.exists('booking.csv')):

            with open('booking.csv', 'r') as readfile:
                file_reader = csv.reader(readfile, delimiter = '|')

                for line in file_reader:
                    bob = Booker(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
                    bookings.bookinglist.append(bob)


    def writebooking():
        with open('booking.csv', 'w') as writefile:
            file_writer = csv.writer(writefile, delimiter = '|')

            for i in bookings.bookinglist:
                file_writer.writerow([i.name, i.email, i.mnum, i.seats, i.movie, i.date, i.slot])



app = Flask(__name__)

#Cookie Stuff
#Setting a key for the user to remember that he is logged in
app.config['SECRET_KEY']="4825b5623e518dff25c22b4e1fd1d166"

#Filling up the users already present in file
user_ops.extractusers()

#Filling up the booking list
bookings.extractbooking()


#A 2D list representing all possible seats having seat as its element
allseats = [];
for i in range(10):
    row = []
    col1 = []
    for j in range(10):
        col1.append(str(i) + "-" + str(j))
    row.append(col1)

    col2 = []
    for j in range(10, 20):
        col2.append(str(i) + "-" + str(j))
    row.append(col2)
    allseats.append(row)

# reading all the directories of movies, date, timeslots and seats booked at that timeslot in the form
# of nested dictionary
movs = readcsv()

#for converting slot to time
slottotime = {"s1": "8:00 AM", "s2" : "12:00 PM", "s3" : "1:00 PM", "s4" : "4:00 PM", "s5" : "6:00 PM", "s6" : "9:00 PM"}

#list of capital letters for conversion
numtoalpha = list(string.ascii_uppercase)









################
#THE ADMIN PAGES
################

gr = []

#we are reading the slots booked for movies
readslots(gr)

dirstomake =[]


@app.route("/addmovie")
def addmovie():
    if(session.get('email') and session.get('type') == "admin"):
        return render_template("addmov.html")

    return "<h1>Please login as an admin to view this</h1>"


@app.route("/slotsel", methods = ["POST"])
def slotsel():
    moviename = spacetoscore(request.form.get("moviename"))
    movdirector = request.form.get("movdirector")
    leadactor = request.form.get("leadactor")
    rating = request.form.get("rating")


    target = os.path.join(os.getcwd(),'static/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = moviename
        destination = os.path.join(target,filename)
        print(destination)
        file.save(destination)


    l = [moviename, movdirector, leadactor, rating]

    with open("movieinfo.csv", "a") as movinfo:
        writeinfo = csv.writer(movinfo)
        writeinfo.writerow(l)

    return render_template("slot.html", gr = gr, moviename = moviename)



@app.route("/movieadded", methods = ["POST"])
def added():
    lis = request.form.getlist("sl")
    # print (list)
    name = request.form.get("moviename")
    name = spacetoscore(name)

    for i in lis:
        ct = 0
        j = i[ct]
        while(j != '-' and ct < len(i)):
            ct += 1
            j = i[ct]
        gr[int(i[0:ct])][int(i[ct+1:len(i)])] = name

        #The following list is of type [mname, date, slot]
        addu = [name, gr[int(i[0:ct])][0], "s" + str(int(i[ct+1:len(i)]))]
        dirstomake.append(addu)

    makefol(dirstomake)

    # print(dirstomake)
    writeslots(gr)
    return "<h1>Movie Added Succesfully</h1>"



@app.route("/delslot")
def slotdel():

    if(session.get('email') and session.get('type') == "admin"):

        return render_template("clearslots.html", gr = gr, scoretospace = scoretospace)

    return "<h1>Please login as an admin to view this</h1>"



@app.route("/slotdeleted", methods = ["POST"])
def deleted():

    dirstodel = []
    if(session.get('email') and session.get('type') == "admin"):
        lis = request.form.getlist("sl")

        for i in lis:
            ct = 0
            j = i[ct]
            while(j != '-' and ct < len(i)):
                ct += 1
                j = i[ct]
            name = gr[int(i[0:ct])][int(i[ct+1:len(i)])]
            gr[int(i[0:ct])][int(i[ct+1:len(i)])] = "nb"

            #The following list is of type [mname, date, slot]
            addu = [name, gr[int(i[0:ct])][0], "s" + str(int(i[ct+1:len(i)]))]
            dirstodel.append(addu)

        a = delfol(dirstodel)

        # Removing movie from the view page also
        if(a):
            lines = []
            with open('movieinfo.csv', 'r') as readFile:
                reader = csv.reader(readFile)

                for row in reader:
                    lines.append(row)
                    for field in row:
                        if field == a:
                            lines.remove(row)

            with open('movieinfo.csv', 'w') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)

        # print(dirstomake)
        writeslots(gr)
        return '''<h1>Slot Deleted Succesfully</h1> <a href = "/">Go back</a>'''

    return "<h1>Please login as an admin to view this</h1>"




###############
#THE USER PAGES
###############


#The seats are 200 in number, 100-100 divided
#allseats is a 2D list representing seats with a gap

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/displaymov")
def viewmov():
    lis = []
    if(os.path.exists("movieinfo.csv")):
        with open("movieinfo.csv", "r") as read:
            rd = csv.reader(read)
            for line in rd:
                lis.append(line)

        return render_template("viewmovies.html", lis = lis, scoretospace = scoretospace)
    else:
        return "<h1>NO MOVIES TO DISPLAY<h1>"



@app.route("/movies")
def selmov():
    if(session.get('email') and session.get('type') == "user"):
        #read dirs before selecting movie
        movs = readcsv()
        #passed the whole dictionary to template to access its keys that are movies
        return render_template("movies.html", movs = movs, scoretospace = scoretospace)

    elif(session.get('email') and session.get('type') == "admin"):
        return "<h1>Please Login as a user to access it</h1>"
    else:
        return "<h1>Please Login to access it</h1>"

movs = readcsv()



@app.route("/movies/date", methods=["POST"])
def seldate():
    movs = readcsv()
    #accessed the things that form at /movies gave to the date, i.e. the movie selected
    selmovie = request.form.get("movie")

    #two arguments are given to render with template, one is to get the options of dates
    #available to select one and other is the name of movie to just propogate
    return render_template("date.html", dates = movs[selmovie], selmovie = selmovie)

movs = readcsv()



@app.route("/movies/date/time", methods=["POST"])
def seltime():
    movs = readcsv()
    seldate = request.form.get("date")
    selmovie = request.form.get("selectedmovie")
    totime = slottotime
    return render_template("time.html", times = movs[selmovie][seldate], selmovie=selmovie, seldate=seldate, totime = totime)

movs = readcsv()



@app.route("/movies/date/time/seats", methods=["POST"])
def seats():
    movs = readcsv()
    seltime = request.form.get("time")
    seldate = request.form.get("selecteddate")
    selmovie = request.form.get("selectedmovie")
    return render_template("seatmat.html", allseats= allseats, bookeds = movs[selmovie][seldate][seltime], seltime=seltime, selmovie=selmovie, seldate=seldate)

movs = readcsv()



@app.route("/movies/date/time/seats/registered", methods=["POST"])
def register():
    movs = readcsv()
    inlist = request.form.getlist("ts")
    seltime = request.form.get("selectedtime")
    seldate = request.form.get("selecteddate")
    selmovie = request.form.get("selectedmovie")

    if(request.method == "POST"):
        if(len(inlist) == 0):
            return "<h1>Please go back and select seats<h1>"
        else:
            movs[selmovie][seldate][seltime].extend(inlist)

    # MAKING A COMBINED STRING OF BOOKED SEATS SEPARATED BY COMMAS
    seatstring = ''
    for i in range(len(inlist)):
        if i != len(inlist) - 1:
            seatstring += inlist[i] + ","
        else:
            seatstring += inlist[i]

    bob = None
    for i in user_ops.users:
        if i.email == session.get('email'):
            bob = Booker(i.name, i.email, i.mnum, seatstring, selmovie, seldate, seltime)
            bookings.bookinglist.append(bob)
            break

    seatstodisp = []
    for i in inlist:

        ct = 0
        j = i[ct]
        while(j != '-' and ct < len(i)):
            ct += 1
            j = i[ct]

        #Row is an alphabet given according to its number
        row = str( numtoalpha[ int(i[0:ct]) ] )

        #column is a number
        col = str( int(i[ct+1:len(i)]) + 1 )

        seatstodisp.append([row, col])

    bookings.writebooking()
    writecsv(movs)
    return render_template("eticket.html", name = bob.name, email = bob.email, seats = seatstodisp, mnum = bob.mnum, movie = bob.movie, date = bob.date, time = bob.slot, slottotime = slottotime, scoretospace = scoretospace)

movs = readcsv()







########################
# LOGIN AND SIGNUP STUFF
########################


#login for an existing user

@app.route("/loginuser", methods=["GET", "POST"])

def userlog():
    if(session.get('email')):
        return "<h1>Please log out before accessing this page</h1>"

    #making a loginform object
    form = loginform()

    if form.validate_on_submit():
        userob = {}
        userob['email'] = form.email.data
        userob['password'] = form.password.data

        print (userob['email'], userob['password'])

        for u in user_ops.users:

            if userob['email'] == u.email:

                if userob['password'] == u.password:
                    flash(f'Login Succesfull for {u.name}!','success')

                    #This is the actual logging in of the user
                    session['email'] = form.email.data
                    session['type'] = 'user'
                    return redirect(url_for('home'))

                else:
                    flash(f'Wrong Credentials','danger')
                    return render_template('login.html', title = "Log in", form = form)

        # If nothing returned it means that obove email is not there
        flash(f'User does not exist','danger')

    return render_template('login.html', title = "Log in", form = form)


@app.route("/logoutuser")
def userlogout():
    if(session.get('email') and session.get('type') == "user"):
        session.pop('email')
        session.pop('type')
        return redirect(url_for('home'))

    else:
        return "<h1>User not logged in</h1>" 

#SIGN UP FOR A NEW USER

@app.route("/signup",methods=['GET','POST'])
def signup():

    form=signupform()
    # print (form.validate_on_submit())
    # print(form.errors)


    if form.validate_on_submit():

        #if form is valid, we create a User object to store user
        userob = User(form.name.data, form.email.data, form.mnum.data, form.password.data)

        for u in user_ops.users:
            if u.email == userob.email:
                flash(f'Email already exists!','danger')
                return render_template('signup.html',title="signup",form=form)

        flash(f'Signup Succesfull for {form.name.data}!','success')
        user_ops.users.append(userob)

        user_ops.writeusers()

        return redirect(url_for('home'))

    #After post if it reaches here then it means that it is not validated
    return render_template('signup.html',title="signup",form=form)







# ADMIN LOGIN AND LOG OUT
# ONLY ONE ADMIN IS THERE AND HE IS PREDEFINED

@app.route("/loginadmin", methods=["GET", "POST"])
def adminlog():

    if(session.get('email')):
        return "<h1>Log out to access this page</h1>"

    else:
        form = admloginform()
        alert = None

        # The validate on submit takes care if the method is post and no error is there
        # in form.errors dictionary and we are checking if admin credentials are right

        if (form.validate_on_submit() and validadm(form.email.data, form.password.data)):
            
            #If admin logged in it means that their email is in the session
            #also the type of user is admin
            session['email'] = form.email.data
            session['type'] = 'admin'
            return redirect(url_for('home'))
        

        if (form.validate_on_submit() and not validadm(form.email.data, form.password.data)):
            alert = 'Wrong Credentials!'
            #print("Mai challeya")

        #print (alert)

        return render_template("adminlogin.html", form = form, alert = alert)

@app.route("/logoutadmin")
def adminlogout():
    if(session.get('email') and session.get('type') == "admin"):
        session.pop('email')
        session.pop('type')
        return redirect(url_for('home'))

    else:
        return "<h1>Admin not logged in</h1>"    


if(__name__ == "__main__"):
    app.run()
