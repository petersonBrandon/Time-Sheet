
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
import calendar


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
        "initials": initials.get(),
        "project": project.get()
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
                    "project" : "",
                    "clockIn": "",
                    "lunchOut": "",
                    "lunchIn": "",
                    "clockOut": "",
                    "regularHrs": "",
                    "overtimeHrs": ""
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

#! ======================= CALCULATE HOURS ===========================
#! Description:
#!      Determines hours worked for the day. On friday total hours 
#!      are counted and overtime is set on the last day.
#! ===================================================================

# TODO: Capability to change "last day of week" based on user preference.
def calculateHours():
    setUserDayTime("update")
    todayIn = datetime.strptime(dayTimeSheet.get("clockIn"), "%I:%M %p")
    todayLunchOut = datetime.strptime(dayTimeSheet.get("lunchOut"), "%I:%M %p")
    todayLunchIn = datetime.strptime(dayTimeSheet.get("lunchIn"), "%I:%M %p")
    todayOut = datetime.strptime(dayTimeSheet.get("clockOut"), "%I:%M %p")
    
    day = calendar.day_name[datetime.today().weekday()]
    # day = calendar.day_name[4]
    hour1 = (((todayLunchOut - todayIn).seconds)/60)/60
    hour2 = (((todayOut - todayLunchIn).seconds)/60)/60
    regularHours = hour1 + hour2
    regularHours = '{0:.1g}'.format(regularHours)
    
    if(day == "Friday"):
        totalHours = 0
        for day in timeSheet.get("time"):
            dayIn = datetime.strptime(day.get("clockIn"), "%I:%M %p")
            dayLunchOut = datetime.strptime(day.get("lunchOut"), "%I:%M %p")
            dayLunchIn = datetime.strptime(day.get("lunchIn"), "%I:%M %p")
            dayOut = datetime.strptime(day.get("clockOut"), "%I:%M %p")

            hour1 = (((dayLunchOut - dayIn).seconds)/60)/60
            hour2 = (((dayOut - dayLunchIn).seconds)/60)/60
            hours = hour1 + hour2
            hours = '{0:.1g}'.format(hours)
            totalHours = totalHours + float(hours)
        if(totalHours > 40):
            regularHours = "8"
            overtimeHours = totalHours - 40
            dayTimeSheet.update({"overtimeHrs": str(overtimeHours)})
        
    dayTimeSheet.update({"regularHrs": regularHours})


#! ========================= SET TIMESTAMP ===========================
#! Description:
#!      Sets current date, and sets the timestamp for each card punch.
#! ===================================================================
def setTimestamp(set):
    global newSheet
    if(set == 0):
        dayTimeSheet.update({"date": datetime.now().strftime("%m-%d-%Y")})
        dayTimeSheet.update({"project": project.get()})
        dayTimeSheet.update({"clockIn": datetime.now().strftime("%I:%M %p")})
        # dayTimeSheet.update({"clockIn": "09:00 AM"})
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
        # dayTimeSheet.update({"lunchOut": "01:00 PM"})
        setUserDayTime("update")
    elif(set == 2):
        dayTimeSheet.update({"lunchIn": datetime.now().strftime("%I:%M %p")})
        # dayTimeSheet.update({"lunchIn": "02:00 PM"})
        setUserDayTime("update")
    else:
        dayTimeSheet.update({"clockOut": datetime.now().strftime("%I:%M %p")})
        # dayTimeSheet.update({"clockOut": "07:00 PM"})
        calculateHours()
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
                "clockOut": "",
                "regularHrs": "",
                "overtimeHrs": ""
            }
            timeSheet.get("time").append(tempTime)

#* App Title
header = customtkinter.CTkLabel(master=root_tk, text="Time Sheet", text_font=("Roboto Medium", -24))
header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


#! ======================= PUCH CARD LABELS ==========================
#! Description:
#!      Display the timestamp for the punch button clicked.
#! ===================================================================
yLabelRef = 0.4
xLabelRef = 0.56

def getClockInLabel():
    clockInLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("clockIn"), width=50, text_font=("Roboto Medium", -15))
    clockInLabel.place(relx=xLabelRef, rely=yLabelRef, anchor=tkinter.CENTER)

def getLunchOutLabel():
    lunchOutLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("lunchOut"), width=50, text_font=("Roboto Medium", -15))
    lunchOutLabel.place(relx=xLabelRef, rely=yLabelRef + 0.1, anchor=tkinter.CENTER)

def getLunchInLabel():
    lunchInLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("lunchIn"), width=50, text_font=("Roboto Medium", -15))
    lunchInLabel.place(relx=xLabelRef, rely=yLabelRef + 0.2, anchor=tkinter.CENTER)

def getClockOutLabel():
    clockOutLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("clockOut"), width=50, text_font=("Roboto Medium", -15))
    clockOutLabel.place(relx=xLabelRef, rely=yLabelRef + 0.3, anchor=tkinter.CENTER)

#! ======================== BUTTON METHODS ===========================
#! Description:
#!      Methods that handle the clock in, clock out, lunch in, and 
#!      lunch out button functions.
#! ===================================================================
def clock_in():
    clockIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchOut.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    clockOut.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    setUserData()
    checkDates()
    setTimestamp(0)
    getClockInLabel()

def lunch_out():
    lunchOut.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchIn.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    setTimestamp(1)
    getLunchOutLabel()

def lunch_in():
    lunchIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    setTimestamp(2)
    getLunchInLabel()

def clock_out():
    clockIn.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    clockOut.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    setTimestamp(3)
    getClockOutLabel()

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

lunchOut = customtkinter.CTkButton(master=root_tk, text="Lunch Out", state=tkinter.DISABLED, fg_color="#6C6C6C", command=lunch_out)
lunchOut.place(relx=xButtonRef, rely=yButtonRef + 0.1, anchor=tkinter.CENTER)

lunchIn = customtkinter.CTkButton(master=root_tk, text="Lunch In", state=tkinter.DISABLED, fg_color="#6C6C6C", command=lunch_in)
lunchIn.place(relx=xButtonRef, rely=yButtonRef + 0.2, anchor=tkinter.CENTER)

clockOut = customtkinter.CTkButton(master=root_tk, text="Clock Out", state=tkinter.DISABLED, fg_color="#6C6C6C", command=clock_out)
clockOut.place(relx=xButtonRef, rely=yButtonRef + 0.3, anchor=tkinter.CENTER)

endPeriod = customtkinter.CTkButton(master=root_tk, text="End Pay Peroid", fg_color="#D31515", hover_color="#950F0F", command=end_period)
endPeriod.place(relx=xButtonRef, rely=yButtonRef + 0.5, anchor=tkinter.CENTER)

#! ======================= BUTTON PRECONFIG ==========================
#! Description:
#!      Disable or enable buttons based on todays timestamps.
#!      Designed to be a safety if the app crashes or is closed on
#!      accident.
#! ===================================================================
if(dayTimeSheet.get("clockIn") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchOut.configure(state=tkinter.NORMAL,fg_color="#1c94cf")
    clockOut.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    getClockInLabel()

if(dayTimeSheet.get("lunchOut") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchOut.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchIn.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    getLunchOutLabel()

if(dayTimeSheet.get("lunchIn") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockOut.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    clockIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchOut.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    lunchIn.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    getLunchInLabel()

if(dayTimeSheet.get("clockOut") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.NORMAL, fg_color="#1c94cf")
    clockOut.configure(state=tkinter.DISABLED, fg_color="#6C6C6C")
    getClockOutLabel()

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