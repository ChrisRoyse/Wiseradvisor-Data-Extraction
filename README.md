# WiserAdvisor Financial Advisors Scraper

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Logging](#logging)
- [Output](#output)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The **WiserAdvisor Financial Advisors Scraper** is a Python-based web scraping tool designed to extract comprehensive data on financial advisors from [WiserAdvisor](https://www.wiseradvisor.com). This scraper navigates through various states and cities in the Northern areas of Greater Cincinnati, collecting essential information such as company names, contact details, addresses, industries, and key decision-makers. The extracted data is organized into a CSV file, facilitating marketing and outreach efforts for commercial cleaning companies or other businesses seeking detailed financial advisor information.

## Features

- **State and City Navigation:** Automatically navigates through specified states and cities to gather targeted data.
- **Comprehensive Data Extraction:** Extracts business name, address, phone number, email, website, industry/category, and contact names of key decision-makers.
- **Pagination Handling:** Automatically processes multiple pages within each city to ensure complete data collection.
- **Error Handling:** Logs and handles various errors such as unreachable URLs, missing data, and technical issues.
- **Logging:** Detailed logging of the scraping process for monitoring and troubleshooting.
- **CSV Output:** Organized data saved in a CSV file for easy integration with other tools and platforms.

## Prerequisites

Before running the scraper, ensure you have the following installed on your system:

- **Python 3.8 or higher:** [Download Python](https://www.python.org/downloads/)
- **Required Python Libraries:**
  - `requests`
  - `beautifulsoup4`
  - `lxml`

You can install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 lxml
