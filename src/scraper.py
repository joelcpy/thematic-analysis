import requests
from bs4 import BeautifulSoup
import html


def scraper(url: str) -> str:
    """
    Function which scrapes text from URL
    Args:
    - url: url of sec filing
    
    Return:
    - Item 1 Business content
    """

    # Specify the URL of the SEC filing
    # Testing URL
    # url = 'https://www.sec.gov/Archives/edgar/data/1267238/000126723822000006/aiz-20211231.htm'

    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    # Send an HTTP GET request to fetch the HTML content
    response = requests.get(url, headers = headers)
    html_content = response.content

    # # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    all_text = soup.get_text()
    all_text_processed = html.unescape(str(all_text))

    # convert special characters
    ls = all_text_processed.encode('ascii', 'ignore').decode('ascii')

    ls2 = ls.split("Item1. Business")

    item1Content = ls2[1].split("Item1A. Risk Factors")[0]

    return item1Content