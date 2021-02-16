import os
import csv
import config
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import pyautogui

def upload_file(filepath):
	pyautogui.write(filepath)
	pyautogui.press('enter') 

def _open_browser(media):
	e_path = os.path.join(os.getcwd(), "chromedriver")
	if media == "instagram":
		mobile_emulation = {
			"deviceScaleFactor": 3, 
			"mobile": True, 
			"height": 640, 
			"width": 360, 
			"touch": True, 
			"userAgent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4239.0 Mobile Safari/537.36"
		}
		"""{\"deviceScaleFactor\": 3, \"mobile\": true, \"height\": 640, \"width\": "
    "360, \"touch\": true, \"userAgent\": \"Mozilla/5.0 (Linux; Android 6.0.1; "
    "Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4239.0 "
    "Mobile Safari/537.36\"}
		"""
		try:
			browser = webdriver.ChromeOptions()
			browser.add_experimental_option('mobileEmulation', mobile_emulation)
			browser = webdriver.Chrome(options=browser)
		except:
			browser = webdriver.ChromeOptions()
			browser.add_experimental_option('mobileEmulation', mobile_emulation)
			browser = webdriver.Chrome(options=browser, executable_path=e_path)
	else:
		try:
			browser = webdriver.Chrome()
		except:
			browser = webdriver.Chrome(executable_path=e_path)
	return browser

def get_status(image_path, image):
	dir_ = os.path.dirname(image_path)
	files = os.listdir(dir_)
	files = list(filter((lambda x: x[-4:] == ".csv"), files))
	status_info = ""
	header = []
	with open(os.path.join(dir_, files[0])) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if header == []:
				header = row
			elif row[0] == image:
				status_info = row
	return _create_status(row[1], row[2])

def _create_status(body, tags):
	tags_formatted =  "#"+ (" #".join(tags.split(" ")))
	return body + "\n\n\n" + tags_formatted


def setup_twitter(filepath, status):
	browser = _open_browser("twitter")
	browser.get("https://twitter.com/login")

	inps = browser.find_elements_by_css_selector('form div div label div div input')
	inps[0].send_keys(config.twitter_handle)
	inps[1].send_keys(config.twitter_pw)
	browser.find_element_by_css_selector('div[role="button"]').click()

	post_box = WebDriverWait(browser, 10).until(
    	lambda x: x.find_element_by_class_name("public-DraftStyleDefault-block"))
	post_box.send_keys(status)

	browser.find_element_by_css_selector('div[aria-label="Add photos or video"]').click()

	upload_file(filepath)

	return browser

def setup_instagram(filepath, status):
	wait_time = 10
	selectors = {
		"login_button":['.coreSpriteLoggedOutWordmark+div button'],
		"user": ['input[aria-label="Phone number, username, or email"]', 0],
		"submit_login": ['button[type="submit"]'],
		"pw": ['input[aria-label="Password"]', 0],
		"popup": ['div[role="dialog"] button:last-of-type', 0],
		"new_post": ['svg[aria-label="New Post"]', 0],
		"next": ["#react-root header button", 1],
		"textarea": ['textarea[aria-label="Write a caption…"]', 0],
	}

	browser = _open_browser("instagram")
	#browser.set_window_size(360, 640) #Moto G4 dimensions for mobile interface 
	browser.get("https://www.instagram.com/")
	time.sleep(wait_time)

	browser.find_element_by_css_selector(selectors["login_button"][0]).click()
	time.sleep(wait_time)

	browser.find_elements_by_css_selector(selectors["user"][0])[selectors["pw"][1]].send_keys(config.insta_handle)
	browser.find_elements_by_css_selector(selectors["pw"][0])[selectors["pw"][1]].send_keys(config.insta_pw)

	browser.find_element_by_css_selector(selectors["submit_login"][0]).click()

	insta_clear_popup(browser, wait_time)
	insta_clear_popup(browser, wait_time*5)
	browser.find_element_by_css_selector(selectors["new_post"][0]).click()

	upload_file(filepath)

	time.sleep(wait_time)
	header_buttons = browser.find_element_by_css_selector(selectors["next"][0])
	browser.find_elements_by_css_selector(selectors["next"][0])[1].click()

	time.sleep(wait_time)
	post_box = browser.find_element_by_css_selector(selectors["textarea"][0])
	post_box.send_keys(status)
	
	return browser


def insta_clear_popup(browser, wait_time):
	time.sleep(wait_time)
	popup_selector = 'div[role="dialog"] button:last-of-type'
	popup_button = browser.find_elements_by_css_selector(popup_selector)
	if (len(popup_button) > 0):
		popup_button[0].click()