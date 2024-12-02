import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import logging
from urllib.parse import urljoin, urlparse
import os

# Configure logging to display on console and write to file
logging.basicConfig(
    filename='scraper.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define headers to mimic a real browser
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/112.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
}

def main():
    # Print the current working directory
    current_dir = os.getcwd()
    print(f"Current Working Directory: {current_dir}")
    logging.info(f"Current Working Directory: {current_dir}")

    base_url = "https://www.wiseradvisor.com"
    directory_url = f"{base_url}/financial-advisors.asp"

    advisors = []

    # Get the list of state URLs from the main directory page
    state_urls = get_state_urls(directory_url, base_url)

    logging.info(f"Found {len(state_urls)} states.")
    print(f"Found {len(state_urls)} states.")

    if not state_urls:
        logging.error("No states found. Exiting the script.")
        print("No states found. Exiting the script.")
        return

    # For each state, get city URLs
    for state_name, state_url in state_urls.items():
        logging.info(f"Processing state: {state_name} - URL: {state_url}")
        print(f"Processing state: {state_name}")

        city_urls = get_city_urls(state_url, base_url, state_name)

        logging.info(f"Found {len(city_urls)} cities in {state_name}.")
        print(f"Found {len(city_urls)} cities in {state_name}.")

        if not city_urls:
            logging.warning(f"No cities found for state: {state_name}. Skipping.")
            print(f"No cities found for state: {state_name}. Skipping.")
            continue

        # For each city, get advisor URLs
        for city_name, city_url in city_urls.items():
            logging.info(f"Processing city: {city_name}, {state_name} - URL: {city_url}")
            print(f"Processing city: {city_name}, {state_name}")

            advisor_urls = get_advisor_urls(city_url, base_url)

            logging.info(f"Found {len(advisor_urls)} advisors in {city_name}, {state_name}.")
            print(f"Found {len(advisor_urls)} advisors in {city_name}, {state_name}.")

            if not advisor_urls:
                logging.warning(f"No advisors found for city: {city_name}, {state_name}. Skipping.")
                print(f"No advisors found for city: {city_name}, {state_name}. Skipping.")
                continue

            # For each advisor, get contact info
            for advisor_url in advisor_urls:
                logging.debug(f"Processing advisor URL: {advisor_url}")
                print(f"Processing advisor URL: {advisor_url}")
                advisor_data = get_advisor_data(advisor_url)

                if advisor_data:
                    advisors.append(advisor_data)
                else:
                    logging.warning(f"Failed to extract data for advisor: {advisor_url}")
                    print(f"Failed to extract data for advisor: {advisor_url}")

                # Sleep to be polite to the server
                time.sleep(1)

    # Define the output file path to be in the c:/python39 directory
    OUTPUT_DIR = 'c:/python39'
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'advisors.csv')

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Write data to CSV
    write_to_csv(advisors, OUTPUT_FILE)

    # Final log and print statement
    logging.info("Script execution completed.")
    print("Script execution completed.")

def get_state_urls(directory_url, base_url):
    state_urls = {}
    try:
        response = requests.get(directory_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully retrieved directory page: {directory_url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching directory page: {e}")
        return state_urls

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags with href matching the state URL pattern
    state_links = soup.find_all('a', href=re.compile(r'^/financial-advisors/[a-zA-Z\-]+/?$'))

    logging.info(f"Total potential state links found: {len(state_links)}")

    for link in state_links:
        href = link['href']
        state_name = link.get_text(strip=True)
        if href and state_name:
            # Validate that state_name is indeed a US state
            if is_valid_state(state_name):
                state_url = urljoin(base_url, href)
                state_urls[state_name] = state_url
                logging.debug(f"Found state: {state_name} - URL: {state_url}")
            else:
                logging.warning(f"Unrecognized state name: '{state_name}'. Skipping this link.")
                print(f"Unrecognized state name: '{state_name}'. Skipping this link.")

    if not state_urls:
        logging.warning("No state URLs found with the current selectors.")

    return state_urls

def is_valid_state(state_name):
    # List of US states for validation, including District of Columbia
    us_states = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
        'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
        'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
        'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'District of Columbia'
    ]
    # Normalize state_name by stripping and capitalizing each word
    normalized_state = ' '.join(word.capitalize() for word in state_name.strip().split())
    if normalized_state in us_states:
        return True
    else:
        return False

def get_city_urls(state_url, base_url, current_state):
    city_urls = {}
    try:
        response = requests.get(state_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully retrieved state page: {state_url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching state page {state_url}: {e}")
        return city_urls

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags with href matching the city URL pattern
    city_links = soup.find_all('a', href=re.compile(r'^/financial-advisors/[a-zA-Z\-]+/[a-zA-Z\-]+/?$'))

    logging.info(f"Total potential city links found: {len(city_links)}")

    for link in city_links:
        href = link['href']
        # Extract state and city from URL
        parsed_url = urlparse(urljoin(base_url, href))
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 3:
            state_segment = path_parts[1].replace('-', ' ').title()
            city_segment = path_parts[2]
            # Check if the state in the URL matches the current state
            if state_segment != current_state:
                logging.warning(f"City link '{href}' state '{state_segment}' does not match current state '{current_state}'. Skipping.")
                continue
            # Replace hyphens with spaces and capitalize each word for city name
            city_name = city_segment.replace('-', ' ').title()
            city_url = urljoin(base_url, href)
            if city_name not in city_urls:
                city_urls[city_name] = city_url
                logging.debug(f"Found city: {city_name} - URL: {city_url}")
        else:
            logging.warning(f"Unexpected URL format for city link: {href}")

    if not city_urls:
        logging.warning(f"No city URLs found on state page: {state_url}")

    return city_urls

def get_advisor_urls(city_url, base_url):
    advisor_urls = []
    page = 1
    while True:
        paged_url = f"{city_url}?page={page}"
        try:
            response = requests.get(paged_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            logging.info(f"Successfully retrieved city page: {paged_url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching city page {paged_url}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all advisor links matching the pattern
        advisor_links = soup.find_all('a', href=re.compile(r'^/financial-advisors/[a-zA-Z\-]+/[a-zA-Z\-]+/.+/\d+/?$'))

        if not advisor_links:
            logging.info(f"No advisor links found on page: {paged_url}")
            break

        for link in advisor_links:
            href = link['href']
            advisor_url = urljoin(base_url, href)
            if advisor_url not in advisor_urls:
                advisor_urls.append(advisor_url)
                logging.debug(f"Found advisor URL: {advisor_url}")

        # Check if there's a next page
        pagination = soup.find('div', {'class': 'pagination'})
        if pagination and pagination.find('a', text=re.compile(r'Next', re.I)):
            page += 1
            logging.info(f"Proceeding to next page: {page} for city URL: {city_url}")
            time.sleep(1)  # Be polite to the server
        else:
            logging.info(f"No more pages found for city URL: {city_url}")
            break

    return advisor_urls

def get_advisor_data(advisor_url):
    try:
        response = requests.get(advisor_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully retrieved advisor page: {advisor_url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching advisor page {advisor_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    advisor_data = {}
    try:
        # Company Name
        company_tag = soup.find('h1')
        if company_tag:
            company_name = company_tag.get_text(strip=True)
            advisor_data['Company'] = company_name
        else:
            advisor_data['Company'] = 'N/A'

        # Advisor Name
        advisor_data['First Name'] = 'N/A'
        advisor_data['Last Name'] = 'N/A'

        # Address and Phone
        address_div = soup.find('div', style=re.compile(r'margin:\s*20px\s+0\s+20px\s+0'))
        if address_div:
            # Extract Phone
            tel_div = address_div.find('div', string=re.compile('Tel:', re.I))
            if tel_div:
                phone_text = tel_div.get_text(strip=True)
                advisor_data['Phone'] = phone_text.replace('Tel:', '').strip()
                tel_div.extract()  # Remove phone from address_div
            else:
                advisor_data['Phone'] = 'N/A'

            # Extract Address Lines
            address_lines = list(address_div.stripped_strings)
            address_lines = [line for line in address_lines if not re.match(r'^Tel:', line, re.I)]

            # Assign Address Components
            if len(address_lines) >= 3:
                advisor_data['Street'] = address_lines[0]
                advisor_data['Street 2'] = address_lines[1]
                city_state = address_lines[2]
                zip_code = address_lines[3] if len(address_lines) > 3 else 'N/A'

                # Parse City and State
                match = re.match(r'^(.*),\s*([A-Z]{2})$', city_state)
                if match:
                    advisor_data['City'] = match.group(1)
                    advisor_data['State'] = match.group(2)
                else:
                    # Try splitting manually
                    parts = city_state.split(',')
                    if len(parts) == 2:
                        advisor_data['City'] = parts[0].strip()
                        state_zip = parts[1].strip()
                        state_zip_parts = state_zip.split()
                        if len(state_zip_parts) >= 2:
                            advisor_data['State'] = state_zip_parts[0]
                            advisor_data['Zip'] = state_zip_parts[1]
                        else:
                            advisor_data['State'] = 'N/A'
                            advisor_data['Zip'] = 'N/A'
                    else:
                        advisor_data['City'] = 'N/A'
                        advisor_data['State'] = 'N/A'
                        advisor_data['Zip'] = 'N/A'
            else:
                # Assign N/A if insufficient address lines
                advisor_data.update({
                    'Street': 'N/A',
                    'Street 2': 'N/A',
                    'City': 'N/A',
                    'State': 'N/A',
                    'Zip': 'N/A'
                })
        else:
            advisor_data.update({
                'Street': 'N/A',
                'Street 2': 'N/A',
                'City': 'N/A',
                'State': 'N/A',
                'Zip': 'N/A',
                'Phone': 'N/A'
            })

        # Email
        email_tag = soup.find('a', href=re.compile(r'^mailto:', re.I))
        advisor_data['Email'] = email_tag['href'].replace('mailto:', '') if email_tag else 'N/A'

        logging.debug(f"Extracted data for advisor: {advisor_data}")
        return advisor_data

    except Exception as e:
        logging.error(f"Error parsing advisor data from {advisor_url}: {e}")
        return None

def write_to_csv(advisors, filename):
    if not advisors:
        logging.warning("No advisor data to write to CSV.")
        print("No advisor data to write.")
        return

    fieldnames = advisors[0].keys()

    abs_path = os.path.abspath(filename)
    logging.info(f"Preparing to write CSV to {abs_path}")
    print(f"Preparing to write CSV to {abs_path}")

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for advisor in advisors:
                writer.writerow(advisor)
        logging.info(f"Successfully wrote {len(advisors)} advisor records to {abs_path}.")
        print(f"Successfully wrote {len(advisors)} advisor records to {abs_path}.")
    except Exception as e:
        logging.error(f"Error writing to CSV file {filename}: {e}")
        print(f"Error writing to CSV file {filename}: {e}")

if __name__ == '__main__':
    main()
