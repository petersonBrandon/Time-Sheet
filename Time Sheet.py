
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
#? External Dependencies:
#?      - customtkinter
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
import subprocess
from rocketchat.api import RocketChatAPI


#! ======================== MAIN WINDOW SETUP ========================
#! Description:
#!      Sets up over theme and window configuration.
#! ===================================================================
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry("600x400") # Set window dimenstions
root_tk.resizable(width=False, height=False) # Prevent window resizing
root_tk.title("Time Sheet") # Set window title

icon = "public\clock-icon.ico"
root_tk.iconbitmap(icon)

#! ===================== ROCKET CHAT API SETUP =======================
#! Description:
#!      Sets up the Rocket Chat API.
#! ===================================================================
apiInfo = open("apiInfo.json")
apiInfo = json.load(apiInfo)
apiSettings = {'token': apiInfo.get("token"), 'user_id': apiInfo.get("userId"), 'domain': apiInfo.get("domain")}
api = RocketChatAPI(settings=apiSettings)
user = api.get_my_info()
apiSettings['username'] = user.get('username')
api.settings=apiSettings

rocketchat_rooms = {}
rooms = api.get_im_rooms()
for x in rooms:
    rocketchat_rooms[x['username']] = x['id']

# print(rocketchat_rooms['attendance-bot'])

#! ======================== GLOBAL VARIABLES =========================
#! Description:
#!      Sets up over theme and window configuration.
#! ===================================================================
userDataFile = "userData.json"
timeDataFile = "timeData.json"

userData = "0"
noData = True
newSheet = False

yRef = 0.4
xRef = 0.2

buttonHorizontalOffset = 0.45
labelHorizontalOffset = 0.26
breakHorizontalOffset = 0.22

debug = True

btnDisabledColor = "#6C6C6C"
btnColor01 = "#1c94cf"

endPeriodBtnColor = "#D31515"
endPeriodBtnHoverColor = "#950F0F"

def saveTempData(onBreak):
    defaultData = { 
        "onBreak": onBreak
    }
    jsonString = json.dumps(defaultData)
    jsonFile = open("temp.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

tempData = ""
tempDataMissing = True
while(tempDataMissing):
    try:
        tempDataFile = open("temp.json")
        tempData = json.load(tempDataFile)
        tempDataMissing = False
    except:
        saveTempData(False)
        preferencesMissing = True

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
    todayIn = datetime.strptime(dayTimeSheet.get("clockIn"), "%I:%M%p")
    todayLunchOut = datetime.strptime(dayTimeSheet.get("lunchOut"), "%I:%M%p")
    todayLunchIn = datetime.strptime(dayTimeSheet.get("lunchIn"), "%I:%M%p")
    todayOut = datetime.strptime(dayTimeSheet.get("clockOut"), "%I:%M%p")
    
    hour1 = (((todayLunchOut - todayIn).seconds)/60)/60
    hour2 = (((todayOut - todayLunchIn).seconds)/60)/60
    regularHours = hour1 + hour2
    overtimeHours = 0
    
    totalHours = 0
    day = datetime.today().weekday()
    # day = 0 #Monday
    # day = 1 #Tuesday
    # day = 2 #Wednesday
    # day = 3 #Thursday
    # day = 4 #Friday
    for index in range(day + 1):
        day = timeSheet.get("time")[len(timeSheet.get("time")) - 1 - index]
        try:
            dayIn = datetime.strptime(day.get("clockIn"), "%I:%M%p")
            dayLunchOut = datetime.strptime(day.get("lunchOut"), "%I:%M%p")
            dayLunchIn = datetime.strptime(day.get("lunchIn"), "%I:%M%p")
            dayOut = datetime.strptime(day.get("clockOut"), "%I:%M%p")

            hour1 = (((dayLunchOut - dayIn).seconds)/60)/60
            hour2 = (((dayOut - dayLunchIn).seconds)/60)/60
            hours = hour1 + hour2
            totalHours = totalHours + float(hours)
        except:
            print("This date did not have any time stamps.")
    if(totalHours > 40):
        overtimeHours = totalHours - 40
        regularHours = float(regularHours) - overtimeHours

    if(overtimeHours == 0):
        overtimeHours = ""
    if(regularHours <= 0):
        regularHours = ""

    if(overtimeHours != ""):
        dayTimeSheet.update({"overtimeHrs": "{:.1f}".format(overtimeHours)})
    else:
        dayTimeSheet.update({"overtimeHrs": str(overtimeHours)})
    
    if(regularHours != ""):  
        dayTimeSheet.update({"regularHrs": "{:.1f}".format(regularHours)})
    else:
        dayTimeSheet.update({"regularHrs": str(regularHours)})

#! ===================== CHECK END OF PERIOD =========================
#! Description:
#!      Checks to see if it is the last day of the pay period. If it
#!      is, it will enable the endPeriod button.
#! ===================================================================
def checkEndOfPeriod():
    if(len(timeSheet.get("time")) == 10): 
        endPeriod.configure(state=tkinter.NORMAL, fg_color=endPeriodBtnColor, hover_color=endPeriodBtnHoverColor)

#! ========================= SET TIMESTAMP ===========================
#! Description:
#!      Sets current date, and sets the timestamp for each card punch.
#! ===================================================================
def setTimestamp(set):
    global newSheet
    if(set == 0):
        dayTimeSheet.update({"date": datetime.now().strftime("%m-%d-%Y")})
        dayTimeSheet.update({"project": project.get()})
        dayTimeSheet.update({"clockIn": datetime.now().strftime("%I:%M%p")})
        if(debug):
            dayTimeSheet.update({"clockIn": "09:00AM"})
        if(newSheet):
            setUserDayTime("update")
            newSheet = False
        else:
            dayTimeSheet.update({"lunchOut": ""})
            dayTimeSheet.update({"lunchIn": ""})
            dayTimeSheet.update({"clockOut": ""})
            setUserDayTime("add")
    elif(set == 1):
        dayTimeSheet.update({"lunchOut": datetime.now().strftime("%I:%M%p")})
        if(debug):
            dayTimeSheet.update({"lunchOut": "01:00PM"})
        setUserDayTime("update")
    elif(set == 2):
        dayTimeSheet.update({"lunchIn": datetime.now().strftime("%I:%M%p")})
        if(debug):
            dayTimeSheet.update({"lunchIn": "02:00PM"})
        setUserDayTime("update")
    else:
        dayTimeSheet.update({"clockOut": datetime.now().strftime("%I:%M%p")})
        if(debug):
            dayTimeSheet.update({"clockOut": "09:00PM"})
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
    weekDay = calendar.day_name[datetime.today().weekday()]
    lastClockedDate = timeSheet.get("time")[len(timeSheet.get("time")) - 1].get("date").split("-")
    if(lastClockedDate[0] != ""):
        lastDate = datetime(int(lastClockedDate[2]), int(lastClockedDate[0]), int(lastClockedDate[1]))
    if(lastClockedDate[0] != "" and lastDate < currentDate):
        timeSpan = currentDate - lastDate
        timeSpan = timeSpan.days
        newDate = datetime(int(lastClockedDate[2]), int(lastClockedDate[0]), int(lastClockedDate[1]))
        for i in range(timeSpan - 1):
            newDate += timedelta(days=1)
            day = calendar.day_name[newDate.weekday()]
            if(day != "Saturday" and day != "Sunday"):
                tempTime = {
                    "date": newDate.strftime("%m-%d-%Y"),
                    "project" : "",
                    "clockIn": "",
                    "lunchOut": "",
                    "lunchIn": "",
                    "clockOut": "",
                    "regularHrs": "",
                    "overtimeHrs": ""
                }
                timeSheet.get("time").append(tempTime)
    elif(weekDay != "Monday"):
        wd = datetime.today().weekday()
        tempDate = datetime.today() - timedelta(days=wd)
        for i in range(wd + 1):
            day = calendar.day_name[tempDate.weekday()]
            tempTime = {
                "date": tempDate.strftime("%m-%d-%Y"),
                "project" : "",
                "clockIn": "",
                "lunchOut": "",
                "lunchIn": "",
                "clockOut": "",
                "regularHrs": "",
                "overtimeHrs": ""
            }
            if(day == "Monday"):
                timeSheet.get("time")[len(timeSheet.get("time")) - 1] = tempTime.copy()
            else:
                timeSheet.get("time").append(tempTime)
            tempDate += timedelta(days=1)

#* App Title
header = customtkinter.CTkLabel(master=root_tk, text="Time Sheet", text_font=("Roboto Medium", -24))
header.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)


#! ======================= PUCH CARD LABELS ==========================
#! Description:
#!      Display the timestamp for the punch button clicked.
#! ===================================================================

def getClockInLabel():
    clockInLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("clockIn"), width=50, text_font=("Roboto Medium", -15))
    clockInLabel.place(relx=xRef + labelHorizontalOffset, rely=yRef, anchor=tkinter.CENTER)

def getLunchOutLabel():
    lunchOutLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("lunchOut"), width=50, text_font=("Roboto Medium", -15))
    lunchOutLabel.place(relx=xRef + labelHorizontalOffset, rely=yRef + 0.1, anchor=tkinter.CENTER)

def getLunchInLabel():
    lunchInLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("lunchIn"), width=50, text_font=("Roboto Medium", -15))
    lunchInLabel.place(relx=xRef + labelHorizontalOffset, rely=yRef + 0.2, anchor=tkinter.CENTER)

def getClockOutLabel():
    clockOutLabel = customtkinter.CTkLabel(master=root_tk, text=dayTimeSheet.get("clockOut"), width=50, text_font=("Roboto Medium", -15))
    clockOutLabel.place(relx=xRef + labelHorizontalOffset, rely=yRef + 0.3, anchor=tkinter.CENTER)

#! ======================== BUTTON METHODS ===========================
#! Description:
#!      Methods that handle the clock in, clock out, lunch in, and 
#!      lunch out button functions.
#! ===================================================================
def clock_in():
    clockIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    setUserData()
    checkDates()
    setTimestamp(0)
    getClockInLabel()

def lunch_out():
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    setTimestamp(1)
    getLunchOutLabel()

def lunch_in():
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    setTimestamp(2)
    getLunchInLabel()

def clock_out():
    clockIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    setTimestamp(3)
    getClockOutLabel()
    checkEndOfPeriod()

def break_out():
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    saveTempData(True)
    # api.send_message('Test message', rocketchat_rooms['jordan.mcgillivray'])

def break_in():
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    if(dayTimeSheet.get("lunchIn") == "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
        lunchOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    breakIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    saveTempData(False)

#! ======================== END PAY PERIOD ===========================
#! Description:
#!      Saves all user data and time stamps into a single file.
#!      Clears temp timestamp file and calls the fill in script.
#! ===================================================================
def end_period():
    os.mkdir("./Sheets")
    payPeriod = (datetime.today() - timedelta(days=14)).strftime("%m-%d-%Y") + " - " + datetime.now().strftime("%m-%d-%Y")
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
    subprocess.call("python generateWeb.py 1")

#! ======================= BUTTON ELEMENTS ===========================
#! Description:
#!      The button elements seen on the window
#! ===================================================================
clockIn = customtkinter.CTkButton(master=root_tk, text="Clock In", command=clock_in)
clockIn.place(relx=xRef + buttonHorizontalOffset, rely=yRef, anchor=tkinter.CENTER)

lunchOut = customtkinter.CTkButton(master=root_tk, text="Lunch Out", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=lunch_out)
lunchOut.place(relx=xRef + buttonHorizontalOffset, rely=yRef + 0.1, anchor=tkinter.CENTER)

lunchIn = customtkinter.CTkButton(master=root_tk, text="Lunch In", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=lunch_in)
lunchIn.place(relx=xRef + buttonHorizontalOffset, rely=yRef + 0.2, anchor=tkinter.CENTER)

clockOut = customtkinter.CTkButton(master=root_tk, text="Clock Out", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=clock_out)
clockOut.place(relx=xRef + buttonHorizontalOffset, rely=yRef + 0.3, anchor=tkinter.CENTER)

breakOut = customtkinter.CTkButton(master=root_tk, text="Break Out", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=break_out)
breakOut.place(relx=xRef + buttonHorizontalOffset + breakHorizontalOffset, rely=yRef + 0.1, anchor=tkinter.CENTER)

breakIn = customtkinter.CTkButton(master=root_tk, text="Break In", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=break_in)
breakIn.place(relx=xRef + buttonHorizontalOffset + breakHorizontalOffset, rely=yRef + 0.2, anchor=tkinter.CENTER)

endPeriod = customtkinter.CTkButton(master=root_tk, text="End Pay Peroid", state=tkinter.DISABLED, fg_color=btnDisabledColor, command=end_period)
endPeriod.place(relx=xRef + buttonHorizontalOffset, rely=yRef + 0.5, anchor=tkinter.CENTER)

#! ======================= BUTTON PRECONFIG ==========================
#! Description:
#!      Disable or enable buttons based on todays timestamps.
#!      Designed to be a safety if the app crashes or is closed on
#!      accident.
#! ===================================================================
clockedIn = False
if(dayTimeSheet.get("clockIn") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.NORMAL,fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockedIn = True
    getClockInLabel()

if(dayTimeSheet.get("lunchOut") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    getLunchOutLabel()

if(dayTimeSheet.get("lunchIn") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    getLunchInLabel()

if(dayTimeSheet.get("clockOut") != "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
    clockIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    getClockOutLabel()

if(tempData.get("onBreak")):
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)

checkEndOfPeriod()

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

#* Name text input element
name = customtkinter.CTkEntry(master=root_tk, placeholder_text="Name", width=200)
name.place(relx=xRef, rely=yRef, anchor=tkinter.CENTER)
name.insert(0, userData.get("name"))

#* Supervisor text input element
supervisor = customtkinter.CTkEntry(master=root_tk, placeholder_text="Supervisor", width=200)
supervisor.place(relx=xRef, rely=yRef + 0.1, anchor=tkinter.CENTER)
supervisor.insert(0, userData.get("supervisor"))

#* Project text input element
project = customtkinter.CTkEntry(master=root_tk, placeholder_text="Project", width=200)
project.place(relx=xRef, rely=yRef + 0.2, anchor=tkinter.CENTER)
project.insert(0, userData.get("project"))

#* Initials text input element
initials = customtkinter.CTkEntry(master=root_tk, placeholder_text="Initials", width=200)
initials.place(relx=xRef, rely=yRef + 0.3, anchor=tkinter.CENTER)
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