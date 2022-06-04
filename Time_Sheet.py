
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
from doctest import master
import pip

# Install script dependencies automatically
pip.main(["install", "customtkinter"])
pip.main(["install", "rocket-python"])
pip.main(["install", "pygame"])

import tkinter
import json
import os
import time
import customtkinter
import calendar
import subprocess
import pygame
import threading
from sys import platform
from datetime import datetime, timedelta
from rocketchat.api import RocketChatAPI

#! ======================== GLOBAL VARIABLES =========================
#! Description:
#!      Global Variables.
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

debug = False

masterNotificationEnabled = True

chatroom = "attendance-bot"
masterMessagingEnabled = True

btnDisabledColor = "#6C6C6C"
btnColor01 = "#1c94cf"

endPeriodBtnColor = "#D31515"
endPeriodBtnHoverColor = "#950F0F"

#! ======================== SAVE PREFERENCES =========================
#! Description:
#!      Saves all user preferences. (Currently only consists of 
#!      dark mode preference)
#! ===================================================================
preferences = {}
def savePreferences():
    jsonString = json.dumps(preferences)
    jsonFile = open("userPreferences.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

#! ===================== PULL USER PREFERENCES =======================
#! Description:
#!      Get the current user preferences on file. If no file exists,
#!      create a new file and set the default prefences.
#! ===================================================================
preferencesMissing = True
while(preferencesMissing):
    try:
        preferencesFile = open("userPreferences.json")
        preferences = json.load(preferencesFile)
        preferencesMissing = False
    except:
        preferences = {
            "messagingEnabled": True,
            "notificationsEnabled": True,
            "notificationSound": "crystal.mp3"
        }
        savePreferences()
        preferencesMissing = True

#! ======================== MAIN WINDOW SETUP ========================
#! Description:
#!      Sets up over theme and window configuration.
#! ===================================================================
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

WINDOW_WIDTH = "700"
WINDOW_HEIGHT = "400"

root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
root_tk.geometry(WINDOW_WIDTH + "x" + WINDOW_HEIGHT) # Set window dimenstions
root_tk.resizable(width=False, height=False) # Prevent window resizing
root_tk.title("Time Sheet") # Set window title

if (platform == "linux" or platform == "linux2" or platform == "darwin"):
    icon = tkinter.PhotoImage(file='public/clock-icon.png')
elif (platform == "win32"):
    icon = tkinter.PhotoImage(file='public\clock-icon.png')
    
root_tk.iconphoto(True, icon)

def refreshWindow():
    root_tk.destroy()
    os.system('python Time_Sheet.py')

#! ===================== ROCKET CHAT API SETUP =======================
#! Description:
#!      Sets up the Rocket Chat API.
#! ===================================================================
apiInfo = {}
api = ""
rocketchat_rooms = {}
def saveApiData():
    jsonString = json.dumps(apiInfo)
    jsonFile = open("apiInfo.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

apiDataMissing = True
while(apiDataMissing):
    try:
        apiDataFile = open("apiInfo.json")
        apiInfo = json.load(apiDataFile)
        apiDataMissing = False
        if(apiInfo['token'] != "" or apiInfo['userId'] != ''):
            try:
                print("Connecting")
                apiSettings = {'token': apiInfo.get("token"), 'user_id': apiInfo.get("userId"), 'domain': apiInfo.get("domain")}
                api = RocketChatAPI(settings=apiSettings)
                user = api.get_my_info()
                apiSettings['username'] = user.get('username')
                api.settings=apiSettings

                rooms = api.get_im_rooms()               
                for x in rooms:
                    for y in x['usernames']:
                        if(y != apiSettings['username']):
                            rocketchat_rooms[y] = x['_id']
                apiInfo.update({"isLoggedIn": True})
                apiInfo.update({"correctCreds": True})
            except:
                apiInfo.update({"isLoggedIn": False})
                apiInfo.update({"correctCreds": False})

            saveApiData()
    except:
        apiInfo = {
            "token": "",
            "userId": "",
            "domain": "https://digitaldreamforge.chat/",
            "isLoggedIn": False,
            "correctCreds": True
        }
        saveApiData()
        apiDataMissing = True
        apiIsLoggedIn = False

#! ======================== DISCONNECT API ===========================
#! Description:
#!      Removes API user info from files.
#! ===================================================================
def disconnect_rocket_chat():
    apiInfo.update({
            "token": "",
            "userId": "",
            "domain": "https://digitaldreamforge.chat/",
            "isLoggedIn": False,
            "correctCreds": True
        })
    saveApiData()
    refreshWindow()

#! =========================== CONNECT API ===========================
#! Description:
#!      Updates the apiInfo file and refreshes the app with the new
#!      connection info.
#! ===================================================================
def connect_api():
    preferences.update({"messagingEnabled": True})
    savePreferences()
    apiInfo.update({"token": token.get()})
    apiInfo.update({"userId": userId.get()})
    saveApiData()
    refreshWindow()

#! ===================== CONNECT ROCKET CHAT =========================
#! Description:
#!      Creates the subwindow to put in API information.
#! ===================================================================
def connect_rocket_chat():
    apiInfo.update({"correctCreds": True})
    apiInfo.update({"token": ""})
    apiInfo.update({"userId": ""})
    saveApiData()
    settingsWindow = customtkinter.CTkToplevel(root_tk)
    settingsWindow.geometry(WINDOW_WIDTH + "x" + WINDOW_HEIGHT)
    settingsWindow.resizable(width=False, height=False)
    settingsWindow.title("Connect to Rocket Chat")

    apiTitle = customtkinter.CTkLabel(master=settingsWindow, text="Conenct to Rocket Chat", text_font=("Roboto Medium", -24))
    apiTitle.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

    apiStepsTitle = customtkinter.CTkLabel(master=settingsWindow, text="Instructions:", text_font=("Roboto Medium", -16))
    apiStepsTitle.place(relx=0.15, rely=0.2, anchor=tkinter.CENTER)

    apiSteps = customtkinter.CTkLabel(master=settingsWindow, text="1. Click your profile image in Rocket Chat.\n\n" +
                                                             "2. Click the My Account button.\n\n" +
                                                             "3. Click the Personal Access Tokens button.\n\n" +
                                                             "4. Type in a title of your choice in the text box.\n\n" +
                                                             "5. Click the Ignore Two Factor Authentication\n" +
                                                             "    checkbox so that is is checked.\n\n" +
                                                             "6. Click the Add button.\n\n" +
                                                             "7. Copy your UserId and paste it to the right.\n\n" +
                                                             "8. Copy your Token and past it to the right.\n\n" + 
                                                             "9. Click Connect.",
                                                             justify=tkinter.LEFT)
    apiSteps.place(relx=0.3, rely=0.6, anchor=tkinter.CENTER)

    global userId
    userId = customtkinter.CTkEntry(master=settingsWindow, placeholder_text="UserId", width=200)
    userId.place(relx=0.75, rely=0.4, anchor=tkinter.CENTER)

    global token
    token = customtkinter.CTkEntry(master=settingsWindow, placeholder_text="Token", width=200)
    token.place(relx=0.75, rely=0.5, anchor=tkinter.CENTER)

    submitAPI = customtkinter.CTkButton(master=settingsWindow, text="Connect",  command=connect_api)
    submitAPI.place(relx=0.75, rely=0.6, anchor=tkinter.CENTER)

#! ====================== FIND PAY PERIOD START ======================
#! Description:
#!      Locates the start of the pay period.
#! ===================================================================
def findPayPeriodStart():
    initial = datetime(2022, 5, 2)
    today = datetime.today().strftime("%m-%d-%Y")
    today = datetime.strptime(today, "%m-%d-%Y")
    start = initial
    startFound = False
    while(not startFound):
        newStart = initial + timedelta(days=14)
        if(newStart == today):
            start = newStart
            startFound = True
        elif(newStart > today):
            start = initial
            startFound = True
        else:
            initial = newStart

    return start.strftime("%m-%d-%Y")

#! ========================= SAVE TEMP DATA ==========================
#! Description:
#!      Saves temp data passed to it for any data that needs to 
#!      persist if the application is closed or crashes.
#! ===================================================================
tempData = {}
def saveTempData():
    jsonString = json.dumps(tempData)
    jsonFile = open("temp.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

#! =================== TEMP DATA INITIAL SETUP =======================
#! Description:
#!      Initializes the temp data file and preloads the initial
#!      data.
#! ===================================================================
tempDataMissing = True
while(tempDataMissing):
    try:
        tempDataFile = open("temp.json")
        tempData = json.load(tempDataFile)
        tempDataMissing = False
    except:
        tempData = {
            "onBreak": False,
            "payPeriodStart" : findPayPeriodStart()
        }
        saveTempData()
        tempDataMissing = True

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
            dayTimeSheet.update({"clockOut": "06:00PM"})
        calculateHours()
        setUserDayTime("update")

#! ========================== CHECK DATES ============================
#! Description:
#!      Checks if there is a gap between the last date that was
#!      clocked in and the current date. If a discrepancy is found
#!      then the dates in between are filled with blank timestamps.
#! ===================================================================
def checkDates():
    tempData.update({'payPeriodStart': findPayPeriodStart()})
    saveTempData()
    payPeriodStart = datetime.strptime(tempData['payPeriodStart'], "%m-%d-%Y")
    
    currentDate = datetime.now()
    lastClockedDate = timeSheet.get("time")[len(timeSheet.get("time")) - 1].get("date")
    
    if(lastClockedDate != ""):
        lastDate = datetime.strptime(lastClockedDate, "%m-%d-%Y")
    
    if(lastClockedDate != "" and lastDate < currentDate and lastDate >= payPeriodStart):
        timeSpan = currentDate - lastDate
        timeSpan = timeSpan.days
        newDate = datetime.strptime(lastClockedDate, "%m-%d-%Y")
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
    
    # Will be called if the time data is empty for the pay period
    elif(lastClockedDate == ''):
        timeSpan = currentDate - payPeriodStart
        timeSpan = timeSpan.days
        newDate = payPeriodStart
        for i in range(timeSpan + 1):
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
                if(i == 0):
                    timeSheet.get("time")[len(timeSheet.get("time")) - 1] = tempTime.copy()
                else:
                    timeSheet.get("time").append(tempTime)
            newDate += timedelta(days=1)

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
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Day Start ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Clock In message Sent.")

def lunch_out():
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    setTimestamp(1)
    getLunchOutLabel()
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Lunch Start ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Lunch Start message sent.")
    if(preferences['notificationsEnabled']):
        if(masterNotificationEnabled):
            notificationCountdown(60)

def lunch_in():
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    setTimestamp(2)
    getLunchInLabel()
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Lunch End ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Lunch End message sent.")

def clock_out():
    clockIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    setTimestamp(3)
    getClockOutLabel()
    checkEndOfPeriod()
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Day End ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Day End message sent.")

def break_out():
    breakOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    clockOut.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    lunchIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    breakIn.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    tempData.update({'onBreak': True})
    saveTempData()
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Break Start ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Break Start message sent.")
    if(preferences['notificationsEnabled']):
        if(masterNotificationEnabled):
            notificationCountdown(15)

def break_in():
    breakOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    if(dayTimeSheet.get("lunchIn") == "" and datetime.today().date() == datetime.strptime(dayTimeSheet.get("date"), "%m-%d-%Y").date()):
        lunchOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    clockOut.configure(state=tkinter.NORMAL, fg_color=btnColor01)
    breakIn.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
    tempData.update({'onBreak': False})
    saveTempData()
    if(preferences["messagingEnabled"]):
        if(masterMessagingEnabled):
            api.send_message('Break End ' + userData.get('project'), rocketchat_rooms[chatroom])
            print("Break End message sent.")

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

#! ======================= TOGGLE MESSAGING ==========================
#! Description:
#!      Turn messaging on or off.
#! ===================================================================
def toggle_messaging():
    if(toggleMessaging.get() == "on"):
        preferences.update({"messagingEnabled": True}) 
    else:
        preferences.update({"messagingEnabled": False}) 
    savePreferences()

#! ==================== TOGGLE NOTIFICATIONS =========================
#! Description:
#!      Turn notifications on or off.
#! ===================================================================
def toggle_notifications():
    if(toggleNotifications.get() == "on"):
        preferences.update({"notificationsEnabled": True}) 
    else:
        preferences.update({"notificationsEnabled": False}) 
    savePreferences()
    
#! ======================== SOUND FUNCTIONS ==========================
#! Description:
#!      Handle sound capabilities.
#! ===================================================================
playIcon = tkinter.PhotoImage(file='./public/playIcon.png')
stopIcon = tkinter.PhotoImage(file='./public/stop.png')
def stop_sound():
    pygame.mixer.Sound.stop(audio)
    playSoundBtn.set_image(playIcon)
    playSoundBtn.configure(command=play_sound)
    root_tk.update()

def beginSoundLoop():
    while(pygame.mixer.get_busy()):
        playSoundBtn.set_image(stopIcon)
        playSoundBtn.configure(command=stop_sound)
        root_tk.update()
    playSoundBtn.set_image(playIcon)
    playSoundBtn.configure(command=play_sound)
    root_tk.update()

def playNotification(sound, sample):
    soundFile = "./public/sounds/" + sound
    pygame.mixer.init()
    global audio
    audio = pygame.mixer.Sound(soundFile)
    pygame.mixer.Sound.play(audio)
    if(sample):
        beginSoundLoop()

def kill():
    print("KILLING APP")
    root_tk.quit()
    root_tk.destroy()

def notificationCountdown(delay):
    notificationTime = (datetime.now() + timedelta(minutes=delay)) - timedelta(minutes=2)
    while(datetime.now() <= notificationTime):
        root_tk.protocol("WM_DELETE_WINDOW", kill)
        if(delay == 15 and not tempData['onBreak'] or delay == 60 and dayTimeSheet.get("lunchIn") != ''):
            print("STOPPING")
            break
        root_tk.update()
        time.sleep(0.1)
    if(datetime.now() >= notificationTime):
        playNotification(preferences['notificationSound'], False)

def sound_select(option):
    preferences.update({"notificationSound": option})
    savePreferences()
    stop_sound()

def play_sound():
    sound = soundSelect.get()
    playNotification(sound, True)

#! ========================= CLOSE SETTINGS ==========================
#! Description:
#!      Close the settings window.
#! ===================================================================
def close_settings():
    settingsFrame.destroy()
    settingsTitle.destroy()
    settingsExitBtn.destroy()
    toggleMessaging.destroy()
    toggleNotifications.destroy()
    soundSelect.destroy()
    playSoundBtn.destroy()
    connectRCSettings.destroy()
    disconnectRCSettings.destroy()

#! ========================== OPEN SETTINGS ==========================
#! Description:
#!      Open the settings window.
#! ===================================================================
def open_settings():
    global settingsFrame
    global settingsTitle
    global settingsExitBtn
    global toggleMessaging
    global toggleNotifications
    global soundSelect
    global playSoundBtn
    global connectRCSettings
    global disconnectRCSettings
    
    # Place frame on top of existing window
    settingsFrame = customtkinter.CTkFrame(master=root_tk, width=int(WINDOW_WIDTH), height=int(WINDOW_HEIGHT), corner_radius=0, fg_color="#212325")
    settingsFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    
    # Set title
    settingsTitle = customtkinter.CTkLabel(master=root_tk, text="Settings", text_font=("Roboto Medium", -24))
    settingsTitle.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
    
    # Set the X icon
    exitIcon = tkinter.PhotoImage(file='./public/xIcon.png')
    settingsExitBtn = customtkinter.CTkButton(master=root_tk, text="", width=35, height=35, fg_color="#212325", command=close_settings)
    settingsExitBtn.set_image(exitIcon)
    settingsExitBtn.place(relx=0.94, rely=0.08, anchor=tkinter.CENTER)

    # Set the toggle messaging switch
    toggleMessaging = customtkinter.CTkSwitch(master=root_tk, text="Messaging", command=toggle_messaging, onvalue="on", offvalue="off")
    toggleMessaging.place(relx=0.3, rely=0.3, anchor=tkinter.CENTER)
    if(preferences["messagingEnabled"]):
        toggleMessaging.toggle()

    # Set the toggle notification switch
    toggleNotifications = customtkinter.CTkSwitch(master=root_tk, text="Notifications", command=toggle_notifications, onvalue="on", offvalue="off")
    toggleNotifications.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)
    if(preferences["notificationsEnabled"]):
        toggleNotifications.toggle()    

    # Notification Sound settings
    soundOptions = []

    if (platform == "linux" or platform == "linux2" or platform == "darwin"):
        sounds = os.scandir('public/sounds')
    elif (platform == "win32"):
        sounds = os.scandir('public\sounds')
    for x in sounds:
        if(x.is_file and x.path.endswith(".mp3")):
            soundOptions.append(x.name)
    currentSound = customtkinter.StringVar(value=preferences["notificationSound"])
    
    soundSelect = customtkinter.CTkOptionMenu(master=root_tk, values=soundOptions, variable=currentSound, command=sound_select, width=250)
    soundSelect.place(relx=0.6, rely=0.4, anchor=tkinter.CENTER)

    playSoundBtn = customtkinter.CTkButton(master=root_tk, text="", width=35, height=35, fg_color="#212325", command=play_sound)
    playSoundBtn.set_image(playIcon)
    playSoundBtn.place(relx=0.83, rely=0.4, anchor=tkinter.CENTER)

    # Set the Rocket Chat connect button
    connectRCSettings = customtkinter.CTkButton(master=root_tk, text="Connect Rocket Chat", width=200, command=connect_rocket_chat)
    connectRCSettings.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

    # Set the Rocket Chat disconnect button
    disconnectRCSettings = customtkinter.CTkButton(master=root_tk, text="Disonnect Rocket Chat", width=200, fg_color=btnDisabledColor, command=disconnect_rocket_chat, state=tkinter.DISABLED)
    disconnectRCSettings.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
    if(apiInfo["isLoggedIn"]):
        connectRCSettings.configure(state=tkinter.DISABLED, fg_color=btnDisabledColor)
        disconnectRCSettings.configure(state=tkinter.NORMAL, fg_color=endPeriodBtnColor, hover_color=endPeriodBtnHoverColor)

#! ===================== SETTINGS ICON ELEMENT =======================
#! Description:
#!      Puts the settings icon in the top right corner.
#! ===================================================================
settingsIcon = tkinter.PhotoImage(file='./public/settingsSmall.png')
settingsBtn = customtkinter.CTkButton(master=root_tk, text="", width=35, height=35, fg_color="#212325", command=open_settings)
settingsBtn.set_image(settingsIcon)
settingsBtn.place(relx=0.94, rely=0.08, anchor=tkinter.CENTER)

#! ======================= SKIP API CONNECT ==========================
#! Description:
#!      Allows the user to bypass the API connection.
#! ===================================================================
def skip_API_connect():
    preferences.update({"messagingEnabled": False})
    savePreferences()
    refreshWindow()

#! ====================== API CONNECT START ==========================
#! Description:
#!      Show the API connection page if the user is not connected,
#!      and the user has not disabled messaging.
#! ===================================================================
if(not apiInfo['isLoggedIn'] and preferences["messagingEnabled"]):
    frame = customtkinter.CTkFrame(master=root_tk, width=int(WINDOW_WIDTH), height=int(WINDOW_HEIGHT), corner_radius=0)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    if(not apiInfo['correctCreds']):
        errorMsg = customtkinter.CTkLabel(master=root_tk, text="Error: Token or UserID invalid.\n Please Try again.", bg_color="#2E2E2E", text_color=endPeriodBtnColor, text_font=("Roboto Medium", -15))
        errorMsg.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    connectRC = customtkinter.CTkButton(master=root_tk, text="Connect Rocket Chat", bg_color="#2E2E2E", width=200, command=connect_rocket_chat)
    connectRC.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
    exitBtn = customtkinter.CTkButton(master=root_tk, text="Don't Connect", width=200, bg_color="#2E2E2E", fg_color=endPeriodBtnColor, hover_color=endPeriodBtnHoverColor, command=skip_API_connect)
    exitBtn.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

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