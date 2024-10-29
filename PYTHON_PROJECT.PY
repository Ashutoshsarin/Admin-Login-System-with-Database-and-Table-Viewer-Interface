from tkinter import *
from tkinter import messagebox, simpledialog
import mysql.connector

def submit():
    username = e1.get()
    email = e2.get() 
    insert_data(username, email)
    messagebox.showinfo("submit", "Submit Successful!")

def insert_data(username, email):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="omenHP@199",
            database="login_db"
        )
        my_cursor = conn.cursor()
        sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
        values = (username, email)
        my_cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Database", "Data Inserted Successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            my_cursor.close()
            conn.close()

def reset_fields():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)

def show_all_databases():
    admin_password = simpledialog.askstring("Admin Access", "Enter Admin Password:", show="*")
    if admin_password == "123456":  # Replace with actual admin password
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="omenHP@199"
            )
            my_cursor = conn.cursor()
            my_cursor.execute("SHOW DATABASES")
            databases = my_cursor.fetchall()
            db_list = [db[0] for db in databases]
            if db_list:
                selected_db = simpledialog.askstring("Select Database", f"Available Databases:\n{', '.join(db_list)}\n\nEnter the database name to view tables:")
                if selected_db and selected_db in db_list:
                    show_tables(selected_db)
                else:
                    messagebox.showerror("Database Selection", "Invalid or No Database Selected")
            else:
                messagebox.showinfo("Databases", "No databases found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            if conn.is_connected():
                my_cursor.close()
                conn.close()
    else:
        messagebox.showerror("Admin Access", "Incorrect Admin Password")

def show_tables(selected_db):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="omenHP@199",
            database=selected_db
        )
        my_cursor = conn.cursor()
        my_cursor.execute("SHOW TABLES")
        tables = my_cursor.fetchall()
        table_list = [table[0] for table in tables]
        if table_list:
            selected_table = simpledialog.askstring("Select Table", f"Tables in '{selected_db}':\n{', '.join(table_list)}\n\nEnter the table name to view its contents:")
            if selected_table and selected_table in table_list:
                show_table_contents(selected_db, selected_table)
            else:
                messagebox.showerror("Table Selection", "Invalid or No Table Selected")
        else:
            messagebox.showinfo("Tables", f"No tables found in database '{selected_db}'.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            my_cursor.close()
            conn.close()

def show_table_contents(selected_db, selected_table):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="omenHP@199",
            database=selected_db
        )
        my_cursor = conn.cursor()
        my_cursor.execute(f"SELECT * FROM {selected_table}")
        rows = my_cursor.fetchall()
        columns = [i[0] for i in my_cursor.description]  # Get column names
        
        if rows:
            table_data = "\n".join([str(dict(zip(columns, row))) for row in rows])
            messagebox.showinfo(f"Contents of Table '{selected_table}'", f"Table Contents:\n\n{table_data}")
        else:
            messagebox.showinfo(f"Contents of Table '{selected_table}'", "The table is empty.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            my_cursor.close()
            conn.close()

# GUI Setup
top = Tk()
top.geometry("400x300")
top.config(bg="black")
top.title("Login System")

name = Label(top, text="Name", bg="red", fg="white")
name.place(x=30, y=50)

email = Label(top, text="Email", bg="red", fg="white")
email.place(x=30, y=90)

password = Label(top, text="Password", bg="red", fg="white")
password.place(x=30, y=130)

e1 = Entry(top)
e1.place(x=105, y=50)

e2 = Entry(top)
e2.place(x=105, y=90)

e3 = Entry(top, show="*")
e3.place(x=105, y=130)

reset_btn = Button(top, text="Reset", command=reset_fields, bg="red", fg="white")
reset_btn.place(x=150, y=180)

submit_btn = Button(top, text="Submit",command=submit, bg="red", fg="white")
submit_btn.place(x=60, y=180)

admin_btn = Button(top, text="Show All Databases", command=show_all_databases, bg="red", fg="white")
admin_btn.place(x=240, y=180)

top.mainloop()
