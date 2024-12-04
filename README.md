# Financial Advisors Web Scraper

A Python-based web scraper that extracts detailed information about financial advisors from [WiserAdvisor](https://www.wiseradvisor.com). The scraper navigates through states and cities to collect data such as company name, advisor name, contact information, and address details. The collected data is saved into a CSV file for easy analysis and usage.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Environment Setup](#environment-setup)
  - [Prerequisites](#prerequisites)
  - [Step-by-Step Setup Guide](#step-by-step-setup-guide)
    - [1. Install Python](#1-install-python)
    - [2. Create a Virtual Environment (Optional but Recommended)](#2-create-a-virtual-environment-optional-but-recommended)
    - [3. Upgrade pip](#3-upgrade-pip)
    - [4. Install Required Python Packages](#4-install-required-python-packages)
    - [5. Configure NLTK Data Path (If Necessary)](#5-configure-nltk-data-path-if-necessary)
- [Usage](#usage)
  - [1. Configure the Script](#1-configure-the-script)
  - [2. Run the Script](#2-run-the-script)
  - [3. View the Results](#3-view-the-results)
- [Sample Output](#sample-output)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This tool automates the extraction of financial advisors' information from WiserAdvisor's website. By systematically navigating through states and cities, it collects comprehensive data including company names, advisor names, phone numbers, emails, and addresses. The results are compiled into a CSV file, facilitating easy access and analysis for various purposes such as marketing, research, or networking.

## Features

- **State and City Navigation:** Automatically navigates through all available states and their respective cities on WiserAdvisor.
- **Advisor Information Extraction:** Collects detailed information about each financial advisor, including company name, advisor name, phone number, email, and address.
- **Logging:** Maintains detailed logs of the scraping process, including successes, warnings, and errors.
- **CSV Output:** Compiles all extracted data into a well-structured CSV file for easy access and analysis.
- **Polite Scraping:** Implements delays between requests to respect the server's resources.

## Environment Setup

Setting up the environment correctly is crucial for the smooth running of this tool. Follow the step-by-step guide below to set up your environment on a Windows machine.

### Prerequisites

- **Operating System:** Windows 10 or higher
- **Python:** Version 3.6 or higher
- **Git:** For cloning the repository

### Step-by-Step Setup Guide

#### 1. Install Python

Ensure Python 3.6 or higher is installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

After installation, verify the installation by running:

```bash
python --version
```

#### 2. Create a Virtual Environment (Optional but Recommended)

It's good practice to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Command Prompt:**

  ```bash
  venv\Scripts\activate
  ```

- **PowerShell:**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

#### 3. Upgrade pip

Ensure you have the latest version of pip:

```bash
pip install --upgrade pip
```

#### 4. Install Required Python Packages

Create a `requirements.txt` file with the following content:

```plaintext
requests
beautifulsoup4
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

#### 5. Configure NLTK Data Path (If Necessary)

*Note:* This script does not require NLTK. If you have other scripts that require NLTK, ensure to configure the NLTK data path accordingly.

```python
import nltk
nltk.data.path.append(r'C:\Path\To\Your\nltk_data')
```

## Usage

### 1. Configure the Script

Before running the script, ensure that the output directory is correctly set. By default, the script saves the `advisors.csv` file to `C:/Python39`. You can change this by modifying the `OUTPUT_DIR` variable in the script.

```python
# Define the output file path to be in the c:/python39 directory
OUTPUT_DIR = 'c:/python39'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'advisors.csv')
```

Additionally, ensure that the base URL is correct. If WiserAdvisor changes their website structure, you might need to update the URL patterns in the script.

### 2. Run the Script

Execute the script using Python:

```bash
python scraper.py
```

*Replace `scraper.py` with the actual filename if different.*

The script will perform the following actions:

1. Retrieve the main directory page containing links to all states.
2. For each state, retrieve the list of cities.
3. For each city, retrieve the list of financial advisors.
4. For each advisor, extract detailed information including company name, advisor name, phone number, email, and address.
5. Save all collected data into a CSV file located at the specified `OUTPUT_DIR`.

### 3. View the Results

After the script completes execution, navigate to the `OUTPUT_DIR` (default is `C:/Python39`) and open the `advisors.csv` file using Excel, Google Sheets, or any CSV viewer to analyze the extracted data.

## Sample Output

Below is a sample of the output CSV file:

| Company            | First Name | Last Name | Street               | Street 2 | City         | State | Zip     | Phone            | Email                  |
|--------------------|------------|-----------|----------------------|----------|--------------|-------|---------|------------------|------------------------|
| ABC Financial LLC  | John       | Doe       | 123 Main St          | Suite 100| Springfield  | IL    | 62704   | (555) 123-4567   | john.doe@abcfinancial.com |
| XYZ Advisors Inc.  | Jane       | Smith     | 456 Elm Street       |          | Madison      | WI    | 53703   | (555) 987-6543   | jane.smith@xyzadvisors.com |
| ...                | ...        | ...       | ...                  | ...      | ...          | ...   | ...     | ...              | ...                    |

## Dependencies

- **Python 3.6 or Higher**

- **Python Libraries:**
  - [requests](https://pypi.org/project/requests/)
  - [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Configuration

- **Output Directory:**

  By default, the script saves the CSV file to `C:/Python39`. To change this, modify the `OUTPUT_DIR` variable in the script:

  ```python
  OUTPUT_DIR = 'c:/path/to/your/directory'
  OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'advisors.csv')
  ```

- **Logging Configuration:**

  The script logs detailed information to `scraper.log` in the current working directory. You can change the log file location by modifying the `filename` parameter in the `logging.basicConfig` setup:

  ```python
  logging.basicConfig(
      filename='path/to/your/logfile.log',
      filemode='w',
      level=logging.DEBUG,
      format='%(asctime)s - %(levelname)s - %(message)s'
  )
  ```

## Troubleshooting

- **HTTP Request Errors:**

  - **Issue:** The script fails to retrieve pages due to network issues or website changes.
  - **Solution:** 
    - Check your internet connection.
    - Verify that `https://www.wiseradvisor.com` is accessible.
    - Inspect the website for any structural changes that might affect the scraper.
  
- **No Data Found:**

  - **Issue:** The script does not find any states, cities, or advisors.
  - **Solution:** 
    - Ensure that the website structure has not changed.
    - Update the regex patterns in the `find_all` methods if necessary.
    - Check the logs (`scraper.log`) for detailed error messages.
  
- **Permission Issues:**

  - **Issue:** The script cannot create directories or write files.
  - **Solution:** 
    - Run the script with administrative privileges.
    - Ensure that the specified `OUTPUT_DIR` exists and is writable.
  
- **Missing Dependencies:**

  - **Issue:** Import errors for missing Python libraries.
  - **Solution:** 
    - Ensure all required packages are installed by running `pip install -r requirements.txt`.
  
- **Incorrect Output Path:**

  - **Issue:** The CSV file is not saved in the expected location.
  - **Solution:** 
    - Verify the `OUTPUT_DIR` path in the script.
    - Ensure that the path is correctly formatted for your operating system.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add your feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   Describe your changes and submit the pull request for review.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Happy Scraping! 🚀*
```
