from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


###############
##APPLICANT ID#
a = 13


#look up which jobs to apply to
index = int(str(a)[0])
xlsx = pd.ExcelFile('/users/nathanevans/Dropbox/Senior/Thesis/Python Application/Destinations.xlsx')
df1 = pd.read_excel(xlsx, 'Sheet1')
df2 = pd.read_excel(xlsx, 'Sheet4')
cities = []
for i in range(len(df1)):
    if df1[index][i]==a:
        cities.append(df1['City'][i].replace(u'\xa0', u' '))

for i in range(len(df2)):
    if df2['A'][i]==a:
        email = df2['Email'][i]

#go to the site and log in
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.careerbuilder.com/")
elem = driver.find_element_by_id("signin-link")
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "signin-link")))
elem.click()
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cbsys_login_email")))
elem.send_keys("nathan01944@gmail.com")
elem = driver.find_element_by_id("cbsys_login_password")
elem.send_keys("Shelby!234")
elem = driver.find_element_by_name("btnsigninemp")
elem.click()


tOpen = []
jobTitle = []
jobEmployer = []
jobLocation = []
jobSched = []
nth = []
searchLocation = []



#now you have logged in
#loop through cities
totJobsApplied = 0
cityIndex = -1
while totJobsApplied<400:
    cityIndex+=1
    location = cities[cityIndex]
    link = "https://www.careerbuilder.com/jobs?posted=30&pay=&radius=30&emp=&cb_apply=true&keywords=&location=" + location
    driver.get(link)

    #sometimes it goes back to the no location page??? why???
    time.sleep(5)
    driver.get(link)

    ###LOOP THROUGH ALL THE JOBS!!!####
    #loop through all pages
    jobsInThisCity = 0
    i =1
    j=1
    while jobsInThisCity<40:
        #go to next webpage if it would be off curent page
        if i==26:
            j+=1
            link = 'https://www.careerbuilder.com/jobs?cb_apply=true&emp=&keywords=&location=' + location + '&page_number=' + str(j) + '&pay=&posted=30&radius=30'
            driver.get(link)
            time.sleep(2)
            i = 1
        prefix='//*[@id="jobs_collection"]/div['+str(i)+']/a[2]'
            
        xpEmp = '//*[@id="jobs_collection"]/div['+str(i)+']/a[2]/div/div[2]/div[3]/span[1]'
        
        try:
            employer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpEmp))).text
            OutofJobsInCity = 0
        except:
            OutofJobsInCity =1
        if OutofJobsInCity==0:
            if employer in ['Full Time', 'Part Time']:
                employer = ''
            #if employer is already there, do nothing
            if employer in jobEmployer:
                pass
            #if employer isnt there yet, get all data, and then go to opening and apply
            else:
                ##############
                #get data
                #Time since open
                try:
                    tOpen1 = driver.find_element_by_xpath(prefix+ '/div/div[2]/div[1]').text
                except:
                    tOpen1 = ''
                #Job Title
                try:
                    jobTitle1 = driver.find_element_by_xpath(prefix+ '/div/div[2]/div[2]').text
                except:
                    jobTitle1 = ''
                #employer
                try:
                    jobEmployer1 = employer
                except:
                    jobEmployer1 = ''
                #location
                try:
                    jobLocation1 = driver.find_element_by_xpath(prefix+ '/div/div[2]/div[3]/span[2]').text
                except:
                    jobLocation1 = ''
                #Schedule
                try:
                    jobSched1 = driver.find_element_by_xpath(prefix+ '/div/div[2]/div[3]/span[3]').text
                except:
                    jobSched.append('')
                nth1 = str(j)+'-'+str(i)
                searchLocation1 = location
                
                ############
                #apply#####

                try:
                    #click on job
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, prefix))).click()
                    time.sleep(1)
                
                    #click apply
                    ##apply if the job isn't timed out (WHY WOULD THEY LET YOU SEE TIMED OUT JOBS?)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hide-fixed-top"]/a'))).click()
                    
                    #sometimes you need to click a few more things
                    try:
                        xpath = '//*[@id="upload-resume"]'
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                    
                        xpath = '/html/body/div[2]/div[1]/div/div[3]/div[2]/div/form/ng-form/div[4]/ng-form/div/div/button'
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
                    except:
                        pass

                except:
                    success=0
                    
                #did you successfully apply?
                print('trying now')
                currentURL = driver.current_url
                if 'recommended' in currentURL:
                    success=1
                else:
                    success=0
                    
                if success==1:
                    #write down the data
                    tOpen.append(tOpen1)
                    jobTitle.append(jobTitle1)
                    jobEmployer.append(jobEmployer1)
                    jobLocation.append(jobLocation1)
                    jobSched.append(jobSched1)
                    nth.append(nth1)
                    searchLocation.append(searchLocation1)
                    
                    totJobsApplied+=1
                    jobsInThisCity+=1
                    print(jobTitle[-1])
                    print(str(totJobsApplied)+ ' total jobs - ' + str(jobsInThisCity)+' in '+location)
                #if the job was timed out you don't add it to list of applied jobs
                if success==0:
                    print('unsuccessful app')


                driver.get(link)
                

                
                
            i+=1
        else:
            #break the loop by setting jobs in this city to 40
            jobsInThisCity=40



data = {'tOpen': tOpen, 'jobtitle': jobTitle, 'employer': jobEmployer, 'location': jobLocation, 'schedule': jobSched, 'n':nth, 'searchLocation': searchLocation}
df = pd.DataFrame(data, columns=['tOpen', 'jobtitle', 'employer','location','schedule','n','searchLocation'])

df.to_excel('/users/nathanevans/Documents/Senior/Thesis/Python Application/JobApplications' + str(a)+'.xlsx',sheet_name='Sheet1')

