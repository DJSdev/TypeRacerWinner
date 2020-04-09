import time
import requests
from GoogleVision import Vision
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Racer:

    def __init__(self):
        self.typeracer_url = "https://play.typeracer.com/"
        self.driver = None
        self.wait = None
    
    def open_browser(self, browser=None):
        '''
        Parameters:
        browser -- Name of a browser to open (Only supports Chrome and Firefox)

        The proper driver (chromedriver.exe or gechodriver.exe) for the browser must exist in PATH or in the directory this is run from
        '''
        browser_dict = {"chrome": webdriver.Chrome, 'firefox': webdriver.Firefox}
        browser = browser.lower()
        try:
            self.driver = browser_dict[browser]()
            self.driver.implicitly_wait(15)
            self.wait = WebDriverWait(self.driver, 15)
        except KeyError as e:
            raise Exception("Browser not supported. Only Chrome and Firefox")
        except WebDriverException as e:
            raise e
            
    def login_typeracer(self, username: str, password: str):
        '''
        Parameters:
        username -- username for typeracer.com account
        password -- password for typeracer.com account

        Navigates to TypeRacer.com and logs into an account.
        '''
        self.driver.get("https://play.typeracer.com/")
        time.sleep(1)
        try:
            self.driver.find_element_by_class_name("gwt-Anchor").click()
            self.driver.find_element_by_class_name("gwt-TextBox").send_keys(username)
            self.driver.find_element_by_class_name("gwt-PasswordTextBox").send_keys(password)
            self.driver.find_element_by_class_name("gwt-Button").click()
        except NoSuchElementException as e:
            raise e

    def do_race(self, secs_between_keystrokes: float=.1, room_for_error: int=0):
        '''
        Parameters:
        secs_between_keystrokes -- float to approximately pause between keystrokes
        room_for_error -- a number 0-3 used to add typing errors with corrections for seemlying real typing. 0 = no errors, 3=most errors

        Default of secs_between_keystrokes: float=.1, room_for_error: int=0 lead to a roughly 110wpm typing test. Adjusting either value changes the varience. 
        Keep secs_between_keystrokes .03 or higher. With a secs_between_keystrokes = .03 and room_for_error=0 gives around 390wpm without getting flagged for cheating
        '''
        if room_for_error not in [0,1,2,3]:
            raise Exception("Room for error can only be 0, 1, 2, 3")
        if type(secs_between_keystrokes) not in [int, float]:
            raise TypeError("secs_between_keystrokes needs to be a float (or an int)")

        time.sleep(1)
        # type_race_words is the magic XPATH to the words that make up the typing test
        type_race_words = '//*[@id="gwt-uid-16"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div'
        self.driver.find_element_by_link_text("Enter a typing race").click()
        words  = self.wait.until(EC.presence_of_element_located((By.XPATH, type_race_words)))
        inputbox = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "txtInput")))
        error_modulus = {0:10, 1:5, 2:3, 3:2}

        for letter in words.text:
            rannum = random.randint(2, 9)
            if rannum % error_modulus[room_for_error] == 0:
                inputbox.send_keys(rannum)
                time.sleep(secs_between_keystrokes)
                inputbox.send_keys(Keys.BACKSPACE)
                inputbox.send_keys(letter)
                time.sleep(secs_between_keystrokes)
            else:
                inputbox.send_keys(letter)
                time.sleep(secs_between_keystrokes)

    def complete_captcha_challenge(self, api_key: str):
        '''
        Parameters:
        api_key -- Google Vision API key for uploading captcha and completing the challenge

        In the event that typeracer detects you are cheating they prompt you with a shitty captcha that Google Vision can solve
        '''
        try:
            submitchallenge = self.driver.find_element_by_class_name("gwt-Button")
            submitchallenge.click()
            textArea = self.driver.find_element_by_class_name("challengeTextArea")
            img = self.driver.find_element_by_class_name("challengeImg")
            gv = Vision(api_key)
            challengetext = gv.finish_challenge(img.get_attribute('src'))
            textArea.send_keys(challengetext.replace('\n', ' '))
            submitchallenge = self.driver.find_element_by_class_name("gwt-Button")
            submitchallenge.click()
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[6]/div/div/div[2]/span"),"Typing Challenge Passed"))
        except NoSuchElementException as e:
            print(e)
            print("Captcha not found - It's possible that it isn't required")


if __name__=="__main__":
    racer = Racer()
    racer.open_browser(browser="Firefox")
    racer.login_typeracer("username", "password")
    racer.do_race(secs_between_keystrokes=.02, room_for_error=0)
    racer.complete_captcha_challenge(api_key="Google_Vision_API_Key")

