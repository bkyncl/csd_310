import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='movies_user',
    password='popcorn',
    port='3306',
    database='movies'
)
mycursor = db.cursor()
mycursor.execute('select * from film')
film = mycursor.fetchall()

print()
print('-----------------------------------------------------')
print(film)
print('-----------------------------------------------------')
for film in film:
    print('\nFilm: ' + film[1])
    print('Film Release Date: ' + film[2])
    print('Film Director: ' + film[4])

mycursor.execute('select * from studio')
studio = mycursor.fetchall()

print()
print('-----------------------------------------------------')
print(studio)
print('-----------------------------------------------------')
for studio in studio:
    print('\nStudio name: ' + studio[1])

