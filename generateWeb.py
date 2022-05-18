from selenium import webdriver
import time
import json
from datetime import datetime, timedelta
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# load JSON file with input information
today = datetime.today()
payStart = (today - timedelta(days=14)).strftime("%m-%d-%Y")
payPeriodFile = payStart + " - " + today.strftime("%m-%d-%Y")
file = open("Sheets/" + payPeriodFile + ".json")
data = json.load(file)
userInfo = data.get("userInfo")
timeSheetInfo = data.get("time")

# load the website
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.maximize_window()
# driver.get("http://timesheet.digitaldreamforge.tools")
driver.get("http://previoustimesheet.digitaldreamforge.tools")

# close info prompt
time.sleep(2)
close_info_prompt = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/button")
close_info_prompt.click()

def find_and_enter(loc, entry):
    field = driver.find_element_by_id(loc)
    field.clear()
    field.send_keys(entry)

""" Top """
# Name field
find_and_enter("field_name1", userInfo.get("name"))

# Supervisor field
find_and_enter("field_name2", userInfo.get("supervisor"))

""" Week 1 """
y = 1
index = 0
for x in range(1, 6):
    # start time
    find_and_enter("field_" + str(y), timeSheetInfo[index].get("clockIn"))
    # lunch out
    find_and_enter("field_" + str(y+1), timeSheetInfo[index].get("lunchOut"))
    # lunch back
    find_and_enter("field_" + str(y+2), timeSheetInfo[index].get("lunchIn"))
    # end of day
    find_and_enter("field_" + str(y+3), timeSheetInfo[index].get("clockOut"))
    # reg hours
    find_and_enter("field_" + str(y+6), timeSheetInfo[index].get("regularHrs"))
    # overtime hours
    find_and_enter("field_" + str(y+7), timeSheetInfo[index].get("overtimeHrs"))
    # project
    find_and_enter("field_" + str(y+8), timeSheetInfo[index].get("project"))
    # initials
    find_and_enter("field_" + str(y+9), userInfo.get("initials"))
    y += 10
    index += 1

""" Week 2 """
y = 71
for x in range(1, 6):
    # start time
    find_and_enter("field_" + str(y), timeSheetInfo[index].get("clockIn"))
    # lunch out
    find_and_enter("field_" + str(y+1), timeSheetInfo[index].get("lunchOut"))
    # lunch back
    find_and_enter("field_" + str(y+2), timeSheetInfo[index].get("lunchIn"))
    # end of day
    find_and_enter("field_" + str(y+3), timeSheetInfo[index].get("clockOut"))
    # reg hours
    find_and_enter("field_" + str(y+6), timeSheetInfo[index].get("regularHrs"))
    # overtime hours
    find_and_enter("field_" + str(y+7), timeSheetInfo[index].get("overtimeHrs"))
    # project
    find_and_enter("field_" + str(y+8), timeSheetInfo[index].get("project"))
    # initials
    find_and_enter("field_" + str(y+9), userInfo.get("initials"))
    y += 10
    index += 1