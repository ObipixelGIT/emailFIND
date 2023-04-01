# emailFIND
emailFIND allow you to scrape a given website for email addresses and is used as an OSINT tool.

## How this script works?

Designed to scrape a given website for email addresses. It does this by recursively following hyperlinks on the website and searching the HTML content of each page for email addresses using regular expressions.

The script uses the following Python libraries:

- requests: This library is used to make HTTP requests to the website being scraped.
- BeautifulSoup: This library is used to parse the HTML content of each page being scraped.
- re: This is Python's built-in regular expression library, which is used to search the HTML content for email addresses.
- prettytable: This library is used to display the discovered email addresses in a neat and organized way.

## Preparation

To use this script, you will need to have Python 3 installed on your system, along with the above libraries.
You can install them using pip, Python's package manager, by running the following commands in your terminal:

```bash
pip3 install requests
pip3 install beautifulsoup4
pip3 install prettytable
```

## Permissions

Ensure you give the script permissions to execute. Do the following from the terminal:
```bash
sudo chmod +x emailFIND.py
```

## Usage
```
sudo python3 emailFIND.py

    ▒██▀░█▄▒▄█▒▄▀▄░█░█▒░▒█▀░█░█▄░█░█▀▄
    ░█▄▄░█▒▀▒█░█▀█░█▒█▄▄░█▀░█░█▒▀█▒█▄▀

Enter the URL to search for email addresses:
```

## Example script
```python
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
```

## Disclaimer
"The scripts in this repository are intended for authorized security testing and/or educational purposes only. Unauthorized access to computer systems or networks is illegal. These scripts are provided "AS IS," without warranty of any kind. The authors of these scripts shall not be held liable for any damages arising from the use of this code. Use of these scripts for any malicious or illegal activities is strictly prohibited. The authors of these scripts assume no liability for any misuse of these scripts by third parties. By using these scripts, you agree to these terms and conditions."

## License Information

This library is released under the [Creative Commons ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/). You are welcome to use this library for commercial purposes. For attribution, we ask that when you begin to use our code, you email us with a link to the product being created and/or sold. We want bragging rights that we helped (in a very small part) to create your 9th world wonder. We would like the opportunity to feature your work on our homepage.
