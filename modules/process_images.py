import os 
import random
import config
import PIL.Image as Image
from math import ceil as ceiling

def get_working_file():
	"""
	Chooses an image to upload. If there's something in current, process that.
	If not, pick something out of the queue
	"""
	path = os.path.join(os.getcwd(), config.current_dir)
	images = _get_dir_files(path)
	if len(images) == 0:
		path = os.path.join(os.getcwd(), config.queue_dir)
		images = _get_dir_files(path)
	image = random.choice(images)
	image_path = os.path.join(path, image)
	return (image_path, image)

def _get_dimensions(img, setting):
	"""
	Gets dimension of resized images for each social media
	"""
	min_size = min([img.width, img.height])
	if setting == "twitter": 
		zoom = ceiling(config.twitter_width / min_size)
	elif setting == "instagram":
		zoom = ceiling(config.instagram_width / min_size)
	else:
		zoom = 1
	return (img.width * zoom, img.height * zoom)

def save_images(image_path, image):
	"""
	Saves insta and twitter versions of the images
	"""
	working_dir = os.path.join(os.getcwd(), config.working_dir)
	source_img = Image.open(image_path)

	twitter_img = source_img.copy()
	twitter_img = twitter_img.resize(_get_dimensions(source_img, "twitter"), 
		Image.NEAREST)
	twitter_img.save(os.path.join(working_dir, image))

	insta_img = source_img.copy()
	insta_img = insta_img.resize(_get_dimensions(source_img, "instagram"), 
		Image.NEAREST)
	insta_img = insta_img.convert("RGB")
	insta_image_name = os.path.join(working_dir, image.split(".")[0] + ".jpg")
	insta_img.save(insta_image_name, quality=100, subsampling=0)

def _get_dir_files(dir_):
	"""lists gifs and pngs in dir. I'm never saving in other formats"""
	current_files = os.listdir(dir_)
	return list(filter(_is_image, current_files))

def _is_image(filename):
	"""filter for gifs/pngs"""
	try:
		return filename[-4:] == ".gif" or filename[-4:] == ".png"
	except: # current dir is "."
		return False
