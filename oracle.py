import re
import os
import shelve
import urllib.robotparser
# import tldextract
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse, urldefrag, urljoin
from tokenizer import tokenize
from collections import defaultdict
def extract_word_counts():
    with shelve.open('answers/word_counts') as word_counts:
        with open('answers/txt_word_counts.txt', 'w') as word_counts_text:
            for word, count in word_counts.items():
                word_counts_text.write(f'{word}: {count}\n')

def extract_scraped_pages(file):
    with shelve.open(file) as scraped_pages:
        with open('answers/txt_word_counts.txt', 'w') as scraped_pages_text:
            for subdomain in scraped_pages.keys():
                scraped_pages_text.write(f'|-- {subdomain} --|\n')
                for actual_url in scraped_pages[subdomain].keys():
                    scraped_pages_text.write(f' |{actual_url}:\n')
                    for url in scraped_pages[subdomain][actual_url]:
                        scraped_pages_text.write(f'    {url}\n')


if __name__ == '__main__':
    extract_word_counts()
    # extract_scraped_pages('answers/scraped_pages')