import os
import csv
import config
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import pyautogui

def _open_browser():
	try:
		browser = webdriver.Chrome()
	except:
		e_path = os.path.join(os.getcwd(), "chromedriver")
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
	browser = _open_browser()
	browser.get("https://twitter.com/login")

	inps = browser.find_elements_by_css_selector('form div div label div div input')
	inps[0].send_keys(config.twitter_handle)
	inps[1].send_keys(config.twitter_pw)
	browser.find_element_by_css_selector('div[role="button"]').click()

	post_box = WebDriverWait(browser, 10).until(
    	lambda x: x.find_element_by_class_name("public-DraftStyleDefault-block"))
	post_box.send_keys(status)

	browser.find_element_by_css_selector('div[aria-label="Add photos or video"]').click()

	pyautogui.write(filepath)
	pyautogui.press('enter') 

	return browser

def setup_instagram(filepath, status):
	browser = _open_browser()
	browser.set_window_size(360, 640) #Moto G4 dimensions for mobile interface 
	browser.get("https://www.instagram.com/")

	user_selector = 'input[aria-label="Phone number, username, or email"]'
	pw_selector = 'input[aria-label="Password"]'

	browser.find_elements_by_css_selector(user_selector).send_keys(config.insta_handle)
	browser.find_elements_by_css_selector(pw_selector).send_keys(config.insta_pw)

	browser.find_element_by_css_selector('button[type="submit"]').click()

	input(...)

	return browser


