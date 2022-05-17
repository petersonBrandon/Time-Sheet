
#?  ________ ______ __       __ ________       ______  __    __ ________ ________ ________ 
#? |        \      \  \     /  \        \     /      \|  \  |  \        \        \        \
#?  \▓▓▓▓▓▓▓▓\▓▓▓▓▓▓ ▓▓\   /  ▓▓ ▓▓▓▓▓▓▓▓    |  ▓▓▓▓▓▓\ ▓▓  | ▓▓ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓\▓▓▓▓▓▓▓▓
#?    | ▓▓    | ▓▓ | ▓▓▓\ /  ▓▓▓ ▓▓__        | ▓▓___\▓▓ ▓▓__| ▓▓ ▓▓__   | ▓▓__      | ▓▓   
#?    | ▓▓    | ▓▓ | ▓▓▓▓\  ▓▓▓▓ ▓▓  \        \▓▓    \| ▓▓    ▓▓ ▓▓  \  | ▓▓  \     | ▓▓   
#?    | ▓▓    | ▓▓ | ▓▓\▓▓ ▓▓ ▓▓ ▓▓▓▓▓        _\▓▓▓▓▓▓\ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓  | ▓▓▓▓▓     | ▓▓   
#?    | ▓▓   _| ▓▓_| ▓▓ \▓▓▓| ▓▓ ▓▓_____     |  \__| ▓▓ ▓▓  | ▓▓ ▓▓_____| ▓▓_____   | ▓▓   
#?    | ▓▓  |   ▓▓ \ ▓▓  \▓ | ▓▓ ▓▓     \     \▓▓    ▓▓ ▓▓  | ▓▓ ▓▓     \ ▓▓     \  | ▓▓   
#?     \▓▓   \▓▓▓▓▓▓\▓▓      \▓▓\▓▓▓▓▓▓▓▓      \▓▓▓▓▓▓ \▓▓   \▓▓\▓▓▓▓▓▓▓▓\▓▓▓▓▓▓▓▓   \▓▓   
#? ========================================================================================
#? Author: Brandon Peterson
#? Version: 1.0.0
#? Description:
#?      A relatively simple time sheet generator/digital punch card.
#? 
#? Recommended VSCode Extensions:
#?      - Better Comments
#?
#? GitHub:
#?      https://github.com/petersonBrandon/Time-Sheet      
#?
#? ========================================================================================                                                                                       

import tkinter
import json
import os
import customtkinter
from datetime import datetime, timedelta


#! ======================== MAIN WINDOW SETUP ========================
#! Description:
#!      Sets up over theme and window configuration.
#! ===================================================================
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry("500x400") # Set window dimenstions
root_tk.resizable(width=False, height=False) # Prevent window resizing
root_tk.title("Time Sheet") # Set window title

#! ======================== GLOBAL VARIABLES =========================
#! Description:
#!      Sets up over theme and window configuration.
#! ===================================================================
userDataFile = "userData.json"
timeDataFile = "timeData.json"

userData = "0"
noData = True
newSheet = False

#! ====================== PRE-LOAD USER DATA =========================
#! Description:
#!      Loads previously set user data.
#!          - name
#!          - supervisor
#!          - project
#!          - initials
#! ===================================================================
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

#! ========================= SET USER DATA ===========================
#! Description:
#!     Updates the user data upon clocking in.
#! ===================================================================
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

#! ========================= GET TIME SHEET ==========================
#! Description:
#!      Pulls the time sheet data from the timeData json file. If
#!      no file exists, a new file is created with placeholder data.
#! ===================================================================
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

#! ===================== SET TODAY'S TIMESTAMPS ======================
#! Description:
#!      Either updates or appends a timestamp to the current workday.
#! ===================================================================
def setUserDayTime(mode):
    if(mode == "update"):
        timeSheet.get("time")[len(timeSheet.get("time")) - 1] = dayTimeSheet.copy()
    elif(mode == "add"):
        timeSheet.get("time").append(dayTimeSheet)
    jsonString = json.dumps(timeSheet)
    jsonFile = open(timeDataFile, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

#! ========================= SET TIMESTAMP ===========================
#! Description:
#!      Sets current date, and sets the timestamp for each card punch.
#! ===================================================================
def setTimestamp(set):
    global newSheet
    if(set == 0):
        dayTimeSheet.update({"date": datetime.now().strftime("%m-%d-%Y")})
        dayTimeSheet.update({"clockIn": datetime.now().strftime("%I:%M %p")})
        if(newSheet):
            setUserDayTime("update")
            newSheet = False
        else:
            dayTimeSheet.update({"lunchOut": ""})
            dayTimeSheet.update({"lunchIn": ""})
            dayTimeSheet.update({"clockOut": ""})
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

#! ========================== CHECK DATES ============================
#! Description:
#!      Checks if there is a gap between the last date that was
#!      clocked in and the current date. If a discrepancy is found
#!      then the dates in between are filled with blank timestamps.
#! ===================================================================
def checkDates():
    currentDate = datetime.now()
    currentDay = datetime.now().strftime("%d")
    lastClockedDate = timeSheet.get("time")[len(timeSheet.get("time")) - 1].get("date").split("-")
    if(lastClockedDate[0] != ""):
        lastDate = datetime(int(lastClockedDate[2]), int(lastClockedDate[0]), int(lastClockedDate[1]))
    if(lastClockedDate[0] != "" and lastDate < currentDate):
        timeSpan = currentDate - lastDate
        timeSpan = timeSpan.days
        newDate = datetime(int(lastClockedDate[2]), int(lastClockedDate[0]), int(lastClockedDate[1]))
        for i in range(timeSpan - 1):
            newDate += timedelta(days=1)
            tempTime = {
                "date": newDate.strftime("%m-%d-%Y"),
                "clockIn": "",
                "lunchOut": "",
                "lunchIn": "",
                "clockOut": ""
            }
            timeSheet.get("time").append(tempTime)

#* App Title
header = customtkinter.CTkLabel(master=root_tk, text="Time Sheet", text_font=("Roboto Medium", -24))
header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

#! ======================== BUTTON METHODS ===========================
#! Description:
#!      Methods that handle the clock in, clock out, lunch in, and 
#!      lunch out button functions.
#! ===================================================================
def clock_in():
    clockIn.configure(state=tkinter.DISABLED)
    clockOut.configure(state=tkinter.NORMAL)
    setUserData()
    checkDates()
    setTimestamp(0)

def lunch_out():
    lunchOut.configure(state=tkinter.DISABLED)
    lunchIn.configure(state=tkinter.NORMAL)
    setTimestamp(1)

def lunch_in():
    lunchIn.configure(state=tkinter.DISABLED)
    setTimestamp(2)

def clock_out():
    clockIn.configure(state=tkinter.NORMAL)
    lunchOut.configure(state=tkinter.NORMAL)
    clockOut.configure(state=tkinter.DISABLED)
    setTimestamp(3)

#! ======================== END PAY PERIOD ===========================
#! Description:
#!      Saves all user data and time stamps into a single file.
#!      Clears temp timestamp file and calls the fill in script.
#! ===================================================================
def end_period():
    os.mkdir("./Sheets")
    payPeriod = timeSheet.get("time")[0].get("date") + " - " + datetime.now().strftime("%m-%d-%Y")
    payPeriodObj = timeSheet
    payPeriodObj["userInfo"] = userData
    print(payPeriodObj)
    jsonString = json.dumps(payPeriodObj)
    jsonFile = open(os.path.join("./Sheets", payPeriod + ".json"), "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    
    # Reset temp time stamp file
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


#! ======================= BUTTON ELEMENTS ===========================
#! Description:
#!      The button elements seen on the window
#! ===================================================================
#* Button global offset
yButtonRef = 0.4
xButtonRef = 0.8

clockIn = customtkinter.CTkButton(master=root_tk, text="Clock In", command=clock_in)
clockIn.place(relx=xButtonRef, rely=yButtonRef, anchor=tkinter.CENTER)

lunchOut = customtkinter.CTkButton(master=root_tk, text="Lunch Out", command=lunch_out)
lunchOut.place(relx=xButtonRef, rely=yButtonRef + 0.1, anchor=tkinter.CENTER)

lunchIn = customtkinter.CTkButton(master=root_tk, text="Lunch In", state=tkinter.DISABLED, command=lunch_in)
lunchIn.place(relx=xButtonRef, rely=yButtonRef + 0.2, anchor=tkinter.CENTER)

clockOut = customtkinter.CTkButton(master=root_tk, text="Clock Out", state=tkinter.DISABLED, command=clock_out)
clockOut.place(relx=xButtonRef, rely=yButtonRef + 0.3, anchor=tkinter.CENTER)

endPeriod = customtkinter.CTkButton(master=root_tk, text="End Pay Peroid", fg_color="#D31515", hover_color="#950F0F", command=end_period)
endPeriod.place(relx=xButtonRef, rely=yButtonRef + 0.5, anchor=tkinter.CENTER)

#! ======================== SAVE PREFERENCES =========================
#! Description:
#!      Saves all user preferences. (Currently only consists of 
#!      dark mode preference)
#! ===================================================================
def savePreferences(darkEnabled):
    defaultData = { 
        "darkEnabled": darkEnabled
    }
    jsonString = json.dumps(defaultData)
    jsonFile = open("userPreferences.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

#! ======================== DARK MODE TOGGLE =========================
#! Description:
#!      Toggles dark mode on or off.
#! ===================================================================
def dark_toggle():
    if(switch_1.get() == "on"):
        customtkinter.set_appearance_mode("dark")
        savePreferences(True)
    else:
        customtkinter.set_appearance_mode("light")
        savePreferences(False)

#* Dark mode switch element
switch_1 = customtkinter.CTkSwitch(master=root_tk, text="Dark Mode", command=dark_toggle, onvalue="on", offvalue="off")
switch_1.place(relx=0.15, rely=0.9, anchor=tkinter.CENTER)

#! ===================== PULL USER PREFERENCES =======================
#! Description:
#!      Get the current user preferences on file. If no file exists,
#!      create a new file and set the default prefences.
#! ===================================================================
preferences = ""
preferencesMissing = True
while(preferencesMissing):
    try:
        preferencesFile = open("userPreferences.json")
        preferences = json.load(preferencesFile)
        print(preferences)
        preferencesMissing = False
    except:
        savePreferences(True)
        preferencesMissing = True

if(preferences.get("darkEnabled")):
    switch_1.select()


#! ======================= TEXTBOX ELEMENTS ==========================
#! Description:
#!      All the textbox elements displayed on screen.
#! ===================================================================
#* Text Input global offset
yInputRef = 0.4
xInputRef = 0.25

#* Name text input element
name = customtkinter.CTkEntry(master=root_tk, placeholder_text="Name", width=200)
name.place(relx=xInputRef, rely=yInputRef, anchor=tkinter.CENTER)
name.insert(0, userData.get("name"))

#* Supervisor text input element
supervisor = customtkinter.CTkEntry(master=root_tk, placeholder_text="Supervisor", width=200)
supervisor.place(relx=xInputRef, rely=yInputRef + 0.1, anchor=tkinter.CENTER)
supervisor.insert(0, userData.get("supervisor"))

#* Project text input element
project = customtkinter.CTkEntry(master=root_tk, placeholder_text="Project", width=200)
project.place(relx=xInputRef, rely=yInputRef + 0.2, anchor=tkinter.CENTER)
project.insert(0, userData.get("project"))

#* Initials text input element
initials = customtkinter.CTkEntry(master=root_tk, placeholder_text="Initials", width=200)
initials.place(relx=xInputRef, rely=yInputRef + 0.3, anchor=tkinter.CENTER)
initials.insert(0, userData.get("initials"))

#! ======================== LABELS FOR INPUTS ========================
#! Current status: Functional
#! Description:
#!      Currently is working. If wanting to implement set xInputRef
#!      to 0.4.
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
#!      Currently works, the only issue is the time display will flash
#!      constantly as the time is being updated.
#! ====================================================================
# while(True):
#     now = datetime.now()
#     current_time = now.strftime("%I:%M:%S %p")
#     label = customtkinter.CTkLabel(master=root_tk, text=current_time, text_font=("Roboto Medium", -32))
#     label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
#     label.update()

root_tk.mainloop()