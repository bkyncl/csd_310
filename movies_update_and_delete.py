# movie_updates_and_delete.py
# Module 8.2 Assignment 
# Name: Brittany Kyncl
# Date: 11.25.22
# Course: CSD310
# Assignment: Movies Updates and Deletes

import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='movies_user',
    password='popcorn',
    port='3306',
    database='movies'
)
mycursor = db.cursor()

def insert_film(mycursor, film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id):
    # method to execute insert into

    # insert into film table
    mycursor.execute("insert into film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) values(%s,%s,%s,%s,%s,%s)", 
                    (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id))
    db.commit() # commit new change to database

    # query to show new film record
    mycursor.execute("select * from film order by film_id desc limit 1")
    # get results from mycursor object
    newfilms = mycursor.fetchall()
    
    print("\n -- Film {} Added --".format(film_name))

    # iterate over film table to display updated data
    for newfilm in newfilms:
        print("Film ID: {}\nFilm Name: {}\nRelease Date: {}\nRuntime: {}\nDirector: {}\nStudio ID: {}\nGenre ID: {}\n".format
            (newfilm[0],newfilm[1],newfilm[2],newfilm[3],newfilm[4],newfilm[5],newfilm[6]))

def show_films(mycursor, title):
    # method to execute an inner join on all tables

    # inner join query
    mycursor.execute("select film_name as Name, film_director as Director, genre_name as Genre, studio_name as 'Studio Name'"
                    "from film inner join genre on film.genre_id = genre.genre_id inner join studio on film.studio_id = studio.studio_id order by name asc")

    # get results from the mycursor object
    films = mycursor.fetchall()

    print("\n -- {} --".format(title))

    # iterate over the film data and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0],film[1],film[2],film[3],))

def change_genre(mycursor,new_genreid, film_id):
    # method to update genre within film table

    # execute update statement
    mycursor.execute("update film set genre_id = %s where film_id = %s", (new_genreid, film_id))
    db.commit() # commit new change to database

    print("\n -- DISPLAYING FILMS AFTER UPDATE -- ")

    mycursor.execute("Select * from all_view")
    # get results from mycursor object
    films = mycursor.fetchall()

    # iterate over the film data and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0],film[1],film[2],film[3],))


def delete_film(mycursor, film_id):
    # method to update genre within film table

    #execute delete record statement
    mycursor.execute("delete from film where film_id = {}".format(film_id))
    db.commit() # commit new change to database
    mycursor.execute("alter table film auto_increment =1")

    print("\n -- DISPLAYING FILMS AFTER DELETION -- ")

    mycursor.execute("Select * from all_view")
    # get results from mycursor object
    films = mycursor.fetchall()

    # iterate over the film data and display the results
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0],film[1],film[2],film[3],))

# show_films(mycursor, "DISPLAYING FILMS")
# insert_film(mycursor, "Gladiator", 2005, 160, "Ridley Scott", 2, 2)
# show_films(mycursor, "DISPLAYING FILMS AFTER INSERT")
# change_genre(mycursor, 1, 2)
# delete_film(mycursor, 5)

db.close()

close = input("Press enter to close: ")