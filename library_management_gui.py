import tkinter as tk
from tkinter import messagebox
import pyodbc


# Set up the connection string
server = 'DESKTOP-PS5CQ9U'
database = 'loka'
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

# Establish the connection
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Global variables to keep track of the current student and admin
current_student = None
current_admin = None

# Function to sign in a student
def sign_in_student(email, password):
    global current_student
    # Assuming you have initialized your cursor and connection elsewhere
    query = "SELECT * FROM STUDENT WHERE EMAIL = ? AND PASSWORD = ?"
    cursor.execute(query, (email, password))
    student = cursor.fetchone()
    if student:
        current_student = student
        return True
    else:
        return False

def sign_in_admin(email, password):
    global current_admin
    # Assuming you have initialized your cursor and connection elsewhere
    query = "SELECT * FROM ADMIN WHERE EMAIL = ? AND PASSWORD = ?"
    cursor.execute(query, (email, password))
    admin = cursor.fetchone()
    if admin:
        current_admin = admin
        return True
    else:
        return False



# Function to sign up a student
def sign_up_student(ssn, id, fname, lname, gender, email, password, age, cursor, connection):
    try:
        query = "INSERT INTO STUDENT (SSN, ID, FNAME, LNAME, GENDER, EMAIL, PASSWORD, AGE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (ssn, id, fname, lname, gender, email, password, age))
        connection.commit()
        messagebox.showinfo("Info", "Student signed up successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def sign_up_admin(admin_id, admin_name, password, email, address, gender, admin_age, cursor, connection):
    try:
        # Insert admin data into the database
        query = "INSERT INTO ADMIN (ADMIN_ID, ADMIN_NAME, PASSWORD, EMAIL, ADDRESS, GENDER, ADMIN_AGE)  VALUES (?, ?, ?, ?, ?, ?, ?)"
        values = (admin_id, admin_name, password, email, address, gender, admin_age)

        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Info", "Admin signed up successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to display all books
def browse_books():
    browse_books_window = tk.Toplevel(root)
    browse_books_window.title("Browse All Books")

    # Adjust the SQL query to fetch books from the 'BOOK' table
    query = "SELECT TITLE, PUBLISHER, PUBLICATION_DATE, ISBN FROM BOOK"
    cursor.execute(query)
    books = cursor.fetchall()

    listbox = tk.Listbox(browse_books_window, width=100)
    listbox.pack(pady=20)

    for book in books:
        title = book[0]
        publisher = book[1]
        publication_date = book[2] if book[2] else "N/A"
        isbn = book[3]
        listbox.insert(tk.END, f"Title: {title}, Publisher: {publisher}, Publication Date: {publication_date}, ISBN: {isbn}")

def search_books(criteria):
    search_books_window = tk.Toplevel(root)
    search_books_window.title(f"Search Books by {criteria.capitalize()}")

    def perform_search():
        search_term = search_entry.get()
        
        if criteria == 'author':
            query = """
                SELECT BOOK.TITLE, BOOK.PUBLISHER, BOOK.ISBN FROM BOOK
                JOIN WRITE ON BOOK.BOOK_ID = WRITE.BOOK_ID
                JOIN AUTHOR ON WRITE.AUTHOR_ID = AUTHOR.AUTHOR_ID
                WHERE AUTHOR.AUTHOR_NAME LIKE ?
            """
       
        else:
            query = f"SELECT TITLE, PUBLISHER, ISBN FROM BOOK WHERE {criteria.upper()} LIKE ?"

        cursor.execute(query, ('%' + search_term + '%',))
        results = cursor.fetchall()

        listbox.delete(0, tk.END)
        for book in results:
            title = book[0]
            publisher = book[1]
            isbn = book[2]
            listbox.insert(tk.END, f"Title: {title}, Publisher: {publisher}, ISBN: {isbn}")

    search_label = tk.Label(search_books_window, text=f"Enter {criteria.capitalize()}:")
    search_label.pack(pady=5)
    search_entry = tk.Entry(search_books_window)
    search_entry.pack(pady=5)
    search_button = tk.Button(search_books_window, text="Search", command=perform_search)
    search_button.pack(pady=5)

    listbox = tk.Listbox(search_books_window, width=100)
    listbox.pack(pady=20)
    
def borrow_book():
    borrow_book_window = tk.Toplevel(root)
    borrow_book_window.title("Borrow Book")

    ssn_label = tk.Label(borrow_book_window, text="Enter your SSN:")
    ssn_label.pack(pady=5)
    ssn_entry = tk.Entry(borrow_book_window)
    ssn_entry.pack(pady=5)

    id_label = tk.Label(borrow_book_window, text="Enter your ID:")
    id_label.pack(pady=5)
    id_entry = tk.Entry(borrow_book_window)
    id_entry.pack(pady=5)

    book_id_label = tk.Label(borrow_book_window, text="Enter the book ID you want to borrow:")
    book_id_label.pack(pady=5)
    book_id_entry = tk.Entry(borrow_book_window)
    book_id_entry.pack(pady=5)

    def confirm_borrow():
        ssn = ssn_entry.get()
        id = id_entry.get()
        book_id = book_id_entry.get()

        try:
            # Check if the book ID exists in the BOOK table
            book_query = "SELECT * FROM BOOK WHERE BOOK_ID = ?"
            cursor.execute(book_query, (book_id,))
            book = cursor.fetchone()

            if book:
                # Insert borrow record into the BORROW table
                borrow_query = "INSERT INTO BORROW (SSN, ID, BOOK_ID) VALUES (?, ?, ?)"
                borrow_values = (ssn, id, book_id)
                cursor.execute(borrow_query, borrow_values)
                connection.commit()
                messagebox.showinfo("Info", "Book borrowed successfully")
                borrow_book_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid book ID. Please enter a valid book ID.")
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    borrow_button = tk.Button(borrow_book_window, text="Borrow Book", command=confirm_borrow)
    borrow_button.pack(pady=10)
    
def update_user_details():
    global current_student
    # Check if a student is signed in
    if not current_student:
        messagebox.showerror("Error", "student not signed in. Please sign in as a student.")
        return

    # Get the current student's ID
    id = current_student[1]

    # Fetch the student's details from the database
    query = "SELECT * FROM STUDENT WHERE ID = ?"
    cursor.execute(query, (id,))
    user = cursor.fetchone()

    if not user:
        messagebox.showerror("Error", "User not found.")
        return

    def submit_update():
        # Get updated values from entry widgets
        updated_fname = fname_entry.get()
        updated_lname = lname_entry.get()
        updated_email = email_entry.get()
        updated_password = password_entry.get()
        updated_age = age_entry.get()
        updated_gender = gender_entry.get()

        # Construct the SQL update query
        update_query = "UPDATE STUDENT SET"
        update_values = []

        if updated_fname:
            update_query += " FNAME = ?,"
            update_values.append(updated_fname)
        if updated_lname:
            update_query += " LNAME = ?,"
            update_values.append(updated_lname)
        if updated_email:
            update_query += " EMAIL = ?,"
            update_values.append(updated_email)
        if updated_password:
            update_query += " PASSWORD = ?,"
            update_values.append(updated_password)
        if updated_age:
            update_query += " AGE = ?,"
            update_values.append(updated_age)
        if updated_gender:
            update_query += " GENDER = ?,"
            update_values.append(updated_gender)

        # Remove the trailing comma and add the WHERE clause
        update_query = update_query.rstrip(',') + " WHERE ID = ?"
        update_values.append(id)

        try:
            # Execute the update query
            cursor.execute(update_query, update_values)
            connection.commit()
            messagebox.showinfo("Info", "User details updated successfully.")
            update_user_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create a new window for the update form
    update_user_window = tk.Toplevel(root)
    update_user_window.title("Update User Details")

    # Create and place entry widgets for each field
    fname_label = tk.Label(update_user_window, text="First Name:")
    fname_label.pack(pady=5)
    fname_entry = tk.Entry(update_user_window)
    fname_entry.pack(pady=5)

    lname_label = tk.Label(update_user_window, text="Last Name:")
    lname_label.pack(pady=5)
    lname_entry = tk.Entry(update_user_window)
    lname_entry.pack(pady=5)

    email_label = tk.Label(update_user_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(update_user_window)
    email_entry.pack(pady=5)

    password_label = tk.Label(update_user_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(update_user_window)
    password_entry.pack(pady=5)

    age_label = tk.Label(update_user_window, text="Age:")
    age_label.pack(pady=5)
    age_entry = tk.Entry(update_user_window)
    age_entry.pack(pady=5)

    gender_label = tk.Label(update_user_window, text="Gender:")
    gender_label.pack(pady=5)
    gender_entry = tk.Entry(update_user_window)
    gender_entry.pack(pady=5)

    # Create a button to submit the update
    submit_button = tk.Button(update_user_window, text="Update User", command=submit_update)
    submit_button.pack(pady=10)
    
    

def display_student_options():
    student_options_window = tk.Toplevel(root)
    student_options_window.title("student Options")

    def sign_out_student():
        global current_student
        current_student = None
        messagebox.showinfo("Info", "Signed out successfully")
        student_options_window.destroy()

    tk.Label(student_options_window, text="Please select an option:", font=("Helvetica", 20)).pack(pady=20)
    tk.Button(student_options_window, text="Browse all books", command=browse_books).pack(pady=10)
    tk.Button(student_options_window, text="Search books by title", command=lambda: search_books('title')).pack(pady=10)
    tk.Button(student_options_window, text="Search books by publisher", command=lambda: search_books('publisher')).pack(pady=10)
    tk.Button(student_options_window, text="Search books by author", command=lambda: search_books('author')).pack(pady=10)
    tk.Button(student_options_window, text="Borrow book", command=borrow_book).pack(pady=10)
    tk.Button(student_options_window, text="Update account detials", command=update_user_details).pack(pady=10)
    tk.Button(student_options_window, text="Sign out", command=sign_out_student).pack(pady=10)
    

def add_book():
    add_book_window = tk.Toplevel(root)
    add_book_window.title("Add a Book")

    def submit_book():
        book_id = book_id_entry.get()
        title = title_entry.get()
        publisher = publisher_entry.get()
        year = year_entry.get()
        isbn = isbn_entry.get()

        author_id = author_id_entry.get()
        author_name = author_name_entry.get()

        category_id = category_id_entry.get()
        category_name = category_name_entry.get()

        copy_no = copy_no_entry.get()
        book_status = book_status_entry.get()

        try:
            # Insert book data
            book_query = "INSERT INTO BOOK (BOOK_ID, TITLE, PUBLISHER, PUBLICATION_DATE, ISBN) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(book_query, (book_id, title, publisher, year if year else None, isbn))

            # Insert author data
            author_query = "INSERT INTO AUTHOR (AUTHOR_ID, AUTHOR_NAME) VALUES (?, ?)"
            cursor.execute(author_query, (author_id, author_name))

            # Insert category data
            category_query = "INSERT INTO CATAGORY (CATAGORY_ID, CATAGORY_NAME) VALUES (?, ?)"
            cursor.execute(category_query, (category_id, category_name))

            # Insert relationship into BELONGS_TO table
            belongs_to_query = "INSERT INTO BELONGS_TO (BOOK_ID, CATAGORY_ID) VALUES (?, ?)"
            cursor.execute(belongs_to_query, (book_id, category_id))

            # Insert relationship into WRITE table
            write_query = "INSERT INTO WRITE (AUTHOR_ID, BOOK_ID) VALUES (?, ?)"
            cursor.execute(write_query, (author_id, book_id))

            # Insert data into COPY table
            copy_query = "INSERT INTO COPY (BOOK_ID, COPY_NO, BOOK_STATUS) VALUES (?, ?, ?)"
            cursor.execute(copy_query, (book_id, copy_no, book_status))

            connection.commit()
            messagebox.showinfo("Info", "Book, author, category, write relationship, and copy added successfully.")
            add_book_window.destroy()
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Book details
    book_id_label = tk.Label(add_book_window, text="Book ID:")
    book_id_label.pack(pady=5)
    book_id_entry = tk.Entry(add_book_window)
    book_id_entry.pack(pady=5)

    title_label = tk.Label(add_book_window, text="Title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(add_book_window)
    title_entry.pack(pady=5)

    publisher_label = tk.Label(add_book_window, text="Publisher:")
    publisher_label.pack(pady=5)
    publisher_entry = tk.Entry(add_book_window)
    publisher_entry.pack(pady=5)

    year_label = tk.Label(add_book_window, text="Publication Year:")
    year_label.pack(pady=5)
    year_entry = tk.Entry(add_book_window)
    year_entry.pack(pady=5)

    isbn_label = tk.Label(add_book_window, text="ISBN:")
    isbn_label.pack(pady=5)
    isbn_entry = tk.Entry(add_book_window)
    isbn_entry.pack(pady=5)

    # Author details
    author_id_label = tk.Label(add_book_window, text="Author ID:")
    author_id_label.pack(pady=5)
    author_id_entry = tk.Entry(add_book_window)
    author_id_entry.pack(pady=5)

    author_name_label = tk.Label(add_book_window, text="Author Name:")
    author_name_label.pack(pady=5)
    author_name_entry = tk.Entry(add_book_window)
    author_name_entry.pack(pady=5)

    # Category details
    category_id_label = tk.Label(add_book_window, text="Category ID:")
    category_id_label.pack(pady=5)
    category_id_entry = tk.Entry(add_book_window)
    category_id_entry.pack(pady=5)

    category_name_label = tk.Label(add_book_window, text="Category Name:")
    category_name_label.pack(pady=5)
    category_name_entry = tk.Entry(add_book_window)
    category_name_entry.pack(pady=5)

    # Copy details
    copy_no_label = tk.Label(add_book_window, text="Copy Number:")
    copy_no_label.pack(pady=5)
    copy_no_entry = tk.Entry(add_book_window)
    copy_no_entry.pack(pady=5)

    book_status_label = tk.Label(add_book_window, text="Book Status:")
    book_status_label.pack(pady=5)
    book_status_entry = tk.Entry(add_book_window)
    book_status_entry.pack(pady=5)

    submit_button = tk.Button(add_book_window, text="Add Book", command=submit_book)
    submit_button.pack(pady=10)
    
def update_book():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        print("Admin not signed in. Please sign in as an admin.")
        return

    update_book_window = tk.Toplevel(root)
    update_book_window.title("Update Book")

    def submit_update():
        # Get updated values from entry widgets
        book_id = book_id_entry.get()

        updated_title = title_entry.get()
        updated_publisher = publisher_entry.get()
        updated_publication_date = publication_date_entry.get()
        updated_isbn = isbn_entry.get()

        updated_author_id = author_id_entry.get()
        updated_author_name = author_name_entry.get()

        updated_category_id = category_id_entry.get()
        updated_category_name = category_name_entry.get()

        updated_copy_no = copy_no_entry.get()
        updated_book_status = book_status_entry.get()

        try:
            # Update book details
            if updated_title or updated_publisher or updated_publication_date or updated_isbn:
                update_query = "UPDATE BOOK SET"
                update_values = []

                if updated_title:
                    update_query += " TITLE = ?,"
                    update_values.append(updated_title)
                if updated_publisher:
                    update_query += " PUBLISHER = ?,"
                    update_values.append(updated_publisher)
                if updated_publication_date:
                    update_query += " PUBLICATION_DATE = ?,"
                    update_values.append(updated_publication_date)
                if updated_isbn:
                    update_query += " ISBN = ?,"
                    update_values.append(updated_isbn)

                update_query = update_query.rstrip(',')
                update_query += " WHERE BOOK_ID = ?"
                update_values.append(book_id)

                cursor.execute(update_query, update_values)

            # Update author details
            if updated_author_id and updated_author_name:
                author_query = "UPDATE AUTHOR SET AUTHOR_NAME = ? WHERE AUTHOR_ID = ?"
                cursor.execute(author_query, (updated_author_name, updated_author_id))
            
            # Update category details
            if updated_category_id and updated_category_name:
                category_query = "UPDATE CATAGORY SET CATAGORY_NAME = ? WHERE CATAGORY_ID = ?"
                cursor.execute(category_query, (updated_category_name, updated_category_id))
            
            # Update copy details
            if updated_copy_no and updated_book_status:
                copy_query = "UPDATE COPY SET COPY_NO = ?, BOOK_STATUS = ? WHERE BOOK_ID = ?"
                cursor.execute(copy_query, (updated_copy_no, updated_book_status, book_id))

            connection.commit()
            messagebox.showinfo("Info", "Book, author, category, and copy details updated successfully.")
            update_book_window.destroy()
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create entry fields for book details
    book_id_label = tk.Label(update_book_window, text="Book ID:")
    book_id_label.pack(pady=5)
    book_id_entry = tk.Entry(update_book_window)
    book_id_entry.pack(pady=5)

    title_label = tk.Label(update_book_window, text="Title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(update_book_window)
    title_entry.pack(pady=5)

    publisher_label = tk.Label(update_book_window, text="Publisher:")
    publisher_label.pack(pady=5)
    publisher_entry = tk.Entry(update_book_window)
    publisher_entry.pack(pady=5)

    publication_date_label = tk.Label(update_book_window, text="Publication Date:")
    publication_date_label.pack(pady=5)
    publication_date_entry = tk.Entry(update_book_window)
    publication_date_entry.pack(pady=5)

    isbn_label = tk.Label(update_book_window, text="ISBN:")
    isbn_label.pack(pady=5)
    isbn_entry = tk.Entry(update_book_window)
    isbn_entry.pack(pady=5)

    # Create entry fields for author details
    author_id_label = tk.Label(update_book_window, text="Author ID:")
    author_id_label.pack(pady=5)
    author_id_entry = tk.Entry(update_book_window)
    author_id_entry.pack(pady=5)

    author_name_label = tk.Label(update_book_window, text="Author Name:")
    author_name_label.pack(pady=5)
    author_name_entry = tk.Entry(update_book_window)
    author_name_entry.pack(pady=5)

    # Create entry fields for category details
    category_id_label = tk.Label(update_book_window, text="Category ID:")
    category_id_label.pack(pady=5)
    category_id_entry = tk.Entry(update_book_window)
    category_id_entry.pack(pady=5)

    category_name_label = tk.Label(update_book_window, text="Category Name:")
    category_name_label.pack(pady=5)
    category_name_entry = tk.Entry(update_book_window)
    category_name_entry.pack(pady=5)

    # Create entry fields for copy details
    copy_no_label = tk.Label(update_book_window, text="Copy Number:")
    copy_no_label.pack(pady=5)
    copy_no_entry = tk.Entry(update_book_window)
    copy_no_entry.pack(pady=5)

    book_status_label = tk.Label(update_book_window, text="Book Status:")
    book_status_label.pack(pady=5)
    book_status_entry = tk.Entry(update_book_window)
    book_status_entry.pack(pady=5)

    # Create a button to submit the update
    submit_button = tk.Button(update_book_window, text="Update Book", command=submit_update)
    submit_button.pack(pady=10)


def delete_book():
    delete_book_window = tk.Toplevel(root)
    delete_book_window.title("Delete Book")

    # Fetch all books from the database
    query = "SELECT BOOK_ID, TITLE, ISBN FROM BOOK"
    cursor.execute(query)
    books = cursor.fetchall()

    # Create a listbox to display the books
    listbox = tk.Listbox(delete_book_window, selectmode=tk.SINGLE)
    for book in books:
        listbox.insert(tk.END, f"{book[0]} - {book[1]} - ISBN: {book[2]}")
    listbox.pack(pady=10)

    def confirm_delete():
        # Get the selected book ID from the listbox
        selected_index = listbox.curselection()
        if selected_index:
            selected_book_id = books[selected_index[0]][0]
            try:
                # Delete the selected book from the database
                book_query = "DELETE FROM BOOK WHERE BOOK_ID = ?"
                cursor.execute(book_query, (selected_book_id,))
                
                author_query = "DELETE FROM AUTHOR WHERE AUTHOR_ID IN (SELECT AUTHOR_ID FROM WRITE WHERE BOOK_ID = ?)"
                cursor.execute(author_query, (selected_book_id,))
                
                copy_query = "DELETE FROM COPY WHERE BOOK_ID = ?"
                cursor.execute(copy_query, (selected_book_id,))
                
                connection.commit()
                messagebox.showinfo("Info", "Book and associated data deleted successfully")
                delete_book_window.destroy()
            except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please select a book to delete.")

    # Create a button to confirm deletion
    delete_button = tk.Button(delete_book_window, text="Delete Book", command=confirm_delete)
    delete_button.pack(pady=10)

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


def delete_student():
    delete_student_window = tk.Toplevel(root)
    delete_student_window.title("Delete Student")

    # Fetch all students from the database
    query = "SELECT SSN, FNAME, LNAME FROM STUDENT"
    cursor.execute(query)
    students = cursor.fetchall()

    # Create a listbox to display the students
    listbox = tk.Listbox(delete_student_window, selectmode=tk.SINGLE)
    for student in students:
        listbox.insert(tk.END, f"{student[0]} - {student[1]} {student[2]}")
    listbox.pack(pady=10)

    def confirm_delete():
        # Get the selected student's SSN from the listbox
        selected_index = listbox.curselection()
        if selected_index:
            selected_ssn = students[selected_index[0]][0]
            try:
                # Delete the selected student from the database
                query = "DELETE FROM STUDENT WHERE SSN = ?"
                cursor.execute(query, (selected_ssn,))
                connection.commit()
                messagebox.showinfo("Info", "Student deleted successfully")
                delete_student_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Error", "Please select a student to delete.")

    # Create a button to confirm deletion
    delete_button = tk.Button(delete_student_window, text="Delete Student", command=confirm_delete)
    delete_button.pack(pady=10)
    
def update_user_details_by_admin():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        messagebox.showerror("Error", "Admin not signed in. Please sign in as an admin.")
        return

    def submit_update():
        # Get user ID and updated values from entry widgets
        user_id = id_entry.get()
        updated_ssn = ssn_entry.get()
        updated_id = new_id_entry.get()
        updated_fname = fname_entry.get()
        updated_lname = lname_entry.get()
        updated_email = email_entry.get()
        updated_password = password_entry.get()
        updated_age = age_entry.get()
        updated_gender = gender_entry.get()

        # Construct the SQL update query
        update_query = "UPDATE STUDENT SET"
        update_values = []

        if updated_ssn:
            update_query += " SSN = ?,"
            update_values.append(updated_ssn)
        if updated_id:
            update_query += " ID = ?,"
            update_values.append(updated_id)
        if updated_fname:
            update_query += " FNAME = ?,"
            update_values.append(updated_fname)
        if updated_lname:
            update_query += " LNAME = ?,"
            update_values.append(updated_lname)
        if updated_email:
            update_query += " EMAIL = ?,"
            update_values.append(updated_email)
        if updated_password:
            update_query += " PASSWORD = ?,"
            update_values.append(updated_password)
        if updated_age:
            update_query += " AGE = ?,"
            update_values.append(updated_age)
        if updated_gender:
            update_query += " GENDER = ?,"
            update_values.append(updated_gender)

        # Remove the trailing comma and add the WHERE clause
        update_query = update_query.rstrip(',') + " WHERE ID = ?"
        update_values.append(user_id)

        try:
            # Execute the update query
            cursor.execute(update_query, update_values)
            connection.commit()
            messagebox.showinfo("Info", "User details updated successfully.")
            update_user_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create a new window for the update form
    update_user_window = tk.Toplevel(root)
    update_user_window.title("Update User Details")

    # Create and place entry widgets for each field
    id_label = tk.Label(update_user_window, text="User ID:")
    id_label.pack(pady=5)
    id_entry = tk.Entry(update_user_window)
    id_entry.pack(pady=5)

    ssn_label = tk.Label(update_user_window, text="New SSN (press Enter to skip):")
    ssn_label.pack(pady=5)
    ssn_entry = tk.Entry(update_user_window)
    ssn_entry.pack(pady=5)

    new_id_label = tk.Label(update_user_window, text="New ID (press Enter to skip):")
    new_id_label.pack(pady=5)
    new_id_entry = tk.Entry(update_user_window)
    new_id_entry.pack(pady=5)

    fname_label = tk.Label(update_user_window, text="New First Name (press Enter to skip):")
    fname_label.pack(pady=5)
    fname_entry = tk.Entry(update_user_window)
    fname_entry.pack(pady=5)

    lname_label = tk.Label(update_user_window, text="New Last Name (press Enter to skip):")
    lname_label.pack(pady=5)
    lname_entry = tk.Entry(update_user_window)
    lname_entry.pack(pady=5)

    email_label = tk.Label(update_user_window, text="New Email (press Enter to skip):")
    email_label.pack(pady=5)
    email_entry = tk.Entry(update_user_window)
    email_entry.pack(pady=5)

    password_label = tk.Label(update_user_window, text="New Password (press Enter to skip):")
    password_label.pack(pady=5)
    password_entry = tk.Entry(update_user_window)
    password_entry.pack(pady=5)

    age_label = tk.Label(update_user_window, text="New Age (press Enter to skip):")
    age_label.pack(pady=5)
    age_entry = tk.Entry(update_user_window)
    age_entry.pack(pady=5)

    gender_label = tk.Label(update_user_window, text="New Gender (press Enter to skip):")
    gender_label.pack(pady=5)
    gender_entry = tk.Entry(update_user_window)
    gender_entry.pack(pady=5)

    # Create a button to submit the update
    submit_button = tk.Button(update_user_window, text="Update User", command=submit_update)
    submit_button.pack(pady=10)

def update_admin_details():
    global current_admin
    # Check if an admin is signed in
    if not current_admin:
        messagebox.showerror("Error", "Admin not signed in. Please sign in as an admin.")
        return

    def submit_update():
        # Get updated values from entry widgets
        updated_name = name_entry.get()
        updated_password = password_entry.get()
        updated_email = email_entry.get()
        updated_address = address_entry.get()
        updated_gender = gender_entry.get()
        updated_age = age_entry.get()

        # Construct the SQL update query
        update_query = "UPDATE ADMIN SET"
        update_values = []

        if updated_name:
            update_query += " ADMIN_NAME = ?,"
            update_values.append(updated_name)
        if updated_password:
            update_query += " PASSWORD = ?,"
            update_values.append(updated_password)
        if updated_email:
            update_query += " EMAIL = ?,"
            update_values.append(updated_email)
        if updated_address:
            update_query += " ADDRESS = ?,"
            update_values.append(updated_address)
        if updated_gender:
            update_query += " GENDER = ?,"
            update_values.append(updated_gender)
        if updated_age:
            update_query += " ADMIN_AGE = ?,"
            update_values.append(updated_age)

        # Remove the trailing comma and add the WHERE clause
        update_query = update_query.rstrip(',') + " WHERE ADMIN_ID = ?"
        update_values.append(current_admin[0])

        try:
            # Execute the update query
            cursor.execute(update_query, update_values)
            connection.commit()
            messagebox.showinfo("Info", "Admin details updated successfully.")
            update_admin_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create a new window for the update form
    update_admin_window = tk.Toplevel(root)
    update_admin_window.title("Update Admin Details")

    # Create and place entry widgets for each field
    name_label = tk.Label(update_admin_window, text="Name:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(update_admin_window)
    name_entry.pack(pady=5)
    name_entry.insert(0, current_admin[1])

    password_label = tk.Label(update_admin_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(update_admin_window)
    password_entry.pack(pady=5)

    email_label = tk.Label(update_admin_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(update_admin_window)
    email_entry.pack(pady=5)
    email_entry.insert(0, current_admin[3])

    address_label = tk.Label(update_admin_window, text="Address:")
    address_label.pack(pady=5)
    address_entry = tk.Entry(update_admin_window)
    address_entry.pack(pady=5)
    address_entry.insert(0, current_admin[4])

    gender_label = tk.Label(update_admin_window, text="Gender:")
    gender_label.pack(pady=5)
    gender_entry = tk.Entry(update_admin_window)
    gender_entry.pack(pady=5)
    gender_entry.insert(0, current_admin[5])

    age_label = tk.Label(update_admin_window, text="Age:")
    age_label.pack(pady=5)
    age_entry = tk.Entry(update_admin_window)
    age_entry.pack(pady=5)
    age_entry.insert(0, current_admin[6])

    # Create a button to submit the update
    submit_button = tk.Button(update_admin_window, text="Update Admin", command=submit_update)
    submit_button.pack(pady=10)
def generate_report():
    report_window = tk.Toplevel(root)
    report_window.title("Last 10 Books Added by Publisher")

    query = """
    SELECT TOP 10 B.TITLE, B.PUBLISHER, B.PUBLICATION_DATE, B.ISBN, A.AUTHOR_ID, A.AUTHOR_NAME
    FROM BOOK B
    JOIN WRITE W ON B.BOOK_ID = W.BOOK_ID
    JOIN AUTHOR A ON W.AUTHOR_ID = A.AUTHOR_ID
    ORDER BY B.PUBLICATION_DATE DESC
    """
    try:
        cursor.execute(query)
        books = cursor.fetchall()

        listbox = tk.Listbox(report_window, width=120)
        listbox.pack(pady=20)

        for book in books:
            title = book[0]
            publisher = book[1]
            publication_date = book[2] if book[2] else "N/A"
            isbn = book[3]
            author_id = book[4]
            author_name = book[5]
            listbox.insert(tk.END, f"Title: {title}, Publisher: {publisher}, Publication Date: {publication_date}, ISBN: {isbn}, Author ID: {author_id}, Author Name: {author_name}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    
def display_admin_options():
    admin_options_window = tk.Toplevel(root)
    admin_options_window.title("Admin Options")    


    def sign_out_admin():
        global current_admin
        current_admin = None
        messagebox.showinfo("Info", "Signed out successfully")
        admin_options_window.destroy()

    tk.Label(admin_options_window, text="Please select an option:", font=("Helvetica", 20)).pack(pady=20)
    tk.Button(admin_options_window, text="Add a book", command=add_book).pack(pady=15)
    tk.Button(admin_options_window, text="Update a book", command=update_book).pack(pady=15)
    tk.Button(admin_options_window, text="Delete a book", command=delete_book).pack(pady=15)
    tk.Button(admin_options_window, text="Delete a student account", command=delete_student).pack(pady=15)
    tk.Button(admin_options_window, text="Browse all books", command=browse_books).pack(pady=10)
    tk.Button(admin_options_window, text="Search books by title", command=lambda: search_books('title')).pack(pady=15)
    tk.Button(admin_options_window, text="Search books by publisher", command=lambda: search_books('publisher')).pack(pady=15)
    tk.Button(admin_options_window, text="Search books by author", command=lambda: search_books('author')).pack(pady=15)
    tk.Button(admin_options_window, text="Update Admin account", command=update_admin_details).pack(pady=10)
    tk.Button(admin_options_window, text="Update Student account", command=update_user_details_by_admin).pack(pady=10)
    tk.Button(admin_options_window, text="Generate Report", command=generate_report).pack(pady=10)
    tk.Button(admin_options_window, text="Sign out", command=sign_out_admin).pack(pady=10)


def student_sign_in():
    # Create a new window for student sign-in
    student_sign_in_window = tk.Toplevel(root)
    student_sign_in_window.title("Student Sign In")

    def validate_student():
        # Get the input values from the entry widgets
        email = email_entry.get()
        password = password_entry.get()

        try:
            # Validate the credentials using the sign_in_student() function
            if sign_in_student(email, password):
                messagebox.showinfo("Info", "Sign-in successful")
                student_sign_in_window.destroy()
                display_student_options()
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create labels and entry widgets for email and password
    email_label = tk.Label(student_sign_in_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(student_sign_in_window)
    email_entry.pack(pady=5)

    password_label = tk.Label(student_sign_in_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(student_sign_in_window, show="*")
    password_entry.pack(pady=5)

    # Create a button to validate the credentials
    sign_in_button = tk.Button(student_sign_in_window, text="Sign In", command=validate_student)
    sign_in_button.pack(pady=10)

def admin_sign_in():
    # Create a new window for admin sign-in
    admin_sign_in_window = tk.Toplevel(root)
    admin_sign_in_window.title("Admin Sign In")

    def validate_admin():
        # Get the input values from the entry widgets
        email = email_entry.get()
        password = password_entry.get()

        try:
            # Validate the credentials using sign_in_admin() function
            if sign_in_admin(email, password):
                messagebox.showinfo("Info", "Sign-in successful")
                admin_sign_in_window.destroy()
                display_admin_options()
            else:
                messagebox.showerror("Error", "Invalid email or password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create labels and entry widgets for email and password
    email_label = tk.Label(admin_sign_in_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(admin_sign_in_window)
    email_entry.pack(pady=5)

    password_label = tk.Label(admin_sign_in_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(admin_sign_in_window, show="*")
    password_entry.pack(pady=5)

    # Create a button to validate the credentials
    sign_in_button = tk.Button(admin_sign_in_window, text="Sign In", command=validate_admin)
    sign_in_button.pack(pady=10)


def student_sign_up():
    # Create a new window for student sign-up
    student_sign_up_window = tk.Toplevel(root)
    student_sign_up_window.title("Student Sign Up")

    def register_student():
        # Get the input values from the entry widgets
        ssn = ssn_entry.get()
        student_id = id_entry.get()
        fname = fname_entry.get()
        lname = lname_entry.get()
        gender = gender_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        age = age_entry.get()

        try:
            # Register the student using the sign_up_student() function
            sign_up_student(ssn, student_id, fname, lname, gender, email, password, age, cursor, connection)
            messagebox.showinfo("Info", "Student signed up successfully")
            student_sign_up_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create labels and entry widgets for student details
    ssn_label = tk.Label(student_sign_up_window, text="SSN:")
    ssn_label.pack(pady=5)
    ssn_entry = tk.Entry(student_sign_up_window)
    ssn_entry.pack(pady=5)

    id_label = tk.Label(student_sign_up_window, text="ID:")
    id_label.pack(pady=5)
    id_entry = tk.Entry(student_sign_up_window)
    id_entry.pack(pady=5)

    fname_label = tk.Label(student_sign_up_window, text="First Name:")
    fname_label.pack(pady=5)
    fname_entry = tk.Entry(student_sign_up_window)
    fname_entry.pack(pady=5)

    lname_label = tk.Label(student_sign_up_window, text="Last Name:")
    lname_label.pack(pady=5)
    lname_entry = tk.Entry(student_sign_up_window)
    lname_entry.pack(pady=5)

    gender_label = tk.Label(student_sign_up_window, text="Gender:")
    gender_label.pack(pady=5)
    gender_entry = tk.Entry(student_sign_up_window)
    gender_entry.pack(pady=5)

    email_label = tk.Label(student_sign_up_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(student_sign_up_window)
    email_entry.pack(pady=5)

    password_label = tk.Label(student_sign_up_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(student_sign_up_window, show="*")
    password_entry.pack(pady=5)

    age_label = tk.Label(student_sign_up_window, text="Age:")
    age_label.pack(pady=5)
    age_entry = tk.Entry(student_sign_up_window)
    age_entry.pack(pady=5)

    # Create a button to register the student
    sign_up_button = tk.Button(student_sign_up_window, text="Sign Up", command=register_student)
    sign_up_button.pack(pady=10)

def admin_sign_up():
    # Create a new window for admin sign-up
    admin_sign_up_window = tk.Toplevel(root)
    admin_sign_up_window.title("Admin Sign Up")

    def register_admin():
        # Get the input values from the entry widgets
        admin_id = admin_id_entry.get()
        admin_name = admin_name_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        address = address_entry.get()
        gender = gender_entry.get()
        admin_age = admin_age_entry.get()

        try:
            # Register the admin using the sign_up_admin() function
            sign_up_admin(admin_id, admin_name, password, email, address, gender, admin_age, cursor, connection)
            messagebox.showinfo("Info", "Admin signed up successfully")
            admin_sign_up_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create labels and entry widgets for admin details
    admin_id_label = tk.Label(admin_sign_up_window, text="Admin ID:")
    admin_id_label.pack(pady=5)
    admin_id_entry = tk.Entry(admin_sign_up_window)
    admin_id_entry.pack(pady=5)

    admin_name_label = tk.Label(admin_sign_up_window, text="Admin Name:")
    admin_name_label.pack(pady=5)
    admin_name_entry = tk.Entry(admin_sign_up_window)
    admin_name_entry.pack(pady=5)

    password_label = tk.Label(admin_sign_up_window, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(admin_sign_up_window, show="*")
    password_entry.pack(pady=5)

    email_label = tk.Label(admin_sign_up_window, text="Email:")
    email_label.pack(pady=5)
    email_entry = tk.Entry(admin_sign_up_window)
    email_entry.pack(pady=5)

    address_label = tk.Label(admin_sign_up_window, text="Address:")
    address_label.pack(pady=5)
    address_entry = tk.Entry(admin_sign_up_window)
    address_entry.pack(pady=5)

    gender_label = tk.Label(admin_sign_up_window, text="Gender:")
    gender_label.pack(pady=5)
    gender_entry = tk.Entry(admin_sign_up_window)
    gender_entry.pack(pady=5)

    admin_age_label = tk.Label(admin_sign_up_window, text="Age:")
    admin_age_label.pack(pady=5)
    admin_age_entry = tk.Entry(admin_sign_up_window)
    admin_age_entry.pack(pady=5)

    # Create a button to register the admin
    sign_up_button = tk.Button(admin_sign_up_window, text="Sign Up", command=register_admin)
    sign_up_button.pack(pady=10)

def sign_in():
    # Create a new window for sign-in
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")

    student_sign_in_button = tk.Button(sign_in_window, text="student Sign In", command=student_sign_in)
    student_sign_in_button.pack(pady=10)

    admin_sign_in_button = tk.Button(sign_in_window, text="Admin Sign In", command=admin_sign_in)
    admin_sign_in_button.pack(pady=10)

def sign_up():
    # Create a new window for sign-up
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")

    student_sign_up_button = tk.Button(sign_up_window, text="student Sign Up", command=student_sign_up)
    student_sign_up_button.pack(pady=10)

    admin_sign_up_button = tk.Button(sign_up_window, text="Admin Sign Up", command=admin_sign_up)
    admin_sign_up_button.pack(pady=10)

# Create the main application window
root = tk.Tk()
root.title("Book Database Application")

# Welcome text
welcome_label = tk.Label(root, text="Welcome to the Book Database Application", font=("Script", 40))
welcome_label.pack(pady=20)


# Buttons for sign-in and sign-up
sign_in_button = tk.Button(root, text="Sign In", command=sign_in)
sign_in_button.pack(pady=10)

sign_up_button = tk.Button(root, text="Sign Up", command=sign_up)
sign_up_button.pack(pady=10)

# Run the application
root.mainloop()
