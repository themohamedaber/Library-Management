import pyodbc

# Set up the connection string
server = 'DESKTOP-PS5CQ9U'
database = 'loka'
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
#driver
#DRIVER={SQL Server};SERVER=.\SQLEXPRESS;DATABASE=master;Trusted_Connection=yes

# Establish the connection
connection = pyodbc.connect(connection_string)


current_user = None
current_admin = None



def sign_up_user():
    # Prompt the user for input
    ssn = input("Enter SSN: ")
    id = input("Enter ID: ")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    gender = input("Enter gender: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    age = input("Enter age: ")

    # Insert user data into the database
    query = f"INSERT INTO STUDENT (SSN, ID, FNAME, LNAME, GENDER, EMAIL, PASSWORD, AGE) " \
            f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    values = (ssn, id, fname, lname, gender, email, password, age)

    cursor.execute(query, values)
    connection.commit()

    print("User signed up successfully.")
    #########################################################################3
    
def sign_up_admin():
    # Prompt the admin for input
    admin_id = input("Enter Admin ID: ")
    admin_name = input("Enter Admin name: ")
    password = input("Enter password: ")
    email = input("Enter email: ")
    address = input("Enter address (optional): ")
    gender = input("Enter gender (optional): ")
    admin_age = input("Enter age (optional): ")

    # Validate input (you can add more validation logic here)

    # Insert admin data into the database
    query = f"INSERT INTO ADMIN (ADMIN_ID, ADMIN_NAME, PASSWORD, EMAIL, ADDRESS, GENDER, ADMIN_AGE) " \
            f"VALUES (?, ?, ?, ?, ?, ?, ?)"
    values = (admin_id, admin_name, password, email, address, gender, admin_age)

    cursor.execute(query, values)
    connection.commit()

    print("Admin signed up successfully.")

def sign_in_user():
    global current_user
    # Prompt the user for their email and password
    email = input("Enter email: ")
    password = input("Enter password: ")

    # Check if the user exists and the credentials are correct
    query = "SELECT * FROM STUDENT WHERE EMAIL = ? AND PASSWORD = ?"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        print("Sign-in successful.")
        current_user = user
    else:
        print("Invalid email or password.")


def sign_in_admin():
    global current_admin
    # Prompt the admin for their email and password
    email = input("Enter email: ")
    password = input("Enter password: ")

    # Check if the admin exists and the credentials are correct
    query = "SELECT * FROM ADMIN WHERE EMAIL = ? AND PASSWORD = ?"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()

    if admin:
        print("Sign-in successful.")
        current_admin = admin
    else:
        print("Invalid email or password.")


def sign_out_user():
    global current_user
    if current_user:
        current_user = None
        print("User signed out successfully.")
    else:
        print("No user is currently signed in.")

def sign_out_admin():
    global current_admin
    if current_admin:
        current_admin = None
        print("Admin signed out successfully.")
    else:
        print("No admin is currently signed in.")
   
#add book function
def add_book():
    global current_admin

    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.")
        return

    # Prompt the admin for book details
    id = input("Enter book id: ")
    title = input("Enter book title: ")
    publisher = input("Enter publisher: ")
    publication_date = input("Enter publication date (YYYY-MM-DD) (optional): ")
    isbn = input("Enter ISBN: ")

    # Prompt for author details
    author_id = input("Enter author id: ")
    author_name = input("Enter author name: ")

    # Prompt for category details
    category_id = input("Enter category id: ")
    category_name = input("Enter category name: ")

    # Prompt for copy details
    copy_no = input("Enter copy number: ")
    book_status = input("Enter book status: ")

    # Insert book data into the database
    book_query = "INSERT INTO BOOK (BOOK_ID, TITLE, PUBLISHER, PUBLICATION_DATE, ISBN) VALUES (?, ?, ?, ?, ?)"
    book_values = (id, title, publisher, publication_date if publication_date else None, isbn)

    # Insert author data into the database
    author_query = "INSERT INTO AUTHOR (AUTHOR_ID, AUTHOR_NAME) VALUES (?, ?)"
    author_values = (author_id, author_name)

    # Insert category data into the database
    category_query = "INSERT INTO CATAGORY (CATAGORY_ID, CATAGORY_NAME) VALUES (?, ?)"
    category_values = (category_id, category_name)

    # Insert relationship into BELONGS_TO table
    belongs_to_query = "INSERT INTO BELONGS_TO (BOOK_ID, CATAGORY_ID) VALUES (?, ?)"
    belongs_to_values = (id, category_id)

    # Insert relationship into WRITE table
    write_query = "INSERT INTO WRITE (AUTHOR_ID, BOOK_ID) VALUES (?, ?)"
    write_values = (author_id, id)

    # Insert data into COPY table
    copy_query = "INSERT INTO COPY (BOOK_ID, COPY_NO, BOOK_STATUS) VALUES (?, ?, ?)"
    copy_values = (id, copy_no, book_status)

    try:
        cursor.execute(book_query, book_values)
        cursor.execute(author_query, author_values)
        cursor.execute(category_query, category_values)
        cursor.execute(belongs_to_query, belongs_to_values)
        cursor.execute(write_query, write_values)
        cursor.execute(copy_query, copy_values)
        connection.commit()
        print("Book, author, category, write relationship, and copy added successfully.")
    except Exception as e:
        connection.rollback()
        print(f"An error occurred: {e}")


def update_book():
    global current_admin

    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.")
        return

    # Prompt the admin for book ID and the details to update
    book_id = input("Enter Book ID to update: ")
    
    # Book details
    title = input("Enter new book title (press Enter to skip): ")
    publisher = input("Enter new publisher (press Enter to skip): ")
    publication_date = input("Enter new publication date (YYYY-MM-DD) (press Enter to skip): ")
    isbn = input("Enter new ISBN (press Enter to skip): ")

    # Author details
    author_id = input("Enter new author ID (press Enter to skip): ")
    author_name = input("Enter new author name (press Enter to skip): ")

    # Category details
    category_id = input("Enter new category ID (press Enter to skip): ")
    category_name = input("Enter new category name (press Enter to skip): ")

    # Copy details
    copy_no = input("Enter new copy number (press Enter to skip): ")
    book_status = input("Enter new book status (press Enter to skip): ")

    try:
        # Update book details
        if title or publisher or publication_date or isbn:
            update_query = "UPDATE BOOK SET"
            update_values = []

            if title:
                update_query += " TITLE = ?,"
                update_values.append(title)
            if publisher:
                update_query += " PUBLISHER = ?,"
                update_values.append(publisher)
            if publication_date:
                update_query += " PUBLICATION_DATE = ?,"
                update_values.append(publication_date)
            if isbn:
                update_query += " ISBN = ?,"
                update_values.append(isbn)

            update_query = update_query.rstrip(',')
            update_query += " WHERE BOOK_ID = ?"
            update_values.append(book_id)

            cursor.execute(update_query, update_values)

        # Update author details
        if author_id or author_name:
            if author_id and author_name:
                author_query = "UPDATE AUTHOR SET AUTHOR_NAME = ? WHERE AUTHOR_ID = ?"
                cursor.execute(author_query, (author_name, author_id))
            elif author_id:
                author_query = "UPDATE AUTHOR SET AUTHOR_ID = ? WHERE BOOK_ID = ?"
                cursor.execute(author_query, (author_id, book_id))
            elif author_name:
                author_query = "UPDATE AUTHOR SET AUTHOR_NAME = ? WHERE AUTHOR_ID = (SELECT AUTHOR_ID FROM WRITE WHERE BOOK_ID = ?)"
                cursor.execute(author_query, (author_name, book_id))

        # Update category details
        if category_id or category_name:
            if category_id and category_name:
                category_query = "UPDATE CATAGORY SET CATAGORY_NAME = ? WHERE CATAGORY_ID = ?"
                cursor.execute(category_query, (category_name, category_id))
            elif category_id:
                category_query = "UPDATE CATAGORY SET CATAGORY_ID = ? WHERE BOOK_ID = ?"
                cursor.execute(category_query, (category_id, book_id))
            elif category_name:
                category_query = "UPDATE CATAGORY SET CATAGORY_NAME = ? WHERE CATAGORY_ID = (SELECT CATAGORY_ID FROM BELONGS_TO WHERE BOOK_ID = ?)"
                cursor.execute(category_query, (category_name, book_id))

        # Update copy details
        if copy_no or book_status:
            if copy_no and book_status:
                copy_query = "UPDATE COPY SET COPY_NO = ?, BOOK_STATUS = ? WHERE BOOK_ID = ?"
                cursor.execute(copy_query, (copy_no, book_status, book_id))
            elif copy_no:
                copy_query = "UPDATE COPY SET COPY_NO = ? WHERE BOOK_ID = ?"
                cursor.execute(copy_query, (copy_no, book_id))
            elif book_status:
                copy_query = "UPDATE COPY SET BOOK_STATUS = ? WHERE BOOK_ID = ?"
                cursor.execute(copy_query, (book_status, book_id))

        connection.commit()
        print("Book, author, category, and copy details updated successfully.")
    except Exception as e:
        connection.rollback()
        print(f"An error occurred: {e}")

def browse_books():
    # Retrieve all books from the database
    query = "SELECT * FROM BOOK"
    cursor.execute(query)
    books = cursor.fetchall()

    # Display the books
    if books:
        print("List of books:")
        for book in books:
            print(book)
    else:
        print("No books found.")

def search_books():
    # Define a list of valid criteria
    valid_criteria = ['TITLE', 'PUBLISHER', 'AUTHOR_NAME']

    # Prompt the user for search criteria
    print(f"Valid search criteria: {', '.join(valid_criteria)}")
    criteria = input("Enter the criteria to search by: ").upper()

    # Check if the provided criteria is valid
    if criteria not in valid_criteria:
        print(f"Invalid criteria '{criteria}'.")
        return

    # Prompt the user for the search value
    value = input(f"Enter {criteria} to search: ")

    # Construct the SQL query based on the criteria
    if criteria == 'AUTHOR_NAME':
        query = """
            SELECT BOOK.* FROM BOOK
            JOIN WRITE ON BOOK.BOOK_ID = WRITE.BOOK_ID
            JOIN AUTHOR ON WRITE.AUTHOR_ID = AUTHOR.AUTHOR_ID
            WHERE AUTHOR.AUTHOR_NAME LIKE ?
        """
  
    else:
        query = f"SELECT * FROM BOOK WHERE {criteria} LIKE ?"

    cursor.execute(query, ('%' + value + '%',))
    books = cursor.fetchall()

    # Display the search results
    if books:
        print(f"Books matching {criteria} '{value}':")
        for book in books:
            print(book)
    else:
        print(f"No books found matching {criteria} '{value}'.")


def delete_book():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.")
        return

    # Prompt the admin for the ID of the book to delete
    book_id = input("Enter Book ID to delete: ")

    try:
        # Execute the SQL DELETE queries
        book_query = "DELETE FROM BOOK WHERE BOOK_ID = ?"
        cursor.execute(book_query, (book_id,))
        author_query = "DELETE FROM AUTHOR WHERE AUTHOR_ID IN (SELECT AUTHOR_ID FROM WRITE WHERE BOOK_ID = ?)"
        cursor.execute(author_query, (book_id,))
        copy_query = "DELETE FROM COPY WHERE BOOK_ID = ?"
        cursor.execute(copy_query, (book_id,))
        
        connection.commit()

        if cursor.rowcount > 0:
            print("Book and associated data deleted successfully.")
        else:
            print("Book not found or could not be deleted.")
    except Exception as e:
        connection.rollback()
        print(f"An error occurred: {e}")

        
def borrow_book():
    # Prompt the user for their SSN, ID, and the book ID they want to borrow
    ssn = input("Enter your SSN: ")
    id = input("Enter your ID: ")
    book_id = input("Enter the book ID you want to borrow: ")

    # Check if the student exists in the STUDENT table
    student_query = "SELECT * FROM STUDENT WHERE SSN = ? AND ID = ?"
    cursor.execute(student_query, (ssn, id))
    student = cursor.fetchone()

    if not student:
        print("\033[31mStudent not found. Please enter valid SSN and ID.\033[0m \n")
        return

    # Check if the book is available for borrowing
    copy_query = "SELECT * FROM COPY WHERE BOOK_ID = ? AND BOOK_STATUS = 'available'"
    cursor.execute(copy_query, (book_id,))
    copy = cursor.fetchone()

    if not copy:
        print("\033[31mBook not available for borrowing.\033[0m \n")
        return

    # Insert borrow record into the BORROW table
    borrow_query = "INSERT INTO BORROW (SSN, ID, BOOK_ID) VALUES (?, ?, ?)"
    borrow_values = (ssn, id, book_id)
    cursor.execute(borrow_query, borrow_values)
    connection.commit()
    print("\033[32mBook borrowed successfully.\033[0m \n")
        

def update_user_details():
    global current_user
    # Check if an admin is signed in=
    if not current_user:
        print("User not signed in. Please sign in as an user.\n")
        return

    # pass the current user id
    id = current_user[1]
    query = "SELECT * FROM STUDENT WHERE ID = ?"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    if not user:
        print("User not found.\n")
        return
    else:
        # Construct the SQL update query
        fname = input("Enter new first name (press Enter to skip): ")
        lname = input("Enter new last name (press Enter to skip): ")
        email = input("Enter new email (press Enter to skip): ")
        password = input("Enter new password (press Enter to skip): ")
        age = input("Enter new age (press Enter to skip): ")
        gender = input("Enter new gender (press Enter to skip): ")
        update_query = "UPDATE STUDENT SET"
        update_values = []

        if fname:
            update_query += " FNAME = ?,"
            update_values.append(fname)
        if lname:
            update_query += " LNAME = ?,"
            update_values.append(lname)
        if email:
            update_query += " EMAIL = ?,"
            update_values.append(email)
        if password:
            update_query += " PASSWORD = ?,"
            update_values.append(password)
        if age:
            update_query += " AGE = ?,"
            update_values.append(age)
        if gender:
            update_query += " GENDER = ?,"
            update_values.append(gender)
        
        update_query = update_query[:-1] + " WHERE ID = ?"
        update_values.append(id)
        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()
        print("\033[32mUser details updated successfully.\033[0m \n")
        return
    
def delete_user():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.")
        return

    # Prompt the admin for the email of the user to delete
    user_email = input("Enter user email to delete: ")

    # Execute the SQL DELETE query
    query = "DELETE FROM STUDENT WHERE EMAIL = ?"
    cursor.execute(query, (user_email,))
    connection.commit()

    if cursor.rowcount > 0:
        print("User account deleted successfully.")
    else:
        print("User account not found or could not be deleted.")
        
def update_user_details_by_admin():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.\n")
        return

    # Prompt the admin for user ID and the details to update
    id = input("Enter user ID to update: ")
    query = "SELECT * FROM STUDENT WHERE ID = ?"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    if not user:
        print("User not found.\n")
        return
    else:
        # Construct the SQL update query
        ssn = input("Enter new SSN (press Enter to skip): ")
        id = input("Enter new ID (press Enter to skip): ")
        fname = input("Enter new first name (press Enter to skip): ")
        lname = input("Enter new last name (press Enter to skip): ")
        email = input("Enter new email (press Enter to skip): ")
        password = input("Enter new password (press Enter to skip): ")
        age = input("Enter new age (press Enter to skip): ")
        gender = input("Enter new gender (press Enter to skip): ")
        update_query = "UPDATE STUDENT SET"
        update_values = []

        if ssn:
            update_query += " SSN = ?,"
            update_values.append(ssn)
        if id:
            update_query += " ID = ?,"
            update_values.append(id)
        if fname:
            update_query += " FNAME = ?,"
            update_values.append(fname)
        if lname:
            update_query += " LNAME = ?,"
            update_values.append(lname)
        if email:
            update_query += " EMAIL = ?,"
            update_values.append(email)
        if password:
            update_query += " PASSWORD = ?,"
            update_values.append(password)
        if age:
            update_query += " AGE = ?,"
            update_values.append(age)
        if gender:
            update_query += " GENDER = ?,"
            update_values.append(gender)
        
        update_query = update_query[:-1] + " WHERE ID = ?"
        update_values.append(id)
        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()
        print("\033[32mUser details updated successfully.\033[0m \n")
        return

def update_admin_details():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.\n")
        return

    # Prompt the admin for admin ID and the details to update
    id = input("Enter admin ID to update: ")
    query = "SELECT * FROM ADMIN WHERE ADMIN_ID = ?"
    cursor.execute(query, (id,))
    admin = cursor.fetchone()
    if not admin:
        print("Admin not found.\n")
        return
    else:
        # Construct the SQL update query
        name = input("Enter new name (press Enter to skip): ")
        password = input("Enter new password (press Enter to skip): ")
        email = input("Enter new email (press Enter to skip): ")
        address = input("Enter new address (press Enter to skip): ")
        gender = input("Enter new gender (press Enter to skip): ")
        age = input("Enter new age (press Enter to skip): ")
        update_query = "UPDATE ADMIN SET"
        update_values = []

        if name:
            update_query += " ADMIN_NAME = ?,"
            update_values.append(name)
        if password:
            update_query += " PASSWORD = ?,"
            update_values.append(password)
        if email:
            update_query += " EMAIL = ?,"
            update_values.append(email)
        if address:
            update_query += " ADDRESS = ?,"
            update_values.append(address)
        if gender:
            update_query += " GENDER = ?,"
            update_values.append(gender)
        if age:
            update_query += " ADMIN_AGE = ?,"
            update_values.append(age)

        update_query = update_query[:-1] + " WHERE ADMIN_ID = ?"
        update_values.append(id)
        # Execute the update query
        cursor.execute(update_query, update_values)
        connection.commit()
        print("\033[32mAdmin details updated successfully.\033[0m\n")
        return


def main():
    global cursor
    try:
        cursor = connection.cursor()
        print("<<<<<<<<<<Welcome to the database project!>>>>>>>>>>")
        while True:
            print("Please select an option:")
            print("1. Sign up as a user")
            print("2. Sign up as an admin")
            print("3. Sign in as a user")
            print("4. Sign in as an admin")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                sign_up_user()
            elif choice == '2':
                sign_up_admin()
            elif choice == '3':
                sign_in_user()
            if current_user:
                    while current_user:
                        print("Please select an option:")
                        # user can browse all books
                        print("1. Browse all books")
                        # user can search books by critrea which is title or PUPLISHER
                        print("2. Search books by ...")
                        print("3. Update my account")
                        print("4. Borrow book")
                        print("5. sign out")
                        user_choice = input("Enter your choice: ")
                        if user_choice == '1':
                            browse_books()
                        elif user_choice == '2':
                            search_books()
                        elif user_choice == '3':
                            update_user_details()                        
                        elif user_choice == '4':
                            borrow_book()
                        elif user_choice == '5':
                            sign_out_user()                
                            break
                        else:
                            print("Invalid choice. Please try again.")

            elif choice == '4':
                sign_in_admin()
                if current_admin:
                    while current_admin:
                        print("Please select an option:")
                        print("1. Add a book")
                        print("2. Update a book")
                        print("3. Delete a book")
                        print("4. Browse all books")
                        print("5. Search books by ...")
                        print("6. Update my account")
                        print("7. Update User account")
                        print("8. Delete a user account")
                        print("9. Sign out")
                        admin_choice = input("Enter your choice: ")
                        if admin_choice == '1':
                            add_book()
                        elif admin_choice == '2':
                            update_book()
                        elif admin_choice == '3':
                            delete_book()
                        elif admin_choice == '4':
                            browse_books()
                        elif admin_choice == '5':
                            search_books()
                        elif admin_choice == '6':
                            update_admin_details()  
                        elif admin_choice == '7':
                            update_user_details_by_admin()      
                        elif admin_choice == '8':
                            delete_user()
                        elif admin_choice == '9':
                            sign_out_admin()
                            break
                        else:
                            print("Invalid choice. Please try again.")
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    main()
