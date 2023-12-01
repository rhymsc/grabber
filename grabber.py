import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import random

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        # Add more user agents as needed
    ]
    return random.choice(user_agents)

def extract_urls_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = [url.get('href') for url in soup.find_all('a', href=True)]
    
    cleaned_urls = []
    for url in urls:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            # Construct URL without path segments and trailing slashes
            full_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            cleaned_urls.append(full_url)
            
    return cleaned_urls

def filter_urls_by_regex(urls, regex_patterns):
    cleaned_urls = [re.sub(r'[^/]+/$', '', url) for url in urls]
    return [url for url in cleaned_urls if any(re.match(pattern, url) for pattern in regex_patterns)]

def read_html_from_url(url):
    try:
        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while retrieving content from {url}: {str(e)}")
        return None

def read_html_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def main():
    banner = r"""
    ______ _   ___   ____  ___ _____ _____ 
    | ___ \ | | \ \ / /  \/  |/  ___/  __ \
    | |_/ / |_| |\ V /| .  . |\ `--.| /  \/
    |    /|  _  | \ / | |\/| | `--. \ |    
    | |\ \| | | | | | | |  | |/\__/ / \__/\ 
    \_| \_\_| |_/ \_/ \_|  |_/\____/ \____/
            """
    print(banner)

    choice = input("Pilih cara input (1: URL, 2: File, 3: URL ke halaman): ")

    if choice == '1':
        target_url = input("Masukkan target URL: ")
        html_content = read_html_from_url(target_url)
        if html_content is None:
            return
    elif choice == '2':
        file_path = input("Masukkan path file: ")
        html_content = read_html_from_file(file_path)
        if html_content is None:
            return
    elif choice == '3':
        page_url = input("Masukkan URL halaman: ")
        html_content = read_html_from_url(page_url)
        if html_content is None:
            return
    else:
        print("Pilihan tidak valid.")
        return

    extracted_urls = extract_urls_from_html(html_content)

    regex_patterns = [
        r"(https?://(?:\d+\.\d+\.\d+\.\d+:\d+|[^/]+))",
        r"(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9-]+(\.[a-zA-Z]{2,})",
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    ]

    filtered_urls = filter_urls_by_regex(extracted_urls, regex_patterns)

    output_file_path = input("Masukkan path untuk menyimpan hasil (contoh: hasil.txt): ")
    with open(output_file_path, 'w') as output_file:
        for url in filtered_urls:
            print(url)
            output_file.write(url + "\n")

    print("URLs yang cocok dengan pola regex telah disimpan di", output_file_path)

if __name__ == "__main__":
    main()
