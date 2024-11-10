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

# ----------------------------------

        # crawled_urls = list()
        # try:
        #     found_pages = open('answers/unique_pages.txt', 'r')
        # except FileNotFoundError:
        #     open('answers/unique_pages.txt', 'w')
        # else:
        #     with found_pages:
        #         lines = found_pages.readlines()
        #         for line in lines:
        #             crawled_urls.append(line.strip('\n'))

        # for link in crawled_urls:
        #     if url == link:
        #         return False
