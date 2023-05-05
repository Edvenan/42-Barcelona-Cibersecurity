import requests
import os
import sys
import re
import argparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import validators
import traceback

visited_links = set()
image_inventory = {}
link_inventory = {}
valid_extensions = ['png', 'jpeg', 'jpg', 'bmp', 'tiff', 'gif']
downloaded_counter = 0
repeated_counter = 0
visited_link_counter = 0
out_of_domain_counter = 0
skipped_link_counter = 0
repeated_files = {}
corrupt_files = {}
corrupt_counter = 0
out_of_domain_dict = {}
skipped_dict = {}
depth_counter = 0


######################################
# get_image_links()
######################################
def get_image_links(url):
    
    # get all image links from the given url
    image_links = []

    global image_inventory
    global repeated_files
    global repeated_counter
    
    try:
        response = requests.get(url)
        # Check if response is valid
        if response.status_code >= 300:
            print("RESPONSE STATUS CODE >= 300: ",response.status_code )
            return image_links, None

        # get all html content at url
        soup = BeautifulSoup(response.content, "html.parser",from_encoding=response.encoding)
        
        # Loop through all the img tags in the HTML and store them
        # in 'images' list if they have 'img' attribute and have a valid extension
        #images = [img.get('src') for img in soup.find_all('img') if img.get('src') and (img.get('src').split('.')[-1] in valid_extensions)]
        #images = [img.get('src') for img in soup.find_all('img', src=True) if (img.get('src').split('.')[-1].lower() in valid_extensions)]
        
        #metas = [meta.get('content') for meta in soup.find_all('meta', content=True) if (meta.get('content').split('.')[-1].lower() in valid_extensions)]
        
        images = [img.get('src') for img in soup.find_all(attrs={'src': True}) if (img.get('src').split('.')[-1].lower() in valid_extensions)]
        
        metas = [meta.get('content') for meta in soup.find_all(attrs={'content': True}) if (meta.get('content').split('.')[-1].lower() in valid_extensions)]
    
        srcsets = [srcset.get('srcset') for srcset in soup.find_all(attrs={'srcset': True}) if (srcset.get('srcset').split('.')[-1].lower() in valid_extensions)]
    
        cursors = soup.find_all(cursor=re.compile(': url'))
        cursor_images = []
        for bg in cursors:
            cursor = bg.get('cursor')
            if cursor:
                match = re.search(r'url\((.*?)\)', cursor)
                if match:
                    bg_url = match.group(1)
                    # store thebg image if it has valid extension
                    #if any(ext in bg_url for ext in valid_extensions):
                    if (bg_url.split('.')[-1].lower() in valid_extensions):
                        cursor_images.append(bg_url)
        
        # Find all background-image styles in the HTML
        #bg_styles = soup.find_all(style=re.compile('background-image: url'))
        bg_styles = soup.find_all(style=re.compile(': url'))
        # Extract URLs from the background-image style of each element
        style_images = []
        for bg in bg_styles:
            style = bg.get('style')
            if style:
                match = re.search(r'url\((.*?)\)', style)
                if match:
                    bg_url = match.group(1)
                    # store thebg image if it has valid extension
                    #if any(ext in bg_url for ext in valid_extensions):
                    if (bg_url.split('.')[-1].lower() in valid_extensions):
                        style_images.append(bg_url)
        
        all_images = images + metas + srcsets + cursor_images + style_images
        
        
        # loop through each img to check if absolute path is required
        for img in all_images:
            # If the source image URL is relative, make it absolute
            # adding url's scheme and network location
            if not bool(urlparse(img).netloc):
                img = urlparse(url).scheme+"://"+urlparse(url)[1]+img
                
            # if img link has not been found previously, store it 
            if (not any(img in img_lst for img_lst in image_inventory.values())) and  (img not in image_links):
                image_links.append(img)
            else:
                # repeated image
                repeated_counter += 1
                if url in repeated_files.keys():
                    repeated_files[url].append(img)
                else:
                    repeated_files[url]=[img]
        
        return image_links, soup
    
    except Exception:
        sys.tracebacklimit = 0
        raise ConnectionError("Connection error. Please check the url provided.")
    
    """ except Exception:
        # obtain/print exception info & return Cntxt Mgr object
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback)
        print("WARNING!")
        print(f"{exc_type.__name__}: {exc_value}")
        return image_links, soup """

######################################
# download_images()
######################################
def download_images(image_dict, path, url):
    
    global downloaded_counter
    global corrupt_files
    global corrupt_counter

    # download images from the given dict and store in the specified path
    if not os.path.exists(path):
        os.makedirs(path)
    for key, values in image_dict.items():
        for value in values:
            response = requests.get(value)
            
            file_name = "{}_[{:<5}]_{}".format(str(downloaded_counter+1).zfill(4), urlparse(value).scheme ,urlparse(value).path.split("/")[-1])
            ##########################################
            file_path = os.path.join(path, file_name)
 
            if response.status_code >= 300:
                print("Download FAILED! (Status code: {}) ({})".format(response.status_code, value))
                # remove this image link from image_dict
                image_dict[key].remove(value)
                corrupt_counter += 1
                if url in corrupt_files:
                    corrupt_files[url].append(value)
                else:
                    corrupt_files[url] = [value]
            else:
                
            
                """ 
                count = 0
                # Check if file already exists
                while os.path.exists(file_path):
                    count += 1
                    # If file exists, add a number to the filename
                    file_path = f'{file_path}_{count}.{file_path.split(".")[-1]}'
                """
                with open(file_path, "wb") as f:
                    f.write(response.content)
                downloaded_counter += 1
                print("Downloaded file {:>4}: {}".format(downloaded_counter,file_path))

################################
# SPIDER !!!!
################################
def spider(url, depth, recursive=False, path="./data/"):
    # scrape images from the given url up to the specified depth level
    
    # declare global variables
    global visited_links
    global image_inventory
    global link_inventory
    global domain
    global depth_counter
    global visited_link_counter
    global skipped_link_counter
    global skipped_dict
 
    if not validators.url(url):
        sys.tracebacklimit = 0
        raise TypeError("The provided url is not valid.")
    
    # Check if link has already been visited
    if url in visited_links:
        skipped_link_counter += 1
        skipped_dict[url]=[]

    else:
        # if not visited,
        # Set the domain if it's the first url to visit
        if len(visited_links) == 0:
            # Get the root domain of the URL
            #domain =  urlparse(url).netloc.split('.')[-2] + '.' + urlparse(url).netloc.split('.')[-1]
            domain = urlparse(url).netloc
            print("DOMAIN: ", domain,"\n")

        # add url to visited_links set
        visited_links.add(url)
        visited_link_counter += 1
        link_inventory[url]=[]
    
        image_dict = {}
        link_dict = {}
        
        if depth == 0:
            image_links, soup = get_image_links(url)
            if image_links:
                image_dict[url] = image_links
                download_images(image_dict, path, url)
                image_inventory.update(image_dict)



        elif depth > 0:
            image_links, soup = get_image_links(url)
            if image_links:
                image_dict[url] = image_links
                download_images(image_dict, path, url)
                image_inventory.update(image_dict)


            if recursive:
                link_dict[url] = get_internal_links(url, soup)
                link_inventory.update(link_dict)
                for link in link_dict[url]:
                    spider(link, depth-1, recursive, path)

       


######################################
# get_internal_links()
######################################
def get_internal_links(url, soup):
    """
    Given a url, returns all the internal links within the same domain
    """
    internal_links = []
    out_of_domain_links = []
    skipped_links = []

    global visited_link_counter
    global out_of_domain_counter
    global skipped_link_counter
    global out_of_domain_dict
    global skipped_dict
    
    # Loop through all the 'a' tags in the HTML 
    # containing 'href' attribute
    if soup != None:
        
        links = [link.get('href') for link in soup.find_all('a') if link.get('href')]
        #links = [link.get('href') for link in soup.find_all('a', href=True)]
        for link in links:
                
            # If link in href is relative, make it absolute
            if not bool(urlparse(link).netloc):
                #link = urlparse(url).scheme+"://"+urlparse(url)[1]+link
                link = urlparse(url).scheme+"://"+urlparse(url).netloc+link

            if not validators.url(link):
                continue
            
            if domain in link and link not in visited_links and link not in internal_links: 
                internal_links.append(link)

                
            elif link in visited_links or link in internal_links:
                skipped_links.append(link)
                skipped_link_counter += 1
                
            else:
                out_of_domain_links.append(link)
                out_of_domain_counter += 1

        out_of_domain_dict[url] = out_of_domain_links
        skipped_dict[url] = skipped_links
    
    return internal_links

######################################
# logs and screen print outs
######################################
def log_and_print_out():
    """
    Given a url, returns all the internal links within the same domain
    """
    with open("log.txt", 'w') as f:
        
        f.write("\n")
        f.write("------------------------------------------------------\n")
        f.write("-        DOWNLOADED FILES: {:<3}                       -\n".format(downloaded_counter))
        f.write("-        REPEATED (Skipped) FILES: {:<3}               -\n".format(repeated_counter))
        f.write("-        CORRUPTED FILES: {:<3}                        -\n".format(corrupt_counter))
        f.write("------------------------------------------------------\n")
        f.write("-        VISITED LINKS: {:<3}                          -\n".format(visited_link_counter))
        f.write("-        REPEATED (Skipped) LINKS: {:<3}               -\n".format(skipped_link_counter))
        f.write("-        OUT OF DOMAIN LINKS: {:<3}                    -\n".format(out_of_domain_counter))
        f.write("------------------------------------------------------\n")
        f.write("\n")
        
        
        f.write("------------------------------------------------------\n")
        f.write("-                  DOWNLOADED FILES                  -\n")
        f.write("------------------------------------------------------\n")
        f.write("-     URL            # FILES                   FILES -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in image_inventory.items():
            f.write(f"\n{key}: {len(value)} images :\n")
            for i in value:
                f.write(f"        {i}\n")


        f.write("\n------------------------------------------------------\n")
        f.write("-              REPEATED (Skipped) FILES              -\n")
        f.write("------------------------------------------------------\n")
        f.write("-     URL            # FILES                   FILES -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in repeated_files.items():
            f.write(f"\n{key}: {len(value)} repeated images :\n")
            for i in value:
                f.write(f"        {i}\n")


        f.write("\n------------------------------------------------------\n")
        f.write("-                CORRUPTED FILES                     -\n")
        f.write("------------------------------------------------------\n")
        f.write("-     URL            # FILES                   FILES -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in corrupt_files.items():
            f.write(f"\n{key}: {len(value)} corrupted images :\n")
            for i in value:
                f.write(f"        {i}\n")
                
  
        f.write("\n------------------------------------------------------\n")
        f.write("-                  VISITED LINKS                     -\n")
        f.write("------------------------------------------------------\n")
        f.write("- URL                  # LINKS                LINKS  -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in link_inventory.items():
            f.write(f"\n{key}: {len(value)} links :\n")
            for i in value:
                f.write(f"        {i}\n")
 
        f.write("\n------------------------------------------------------\n")
        f.write("-                REPEATED (Skipped) LINKS            -\n")
        f.write("------------------------------------------------------\n")
        f.write("- URL                  # LINKS                LINKS  -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in skipped_dict.items():
            f.write(f"\n{key}: {len(value)} skipped links :\n")
            for i in value:
                f.write(f"        {i}\n")
                
        f.write("\n------------------------------------------------------\n")
        f.write("-               OUT OF DOMAIN LINKS                  -\n")
        f.write("------------------------------------------------------\n")
        f.write("- URL                  # LINKS                LINKS  -\n")
        f.write("------------------------------------------------------\n\n")
        for key, value in out_of_domain_dict.items():
            f.write(f"\n{key}: {len(value)} out of domain links :\n")
            for i in value:
                f.write(f"        {i}\n")
 
 
        print("\n")
        print("------------------------------------------------------")
        print("-        DOWNLOADED FILES: {:<3}                       -".format(downloaded_counter))
        print("-        REPEATED (Skipped) FILES: {:<3}               -".format(repeated_counter))
        print("-        CORRUPTED FILES: {:<3}                        -".format(corrupt_counter))
        print("------------------------------------------------------")
        print("-        VISITED LINKS: {:<3}                          -".format(visited_link_counter))
        print("-        REPEATED (Skipped) LINKS: {:<3}               -".format(skipped_link_counter))
        print("-        OUT OF DOMAIN LINKS: {:<3}                    -".format(out_of_domain_counter))
        print("------------------------------------------------------")
        print("\n")
    
    
    

######################################
# MAIN
######################################

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

    
    spider(args.url, args.depth_level, args.recursive, args.path)
    log_and_print_out()
    

       
# https://www.42barcelona.com/es , level 5, 74 imatges
