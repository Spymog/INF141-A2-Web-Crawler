import re
import os
import shelve
from bs4 import BeautifulSoup, SoupStrainer

from urllib.parse import urlparse, urldefrag, urljoin
from tokenizer import tokenize

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
        # print('Current Working Directory: ', os.getcwd()) # just checking what the current working directory is 
        if not os.path.exists('answers/unique_pages.txt'):
            # If it doesn't exist, create an empty file
            os.makedirs('answers', exist_ok=True)  # Ensure the directory exists
            with open('answers/unique_pages.txt', 'w') as t:
                pass  # Create the file since 'a' doesn't do it for us. 
        
        with open('answers/unique_pages.txt', 'a') as t:
            if 'ics.uci.edu' in url:
                t.write(f"{url}\n")
        links = extract_next_links(url, resp) # Get all links from current url
        return [link for link in links if is_valid(link)] # For each link, check if link will lead to a webpage, if so return it
    else:
        print(f"Can't read url: '{url}',\nError code: {resp.status_code}") # Error message if status code isn't 200
        raise
    

# -- MAY NOT ACTUALLY NEED --
# def process_raw_hyperlink(url, hyperlink):
#     parsed_url = urlparse(url)
#     parsed_link = urlparse(hyperlink)

#     if not parsed_link.scheme:
#         parsed_link = parsed_link._replace(scheme=parsed_url.scheme)
#     elif parsed_link.scheme not in set(["http", "https"]):
#         return
    
#     if not parsed_link.netloc:

#         if parsed_url.hostname in parsed_link.path:
#             new_path = parsed_link.path.replace(parsed_url.hostname, '', 1)
#             parsed_link = parsed_link._replace(netloc=parsed_url.hostname, path=new_path)
#         elif parsed_link.path.startswith('/'):
#             parsed_link = parsed_link._replace(netloc=parsed_url.hostname)
#         else:
#             current_path = parsed_url.hostname + '/' + parsed_url.path.lstrip('/')
#             parsed_link = parsed_link._replace(netloc=current_path)
#     else:
#         parsed_link = parsed_link._replace(netloc=parsed_link.hostname)

#     if parsed_link.path == '/':
#         parsed_link = parsed_link._replace(path='')

#     parsed_link = urlparse(urldefrag(parsed_link.geturl())[0])

#     return parsed_link.geturl()


def find_longest(url:str, tokens:list):
    '''
    Compares given url and token list to current longest url in terms of words and it's word count

    Takes the current url and a list of all tokens found at the current url as it's arguments.

    Opens longest_page.txt, which is a 2 line txt file:
        1. Number of tokens found at the longest url
        2. The url itself
    Checks if the length of the list of tokens arguement is greater than the recorded longest number of words from the current longest url.
    If tokens argument is longer, write it's length and the name of the current url into longest_page.txt 
    '''
    token_count = len(tokens)
    
    if not os.path.exists('answers/longest_page.txt'):
            # If it doesn't exist, create an empty file
            os.makedirs('answers', exist_ok=True)  # Ensure the directory exists
            with open('answers/longest_page.txt', 'w') as t:
                pass  # Create the file since 'a' doesn't do it for us. 
    
    with open('answers/longest_page.txt', 'r') as current_longest:
        lines = current_longest.readlines()
        longest_count = int(lines[0])
        # longest_url = lines[1] # Maybe don't need

        if token_count > longest_count:
            with open('answers/longest_page.txt', 'w') as new_longest:
                new_longest.write(f'{str(token_count)}\n{url}')


def update_token_counts(tokens:list):
    '''
    Uses shelve to keep a persistent dict{word:count} of all the words and the current count of their occurences.

    Takes a list of tokens as it's argument.

    Opens the file word_counts which is used as the persistent dict and iterates through each token in the tokens list, updating the 
    count of the corresponding key by if such a key exists, otherwise creates a new key with a count of 1.
    '''

    stop_words = "a about above after again against all am an and any are aren't as at be because been before being below between both \
but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't \
have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't \
it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own \
same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's \
these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were \
weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're \
you've your yours yourself yourselves"

    with shelve.open('answers/word_counts') as count:
        for token in tokens:
            if token not in stop_words:
                count[token] = count.get(token, 0) + 1


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

    # Extract the text of the current webpage and convert to tokens
    webpage_text = soup.get_text()
    tokens = tokenize(webpage_text)

    # Get all tokens, use to find if current webpage currently has the most words
    find_longest(url, tokens)
    
    # Count frequencies of all found tokens and update total count of all tokens
    update_token_counts(tokens)

    # Find all the a tags in the html, add them to the set of raw hyperlinks  
    raw_hyperlinks = set() 
    for tag in soup.find_all('a'):
        hyperlink = tag.get('href')
        if hyperlink:
            raw_hyperlinks.add(hyperlink)

    # Convert raw hyperlinks to absolute links, add them all to a list to be returned
    absolute_links = list()
    for link in raw_hyperlinks:
        # processed_link = process_raw_hyperlink(url, link)
        absolute_link = urljoin(url, link)
        absolute_link = urldefrag(absolute_link)[0] # Remove any fragments from the end 
        absolute_links.append(absolute_link)
        # TODO: write processed_link's URL only to a file so we can count it later
        # TODO: use the soup to get all tokens (across all pages), and keep track of the page with the most number of words
        # TODO: using tokens, find 50 most common words
        # TODO: if processed_link is a new subdomain of uci.edu, add it to a file of subdomains. 
            # TODO: sort list alpahbetically and record the # of unique pages in each subdomain, ex. below
            # vision.ics.uci.edu, 10
            # hearing.ics.uci.edu, 100
            # etc. 

        # current_parse = urlparse(link)
        # if not current_parse.scheme:
        #     current_parse = current_parse._replace(scheme=f'{parsed_url.scheme}')
        # if current_parse.hostname:

    
    return absolute_links


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    
    # valid_domains = [
    #     'ics.uci.edu/',
    #     'cs.uci.edu/',
    #     'informatics.uci.edu/',
    #     'stat.uci.edu/',
    #     'today.uci.edu/department/information_computer_sciences/'
    #     ]

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) > 1 and len(path_parts) == len(set(path_parts)):
            return False
        
        valid_domains = r'((\w*\.)*(ics|cs|informatics|stat)\.uci\.edu)|(today\.uci\.edu\/department\/information_computer_sciences)'

        if not re.match(valid_domains, parsed.hostname + parsed.path):
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
