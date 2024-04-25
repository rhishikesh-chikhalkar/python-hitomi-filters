import logging
import os
import sys
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set the logging level for the Selenium library to suppress INFO level logs
# logging.getLogger("selenium").setLevel(logging.ERROR)

# Get the current directory of the script (english_filter.py)
script_dir = os.path.dirname(__file__)
logs_path = os.path.join(script_dir, "..", "logs", "english_filter.log")

# Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(logs_path, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

## BASIC Logging Configuration
# logging.basicConfig(
#     filename=logs_path,
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# Load variables from .env file
dotenv_path = os.path.join(script_dir, "..", "config", ".env")
load_dotenv(dotenv_path)
BASE_URL = os.environ["BASE_URL"]

#  Check if command-line argument is provided
if len(sys.argv) < 2:
    logger.error("URL is not provided in console.")
    sys.exit(1)

# Get the command-line argument
page_base_url = sys.argv[1]

# Base URL of the website
logger.info(f"Page Base URL: {page_base_url}")


def merge_files(source_file, target_file):
    # Read the contents of comic_links.txt
    with open(source_file, "r", encoding="utf-8") as source:
        source_content = source.read()

    # Append the contents of comic_links.txt to backup_links.txt
    with open(target_file, "a", encoding="utf-8") as target:
        target.write(source_content)

    unique_lines = set()
    # Open the input file for reading
    with open(target_file, "r") as f:
        # Read each line from the input file
        for line in f:
            # Add unique lines to the set
            unique_lines.add(line.strip())

    # Open the output file for writing
    with open(target_file, "w") as f:
        # Write the unique lines to the output file
        for line in unique_lines:
            f.write(line + "\n")


# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--log-level=3")  # Disables logging

driver = webdriver.Chrome(options=chrome_options)

all_comic_links: List[str] = []

for page_number in range(2, 41):
    page_url = f"{page_base_url}?page={page_number}"
    # Load the webpage
    driver.get(page_url)

    # Wait for a few seconds to let the page load
    driver.implicitly_wait(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    acg_elements = soup.find_all(class_="acg")

    for element in acg_elements:
        link_element = element.find("a", class_="lillie")
        if link_element:
            link_href = link_element.get("href")

            td_elements = element.find_all("td")
            for td in td_elements:
                a_tag = td.find("a")
                if a_tag:
                    href = a_tag.get("href")
                    if href == "/index-english.html":
                        logger.debug(link_href)
                        all_comic_links.append(link_href)
    logger.debug(f"Page Number: {page_number} | Done.")

# Close the web driver
driver.quit()


file_name = "hitomi_comic_links.txt"

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, file_name)

# Write comic links to a text file
all_comic_links = list(set(all_comic_links))
logger.debug(all_comic_links)
with open(file_path, "w", encoding="utf-8") as file:
    for comic_link in all_comic_links:
        file.write(urljoin(BASE_URL, comic_link) + "\n")


backup_file_name = "hitomi_backup_links.txt"
target_path = os.path.join(os.path.expanduser("~"), "Documents", backup_file_name)

merge_files(source_file=file_path, target_file=target_path)

logger.debug(
    "Comic links added to 'hitomi_comic_links.txt' file (Available on DESKTOP)."
)
