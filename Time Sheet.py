import tkinter
import json
import shutil
import customtkinter
from datetime import datetime

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry("500x400") # Set window dimenstions
root_tk.resizable(width=False, height=False) # Prevent window resizing
root_tk.title("Time Sheet") # Set window title

userDataFile = "userData.json"
timeDataFile = "timeData.json"

userData = "0"
noData = True
newSheet = False

while(noData):
    try:
        userFile = open(userDataFile)
        userData = json.load(userFile)
        noData = False
    except:
        defaultData = { "name": "name", "supervisor": "supervisor", "project": "project", "initials": "initials"}
        jsonString = json.dumps(defaultData)
        jsonFile = open(userDataFile, "w")
        jsonFile.write(jsonString)
        jsonFile.close()
        noData = True

def setUserData():
    userData = {
        "name": name.get(),
        "supervisor": supervisor.get(),
        "project": project.get(),
        "initials": initials.get()
    }
    jsonString = json.dumps(userData)
    jsonFile = open(userDataFile, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def getTimeSheet():
    noData = True
    global newSheet
    while(noData):
        try:
            timeFile = open(timeDataFile)
            timeSheet = json.load(timeFile)
            noData = False
            return timeSheet
        except:
            defaultData = { 
                "time" : [{
                    "date": "",
                    "clockIn": "",
                    "lunchOut": "",
                    "lunchIn": "",
                    "clockOut": ""
                }]
            }
            jsonString = json.dumps(defaultData)
            jsonFile = open(timeDataFile, "w")
            jsonFile.write(jsonString)
            jsonFile.close()
            newSheet = True
            noData = True

timeSheet = getTimeSheet()
dayTimeSheet = timeSheet.get("time")[len(timeSheet.get("time")) - 1].copy()
if(dayTimeSheet.get("clockIn") == ""):
    newSheet = True

# TODO: FIX PREVIOUS DATE STAMP BEING OVERWRITTEN
def setUserDayTime(mode):
    if(mode == "update"):
        timeSheet.get("time")[len(timeSheet.get("time")) - 1] = dayTimeSheet.copy()
    elif(mode == "add"):
        timeSheet.get("time").append(dayTimeSheet)

    jsonString = json.dumps(timeSheet)
    jsonFile = open(timeDataFile, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def setTimestamp(set):
    global newSheet
    if(set == 0):
        dayTimeSheet.update({"date": datetime.now().strftime("%m-%d-%Y")})
        dayTimeSheet.update({"clockIn": datetime.now().strftime("%I:%M %p")})
        if(newSheet):
            setUserDayTime("update")
            newSheet = False
        else:
            setUserDayTime("add")
    elif(set == 1):
        dayTimeSheet.update({"lunchOut": datetime.now().strftime("%I:%M %p")})
        setUserDayTime("update")
    elif(set == 2):
        dayTimeSheet.update({"lunchIn": datetime.now().strftime("%I:%M %p")})
        setUserDayTime("update")
    else:
        dayTimeSheet.update({"clockOut": datetime.now().strftime("%I:%M %p")})
        setUserDayTime("update")

# TODO: CHECK IF THERE IS A GAP BETWEEN CLOCK IN DATES, FILL THE GAP WITH 0'S
def checkDates():
    currentMonth = datetime.now().strftime("%m")
    # currentDay = datetime.now().strftime("%d")
    # lastClockedDate = timeSheet.get("time")[len(timeSheet.get("time")) - 1].get("date").split("-")
    # print(lastClockedDate)
    # if(lastClockedDate[0] != ""):
    #     print(lastClockedDate[1] < currentDay)

# App Title
header = customtkinter.CTkLabel(master=root_tk, text="Time Sheet", text_font=("Roboto Medium", -24))
header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

# Button global offset
yButtonRef = 0.4
xButtonRef = 0.8

# Timestamp buttons and methods
def clock_in():
    clockIn.configure(state=tkinter.DISABLED)
    setUserData()
    checkDates()
    setTimestamp(0)

def lunch_out():
    lunchOut.configure(state=tkinter.DISABLED)
    setTimestamp(1)

def lunch_in():
    lunchIn.configure(state=tkinter.DISABLED)
    setTimestamp(2)

def clock_out():
    clockIn.configure(state=tkinter.NORMAL)
    lunchOut.configure(state=tkinter.NORMAL)
    lunchIn.configure(state=tkinter.NORMAL)
    setTimestamp(3)

def end_period():
    payPeriod = timeSheet.get("time")[0].get("date") + " - " + datetime.now().strftime("%m-%d-%Y")
    jsonFile = open(payPeriod + ".json", "w")
    jsonFile.close()
    shutil.copyfile(timeDataFile, payPeriod + ".json")
    defaultData = { 
        "time" : [{
            "date": "",
            "clockIn": "",
            "lunchOut": "",
            "lunchIn": "",
            "clockOut": ""
        }]
    }
    jsonString = json.dumps(defaultData)
    jsonFile = open(timeDataFile, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

clockIn = customtkinter.CTkButton(master=root_tk, text="Clock In", command=clock_in)
clockIn.place(relx=xButtonRef, rely=yButtonRef, anchor=tkinter.CENTER)

lunchOut = customtkinter.CTkButton(master=root_tk, text="Lunch Out", command=lunch_out)
lunchOut.place(relx=xButtonRef, rely=yButtonRef + 0.1, anchor=tkinter.CENTER)

lunchIn = customtkinter.CTkButton(master=root_tk, text="Lunch In", command=lunch_in)
lunchIn.place(relx=xButtonRef, rely=yButtonRef + 0.2, anchor=tkinter.CENTER)

clockOut = customtkinter.CTkButton(master=root_tk, text="Clock Out", command=clock_out)
clockOut.place(relx=xButtonRef, rely=yButtonRef + 0.3, anchor=tkinter.CENTER)

endPeriod = customtkinter.CTkButton(master=root_tk, text="End Pay Peroid", fg_color="#D31515", hover_color="#950F0F", command=end_period)
endPeriod.place(relx=xButtonRef, rely=yButtonRef + 0.5, anchor=tkinter.CENTER)

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
name.insert(0, userData.get("name"))

# Supervisor text input
supervisor = customtkinter.CTkEntry(master=root_tk, placeholder_text="Supervisor", width=200)
supervisor.place(relx=xInputRef, rely=yInputRef + 0.1, anchor=tkinter.CENTER)
supervisor.insert(0, userData.get("supervisor"))

# Project text input
project = customtkinter.CTkEntry(master=root_tk, placeholder_text="Project", width=200)
project.place(relx=xInputRef, rely=yInputRef + 0.2, anchor=tkinter.CENTER)
project.insert(0, userData.get("project"))

# Initials text input
initials = customtkinter.CTkEntry(master=root_tk, placeholder_text="Initials", width=200)
initials.place(relx=xInputRef, rely=yInputRef + 0.3, anchor=tkinter.CENTER)
initials.insert(0, userData.get("initials"))

#! ======================== LABELS FOR INPUTS ========================
#! Current status: Functional
#! Description:
#!     Currently is working. If wanting to implement set xInputRef
#!     to 0.4.
#! ===================================================================
# nameLabel = customtkinter.CTkLabel(master=root_tk, text="Name", width=50, text_font=("Roboto Medium", -15))
# nameLabel.place(relx=0.13, rely=xInputRef, anchor=tkinter.CENTER)

# supervisorLabel = customtkinter.CTkLabel(master=root_tk, text="Supervisor", width=50, text_font=("Roboto Medium", -15))
# supervisorLabel.place(relx=0.1, rely=xInputRef + 0.1, anchor=tkinter.CENTER)

# projectLabel = customtkinter.CTkLabel(master=root_tk, text="Project", width=50, text_font=("Roboto Medium", -15))
# projectLabel.place(relx=0.12, rely=xInputRef + 0.2, anchor=tkinter.CENTER)

# initialsLabel = customtkinter.CTkLabel(master=root_tk, text="Initials", width=50, text_font=("Roboto Medium", -15))
# initialsLabel.place(relx=0.121, rely=xInputRef + 0.3, anchor=tkinter.CENTER)

#! ==================== EXPERIMENTAL TIME DISPLAY ====================
#! Current status: Partly functional
#! Description: 
#!     Currently works, the only issue is the time display will flash
#!     constantly as the time is being updated.
#! ====================================================================
# while(True):
#     now = datetime.now()
#     current_time = now.strftime("%I:%M:%S %p")
#     label = customtkinter.CTkLabel(master=root_tk, text=current_time, text_font=("Roboto Medium", -32))
#     label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
#     label.update()

root_tk.mainloop()