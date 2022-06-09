import tkinter
import customtkinter
import json

class edit_times:

    WINDOW_HEIGHT = "600"
    WINDOW_WIDTH = "900"

    FRAME_COLOR = "#212325"

    todaysHours = {}
    totalHours = {}

    def __init__(self, root):
        self.root_tk = root
        self.windowFrame = customtkinter.CTkFrame(master=root, width=int(self.WINDOW_WIDTH), height=int(self.WINDOW_HEIGHT), corner_radius=0, fg_color=self.FRAME_COLOR)
        exitIcon = tkinter.PhotoImage(file='./public/xIcon.png')
        self.exitBtn = customtkinter.CTkButton(master=root, text="", width=35, height=35, fg_color=self.FRAME_COLOR, command=self.destroyWindow)
        self.exitBtn.set_image(exitIcon)
        self.saveBtn = customtkinter.CTkButton(master=root, text="Save", width=200, command=self.updateTimeSheet)      
        
        # Day of the week labels
        self.week01DayLabels = {
            "Mon": customtkinter.CTkLabel(master=root, text="Monday", width=50, text_font=("Roboto Medium", -15)),
            "Tue": customtkinter.CTkLabel(master=root, text="Tuesday", width=50, text_font=("Roboto Medium", -15)),
            "Wed": customtkinter.CTkLabel(master=root, text="Wednesday", width=50, text_font=("Roboto Medium", -15)),
            "Thu": customtkinter.CTkLabel(master=root, text="Thursday", width=50, text_font=("Roboto Medium", -15)),
            "Fri": customtkinter.CTkLabel(master=root, text="Friday", width=50, text_font=("Roboto Medium", -15))
        }

        self.week02DayLabels = {
            "Mon": customtkinter.CTkLabel(master=root, text="Monday", width=50, text_font=("Roboto Medium", -15)),
            "Tue": customtkinter.CTkLabel(master=root, text="Tuesday", width=50, text_font=("Roboto Medium", -15)),
            "Wed": customtkinter.CTkLabel(master=root, text="Wednesday", width=50, text_font=("Roboto Medium", -15)),
            "Thu": customtkinter.CTkLabel(master=root, text="Thursday", width=50, text_font=("Roboto Medium", -15)),
            "Fri": customtkinter.CTkLabel(master=root, text="Friday", width=50, text_font=("Roboto Medium", -15))
        }

        self.clockTypeLabels = {
            "Clock In": customtkinter.CTkLabel(master=root, text="Clock In", width=50, text_font=("Roboto Medium", -15)),
            "Lunch Out": customtkinter.CTkLabel(master=root, text="Lunch Out", width=50, text_font=("Roboto Medium", -15)),
            "Lunch In": customtkinter.CTkLabel(master=root, text="Lunch In", width=50, text_font=("Roboto Medium", -15)),
            "Clock Out": customtkinter.CTkLabel(master=root, text="Clock Out", width=50, text_font=("Roboto Medium", -15)),
        }

        # Time stamp boxes
        self.week01TimeStamps = {
            'Mon': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Tue': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Wed': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Thu': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Fri': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
        }

        self.week02TimeStamps = {
            'Mon': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Tue': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Wed': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Thu': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
            'Fri': {
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100),
                customtkinter.CTkEntry(master=root, width=100)
            },
        }

    def getCurrentTimeStamps(self):
        jsonFile = open("timeData.json", "r")
        self.totalHours = json.load(jsonFile)['time']
        

    def updateTimeSheet(self):
        for x in self.totalHours:
            print(x)
        self.recalculateHours
        # TODO: set today's hours
        # TODO: Get all values in text boxes and save them to timeData.json
        self.destroyWindow()

    def createWindow(self):
        self.getCurrentTimeStamps()
        self.root_tk.geometry(self.WINDOW_WIDTH + "x" + self.WINDOW_HEIGHT)
        self.windowFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.createDayLabels()
        self.createClockTypeLabels()
        self.createTimeStampBoxes()
        self.exitBtn.place(relx=0.94, rely=0.08, anchor=tkinter.CENTER)
        self.saveBtn.place(relx=0.84, rely=0.92, anchor=tkinter.CENTER)

    def createDayLabels(self):
        index = 0
        for x in self.week01DayLabels:
            self.week01DayLabels[x].place(relx=0.15, rely=0.2 + index, anchor=tkinter.CENTER)
            index += 0.05
        index += 0.1
        for x in self.week02DayLabels:
            self.week02DayLabels[x].place(relx=0.15, rely=0.2 + index, anchor=tkinter.CENTER)
            index += 0.05

    def createClockTypeLabels(self):
        index = 0
        for x in self.clockTypeLabels:
            self.clockTypeLabels[x].place(relx=0.3 + index, rely=0.15, anchor=tkinter.CENTER)
            index += 0.15

    def createTimeStampBoxes(self):
        yindex = 0
        xindex = 0
        timeStamp = 0
        dateIndex = 0
        for x in self.week01TimeStamps:
            for y in self.week01TimeStamps[x]:
                y.place(relx=0.3 + xindex, rely=0.2 + yindex, anchor=tkinter.CENTER)
                if (timeStamp == 0 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['clockIn'])
                elif (timeStamp == 1 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['lunchOut'])
                elif (timeStamp == 2 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['lunchIn'])
                elif (timeStamp == 3 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['clockOut'])
                xindex += 0.15
                timeStamp += 1
            dateIndex += 1
            timeStamp = 0
            xindex = 0
            yindex += 0.05
        yindex += 0.1
        for x in self.week02TimeStamps:
            for y in self.week02TimeStamps[x]:
                y.place(relx=0.3 + xindex, rely=0.2 + yindex, anchor=tkinter.CENTER)
                if (timeStamp == 0 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['clockIn'])
                elif (timeStamp == 1 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['lunchOut'])
                elif (timeStamp == 2 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['lunchIn'])
                elif (timeStamp == 3 and dateIndex < len(self.totalHours)):
                    y.insert(0, self.totalHours[dateIndex]['clockOut'])
                xindex += 0.15
                timeStamp += 1
            dateIndex += 1
            timeStamp = 0
            xindex = 0
            yindex += 0.05

    def destroyWindow(self):
        self.root_tk.geometry("700x400")
        self.windowFrame.destroy()
        self.destroyDayLabels()
        self.destroyClockTypeLabels()
        self.destroyTimeStampBoxes()
        self.exitBtn.destroy()
        self.saveBtn.destroy()
        # TODO: Destroy text entry boxes 

    def destroyDayLabels(self):
        for x in self.week01DayLabels:
            self.week01DayLabels[x].destroy()
        for x in self.week02DayLabels:
            self.week02DayLabels[x].destroy()

    def destroyClockTypeLabels(self):
        for x in self.clockTypeLabels:
            self.clockTypeLabels[x].destroy()


    def destroyTimeStampBoxes(self):
        for x in self.week01TimeStamps:
            for y in self.week01TimeStamps[x]:
                y.destroy()
        for x in self.week02TimeStamps:
            for y in self.week02TimeStamps[x]:
                y.destroy()

    def recalculateHours(self):
        pass