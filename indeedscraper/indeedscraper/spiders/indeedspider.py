import json
import scrapy
from urllib.parse import urlencode
import re
from indeedscraper.items import IndeedscraperItem


class IndeedspiderSpider(scrapy.Spider):
    name = "indeedspider"
    # allowed_domains = ["indeed.com", "scrapeops.io"]

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {"q": keyword, "l": location}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        keyword = "fulltime"
        location = "Houston"
        # url = "https://www.indeed.com/jobs?q=fulltime&l=Houston%2C+TX"
        indeed_jobs_url = self.get_indeed_search_url(keyword, location)
        yield scrapy.Request(
            indeed_jobs_url,
            callback=self.parse_search_results,
            # meta={"keyword": keyword, "location": location, "offset": 0},
        )

    def parse_search_results(self, response):
        script_tag = response.xpath('//script[@id="mosaic-data"]/text()').get()
        # edited_script_tag = script_tag[1700:-1161]
        # edited_script_tag = script_tag[1700:1750]
        # json_script = json.loads(edited_script_tag)
        edited_script_tag = re.findall(
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
            script_tag,
        )

        json_data = json.loads(edited_script_tag[0])
        jobs = json_data["metaData"]["mosaicProviderJobCardsModel"]["results"]
        job_item = IndeedscraperItem()
        print(jobs[0])
        for job in jobs:

            job_item["company"] = job.get("company", None)
            job_item["company_rating"] = job.get("companyRating", None)
            job_item["extracted_salary"] = job.get("extractedSalary", None)
            job_item["location"] = job.get("formattedLocation", None)
            job_item["job_title"] = job.get("title", None)
            job_item["view_job_link"] = job.get("viewJobLink", None)

            yield job_item
