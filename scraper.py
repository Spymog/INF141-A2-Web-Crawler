import re
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

'''
THINGS TO ANSWER:

- Number of unique pages
- Longest page in terms of number of words (HTML markup not counted)
- 50 most common words in the entire set of pages (ignore english stop words: https://www.ranks.nl/stopwords)
- How many subdomains were found in the uci.edu domain? Submit list of subdomains and number of unique pages in each subdomain
'''


def scraper(url, resp):
    # # Base code for reference
    # links = extract_next_links(url, resp)
    # return [link for link in links if is_valid(link)]

    # # *Experimental* - Another way to check http status code 
    # if resp.status > 399: # If http status code is above 399, i.e. 400, 401, 403, 404, then the webpage could not be reached.
    #     return list() # If webpage can't be reached, return empty list of links.

    if resp.status == 200: # If http status code is 200 (normal response), then continue w/ scraping webpage

        print('Current Working Directory: ', os.getcwd())
        links = extract_next_links(url, resp) # Get all links from current url
        return [link for link in links if is_valid(link)] # For each link, check if link will lead to a webpage, if so return it
    else:
        print(f"Can't read url: '{url}',\nError code: {resp.status_code}") # Error message if status code isn't 200
        raise
    

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    # Takes the raw response from the server and converts in into a Beautiful soup object, which can parse through the response and 
    # allows easy access to certain parts of the html. BeautifulSoup = important part of being able to parse through the html, 
    # but NOT the strings themselves
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser') 
    
    for tag in soup.find_all('a'): # Find all the a tags in the html 
        hyperlink = tag.get('href') # Get the contents of the href attribute from each a tag
        
    return list()

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
