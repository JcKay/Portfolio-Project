from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from time import sleep

### CREATE SELENIUM OBJECT AND CALL MAIN PAGE###
town_city = input('Search Box (multi search using ", ") :> ')
search_target = input('Search Object :: ')
google_map = "https://maps.google.com/"
s = Service('/usr/local/bin/chromedriver')
browser = webdriver.Chrome(service=s)
browser.get(google_map)
# browser.maximize_window()
sleep(4)
seach_box = browser.find_element(By.XPATH, '//*[@id="searchboxinput"]')
seach_box.send_keys(town_city)
seach_box.send_keys(Keys.ENTER)
sleep(4)
clear_btn = browser.find_element(By.XPATH, '//*[@id="searchbox"]/a').click()
seach_box.send_keys(search_target)
seach_box.send_keys(Keys.ENTER)
sleep(4)


### SCROLL DEF TO DO SCROLL EVERY LOOP ###
def scroll_list():
    scroll = browser.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]')
    for i in range(4):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
        # print("scrolling scrolling")
        sleep(0.5)
    # make card list
    card_list = browser.find_elements(By.CLASS_NAME, 'V0h1Ob-haAclf')
    return card_list


n = 1
### MAIN LISTS THAT CONTAIN ALL OF OBJECTS ###
name = []
rating = []
people = []
services = []
phone = []
titles = []
address = []
websites = []
working_hour = []
PROCESSING = True

###-------------------For 10 pages (exactly 11 pages)-------------------###
page = 1
while PROCESSING:
    print(f"--------- |PAGE - {page}| ----------")

    ###-------------------Code for single page w/ 20 cards------------------###
    counts = len(scroll_list())
    # print(counts)
    for i in range(counts):
        cards = scroll_list()[i]
        print(f"------ SI {n} ------")
        ## print by categories
        card = cards.text.split("\n")
        card = [c.strip(' ') for c in card]
        namae = card[0]
        reviews = card[1]
        person = None
        # rating and person
        if "No reviews" in reviews:
            rate = "No reviews"
            person = "No reviews"
        else:
            rate = reviews.split("(")[0]
            person = reviews.split("(")[1].replace(")", "")
        # phone number get
        # for p in card:
        #     if "09 " in p:
        #         phono = p.split("·")[1].strip(" ")

        # objective after directions index
        obj = card[card.index("Directions") + 1:]
        if obj == []:
            obj = "Not Show"

        ## append to main list
        name.append(namae)
        rating.append(rate)
        people.append(person)
        services.append(obj)

        # print to make sure, my data is working
        print(f"name : {namae}\n"
              f"rating : {rate}\n"
              f"people : {person}\n"
              f"service : {obj}"
              )

        ## Click card
        try:
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((cards))).click()
            sleep(1)
        except ElementClickInterceptedException:
            try:
                sleep(20)
                WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((cards))).click()
                sleep(1)
            except:
                print(f"------ SERVER SKIP {namae} -------")
                continue

        ### ----------------- REACH INSIDE --------------------- ###
        # frame = browser.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]')
        # browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", frame)
        # sleep(0.5)
        # title = browser.find_element(By.CLASS_NAME, 'Yr7JMd-pane-hSRGPd').text

        # Title is sometime not include. We need to use try / except
        title = "No Objective"
        try:
            title = browser.find_element(By.XPATH,
                                         '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button').text
        except NoSuchElementException:
            pass

        addr = browser.find_element(By.CLASS_NAME, 'Io6YTe').text
        print(f"title : {title}\n"
              f"address : {addr}")

        ##  GET WEBSITE
        website = "No Website"
        webs = browser.find_elements(By.CLASS_NAME, 'Liguzb')
        web_src = [web.get_attribute('src') for web in webs]
        # print(f"website link : {web.get_attribute('src')}")
        for w in web_src:
            if w == "https://www.gstatic.com/images/icons/material/system_gm/1x/public_gm_blue_24dp.png":
                num = web_src.index(w)
                website = browser.find_elements(By.CLASS_NAME, 'Io6YTe')[num].text
        print(f"Website : {website}")

        ## GET PHONE NUMBER
        phono = "Not Show"
        for p in web_src:
            if p == 'https://www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png':
                num = web_src.index(p)
                phono = browser.find_elements(By.CLASS_NAME, 'Io6YTe')[num].text
        print(f"Phone : {phono}\n")

        ## click open now tap and make day_time list 👇
        day_time = "Not Show"
        if len(list(browser.find_elements(By.CLASS_NAME, 'LJKBpe-open-R86cEd-LgbsSe'))) != 0:
            element = browser.find_element(By.CLASS_NAME, 'LJKBpe-open-R86cEd-LgbsSe')
            browser.implicitly_wait(2)
            ActionChains(browser).move_to_element(element).click(element).perform()

            sleep(1)
            days = browser.find_elements(By.CLASS_NAME, 'ylH6lf')
            times = browser.find_elements(By.CLASS_NAME, 'G8aQO')

            day_list = [d.text for d in days]
            time_list = [t.text for t in times]
            day_time = []
            for dt in range(len(day_list)):
                day_time.append(f"{day_list[dt]} : {time_list[dt]},")

            day_time = '\n'.join(day_time)
            if not "Thursday" in day_time:
                day_time = "Not Show"

        print(f"working_hours : {day_time}")
        # note
        # day = ylH6lf
        # time = G8aQO

        ## append to main list
        titles.append(title)
        address.append(addr)
        websites.append(website)
        working_hour.append(day_time)
        phone.append(phono)

        print("------- END -------")
        back = browser.find_element(By.XPATH, '//*[@id="omnibox-singlebox"]/div[1]/div[1]/button').click()
        sleep(1)
        n += 1
    ###-------------------Code for single page with 20 cards \ Code END------------------###
    try:
        next_btn = browser.find_element(By.XPATH, '//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]').click()
    except ElementClickInterceptedException:
        print("--------- PAGE END / NO NEXT BUTTON -----------")
        PROCESSING = False

    page += 1
    sleep(5)
    cur_page = page - 1
    if cur_page % 5 == 0:
        print("------- |SERVER SLEEPING| --------")
        sleep(45)
    elif cur_page % 3 == 0:
        print("------- |SERVER BREAK-TIME| --------")
        sleep(45)
###---------------------- For 10 pages \ CODE END ----------------------###


###----------------------INPUT TEXT TO FORM TO MAKE EXCEL---------------------###
counter = 1
for num in range(n - 1):
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSeJyHfaywtTOVYOgFo6IP82IRk5ojqr3duSUUV593v2MSZs9A/viewform?usp=sf_link'
    browser.get(url)
    sleep(2)

    si_name = browser.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_name.send_keys(name[num])

    si_obj = browser.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_obj.send_keys(titles[num])

    si_rating = browser.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_rating.send_keys(rating[num])

    si_reviewer = browser.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_reviewer.send_keys(people[num])

    si_service = browser.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_service.send_keys(services[num])

    si_phone = browser.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_phone.send_keys(phone[num])

    si_addr = browser.find_element(By.XPATH,
                                   '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_addr.send_keys(address[num])

    si_web = browser.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[9]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_web.send_keys(websites[num])

    si_open_hour = browser.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input')
    si_open_hour.send_keys(working_hour[num])

    submit = browser.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    sleep(1)

    ### BROWSER BREAK TIME ##
    print(f"----- FORM {counter} FINISHED -----")

    if counter % 100 == 0:
        print('------ SERVER SLEEP 1 MINUTE ------')
        sleep(60)
    elif counter % 50 == 0:
        print('------ SERVER SLEEP 30 SECONDS ------')
        sleep(30)
    elif counter % 10 == 0:
        print('------ SERVER SLEEP 15 SECONDS ------')
        sleep(15)

    counter += 1
