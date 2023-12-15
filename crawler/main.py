import requests
from bs4 import BeautifulSoup
import time
import csv

def get_metadata_from_google_scholar(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" ,'referer':'https://www.google.com/'
    }
    base_url = "https://scholar.google.com/scholar?q="

    search_url = base_url + query
    payload = { 'api_key': 'bf9b7aabe0b17f321bcca53d0f6f06d1', 'url': search_url } 
    response = requests.get('https://api.scraperapi.com/', params=payload)#We use scrapeapi to aim google scholar for some venues. Also, we double check if the abstract is not fully retrieved and if there are some keywords

    #response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        error_message = f"Failed to retrieve the web page for query: '{query}' with status code {response.status_code}."
        if response.status_code == 429:
            error_message += " We might be getting rate limited. Consider extending the sleep duration or using proxies."
        print(error_message)
        return []

    content_after_head = response.content.decode('utf-8').split('</head>', 1)[-1]
    soup = BeautifulSoup(content_after_head, 'html.parser')
    search_results = soup.select('div.gs_r.gs_or.gs_scl')
    
    results = []
    for result in search_results:
        title = result.find('h3', class_='gs_rt').text
        abstract = result.find('div', class_='gs_rs').text if result.find('div', class_='gs_rs') else "N/A"
        results.append({
            'Title': title,
            'Abstract': abstract
        })

    time.sleep(15)  # Sleep for 10 seconds to be polite to Google Scholar.
    return results
            
def save_to_csv(data, filename="output.csv", mode='a'):
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Abstract']) # Change here
        if mode == 'w':
            writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def read_titles_from_csv(filename="input.csv"):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row["Title"] for row in reader]


if __name__ == "__main__":
    input_csv_filename = "input.csv"
    output_csv_filename = "output.csv"

    # Ensure we're starting with an empty file with just the headers if the file doesn't exist.
    try:
        with open(output_csv_filename, 'r', encoding='utf-8') as file:
            pass
    except FileNotFoundError:
        save_to_csv([], output_csv_filename, mode='w')

    paper_titles = read_titles_from_csv(input_csv_filename)
    total_titles = len(paper_titles)
    
    consecutive_failures = 0

    for index, paper_title in enumerate(paper_titles):
        
        results_for_title = get_metadata_from_google_scholar(paper_title)

        if not results_for_title:
            consecutive_failures += 1
            if consecutive_failures >= 3:  # Stop if 3 consecutive requests fail
                print(f"Stopping process after {consecutive_failures} consecutive failures.")
                break
        else:
            consecutive_failures = 0
        
        save_to_csv(results_for_title, output_csv_filename)
        
        percentage_done = (index + 1) / total_titles * 100
        print(f"Processed {index + 1} out of {total_titles} titles ({percentage_done:.2f}% complete).")