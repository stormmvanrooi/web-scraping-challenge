# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import time

# MAC - Set browser

# Set up Splinter
def scrape_info():
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	browser = Browser("chrome", **executable_path, headless=False)

	# Visit redplanetscience.com

	mars_url ='https://redplanetscience.com'
	browser.visit(mars_url)

	time.sleep(1)

	mars_info = {}

	# Scrape page into Soup
	html = browser.html
	soup = bs(html, "html.parser")

	# Retrieve the latest news title
	title = soup.find('div', class_='content_title').text
	# Retrieve the latest news paragraph
	tagline = soup.find('div', class_= 'article_teaser_body').text

	mars_info["news_title"] = title
	mars_info["news_paragraph"] = tagline

	## JPL Mars Space Images - Featured Image

	featured_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'
	browser.visit(featured_image_url)

	# HTML Object
	img_html = browser.html
	img_soup = bs(img_html, "html.parser")

	# Find image url to the full size
	featured_image = img_soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]

	# Display url
	main_url = "https://www.jpl.nasa.gov"


	# Connect website url with scrapped route
	featured_image_url = main_url + featured_image

	# Connect website url with scrapped route
	mars_info["featured_image_url"] = featured_image_url

	### Mars Fact
	mars_facts = 'https://galaxyfacts-mars.com'

	tables = pd.read_html(mars_facts)

	mars_df = mars_facts[0]

	# Create Data Frame
	mars_df.columns = ["Description", "Value"]

	# Set index to Description
	mars_df.set_index("Description", inplace=True)

	# Save html code to folder Assets
	html_table = mars_df.to_html()

	# Strip unwanted newlines to clean up the table
	html_table.replace("\n", '')

	# Save html code
	mars_df.to_html("mars_facts_data.html")

	mars_info["mars_facts"] = html_table

	### Mars Hemispheres

	# Scrape Mars hemisphere title and image
	url_hemi = 'https://marshemispheres.com/'
	browser.visit(url_hemi)

	# HTML object
	html_hemi = browser.html

	# Parse HTML with Beautiful Soup
	soup = bs(html_hemi, 'html.parser')

	results = soup.find_all('div', class_='item')

	hemi_info = []

	# Loop through each hemisphere item
	for result in results:

		# Retrieve the hemisphere title and img
		titles = result.find('h3').text
		hempispheres_img =result.find('a', class_ = 'itemLink product-item')['href']

		#Visit page that contains full image
		browser.visit(url_hemi + hempispheres_img)

		hemi_html = browser.html

		web_info = bs(hemi_html, 'html.parser')

		img_url = url_hemi + web_info.find("img", class_= "wide-image")['src']

		mars_info["title"] = title.strip()
		mars_info["img_url"] = img_url

		hemi_info.append({"title" : titles, "img_url" : img_url})

		mars_info["hemispheres_info"] = hemi_info
		# Close the browser after scraping

		mars__info={
			"news_title" : title,
			"news_tagline" : tagline,
			"featured_img_url":featured_image_url,
			"fact_table": html_table,
			"hemisphere_images":hemi_info
		}

	browser.quit()
	return mars_info