from selenium import webdriver
import time
import json

# load JSON file with input information
with open('C:\WebDriver\\auto_timesheet\\timesheet.JSON') as f:
    data = json.load(f)

# load the website
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.maximize_window()
# driver.get("http://timesheet.digitaldreamforge.tools")  #05-05-22 stayed until 7pm #05-06-22 left at 3:30pm
driver.get("http://previoustimesheet.digitaldreamforge.tools")

# close info prompt
time.sleep(2)
close_info_prompt = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[3]/button")
close_info_prompt.click()

def find_and_enter(loc, key):
    field = driver.find_element_by_id(loc)
    entry = data.get(key)
    field.clear()
    field.send_keys(entry)

""" Top """
# Name field
find_and_enter("field_name1", "name")

# Supervisor field
find_and_enter("field_name2", "supervisor")

""" Week 1 """
y = 1
for x in range(1, 6):
    # start time
    find_and_enter("field_" + str(y), "starttime")
    # lunch out
    find_and_enter("field_" + str(y+1), "lunchout")
    # lunch back
    find_and_enter("field_" + str(y+2), "lunchback")
    # end of day
    find_and_enter("field_" + str(y+3), "endofday")
    # reg hours
    find_and_enter("field_" + str(y+6), "reghours")
    # project
    find_and_enter("field_" + str(y+8), "project")
    # initials
    find_and_enter("field_" + str(y+9), "initials")
    y += 10

""" Week 2 """
y = 71
for x in range(1, 6):
    # start time
    find_and_enter("field_" + str(y), "starttime")
    # lunch out
    find_and_enter("field_" + str(y+1), "lunchout")
    # lunch back
    find_and_enter("field_" + str(y+2), "lunchback")
    # end of day
    find_and_enter("field_" + str(y+3), "endofday")
    # reg hours
    find_and_enter("field_" + str(y+6), "reghours")
    # project
    find_and_enter("field_" + str(y+8), "project")
    # initials
    find_and_enter("field_" + str(y+9), "initials")
    y += 10