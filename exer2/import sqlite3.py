import sqlite3


stephen_king_adaptations_list = []
with open(r'stephen_king_adaptations.txt', 'r') as file:
    stephen_king_adaptations_list = file.readlines()


conn = sqlite3.connect('stephen_king_adaptations.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
             (movieID INTEGER PRIMARY KEY AUTOINCREMENT,
             movieCode TEXT,
             movieName TEXT,
             movieYear INTEGER,
             imdbRating REAL)''')


for adaptation in stephen_king_adaptations_list:
    movie_details = adaptation.strip().split(',')
    try:
        movie_code = movie_details[0]
        movie_name = movie_details[1]
        movie_year = int(movie_details[2])
        imdb_rating = float(movie_details[3])
        c.execute('''INSERT INTO stephen_king_adaptations_table
                     (movieCode, movieName, movieYear, imdbRating)
                     VALUES (?, ?, ?, ?)''',
                  (movie_code, movie_name, movie_year, imdb_rating))
    except ValueError:
        
        continue


conn.commit()


while True:
    print("Search options:")
    print("1. Movie name")
    print("2. Movie year")
    print("3. Movie rating")
    print("4. STOP")
    choice = input("Enter your choice: ")

    if choice == "1":
        movie_name = input("Enter the movie name: ")
        c.execute('''SELECT * FROM stephen_king_adaptations_table
                         WHERE movieName = ?''', (movie_name,))
        results = c.fetchall()
        if results:
            for movie in results:
                print("Movie Code:", movie[1])
                print("Movie Name:", movie[2])
                print("Movie Year:", movie[3])
                print("IMDB Rating:", movie[4])
        else:
            print("No such movie exists in our database")

    elif choice == "2":
        movie_year = input("Enter the movie year: ")
        c.execute('''SELECT * FROM stephen_king_adaptations_table
                     WHERE movieYear = ?''', (int(movie_year),))
        results = c.fetchall()
        if results:
            for movie in results:
                print("Movie Code:", movie[1])
                print("Movie Name:", movie[2])
                print("Movie Year:", movie[3])
                print("IMDB Rating:", movie[4])
        else:
            print("No movies were found for that year in our database.")

    elif choice == "3":
        rating = input("Enter the minimum movie rating: ")
        c.execute('''SELECT * FROM stephen_king_adaptations_table
                     WHERE imdbRating >= ?''', (float(rating),))
        results = c.fetchall()
        if results:
            for movie in results:
                print("Movie Code:", movie[1])
                print("Movie Name:", movie[2])
                print("Movie Year:", movie[3])
                print("IMDB Rating:", movie[4])
        else:
            print("No movies at or above that rating were found in the database.")

    elif choice == "4":
        break

    else:
        print("Invalid choice. Please try again.")


conn.close()
