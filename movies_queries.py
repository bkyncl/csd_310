# movie_queries.py
# Module 7.2 Assignment 
# Name: Brittany Kyncl
# Date: 11.23.22
# Course: CSD310
# Assignment: Tables Queries, Movies database

import mysql.connector

config = {
    "user": "movies_user",
    "password": "popcorn",
    "host": "localhost",
    "database": "movies",
}
db = mysql.connector.connect(**config)
mycursor = db.cursor()

Q1 = "select * from studio"
Q2 = "select * from genre"
Q3 = "select film_name, film_runtime from film where film_runtime < '120'"
Q4 = "select film_name, film_director from film order by film_director"

mycursor.execute(Q1)
studios = mycursor.fetchall()
print('\n-- DISPLAYING Studio RECORDS --')
for studio in studios:
    print("Studio ID: {} \nStudio Name: {}".format(studio[0], studio[1]))
    print()

mycursor.execute(Q2)
genres = mycursor.fetchall()
print('\n-- DISPLAYING Genre RECORDS --')
for genre in genres:
    print("Genre ID: {} \nGenre Name: {}".format(genre[0], genre[1]))
    print()

mycursor.execute(Q3)
films = mycursor.fetchall()
print('\n-- DISPLAYING Short Film RECORDS --')
for film in films:
    print("Film Name: {} \nRuntime: {}".format(film[0], film[1]))
    print()

mycursor.execute(Q4)
directors = mycursor.fetchall()
print('\n-- DISPLAYING Director RECORDS in Order --')
for director in directors:
    print("Film Name: {} \nDirector: {}".format(director[0], director[1]))
    print()
