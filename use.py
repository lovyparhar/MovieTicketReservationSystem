import os
import csv

class User:
	def __init__(self, name , email, mnum, password):
		self.name = name
		self.email = email
		self.mnum = mnum
		self.password = password

class Booker:
	def __init__(self, name , email, mnum, seats, movie, date, slot):
		self.name = name
		self.email = email
		self.mnum = mnum
		self.seats = seats
		self.movie = movie
		self.date = date
		self.slot = slot