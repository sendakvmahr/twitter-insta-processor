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
import modules.process_images
import modules.setup_posts

image_path, image = modules.process_images.get_working_file()
modules.process_images.save_images(image_path, image)

