"""run and manage spider for corona data
"""
from subprocess import check_output
from time import sleep


def call_spider():
    """run spider with subprocess
    """
    spider_name: str = "corona_crawler"
    check_output(["scrapy", "crawl", spider_name])


def run_spider():
    """call `call_spider` function every 5 minutes
    """
    while True:
        call_spider()
        sleep(60*5)
