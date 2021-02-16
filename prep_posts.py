"""
	# dunno how to handle animated gifs yet
	create
	jpg for insta, png for twitter

	go on twitter and insta

	log in

	set up posts

	input to close
"""

import os 
import modules.process_images as process_images
import modules.setup_posts as setup_posts

image_path, image = process_images.get_working_file()
twitter_path, insta_path = process_images.save_images(image_path, image)

status = setup_posts.get_status(image_path, image)
print(status)
twitter_browser = setup_posts.setup_twitter(twitter_path, status)
insta_browser = setup_posts.setup_instagram(insta_path, status)