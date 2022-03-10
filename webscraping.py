from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

PATH = r"C:\Users\natha\milesplitws\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://oh.milesplit.com/login?")

#logining in to milesplit
username = driver.find_element(By.ID, "email")
password = driver.find_element(By.ID, "password")

username.send_keys("username")
password.send_keys("password")
time.sleep(3)
driver.find_element(By.ID, "frmSubmit").click()
time.sleep(5)
driver.get("https://oh.milesplit.com/teams/9910-brecksville")
time.sleep(3)

dropdownEle = driver.find_element(By.ID, "scheduleSeasonYear")
options = dropdownEle.find_elements(By.TAG_NAME, "option")
options_list = [i.text for i in options]

dates = []
athletes = []
times = []
genders = []



for i in range(len(options_list)):
    driver.get("https://oh.milesplit.com/teams/9910-brecksville")
    dropdownEle = driver.find_element(By.ID, "scheduleSeasonYear")
    options = dropdownEle.find_elements(By.TAG_NAME, "option")
    dropdownEle.click()
    options[i].click()
    time.sleep(3)
    results = driver.find_elements(By.XPATH, "//div[4]/a[1]")
    results_list = [i.text for i in results]
    results_items = [i.get_attribute("href") for i in results]

    for u in range(len(results_items)):
        driver.get(results_items[u])
        time.sleep(3)
        date = driver.find_element(By.CSS_SELECTOR, "time").text

        driver.find_element(By.LINK_TEXT, "Teams").click()
        time.sleep(2)
        #location = driver.find_element(By.PARTIAL_LINK_TEXT, "Brecksville")
        #right = driver.find_element(locate_with(By.PARTIAL_LINK_TEXT, "Results").to_right_of(location))
        #right.click()
        findBville = driver.find_elements(By.LINK_TEXT, "Results")
        findBvilleText = [i.get_attribute("href") for i in findBville]
        for d in findBvilleText:
            if "9910" in d:
                driver.get(d)
        time.sleep(3)

        data = driver.find_elements(By.CSS_SELECTOR, "tr")
        dataList = [i.text for i in data]
        if 'BOYS ATHLETE PLACE RESULTS' in dataList:
            boyIndex = dataList.index('BOYS ATHLETE PLACE RESULTS')
        else:
            boyIndex = 1000

        for k in dataList:
            if k[2] != ":":
                continue
            if dataList.index(k) > boyIndex:
                gender = "boy"
            else:
                gender = "girl"

            clock = k[:k.index(" ")]
            kSplit = k.split()
            if kSplit[1] == "SB":
                kSplit.remove(kSplit[1])
            name = kSplit[1] + " " + kSplit[2]

            dates.append(date)
            athletes.append(name)
            times.append(clock)
            genders.append(gender)

        time.sleep(5)


print(dates)
print(athletes)
print(times)
print(genders)

df = pd.DataFrame({'date': dates, 'athlete': athletes, 'time': times, 'gender': genders})
df.to_csv('xcData.csv', index=False, encoding='utf-8')







#driver.find_element(By.XPATH, "//select[@id='scheduleSeasonYear']/option").click()








