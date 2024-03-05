#!/bin/bash

# Run Scrapy spider
scrapy crawl sreality_spider &

# Run Flask application
python app.py
