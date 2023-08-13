"""
This script provides a dashboard GUI for tracking weight loss progress.
"""
import sqlite3
from tkinter import Label, Tk
from tkinter import Button
from tkinter import StringVar
from tkinter import Entry
from PIL import Image, ImageTk
import pygame

# Function to retrieve weight by username from the database.
def get_weight_by_username(username):
    """
    Retrieve the weight of a user from the database.
    """
    conn = sqlite3.connect("User+pass.db")
    cursor = conn.cursor()

    cursor.execute("SELECT weight FROM users WHERE username=?", (username,))
    weight = cursor.fetchone()

    conn.close()

    return weight[0] if weight else None


# Button to close the window.
def close_window():
    '''closes main window   
    '''
    root.destroy()


with open("userDashboard.txt", "r") as user_file:
    userDashboard = user_file.read()


# Function to get user weight and display it.
def get_weight_button():
    """
    Retrieve and display the user's weight when the 'Get Your Weight' button is clicked.

    This function retrieves the user's weight from the database based on the username
    obtained from the 'userDashboard.txt' file. If the user's weight is found, it is
    displayed on the GUI. If the user's weight is not found, an error message is shown.
    """
    global userDashboard

    if userDashboard:
        weight = get_weight_by_username(userDashboard)
        if weight is not None:
            weight_var.set(f"{weight} kg")
            spoiler_label.place_forget()
            info_label.place_forget()
            current_weight_label.place(relx=0.5, rely=0.65, anchor="center")
            calculator_button.place(relx=0.5, rely=0.9, anchor="center")
            calculator_entry.place(relx=0.5, rely=0.7, anchor="center")
            message_label.config(text="")
        else:
            weight_var.set("")
            message_label.config(
                text="Username not found", fg="red", font=("Arial", 12)
            )
            message_label.place(relx=0.5, rely=0.55, anchor="center")

# Function to play a sound effect using pygame.
def playsound(mp3_file_path):
    """
    Play a sound effect using pygame.

    This function initializes the pygame and pygame.mixer modules to play a sound effect
    specified by the provided 'mp3_file_path'. The sound effect is played once.
    """
    pygame.init()
    pygame.mixer.init()

    mp3_file_path = r"Sound effects\Congratulations.mp3"
    pygame.mixer.music.load(mp3_file_path)
    pygame.mixer.music.play(1)

# Function to calculate weight difference and display result.D
def calculate_weight_difference():
    """
    Calculate the weight difference and display the result.

    This function calculates the weight difference by subtracting the value entered in the
    calculator entry from the current weight displayed on the UI. It updates the result_label
    with the calculated weight lost. If the calculated weight is positive, a sound effect is
    played, and a congratulatory message is displayed. If the input is not a valid number,
    an "Invalid input" message is displayed.

    """
    current_weight = float(weight_var.get().split()[0])
    try:
        weight_difference = float(calculator_entry.get())
        updated_weight = current_weight - weight_difference
        result_label.config(text=f"Weight lost: {updated_weight:.2f} kg")

        if updated_weight > 0:
            playsound(r"Sound effects\Congratulations.mp3")
            message_label.config(
                text="Congratulations, you lost weight!",
                fg="black",
                font=("Arial", 12),
            )
        else:
            message_label.config(
                text="You tried your best!", fg="black", font=("Arial", 12)
            )

    except ValueError:
        result_label.config(text="Invalid input")

# Creates the main UI window.
root = Tk()
root.geometry("400x650")
root.resizable(width=False, height=False)
root.configure(bg="#ffc266")

#UI Elements Below.
image = Image.open(r"Images\Food Bowl png.png")
image = image.resize((220, 180))
image_photo = ImageTk.PhotoImage(image)

label_image = Label(root, image=image_photo, bg="#ffc266")
label_image.place(x=83, y=35)

label_login = Label(
    root,
    text="Dashboard",
    font=("Arial", 18, "bold"),
    bg="#ffc266",
    fg="black",
)
label_login.place(relx=0.5, rely=0.38, anchor="center")

weight_var = StringVar(root)
weight_var.set("")

weight_display = Label(
    root, textvariable=weight_var, font=("Arial", 15), bg="#ffc266", fg="black"
)
weight_display.place(relx=0.5, rely=0.5, anchor="center")

weight_label = Label(
    root,
    text="Starting Weight:",
    font=("Arial", 15, "bold"),
    bg="#ffc266",
    fg="black",
)
weight_label.place(relx=0.5, rely=0.45, anchor="center")

spoiler_label = Label(
    root,
    text=("Spoiler warning!!! \n Only click the 'Get Your Weight' button \n"
          "If you want to see your starting weight."),
    font=("Arial", 12, "bold"),
    bg="#ffc266",
    fg="black",
)
spoiler_label.place(relx=0.5, rely=0.65, anchor="center")

info_label = Label(
    root,
    text="This feature is intended for use after 30 days of"
    " following this program \n to see the best results.",
    font=("Arial", 9),
    bg="#ffc266",
    fg="black",
)
info_label.place(relx=0.5, rely=0.83, anchor="center")

button_get_weight = Button(
    root,
    text="Get Your Weight",
    bg="#da3422",
    fg="black",
    activebackground="#da3422",
    command=get_weight_button,
)
button_get_weight.place(relx=0.5, rely=0.9, anchor="center")

calculator_button = Button(
    root,
    text="Calculate Weight Difference",
    bg="#da3422",
    fg="black",
    activebackground="#da3422",
    command=calculate_weight_difference,
)
calculator_button.place_forget()

current_weight_label = Label(
    root,
    text="Enter Current Weight:",
    font=("Arial", 12),
    bg="#ffc266",
    fg="black",
)
current_weight_label.place_forget()

calculator_entry = Entry(root, width=10, bg="#da3422", fg="black")
calculator_entry.place_forget()

result_label = Label(
    root, text="", font=("Arial", 12), bg="#ffc266", fg="black"
)
result_label.place(relx=0.5, rely=0.97, anchor="center")

message_label = Label(
    root, text="", font=("Arial", 12), bg="#ffc266", fg="black"
)
message_label.place(relx=0.5, rely=0.55, anchor="center")

button_image = Image.open(r"Images\icons8-back-100.png")
button_image = button_image.resize((25, 25))
button_photo = ImageTk.PhotoImage(button_image)

close_button = Button(
    root, image=button_photo, bg="#da3422", command=close_window
)
close_button.place(x=10, y=10)

root.mainloop()
