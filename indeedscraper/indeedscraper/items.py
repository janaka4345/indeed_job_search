# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedscraperItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    location = scrapy.Field()
    company_rating = scrapy.Field()
    extracted_salary = scrapy.Field()
    job_title = scrapy.Field()
    view_job_link = scrapy.Field()
