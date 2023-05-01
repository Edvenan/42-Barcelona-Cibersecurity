import requests
import os
import sys
import argparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, SoupStrainer


visited_links = set()
domain = ""
image_inventory = {}
link_inventory = {}
valid_extensions = ['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'gif']
stored_files = 0
skipped_files = 0
repeated_files = {}
depth_counter = 0
final_log = {}

def get_image_links(url):
    
    # get all image links from the given url
    image_links = []
    global domain
    global image_inventory
    global repeated_files
    
    try:
        response = requests.get(url)
        # Check if response is valid
        if response.status_code != 200:
            print("RESPONSE STATUS CODE != 200:  ",response.status_code )
            return [],None
        
        # By using parse_only argument, BeautifulSoup only loads and parses the specific subset of HTML tags,
        # which makes parsing faster and more efficient.
        soup = BeautifulSoup(response.content, "html.parser", parse_only=SoupStrainer('img'))
        soup_links = BeautifulSoup(response.content, "html.parser")
        # Loop through all the img tags in the HTML
        for img in soup:
            if img.has_attr('src'):
                # Get the source URL of the image
                src = img['src']

                # If the source URL is relative, make it absolute
                if not bool(urlparse(src).netloc):
                    src = urljoin(url, src)

                # Get the file extension of the image
                extension = src.split('.')[-1]

                # If the extension is a valid image extension, add it to the dictionary
                if extension in valid_extensions:
                    if domain in src:
                        if not any(src in img_lst for img_lst in image_inventory.values()):
                            image_links.append(src)
                        else:
                            # repeated image
                            if url in repeated_files.keys():
                                repeated_files[url].append(src)
                            else:
                                repeated_files[url]=[src]
        
        # links = soup.find_all("img")
        # image_links = [link.get("src") for link in links]
        print("GET_IMAGE_LINKS:\n    URL: {}\n    Image_links: {}\n".format(url,image_links))
        return image_links, soup_links
    except Exception:
        # obtain/print exception info & return Cntxt Mgr object
        exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_tb(exc_traceback)
        print("FAILED REQUEST" )
        print(f"{exc_type.__name__}: {exc_value}")
        return [],None


def download_images(image_dict, path):
    print("DOWNLOAD_IMAGES:\n    image_dict:\n   {}\n   Path:\n   {}".format(image_dict, path))
    
    # download images from the given dict and store in the specified path
    if not os.path.exists(path):
        os.makedirs(path)
    for key, values in image_dict.items():
        for value in values:
            response = requests.get(value)

            file_name = urlparse(value).path.split("/")[-1]
            print("File name: ", file_name)
            file_path = os.path.join(path, file_name)
            print("File path: ", file_path)
            with open(file_path, "wb") as f:
                f.write(response.content)


################################
# SCRAPER 
################################
def scrape(url, depth, recursive=False, path="./data/"):
    # scrape images from the given url up to the specified depth level
    
    # declare global variables
    global visited_links
    global image_inventory
    global link_invetory
    global domain
    global depth_counter
    global final_log
    
    # Check if link has already been visited
    if url in visited_links:
        return
    else:
        # if not visited,
        # Set the domain if it's the first url to visit
        if len(visited_links) == 0:
            print("visited links set is empty. Assign url to var domain")
            # Get the domain of the URL
            domain = urlparse(url).netloc
        # add url to visited_links set
        visited_links.add(url)
    
    image_dict = {}
    link_dict = {}
    if depth == 0:
        image_links, soup = get_image_links(url)
        if image_links:
            image_dict[url] = image_links
            download_images(image_dict, path)
            image_inventory.update(image_dict)

            
            if len(final_log) == 0 or (abs(depth_counter - depth) not in final_log.keys()):
                final_log[abs(depth_counter - depth)]=image_dict
            else:
                final_log[abs(depth_counter - depth)].update(image_dict)

            
        link_dict[url] = get_internal_links(url, soup)
        link_inventory.update(link_dict)

                
    elif depth > 0:
        image_links, soup = get_image_links(url)
        if image_links:
            image_dict[url] = image_links
            download_images(image_dict, path)
            image_inventory.update(image_dict)
            
            if len(final_log) == 0 or (abs(depth_counter - depth) not in final_log.keys()):
                final_log[abs(depth_counter - depth)]=image_dict
            else:
                final_log[abs(depth_counter - depth)].update(image_dict)

        link_dict[url] = get_internal_links(url, soup)
        link_inventory.update(link_dict)
        
                
        if recursive:
            for link in link_dict[url]:
                scrape(link, depth-1, recursive, path)


""" def get_internal_links(url):
    # get all internal links from the given url

    links = soup.find_all("a")
    internal_links = [
        link.get("href")
        for link in links
        if urlparse(link.get("href")).netloc == urlparse(url).netloc
    ]
    return internal_links """



def get_internal_links(url, soup):
    """
    Given a url, returns all the internal links within the same domain
    """
    internal_links = []
    global visited_links
    global domain

    """ try:
        response = requests.get(url)
    except:
        return internal_links

    # Check if response is valid
    if response.status_code != 200:
        return internal_links

    # Get page content and parse with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get all links on the page
    links = soup.find_all('a', href=True) """


    # Loop through all the img tags in the HTML
    internal_links = [link.get('href') for link in soup.find_all('a') if link.get('href') and domain in link.get('href') and link.get('href') not in visited_links]

    for link in internal_links:
        if link.startswith('/'):
            link = domain + link


    """ # Loop through links and check if they are internal to the domain
    for link in links:
        href = link['href']
        if href.startswith('http'):
            # Check if the link is within the same domain
            if domain in href:
                # Check if the link has already been scraped
                if href in visited_links:
                    continue
                internal_links.append(href)
        # If the source URL is relative, make it absolute
        elif href.startswith('/'):
            internal_link = domain + href
            # Check if the link has already been scraped
            if internal_link in visited_links:
                continue
            internal_links.append(internal_link) """
    print("DOMAIN: ", domain,"\n")
    print("GET_INTERNAL_LINKS:\n    URL: {}\n    Internal_links: {}\n".format(url,internal_links))
    return internal_links




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-r", "--recursive", help="recursively scrape links", action="store_true"
    )
    parser.add_argument(
        "-l",
        "--depth_level",
        help="depth level for recursive search",
        type=int,
        default=5,
    )
    parser.add_argument(
        "-p",
        "--path",
        help="download path for images",
        default="./data/",
    )
    parser.add_argument(
        "url", help="the starting url")
    
    args = parser.parse_args()
    
    depth_counter = args.depth_level
    
    print(args)
    scrape(args.url, args.depth_level, args.recursive, args.path)
    with open("log.txt", 'w') as f:
        f.write("------------------------------------------------------\n")
        f.write("-                  DOWNLOADED FILES                  -\n")
        f.write("------------------------------------------------------\n")
        f.write("- DEPTH        URL      # FILES                FILES -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in final_log.items():
            for u,l in value.items():
                f.write(f"{key}: {u} : {len(l)} images : {l}\n\n")
                stored_files += len(l)
        print("\n\n")
        print("------------------------------------------------------")
        print("-        DOWNLOADED FILES: {:<3}                       -".format(stored_files))
        print("------------------------------------------------------")
        f.write("\n")
        f.write("------------------------------------------------------\n")
        f.write("-           REPEATED (SKIPPED) FILES                 -\n")
        f.write("------------------------------------------------------\n")
        f.write("- URL                  # FILES                 FILES -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in final_log.items():
            for u,l in value.items():
                f.write(f"{key}: {u} : {len(l)} images : {l}\n\n")
                skipped_files += len(l)
        print("\n")
        print("------------------------------------------------------")
        print("-        REPEATED (SKIPPED) FILES: {:<3}               -".format(skipped_files))
        print("------------------------------------------------------")
        print("\n\n")

        for k,v in link_inventory.items():
            print(k)
            for i in v:
                print("    i")

# https://www.42barcelona.com/es , level 5, 74 imatges
