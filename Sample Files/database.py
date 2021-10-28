import tkinter as tk 
from tkinter import *
from PIL import ImageTk, Image
import sqlite3
root = tk.Tk()
root.title("Checkboxes")
root.iconbitmap('D:/Github Repositories/Laptop-PC-Sync/EsbenSchoolFiles/HTHS CSE/Python/TKInter/Images/codemy.ico')
root.geometry("400x400")

#Create a database or connect to one
conn = sqlite3.connect("address_book.db")

#Create cursor instance
c = conn.cursor()





#Creating Tables
'''
c.execute("""CREATE TABLE addresses (
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zip_code integer)""")
'''
#Creating text entry boxes
f_name = tk.Entry(root, width = 30)
f_name.grid(row = 0, column = 0, padx = 20, pady = (10, 0))
l_name = tk.Entry(root, width = 30)
l_name.grid(row = 1, column = 0, padx = 20)
address = tk.Entry(root, width = 30)
address.grid(row = 2, column = 0, padx = 20)
city = tk.Entry(root, width = 30)
city.grid(row = 3, column = 0, padx = 20)
state = tk.Entry(root, width = 30)
state.grid(row = 4, column = 0, padx = 20)
zip_code = tk.Entry(root, width = 30)
zip_code.grid(row = 5, column = 0, padx = 20)

delete_box = tk.Entry(root, width = 30)
delete_box.grid(row = 9, column = 0)

#Text Box Labels
f_name_label = tk.Label(root, text = "First Name")
f_name_label.grid(row = 0, column = 1)
l_name_label = tk.Label(root, text = "Last Name")
l_name_label.grid(row = 1, column = 1)
address_label = tk.Label(root, text = "Address")
address_label.grid(row = 2, column = 1)
city_label = tk.Label(root, text = "City")
city_label.grid(row = 3, column = 1)
state_label = tk.Label(root, text = "State")
state_label.grid(row = 4, column = 1)
zip_label = tk.Label(root, text = "Zip Code")
zip_label.grid(row = 5, column = 1)

delete_label = tk.Label(root, text = "Select OID Number")
delete_label.grid(row = 9, column = 1)

#Submission function
def submit():
    #Create new cursor and database connection
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    #Insert information into database
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zip_code)", 
            {
                'f_name': f_name.get(),
                'l_name': l_name.get(), 
                'address': address.get(),
                'city': city.get(),
                'state': state.get(), 
                'zip_code': zip_code.get()
            })

    #Committing changes
    conn.commit()
    conn.close()

    #Clear the textboxes
    f_name.delete(0, 'end')
    l_name.delete(0, 'end')
    address.delete(0, 'end')
    state.delete(0, 'end')
    city.delete(0, 'end')
    zip_code.delete(0, 'end')

#Query Function
def query():
    #Create new cursor and database connection
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    #Query Database
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()
    # print(records)

    #Loop through results
    print_records = ''
    for record in records:
        # for subrecord in record:
            # print_records += str(subrecord) + "\n"
        print_records += str(record[0]) + " " + str(record[1]) + "\t" + str(record[6]) + "\n"

    query_label = tk.Label(root, text = print_records)
    query_label.grid(row = 12, column = 0, columnspan = 2)

    #Committing changes to database
    conn.commit()
    #Closing database
    conn.close()

#Delete Function
def delete():
    #Create new cursor and database connection
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    #Delete information from database
    c.execute("DELETE FROM addresses WHERE oid="+delete_box.get())

    #Committing changes and closing
    conn.commit()
    conn.close()

#Update Function
def update():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute(""" UPDATE addresses SET 
        first_name = :f_name, 
        last_name = :l_name, 
        address = :address, 
        city = :city,
        state = :state, 
        zip_code = :zip_code

        WHERE oid = :oid""", 
        {
            'f_name': f_name_editor.get(), 
            'l_name': l_name_editor.get(), 
            'address': address_editor.get(), 
            'city': city_editor.get(), 
            'state': state_editor.get(), 
            'zip_code': zip_code_editor.get(), 
            'oid': record_id
        })

    #Commit changes and close database
    conn.commit()
    conn.close()

    editor.destroy()

#Edit function
def edit():
    global editor
    editor = tk.Tk()
    editor.title("Update A Record")
    editor.iconbitmap("D:/Github Repositories/Laptop-PC-Sync/EsbenSchoolFiles/HTHS CSE/Python/TKInter/Images/codemy.ico")
    editor.geometry("400x400")

    #Connect to the database
    conn = sqlite3.connect('address_book.db')
    #Create cursor
    c = conn.cursor()

    record_id = delete_box.get()
    #Querying database
    c.execute("SELECT * FROM addresses WHERE oid=" + str(record_id))
    records = c.fetchall()

    #Creating global variables for text box names
    global f_name_editor
    global l_name_editor
    global address_editor
    global city_editor
    global state_editor
    global zip_code_editor

    #Creating text entry boxes
    f_name_editor = tk.Entry(editor, width = 30)
    f_name_editor.grid(row = 0, column = 0, padx = 20, pady = (10, 0))
    l_name_editor = tk.Entry(editor, width = 30)
    l_name_editor.grid(row = 1, column = 0, padx = 20)
    address_editor = tk.Entry(editor, width = 30)
    address_editor.grid(row = 2, column = 0, padx = 20)
    city_editor = tk.Entry(editor, width = 30)
    city_editor.grid(row = 3, column = 0, padx = 20)
    state_editor = tk.Entry(editor, width = 30)
    state_editor.grid(row = 4, column = 0, padx = 20)
    zip_code_editor = tk.Entry(editor, width = 30)
    zip_code_editor.grid(row = 5, column = 0, padx = 20)

    #Autofilling entry boxes
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zip_code_editor.insert(0, record[5])

    #Text Box Labels
    f_name_label_editor = tk.Label(editor, text = "First Name")
    f_name_label_editor.grid(row = 0, column = 1)
    l_name_label_editor = tk.Label(editor, text = "Last Name")
    l_name_label_editor.grid(row = 1, column = 1)
    address_label_editor = tk.Label(editor, text = "Address")
    address_label_editor.grid(row = 2, column = 1)
    city_label_editor = tk.Label(editor, text = "City")
    city_label_editor.grid(row = 3, column = 1)
    state_label_editor = tk.Label(editor, text = "State")
    state_label_editor.grid(row = 4, column = 1)
    zip_label_editor = tk.Label(editor, text = "Zip Code")
    zip_label_editor.grid(row = 5, column = 1)


    save_btn = tk.Button(editor, text = "Save Record", command = update)
    save_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 145)

    #Committing and closing database changes
    conn.commit()
    conn.close()

#Submit Button
submit = tk.Button(root, text = "Add Record to Database", command = submit)
submit.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10, ipadx = 100)

#Fetch Button
fetch = tk.Button(root, text = "Show Records", command = query)
fetch.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 128)

#Delete Button
delete_btn = tk.Button(root, text = "Delete Record", command = delete)
delete_btn.grid(row = 10, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 128)

#Create an Update Button
update_btn = tk.Button(root, text = "Edit Record", command = edit)
update_btn.grid(row = 11, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 125)

#Commit Changes
conn.commit()

#Close Connection
conn.close()


root.mainloop()