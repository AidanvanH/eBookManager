import sqlite3
from sqlite3 import IntegrityError

book_titles = [] # Change to dictionary that holds id and title to allow for case insensitive book searches

# Creating the table using SQLite3
db = sqlite3.connect('ebookstore')

cursor = db.cursor()

# # Checks if the table “book” exists and if not creates it
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title TEXT UNIQUE, author TEXT, qnt INTEGER)
''')

# Entering the following books into the database
id_1 = 3001
author_1 = 'Charles Dickens'
title_1 = 'A Tale of Two Cities'
qnt_1 = 30

id_2 = 3002
author_2 = 'J.K. Rowling'
title_2 = 'Harry Potter and the Philosopher\'s Stone'
qnt_2 = 40

id_3 = 3003
author_3 = 'C.S Lewis'
title_3 = 'The Lion, the Witch and the Wardrobe'
qnt_3 = 25

id_4 = 3004
author_4 = 'J.R.R Tolkien'
title_4 = 'The Lord of the Rings'
qnt_4 = 37

id_5 = 3005
author_5 = 'Lewis Carroll'
title_5 = 'Alice in Wonderland'
qnt_5 = 12

books_and_author_list = [(id_1, author_1, title_1, qnt_1),
                         (id_2, author_2, title_2, qnt_2),
                         (id_3, author_3, title_3, qnt_3), 
                         (id_4, author_4, title_4, qnt_4),
                         (id_5, author_5, title_5, qnt_5)]

# Using a tuple to pass the query parameter to cursor.execute()
cursor.executemany('''INSERT OR IGNORE INTO book(id, author, title, qnt)
                      VALUES(?,?,?,?)''', books_and_author_list)

# Fills the empty 'book_titles' list with the book titles that are already in the database
cursor.execute('''SELECT title FROM book''')
for row in cursor:
    book_title = ''.join(row)
    # Lowercasing book titles to enable case-insensitive searches.
    book_titles.append(book_title)

db.commit()

# Defining the functions to use in the program
def enter_book():

            
    while True:

        # Asking user to enter new book and removing trailing whitespace if user mistakenly added some
        book_title = input('Enter the new book\'s title: ').rstrip() 

        if book_title in book_titles:
            print('Book title already exists')
        # Checks to see if the user only entered whitespace
        elif book_title.strip() == '':
            print('Invalid input')
        else:
            # Lowercasing book titles to enable case-insensitive searches.
            book_titles.append(book_title)
            break

    while True:

        book_author = input('Enter the new book\'s author: ' ).rstrip()
        if book_author.strip() == '':
            print('Invalid input')
        # Prevents user from entering digit inputs
        elif book_author.isdigit():
            print('Incorrect data type provided')
        else:
            break
    
    while True:

        try:
            book_qnt = int(input('Enter the number of copies: '))
            if book_qnt == '':
                print('Invalid input')
            else:
                break
        # Prevents user from entering non-numeric values 
        except ValueError:
            print('Incorrect data type provided')

    # Inserts new book entry into the database
    cursor.execute('''INSERT OR IGNORE INTO book(title, author, qnt)
                      VALUES(?,?,?)''', (book_title, book_author, book_qnt))

    db.commit()

    print('New entry successfully added')

def update_book():
    

    while True:

        # Convert output to same casing as titles
        which_book = input('Which book would you like to update?: ')   

        if which_book in book_titles:

            # Passing in argument which_book as a tuple as the expected syntax for cursor.execute() methods 
            # requires parameters
            cursor.execute('''SELECT * FROM book WHERE title = ? ''', (which_book,))
            for row in cursor:
                print(row[0], '-', row[1], '-', row[2], '-', row[3])

            while True:

                which_section = input('''
Which section would you like to update:
1. ID number
2. Book title
3. Author
4. Quantity: ''')
                
                if which_section == '1':
                    while True:

                        try:
                            new_id = int(input('Enter book new ID: '))
                            # Saves the changes to book's id in the database
                            cursor.execute('''UPDATE book SET id = ? WHERE title = ?''', (new_id, which_book))
                            db.commit()
                            print('Update was successful!')
                            break
                        # Used to catch UNIQUE constraint errors
                        except IntegrityError:
                            print('Book ID already exists')
                        # Used to catch any other errors
                        except ValueError:
                            print('Invalid input, only insert nums')
                    break

                elif which_section == '2':
                    while True:

                        new_title = input('Enter the books new title: ')
                        if new_title.strip() == '':
                            print('Invalid input')
                        # Prevents user from updating the book to an existing book's title
                        elif new_title in book_titles:
                            print('Book title already exists!')
                        else:
                            # Saves the changes to book's title in the database
                            cursor.execute('''UPDATE book SET title = ? WHERE title = ?''', (new_title, which_book))
                            db.commit()
                            print('Update was successful!')
                            break
                    break

                elif which_section == '3':
                    while True:

                        new_author = input('Enter the books new author: ')
                        # Checks if input is whitespace or numeric
                        if new_author.strip() == '' or new_author.isdigit():
                            print('Invalid input')
                        else:
                            # Saves the changes to book's author in the database
                            cursor.execute('''UPDATE book SET author = ? WHERE title = ?''', (new_author, which_book))
                            db.commit()
                            print('Update was successful!')
                            break
                    break
                
                elif which_section == '4':
                    while True:

                        try:
                            new_qnt = int(input('Enter the new books quantity: '))
                            # Saves the changes to book's quantity in the database
                            cursor.execute('''UPDATE book SET qnt = ? WHERE title = ?''', (new_qnt, which_book))
                            db.commit()
                            print('Update was successful!')
                            break
                        except ValueError:
                            print('Invalid input')
                    break
                else:
                    print('Please select a valid option')
            break

        else:
            print('Book doesn\'t exist')

def delete_book():
    

    while True:

        delete_which_book = input('Which book would you like to delete from the database?: ')
        if delete_which_book in book_titles:
            # Deleting book from the database
            cursor.execute('''DELETE FROM book WHERE title = ?''', (delete_which_book,))
            print('Book successfully deleted from system')
            book_titles.remove(delete_which_book)
            db.commit()
            break
        else:
            print('Book does not exist')

def search_book():
    
    
    while True:
        search_book = input('Which book would you like to search for: ')

        if search_book in book_titles:
            # passing in argument which_book as a tuple
            cursor.execute('''SELECT * FROM book WHERE title = ? ''', (search_book,))
            for row in cursor:
                print(row[0], '-', row[1], '-', row[2], '-', row[3])
            break

        else:
            print('Book doesn\'t exist')

def display_all_books():

    cursor.execute('''SELECT * FROM book''')
    for row in cursor:
        print(row[0], '-', row[1], '-', row[2], '-', row[3])

# Section that prompts and receives user inputs
while True:

    option = input('''
Pick an option:
1.    Enter book 
2.    Update book
3.    Delete book
4.    Search book
5.    Display all books
0.    Exit
      ''')
    
    if option == '1':
        enter_book()
    elif option == '2':
        update_book()
    elif option == '3':
        delete_book()
    elif option == '4':
        search_book()
    elif option == '5':
        display_all_books()
    elif option == '0':
        print('Thanks for using the app. Have a great day!')
        break
    else:
        print("You have made entered an invalid input. Please try again")



# The following article help me prevent users from entering duplicate values into the table by using 
# INSERT OR IGNORE 
# https://stackoverflow.com/questions/36518628/sqlite3-integrityerror-unique-constraint-failed-when-inserting-a-value

# The following article helped me address a problem I had relating to the cursor.execute() syntax. Through the use
# of this article I learned that it is best to use a tuple when entering a single value when using the 
# cursor.execute() method as the expected syntax for cursor.execute() methods requires parameters to be in the 
# form of tuples or lists
# https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta

# I researched for a way that would ensure my program catches UNIQUE constraint entries made by the user and
# found this article that states that importing IntegrityError from sqlite3 is one way to achieve this.
# https://stackoverflow.com/questions/27729487/how-to-catch-a-unique-constraint-failed-404-in-django