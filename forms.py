import os
import csv

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

#getting validators class from wtforms module
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Writing in brackets means it is inheriting from FlaskForm class
class signupform(FlaskForm):
    #adding a string field
    #first argument is the name of the field
    #we also give a list of validator classes that are some checks
    name = StringField('Name', validators=[DataRequired(), Length(min = 2, max = 250)])
    # lastname = StringField('lastname', validators=[DataRequired(), Length(min = 2, max = 250)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 300)])
    confirmpassword = PasswordField('ConfirmPassword', validators=[DataRequired(), EqualTo('password')])
    mnum = StringField('Mobile number', validators=[DataRequired(), Length(min = 8, max = 15)])
    
    submit = SubmitField('Signup')

class loginform(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 300)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class admloginform(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 300)])
    submit = SubmitField('Login')

def validadm(email , password):
    l = []
    with open("admin.csv", "r") as admfile:
        file_reader = csv.reader(admfile)

        for line in file_reader:
            l.append(line)

    if(l[0][0] == email and l[0][1] == password):
        return True

    return False