import shelve

def answer_maker():
    # How many unique pages did you find?
    # Shelve dict has structure { 'subdomain' : { 'actual_url : set(urls) } } 
    page_count = 0
    subdomain_count = 0
    with shelve.open('answers/scraped_pages') as scraped_pages:
        for subdomain in scraped_pages:
            subdomain_count += 1
            for actual_urls in scraped_pages[subdomain]:
                page_count += 1

    # What is the longest page in terms of the number of words?

    # What are the 50 most common words in the entire set of pages crawled under these domains ?
    with open('answers/common_words.txt', 'w') as t:
        with shelve.open('answers/word_counts') as occurence:
            counter = 0
            for (token, count) in sorted(occurence.items(), key=lambda item: item[1],reverse=True):  # sort each pair by value
                t.write(f'{token}\t{count}')
                counter += 1
                if(counter == 50):
                    break

    # How many subdomains did you find in the uci.edu domain?
    with open('answers/q1_and_q4.txt', 'w') as t:
        t.write(f'Total number of unique pages (q1):\t{page_count}\nTotal number of subdomains(q4):\t{subdomain_count}')


if __name__ == '__main__':
    answer_maker()