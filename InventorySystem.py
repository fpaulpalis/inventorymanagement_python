import sqlite3
import csv
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

from PIL.ImageTk import PhotoImage

root = Tk()
root.title("Inventory Management System")
root.geometry("1080x620")
my_tree = ttk.Treeview(root)
leftColumn = "ADD TO DATABASE"
rightColumn = "ITEM LISTS"

idpic = (Image.open('images/id.png'))
resized_id = idpic.resize((80, 70))
new_idimage: PhotoImage = ImageTk.PhotoImage(resized_id)

namepic = (Image.open('images/name.png'))
resized_namepic = namepic.resize((80, 70))
new_namepic = ImageTk.PhotoImage(resized_namepic)

quantitypic = (Image.open('images/quantity.png'))
resized_quantitypic = quantitypic.resize((60, 50))
new_quantitypic = ImageTk.PhotoImage(resized_quantitypic)

pricepic = (Image.open('images/price.png'))
resized_pricepic = pricepic.resize((60, 50))
new_pricepic = ImageTk.PhotoImage(resized_pricepic)
entrysearch = None


def reverse(tuples):
    new_tup = tuples[::-1]
    return new_tup


def insert(itemId, name, price, quantity):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(
            itemId INTEGER NOT NULL,
            itemName TEXT,
            itemPrice MONEY NOT NULL,
            itemQuantity INTEGER NOT NULL
        )""")

    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?, ?)", (int(itemId), str(name), float(price), int(quantity)))
    conn.commit()


def delete(data):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(
            itemId INTEGER NOT NULL,
            itemName TEXT,
            itemPrice MONEY NOT NULL,
            itemQuantity INTEGER NOT NULL
        )""")

    cursor.execute("DELETE FROM inventory WHERE itemId = ?", (str(data),))
    conn.commit()


def update(id, name, price, quantity, idName):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(
            itemId INTEGER NOT NULL,
            itemName TEXT,
            itemPrice MONEY NOT NULL,
            itemQuantity INTEGER NOT NULL
        )""")

    cursor.execute(
        "UPDATE inventory SET itemId = ?, itemName = ?, itemPrice = ?, itemQuantity = ? WHERE itemId=?", (
            int(id), str(name), float(price), int(quantity), str(idName)))
    conn.commit()


def read():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS 
        inventory(
            itemId INTEGER NOT NULL,
            itemName TEXT,
            itemPrice MONEY NOT NULL,
            itemQuantity INTEGER NOT NULL
        )""")

    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    conn.commit()
    return results


# Button Functions
def clear_data():
    entryId.delete(0, END)
    entryName.delete(0, END)
    entryPrice.delete(0, END)
    entryQuantity.delete(0, END)

def export_data():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        sql = "SELECT itemId, itemName, itemPrice, itemQuantity FROM inventory ORDER BY itemId DESC"
        cursor.execute(sql)
        dataraw = cursor.fetchall()

        date = str(datetime.now())
        date = date.replace(' ', '_')
        date = date.replace(':', '-')
        dateFinal = date[0:16]

        export_folder = "exported_files_csv"

        if not os.path.exists(export_folder):
            os.makedirs(export_folder)

        file_path = os.path.join(export_folder, f"inventory_{dateFinal}.csv")

        with open(file_path, 'w', newline='') as f:
            w = csv.writer(f, dialect='excel')
            w.writerow(['ID', 'Name', 'Price', 'Quantity'])
            w.writerows(dataraw)

        print(f"Saved: {file_path}")

        messagebox.showinfo("", "CSV file downloaded")
    except Exception as e:
        print(e)
        messagebox.showwarning("", "Error while exporting CSV. Ref: " + str(e))

def find_data():
    global entrysearch, conn
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        itemId = str(entryId.get())
        name = str(entryName.get())
        price = str(entryPrice.get())
        quantity = str(entryQuantity.get())

        if itemId and itemId.strip():
            sql = f"SELECT itemId, itemName, itemPrice, itemQuantity FROM inventory WHERE itemId LIKE '%{itemId}%' "
        elif name and name.strip():
            sql = f"SELECT itemId, itemName, itemPrice, itemQuantity FROM inventory WHERE itemName LIKE '%{name}%' "
        elif price and price.strip():
            sql = f"SELECT itemId, itemName, itemPrice, itemQuantity FROM inventory WHERE itemPrice LIKE '%{price}%' "
        elif quantity and quantity.strip():
            sql = f"SELECT itemId, itemName, itemPrice, itemQuantity FROM inventory WHERE itemQuantity LIKE '%{quantity}%'"
        else:
            messagebox.showwarning("", "Please fill up one of the entries")
            return

        cursor.execute(sql)
        result = cursor.fetchall()

        for data in my_tree.get_children():
            my_tree.delete(data)

        for res in reverse(result):
            my_tree.insert(parent='', index='end', iid=res, text="", values=res)

        my_tree.tag_configure('row', background='#EEEEEE')
    except Exception as e:
        messagebox.showwarning("", f"Error during search: {str(e)}")
    finally:
        conn.close()

def reset_find():
    global entrysearch
    if entrysearch:
        entrysearch.delete(0, END)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result, text="", values=result)

    my_tree.tag_configure('row', background='#EEEEEE')


def insert_data():
    itemId = entryId.get()
    itemName = entryName.get()
    itemPrice = entryPrice.get()
    itemQuantity = entryQuantity.get()

    if not (itemId.isdigit() and itemPrice.isdigit() and itemQuantity.isdigit()):
        messagebox.showwarning("Input Error", "Please enter valid integers for ID, Price, and Quantity.")
        return
    else:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE itemId=?", (int(itemId),))
        existing_item = cursor.fetchone()
        conn.close()

        if existing_item:
            messagebox.showwarning("Item Exists", f"Item with ID {itemId} already exists.")
            return
        else:
            insert(int(itemId), str(itemName), int(itemPrice), int(itemQuantity))

            for data in my_tree.get_children():
                my_tree.delete(data)

            for result in reverse(read()):
                my_tree.insert(parent='', index='end', values=result)

    my_tree.tag_configure('row', background='#EEEEEE')
    my_tree.place(x=475, y=60)


def delete_data():
    selected_item = my_tree.selection()[0]
    deleteData = str(my_tree.item(selected_item)['values'][0])
    delete(deleteData)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result, text="", values=result)

    my_tree.tag_configure('row', background='#EEEEEE')
    my_tree.place(x=475, y=60)


def select_data():
    selected_item = my_tree.selection()[0]
    selected_data = my_tree.item(selected_item)['values']

    entryId.delete(0, END)
    entryName.delete(0, END)
    entryPrice.delete(0, END)
    entryQuantity.delete(0, END)

    entryId.insert(0, selected_data[0])
    entryName.insert(0, selected_data[1])
    entryPrice.insert(0, selected_data[2])
    entryQuantity.insert(0, selected_data[3])


def update_data():
    if not entryId.get().isdigit() or not (entryPrice.get().replace('.', '').isdigit() or entryPrice.get().replace(
            '.', '').replace('-',
                             '').isdigit()) or not entryQuantity.get().isdigit():
        messagebox.showwarning("Input Error", "Please enter valid integers for ID, Price, and Quantity.")
        return

    selected_item = my_tree.selection()[0]
    update_name = my_tree.item(selected_item)['values'][0]
    update(int(entryId.get()), entryName.get(), float(entryPrice.get()), int(entryQuantity.get()), update_name)

    for data in my_tree.get_children():
        my_tree.delete(data)

    for result in reverse(read()):
        my_tree.insert(parent='', index='end', iid=result, text="", values=result)

    my_tree.tag_configure('row', background='#EEEEEE')
    my_tree.place(x=475, y=60)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]

    def sorting_key(x):
        try:
            if col in ("ID", "Quantity"):
                return int(x[0])
            elif col == "Price":
                return float(x[0])
            else:
                return x[0]
        except ValueError:
            return float('inf')

    l.sort(key=sorting_key, reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


leftLabel = Label(root, text=leftColumn, font=('Arial bold', 25), bd=2)
leftLabel.place(x=90, y=10)
rightLabel = Label(root, text=rightColumn, font=('Arial bold', 25), bd=2)
rightLabel.place(x=650, y=10)

idLabel = Label(root, text="ID", font=('Arial bold', 15))
idLabel.place(x=30, y=75)
nameLabel = Label(root, text="Name", font=('Arial bold', 15))
nameLabel.place(x=18, y=135)
priceLabel = Label(root, text="Price", font=('Arial bold', 15))
priceLabel.place(x=18, y=195)
quantityLabel = Label(root, text="Quantity", font=('Arial bold', 15))
quantityLabel.place(x=8, y=253)

entryId = Entry(root, width=20, bd=5, font=('Arial', 15))
entryId.place(x=100, y=70)
idimg = Label(root, image=new_idimage)
idimg.place(x=340, y=48)

entryName = Entry(root, width=20, bd=5, font=('Arial', 15))
entryName.place(x=100, y=130)
nameimg = Label(root, image=new_namepic)
nameimg.place(x=340, y=110)

entryPrice = Entry(root, width=20, bd=5, font=('Arial', 15))
entryPrice.place(x=100, y=190)
priceimg = Label(root, image=new_pricepic)
priceimg.place(x=350, y=175)

entryQuantity = Entry(root, width=20, bd=5, font=('Arial', 15))
entryQuantity.place(x=100, y=250)
quantityimg = Label(root, image=new_quantitypic)
quantityimg.place(x=350, y=240)

# Buttons
buttonClear = Button(
    root, text="Clear Entries", padx=5, pady=5, width=30,
    bd=3, font=('Arial bold', 15), fg="#000000", command=clear_data)
buttonClear.place(x=25, y=310)

buttonSelect = Button(
    root, text="Select", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#000000", command=select_data)
buttonSelect.place(x=700, y=310)

buttonFind = Button(
    root, text="Find", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#000000", command=find_data)
buttonFind.place(x=800, y=310)

buttonReset = Button(
    root, text="Reset", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#000000", command=reset_find)
buttonReset.place(x=900, y=310)

buttonEnter = Button(
    root, text="Save", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#0099ff", command=insert_data)
buttonEnter.place(x=25, y=380)

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#ff8100", command=update_data)
buttonUpdate.place(x=125, y=380)

buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#e62e00", command=delete_data)
buttonDelete.place(x=225, y=380)

buttonExport = Button(
    root, text="Export", padx=5, pady=5, width=5,
    bd=3, font=('Arial bold', 15), fg="#008000", command=export_data)
buttonExport.place(x=325, y=380)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("ID", "Name", "Price", "Quantity")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=100)
my_tree.column("Name", anchor=W, width=150)
my_tree.column("Price", anchor=W, width=100)
my_tree.column("Quantity", anchor=W, width=150)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)

for col in ("ID", "Name", "Price", "Quantity"):
    my_tree.heading(col, text=col, anchor=W, command=lambda c=col: treeview_sort_column(my_tree, c, False))

my_tree.tag_configure('row', background='#EEEEEE', font=('Arial Bold', 15))
my_tree.place(x=475, y=60)

for data in my_tree.get_children():
    my_tree.delete(data)

for result in reverse(read()):
    my_tree.insert(parent='', index='end', iid=result, text="", values=result)

root.resizable(False, False)
root.mainloop()
