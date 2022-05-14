import tkinter
import customtkinter
from datetime import datetime

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry("500x400") # Set window dimenstions
root_tk.resizable(width=False, height=False) # Prevent window resizing
root_tk.title("Time Sheet") # Set window title

header = customtkinter.CTkLabel(master=root_tk, text="Time Sheet", text_font=("Roboto Medium", -24))
header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

#! ==================== EXPERIMENTAL TIME DISPLAY ====================
#! Current status: Partly functional
#! Description: 
#!     Currently works, the only issue is the time display will flash
#!     constantly as the time is being updated.
#! ====================================================================
#* while(True):
#*     now = datetime.now()
#*     current_time = now.strftime("%I:%M:%S %p")
#*     label = customtkinter.CTkLabel(master=root_tk, text=current_time, text_font=("Roboto Medium", -32))
#*     label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
#*     label.update()

# Button global offset
yButtonRef = 0.4
xButtonRef = 0.8

# Timestamp buttons and methods
def clock_in():
    print(name.get())

def lunch_out():
    print(name.get())

def lunch_in():
    print(name.get())

def clock_out():
    print(name.get())

clockIn = customtkinter.CTkButton(master=root_tk, text="Clock In", command=clock_in)
clockIn.place(relx=xButtonRef, rely=yButtonRef, anchor=tkinter.CENTER)

lunchOut = customtkinter.CTkButton(master=root_tk, text="Lunch Out", command=lunch_out)
lunchOut.place(relx=xButtonRef, rely=yButtonRef + 0.1, anchor=tkinter.CENTER)

lunchIn = customtkinter.CTkButton(master=root_tk, text="Lunch In", command=lunch_in)
lunchIn.place(relx=xButtonRef, rely=yButtonRef + 0.2, anchor=tkinter.CENTER)

clockOut = customtkinter.CTkButton(master=root_tk, text="Clock Out", command=clock_out)
clockOut.place(relx=xButtonRef, rely=yButtonRef + 0.3, anchor=tkinter.CENTER)

# Dark Mode toggle button and method
def dark_toggle():
    if(switch_1.get() == "on"):
        customtkinter.set_appearance_mode("dark")
    else:
        customtkinter.set_appearance_mode("light")

switch_1 = customtkinter.CTkSwitch(master=root_tk, text="Dark Mode", command=dark_toggle, onvalue="on", offvalue="off")
switch_1.place(relx=0.15, rely=0.9, anchor=tkinter.CENTER)
switch_1.select()

# Text Input global offset
yInputRef = 0.4
xInputRef = 0.25

# Name text input
name = customtkinter.CTkEntry(master=root_tk, placeholder_text="Name", width=200)
name.place(relx=xInputRef, rely=yInputRef, anchor=tkinter.CENTER)

# Supervisor text input
supervisor = customtkinter.CTkEntry(master=root_tk, placeholder_text="Supervisor", width=200)
supervisor.place(relx=xInputRef, rely=yInputRef + 0.1, anchor=tkinter.CENTER)

# Project text input
project = customtkinter.CTkEntry(master=root_tk, placeholder_text="Project", width=200)
project.place(relx=xInputRef, rely=yInputRef + 0.2, anchor=tkinter.CENTER)

# Initials text input
initials = customtkinter.CTkEntry(master=root_tk, placeholder_text="Initials", width=200)
initials.place(relx=xInputRef, rely=yInputRef + 0.3, anchor=tkinter.CENTER)

root_tk.mainloop()