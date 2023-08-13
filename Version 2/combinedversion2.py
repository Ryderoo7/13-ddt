'''Login and signup page, where weight, password and username are taken into account.
these variables are then stored in the database against the username'''

import sqlite3
import subprocess
from tkinter import Label, Tk
from tkinter import Button
from tkinter import Entry
from tkinter import ttk
from tkinter import Toplevel
from tkinter import END
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

# function for opening main script.
def openmain():
    subprocess.Popen(
        ["python", r"main.py"])

#function to open the mainguest script.
def openmainguest():
    subprocess.Popen(
        ["python", r"mainguest.py"])

# Function to create necessary database tables.
def create_tables(conn):
    '''
    Create necessary database tables if they don't exist.
    '''
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')

    conn.commit()
    print("Tables created successfully")

# Connect to the database and create tables.
conn = sqlite3.connect('User+pass.db')
create_tables(conn)

# Function to handle user logins.
def login_user():
    """
    Attempt to log in the user by checking credentials against the database.
    If successful, open the main application window.
    """
    username = entry_username.get()
    password = entry_password.get()

    # Connect to the SQLite database.
    conn = sqlite3.connect("User+pass.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password))
    user_pass = cursor.fetchone()

    # Opens the main application window and saves username to a file.
    if user_pass:
        subprocess.Popen(["python", r"Main.py"])
        # Save username to text file
        with open("userDashboard.txt", "w") as user_file:
            user_file.write(entry_username.get())

        root.destroy()
    else:

        messagebox.showerror("Error", "Invalid Username or Password")

    conn.close()

# Functions to remove and insert insterts based on focus in the entry boxes.
def entry_username_focus(event):
    '''
    Triggered when the username entry widget gains focus. If the entry contains
    the placeholder Username and it hasn't been changed yet, this function clears
    the entry and changes its text color to black.
    '''
    if entry_username.get() == "Username":
        entry_username.delete(0, END)
        entry_username.configure(foreground="black")

# Functions to remove and insert insterts based on focus in the entry boxes.
def entry_username_leave(event):
    """
    Triggered when the username entry widget loses focus. If the entry is empty,
    this function restores the Username placeholder and text color.
    """
    if entry_username.get() == "":
        entry_username.insert(0, "Username")
        entry_username.configure(foreground="black")

# Functions to remove and insert insterts based on focus in the entry boxes.
def entry_password_focus(event):
    """
    Triggered when the password entry widget gains focus. If the entry contains
    the placeholder Password, this function clears the entry and changes its text
    color to black, while showing password characters.
    """
    if entry_password.get() == "Password":
        entry_password.delete(0, END)
        entry_password.configure(foreground="black", show="*")

# Functions to remove and insert insterts based on focus in the entry boxes.
def entry_password_leave(event):
    """
    Triggered when the password entry widget loses focus. If the entry is empty,
    this function restores the Password placeholder, hides password characters,
    and changes text color.
    """
    if entry_password.get() == "":
        entry_password.configure(show="")
        entry_password.insert(0, "Password")
        entry_password.configure(foreground="black")


root = Tk()
root.geometry("400x650")
root.resizable(width=False, height=False)
root.configure(bg="#ffc266")

style = ttk.Style()
style.configure("Custom.TFrame", padding=10, background="#ffc266")

logo_image = Image.open(r"Images\Food Bowl png.png")
logo_image = logo_image.resize((220, 180))
logo_photo = ImageTk.PhotoImage(logo_image)

label_logo = Label(root, image=logo_photo, bg="#ffc266")
label_logo.place(relx=0.5, rely=0.15, anchor="center")

frame = ttk.Frame(root, style="Custom.TFrame")
frame.place(relx=0.5, rely=0.55, anchor="center")

label_login = Label(root, text="Login", font=(
    "Arial", 18, "bold"), bg="#ffc266", fg="black")
label_login.place(relx=0.5, rely=0.38, anchor="center")

entry_username = Entry(frame, bg="#da3422", relief="flat")
entry_username.insert(0, "Username")
entry_username.bind('<FocusIn>', entry_username_focus)
entry_username.bind('<FocusOut>', entry_username_leave)
entry_username.pack(pady=10)

entry_password = Entry(frame, bg="#da3422", relief="flat")
entry_password.insert(0, "Password")
entry_password.bind('<FocusIn>', entry_password_focus)
entry_password.bind('<FocusOut>', entry_password_leave)
entry_password.pack(pady=10)

# Function for the signup button.
def signupbutton():
    # Inner function to register a new user upon signing up.
    def register_user():
        global message_label
        username = entry_username_signup.get()
        password = entry_password_signup.get()
        confirm_password = entry_confirm_password_signup.get()
        #makes password length > 6 characters
 
        conn = sqlite3.connect('User+pass.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            messagebox.showerror("Error", "Username already exists")
            conn.close()
            return
        elif not username or not password or not confirm_password:
            messagebox.showerror("Error", "Enter all information please")
            return
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        else:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username,
                 password))
            conn.commit()
            messagebox.showinfo("Success", "Registered Successfully")
            signup_window.destroy()
        conn.close()

    signup_window = Toplevel(root)
    signup_window.geometry("400x650")
    signup_window.resizable(width=False, height=False)
    signup_window.configure(bg="#ffc266")
   
   

   

    # Functions to remove and insert insterts based on focus in the entry boxes.
    def entry_username_focus(event):
        if entry_username_signup.get() == "Username":
            entry_username_signup.delete(0, END)
            entry_username.configure(foreground="black")
    # Functions to remove and insert insterts based on focus in the entry boxes.       
    def entry_username_leave(event):
        if entry_username_signup.get() == "":
            entry_username_signup.insert(0, "Username")
            entry_username_signup.configure(foreground="black")
    # Functions to remove and insert insterts based on focus in the entry boxes.
    def entry_password_focus(event):
        if entry_password_signup.get() == "Password":
            entry_password_signup.delete(0, END)
            entry_password_signup.configure(foreground="black", show="*")
    # Functions to remove and insert insterts based on focus in the entry boxes.
    def entry_password_leave(event):
        if entry_password_signup.get() == "":
            entry_password_signup.configure(show="")
            entry_password_signup.insert(0, "Password")
            entry_password_signup.configure(foreground="black")
    # Functions to remove and insert insterts based on focus in the entry boxes.
    def entry_confirm_password_focus(event):
        if entry_confirm_password_signup.get() == "Confirm Password":
            entry_confirm_password_signup.delete(0, END)
            entry_confirm_password_signup.configure(
                foreground="black", show="*")
    # Functions to remove and insert insterts based on focus in the entry boxes.
    def entry_confirm_password_leave(event):
        if entry_confirm_password_signup.get() == "":
            entry_confirm_password_signup.configure(show="")
            entry_confirm_password_signup.insert(0, "Confirm Password")
            entry_confirm_password_signup.configure(foreground="black")
  
   

    

    frame_signup = ttk.Frame(signup_window, style="Custom.TFrame")
    frame_signup.place(relx=0.5, rely=0.55, anchor="center")

   

    entry_username_signup = Entry(frame_signup, bg="#da3422", relief="flat")
    entry_username_signup.insert(0, "Username")
    entry_username_signup.bind('<FocusIn>', entry_username_focus)
    entry_username_signup.bind('<FocusOut>', entry_username_leave)
    entry_username_signup.pack(pady=10)

    entry_password_signup = Entry(frame_signup, bg="#da3422", relief="flat")
    entry_password_signup.insert(0, "Password")
    entry_password_signup.bind('<FocusIn>', entry_password_focus)
    entry_password_signup.bind('<FocusOut>', entry_password_leave)
    entry_password_signup.pack(pady=10)

    entry_confirm_password_signup = Entry(
        frame_signup, bg="#da3422", relief="flat")
    entry_confirm_password_signup.insert(0, "Confirm Password")
    entry_confirm_password_signup.bind(
        '<FocusIn>', entry_confirm_password_focus)
    entry_confirm_password_signup.bind(
        '<FocusOut>', entry_confirm_password_leave)
    entry_confirm_password_signup.pack(pady=10)

    logo_image_Signup = Image.open(r"Images\Food Bowl png.png")
    logo_image_Signup = logo_image_Signup.resize((220, 180))
    logo_photo_Signup = ImageTk.PhotoImage(logo_image_Signup)

    label_logo_Signup = Label(
        signup_window, image=logo_photo_Signup, bg="#ffc266")
    label_logo_Signup.place(relx=0.5, rely=0.15, anchor="center")

    label_login = Label(signup_window, text="Sign up", font=(
        "Arial", 18, "bold"), bg="#ffc266", fg="black")
    label_login.place(relx=0.5, rely=0.38, anchor="center")

    button_submit = Button(
        signup_window,
        text="Submit",
        bg="#da3422",
        fg="black",
        activebackground="#da3422",
        command=register_user)
    button_submit.place(relx=0.5, rely=0.75, anchor="center")
    button_submit.configure(command=lambda: register_user())

    signup_window.mainloop()

    #Simple code for signup button.
button_signup = Button(
    root,
    text="Sign Up",
    bg="#da3422",
    fg="black",
    activebackground="#da3422",
    command=signupbutton)
button_signup.place(relx=0.5, rely=0.75, anchor="center")


button_login = Button(
    root,
    text="Login",
    bg="#da3422",
    fg="black",
    activebackground="#da3422",
    command=login_user)
button_login.place(relx=0.5, rely=0.68, anchor="center")


button_guest = Button(
    root,
    text="Continue as Guest",
    bg="#da3422",
    fg="black",
    activebackground="#da3422",
    command=openmainguest)
button_guest.place(relx=0.5, rely=0.82, anchor="center")


root.mainloop()