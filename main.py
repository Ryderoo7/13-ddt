"""
This script is a simple calorie calculator application. It calculates
calories based on user input for age, weight, height, gender, and activity level. The user can choose
to maintain weight or lose weight and get an estimated daily calorie intake.
"""

from tkinter import Label, Tk
from tkinter import Button
from tkinter import StringVar
from tkinter import Entry
from tkinter import ttk
from tkinter import Toplevel
from tkinter import BooleanVar
from tkinter import Canvas
from PIL import Image, ImageTk
import subprocess


def calculate_calories():
    """
    Calculate the estimated daily calorie intake based on user input for age, weight, height,
    gender, and activity level. Display the calculated calories in a new window.
    """
    age = entry_age.get()
    weight = entry_weight.get()
    height = entry_height.get()

    # Checks if any criteria is missed, and if so an error message will popup in the form of a window.
    # This window is done with the notation 'top level' ensuring the message is seen.
    if age == "Age" or weight == "Weight" or height == "Height":
        error_window = Toplevel(root)
        error_window.title("Error")
        error_label = Label(
            error_window, text="Please fill in all the criteria."
        )
        error_label.pack(pady=20)
        return

    if gender_option.get() == "Gender":
        error_window = Toplevel(root)
        error_window.title("Error")
        error_label = Label(error_window, text="Please select a gender.")
        error_label.pack(pady=20)
        return

    if activity_option.get() == "Activity Level":
        error_window = Toplevel(root)
        error_window.title("Error")
        error_label = Label(
            error_window, text="Please select an activity level."
        )
        error_label.pack(pady=20)
        return

    try:
        age = int(age)
        weight = float(weight)
        height = float(height)
    except ValueError:
        error_window = Toplevel(root)
        error_window.title("Error")
        error_label = Label(
            error_window,
            text="Please enter valid numeric values for age, weight, and height.",
        )
        error_label.pack(pady=20)
        return

    gender = gender_option.get()
    activity_level = activity_option.get()

    if gender == "Male":
        bmr = 13.397 * weight + 4.799 * height - 5.677 * age + 88.362
    elif gender == "Female":
        bmr = 9.247 * weight + 3.098 * height - 4.330 * age + 447.593
    else:
        return

    if activity_level == "No Activity (<1 hour a week)":
        calories = bmr * 1.2
    elif activity_level == "Small Activity (<3 hours a week)":
        calories = bmr * 1.375
    elif activity_level == "Medium Activity (30 minutes a day)":
        calories = bmr * 1.55
    elif activity_level == "High Activity (1 hour a day)":
        calories = bmr * 1.725
    elif activity_level == "Intense Activity (>1 hour a day)":
        calories = bmr * 1.9
    else:
        return

    if maintain_weight_clicked.get():
        calories *= activity_multiplier[activity_level]
    elif lose_weight_clicked.get():
        calories *= 0.85  # Multiply calories by 0.85 for weight loss.

    calories_window = Toplevel(root)
    calories_window.geometry("400x650")
    calories_window.resizable(width=False, height=False)
    calories_window.configure(bg="#ffc266")

    def close_window():
        '''closes calorie window'''
        calories_window.destroy()

    button_image = Image.open(r"Images\icons8-back-100.png")
    button_image = button_image.resize((25, 25))
    button_photo = ImageTk.PhotoImage(button_image)
    close_button = Button(
        calories_window, image=button_photo, bg="#da3422", command=close_window
    )
    close_button.image = (
        button_photo
    )
    close_button.place(x=10, y=10)

    logo_image = Image.open(r"Images\Food Bowl png.png")
    logo_image = logo_image.resize((220, 180))
    logo_image = ImageTk.PhotoImage(logo_image)

    red_circle_image = Image.open(r"Images\red circle.png")
    red_circle_image = red_circle_image.resize((270, 210))
    red_circle_image = ImageTk.PhotoImage(red_circle_image)

    # Creates and places the logo image.
    logo_label = Label(calories_window, image=logo_image, bg="#ffc266")
    logo_label.image = logo_image
    logo_label.place(relx=0.5, rely=0.2, anchor="center")

    # Creates and places the red circle image.
    red_circle_label = Label(
        calories_window,
        image=red_circle_image,
        bg="#ffc266")
    red_circle_label.image = red_circle_image
    red_circle_label.place(relx=0.51, rely=0.55, anchor="center")

    # Creatse and places the calculated calories label.
    label_calories = Label(
        calories_window,
        text="Calories: {:.2f}".format(calories),
        font=("Arial", 18, "bold"),
        bg="#da3422",
        fg="black",
        padx=0,
        pady=0,
    )
    label_calories.place(x=112, y=330)


root = Tk()
root.geometry("400x650")
root.resizable(width=False, height=False)
root.configure(bg="#ffc266")

style = ttk.Style()
style.configure("Custom.TFrame", padding=10, background="#ffc266")

image = Image.open(r"Images\Food Bowl png.png")
image = image.resize((220, 180))
image_photo = ImageTk.PhotoImage(image)

label_image = Label(root, image=image_photo, bg="#ffc266")
label_image.place(x=85, y=35)

frame1 = ttk.Frame(root, style="Custom.TFrame")
frame1.place(x=140, y=350)

framemenu = ttk.Frame(root, style="Custom.TFrame")
framemenu.place(x=150, y=320)

frame2 = ttk.Frame(root)
frame2.place(x=170, y=600)

gender_option = StringVar()
entry_gender = ["Male", "Female"]
option_menu = ttk.OptionMenu(frame1, gender_option, "Gender", *entry_gender)
option_menu.pack(pady=20)

age_changed = BooleanVar()
age_changed.set(False)

# Entry widgets and placeholders with focus and leave functions.
def age_entry_focus(event):
    """
    Triggered when the age entry widget gains focus.
    If the entry contains the placeholder Age
    and it hasn't been changed yet, this function clears
    the entry and changes its text color to black.
    """
    if entry_age.get() == "Age":
        if not age_changed.get():
            age_changed.set(True)
            entry_age.delete(0, len(entry_age.get()))
            entry_age.configure(foreground="black")

# Entry widgets and placeholders with focus and leave functions.
def age_entry_leave(event):
    """
    Triggered when the age entry widget loses focus.
    If the entry is empty and the placeholder
    has been previously changed, this function restores
    the Age placeholder and text color.
    """
    if entry_age.get() == "":
        if age_changed.get():
            age_changed.set(False)
            entry_age.insert(0, "Age")
            entry_age.configure(foreground="black")


##########################################################################

weight_changed = BooleanVar()
weight_changed.set(False)

# Entry widgets and placeholders with focus and leave functions.
def weight_entry_focus(event):
    """
    Triggered when the weight entry widget gains focus.
    If the entry contains the placeholder Weight
    and it hasn't been changed yet, this function clears
    the entry and changes its text color to black.
    """
    if entry_weight.get() == "Weight":
        if not weight_changed.get():
            weight_changed.set(True)
            entry_weight.delete(0, len(entry_weight.get()))
            entry_weight.configure(foreground="black")

# Entry widgets and placeholders with focus and leave functions.
def weight_entry_leave(event):
    """
    Triggered when the weight entry widget loses focus.
    If the entry is empty and the placeholder
    has been previously changed, this function restores
    the Weight placeholder and text color.
    """
    if entry_weight.get() == "":
        if weight_changed.get():
            weight_changed.set(False)
            entry_weight.insert(0, "Weight")
            entry_weight.configure(foreground="black")


##########################################################################

height_changed = BooleanVar()
height_changed.set(False)

# Entry widgets and placeholders with focus and leave functions.
def height_entry_focus(event):
    """
    Triggered when the height entry widget gains focus.
    If the entry contains the placeholder Height
    and it hasn't been changed yet, this function clears
    the entry and changes its text color to black.
    """
    if entry_height.get() == "Height":
        if not height_changed.get():
            height_changed.set(True)
            entry_height.delete(0, len(entry_height.get()))
            entry_height.configure(foreground="black")

# Entry widgets and placeholders with focus and leave functions.
def height_entry_leave(event):
    """
    Triggered when the height entry widget loses focus.
    If the entry is empty and the placeholder
    has been previously changed, this function restores
    the Height placeholder and text color.
    """
    if entry_height.get() == "":
        if height_changed.get():
            height_changed.set(False)
            entry_height.insert(0, "Height")
            entry_height.configure(foreground="black")


##########################################################################

activity_option = StringVar()
entry_activity = [
    "No Activity (<1 hour a week)",
    "Small Activity (<3 hours a week)",
    "Medium Activity (30 minutes a day)",
    "High Activity (1 hour a day)",
    "Intense Activity (>1 hour a day)",
]
activity_menu = ttk.OptionMenu(
    framemenu, activity_option, "Activity Level", *entry_activity
)
activity_menu.pack(pady=0)

entry_age = Entry(frame1, bg="#da3422", relief="flat")
entry_age.insert(0, "Age")
entry_age.bind("<FocusIn>", age_entry_focus)
entry_age.bind("<FocusOut>", age_entry_leave)
entry_age.pack(pady=20)

entry_height = Entry(frame1, bg="#da3422", relief="flat")
entry_height.insert(0, "Height")
entry_height.bind("<FocusIn>", height_entry_focus)
entry_height.bind("<FocusOut>", height_entry_leave)
entry_height.pack(pady=20)

entry_weight = Entry(frame1, bg="#da3422", relief="flat")
entry_weight.insert(0, "Weight")
entry_weight.bind("<FocusIn>", weight_entry_focus)
entry_weight.bind("<FocusOut>", weight_entry_leave)
entry_weight.pack(pady=20)

style = ttk.Style()
style.configure("Red.TEntry", fieldbackground="#da3422")
style.configure("TMenubutton", background="#da3422")

button1 = Button(
    frame2,
    text="Calculate",
    background="#da3422",
    activebackground="#da3422",
    command=calculate_calories,
)
button1.pack()


image_frame1 = ttk.Frame(root, style="Custom.TFrame")
image_frame1.place(x=40, y=237.7)

image_frame2 = ttk.Frame(root, style="Custom.TFrame")
image_frame2.place(x=208, y=230)

# image 1 for button 1.
image1 = Image.open(r"Images\Maintain weight button.png")
image1 = image1.resize((140, 53), resample=Image.BICUBIC)
image1_photo = ImageTk.PhotoImage(image1)

maintain_weight_clicked = BooleanVar()
maintain_weight_clicked.set(False)


def maintain_weight_click():
    '''puts through maintain weight function'''
    maintain_weight_toggle()
    canvas.place(x=40, y=240)
    root.after(50, lambda: canvas.place(x=40, y=237.7))


canvas = Canvas(
    root,
    width=image1_photo.width(),
    height=image1_photo.height(),
    background="#ffc266",
    highlightbackground="#ffc266",
)
canvas.place(x=40, y=237.7)
canvas.bind("<Button-1>", lambda event: maintain_weight_click())
canvas.create_image(0, 0, anchor="nw", image=image1_photo)

# image 2 for button 2.
image2 = Image.open(r"Images\Lose weight button.png")
image2 = image2.resize((148, 61), resample=Image.BICUBIC)
image2_photo = ImageTk.PhotoImage(image2)

lose_weight_clicked = BooleanVar()
lose_weight_clicked.set(False)

## Maintain Weight and Lose Weight toggle functions.
def lose_weight_click():
    '''puts through lose weight toggle'''
    lose_weight_toggle()
    canvas1.place(x=209, y=232)
    root.after(50, lambda: canvas1.place(x=209, y=229.7))


canvas1 = Canvas(
    root,
    width=image2_photo.width(),
    height=image2_photo.height(),
    background="#ffc266",
    highlightbackground="#ffc266",
)
canvas1.place(x=209, y=229.7)
canvas1.bind("<Button-1>", lambda event: lose_weight_click())
canvas1.create_image(0, 0, anchor="nw", image=image2_photo)


# Maintain Weight and Lose Weight toggle functions.
def maintain_weight_toggle():
    """
    Toggle the maintain weight option and reset the lose weight option.
    """
    maintain_weight_clicked.set(True)
    lose_weight_clicked.set(False)


def lose_weight_toggle():
    """
    Toggle the lose weight option and reset the maintain weight option.
    """
    maintain_weight_clicked.set(False)
    lose_weight_clicked.set(True)


activity_multiplier = {
    "No Activity (<1 hour a week)": 1.0,
    "Small Activity (<3 hours a week)": 1.0,
    "Medium Activity (30 minutes a day)": 1.0,
    "High Activity (1 hour a day)": 1.0,
    "Intense Activity (>1 hour a day)": 1.0,
}


def open_another_script():
    """
    Open another script using the subprocess module.
    """
    subprocess.run(["python", r"storedinformation.py"])


button_image = Image.open(r"Images\settings-icon-287268.png")
button_image = button_image.resize((40, 40))
button_photo = ImageTk.PhotoImage(button_image)


image_button = Button(
    root, image=button_photo, bg="#da3422", command=open_another_script
)
image_button.place(relx=0.9, rely=0.06, anchor="center")


root.mainloop()
