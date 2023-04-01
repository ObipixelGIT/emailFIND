# -*- coding: utf-8 -*-
# Author : Dimitrios Zacharopoulos
# All copyrights to Obipixel Ltd
# 01 April 2023

#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable

class EmailScraper:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth
        self.emails = set()

    def scrape(self):
        self._scrape_page(self.url, self.depth)
        self._print_emails()

    def _scrape_page(self, url, depth):
        # stop scraping if the depth limit has been reached
        if depth == 0:
            return
        # send a GET request to the specified URL and parse the HTML response
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # extract all email addresses from the parsed HTML
        for match in re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', str(soup)):
            self.emails.add(match)
        # recursively scrape all hyperlinks on the page
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                self._scrape_page(href, depth-1)

    def _print_emails(self):
        # create a PrettyTable to display the discovered email addresses
        table = PrettyTable()
        table.field_names = ["Email Addresses"]
        for email in self.emails:
            table.add_row([email])

        # print the table to the screen
        if self.emails:
            print(f"Discovered email addresses for {self.url}:\n")
            print(table)
        else:
            print(f"No email addresses were found for {self.url}.")


if __name__ == "__main__":
    # Print ASCII art
    print("""
    ▒██▀░█▄▒▄█▒▄▀▄░█░█▒░▒█▀░█░█▄░█░█▀▄
    ░█▄▄░█▒▀▒█░█▀█░█▒█▄▄░█▀░█░█▒▀█▒█▄▀
    """)

    # prompt the user for a URL to search for email addresses
    url = input("Enter the URL to search for email addresses (eg. https://www.domain.com): ")
    depth = 2

    # create an instance of the EmailScraper class and start scraping
    email_scraper = EmailScraper(url, depth)
    email_scraper.scrape()