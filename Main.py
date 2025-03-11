import qrcode
import sqlite3
import os
from tkinter import *
from tkinter import messagebox

# Define database file
db_file = "qrcodes.db"

# Create the database if it doesn’t exist
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            location TEXT NOT NULL,
            filename TEXT NOT NULL,
            size INTEGER NOT NULL
            )''')
conn.commit()

# Creating the window
win = Tk()
win.title('QR Code Generator')
win.geometry('650x650')
win.config(bg='DarkTurquoise')

# Function to generate the QR code and save it
def generateCode():
    try:
        qr_text = text.get()
        qr_location = loc.get()
        qr_filename = name.get()
        qr_size = int(size.get())

        if not qr_text or not qr_location or not qr_filename:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Creating QRCode object
        qr = qrcode.QRCode(version=qr_size, box_size=10, border=5)
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image()

        # Ensure directory exists
        if not os.path.exists(qr_location):
            os.makedirs(qr_location)

        # Save QR Code as an image file
        fileDir = os.path.join(qr_location, qr_filename + '.png')
        img.save(fileDir)

        # Insert details into database
        c.execute("INSERT INTO qr_codes (text, location, filename, size) VALUES (?, ?, ?, ?)", 
                  (qr_text, qr_location, qr_filename, qr_size))
        conn.commit()

        messagebox.showinfo("QR Code Generator", "QR Code is saved successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# UI Design
headingFrame = Frame(win, bg="azure", bd=5)
headingFrame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.1)
headingLabel = Label(headingFrame, text="Generate QR Code", bg='azure', font=('Times', 20, 'bold'))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

# Input Fields
def create_input_frame(label_text, y_position):
    frame = Frame(win, bg="DarkTurquoise")
    frame.place(relx=0.1, rely=y_position, relwidth=0.7, relheight=0.2)
    label = Label(frame, text=label_text, bg="DarkTurquoise", fg='azure', font=('FiraMono', 13, 'bold'))
    label.place(relx=0.05, rely=0.2, relheight=0.08)
    entry = Entry(frame, font=('Century 12'))
    entry.place(relx=0.05, rely=0.4, relwidth=1, relheight=0.2)
    return entry

text = create_input_frame("Enter the text/URL: ", 0.15)
loc = create_input_frame("Enter the location to save the QR Code: ", 0.35)
name = create_input_frame("Enter the name of the QR Code: ", 0.55)

# QR Code Size Input
Frame4 = Frame(win, bg="DarkTurquoise")
Frame4.place(relx=0.1, rely=0.75, relwidth=0.7, relheight=0.2)
label4 = Label(Frame4, text="Enter the size (1-40, 1 being 21x21): ", bg="DarkTurquoise", fg='azure', font=('FiraMono', 13, 'bold'))
label4.place(relx=0.05, rely=0.2, relheight=0.08)
size = Entry(Frame4, font=('Century 12'))
size.place(relx=0.05, rely=0.4, relwidth=0.5, relheight=0.2)

# Generate Button
button = Button(win, text='Generate Code', font=('FiraMono', 15, 'normal'), command=generateCode)
button.place(relx=0.35, rely=0.9, relwidth=0.25, relheight=0.05)

# Runs the window till it is closed manually
win.mainloop()

# Close database connection when the window is closed
conn.close()
