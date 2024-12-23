import requests, time
from bs4 import BeautifulSoup


def scrape_sentences(url):
    # Stuur een GET-verzoek naar de URL met een User-Agent header
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # Controleer of de aanvraag succesvol was
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {response.status_code}")
        return []

    # Parse de HTML-inhoud met BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Zoek naar zinnen in de HTML (pas de selector aan op basis van de website)
    sentences = []
    for paragraph in soup.find_all('p'):  # Zoek in alle <p> tags
        sentences.extend(paragraph.text.split('. '))  # Splits op punten om zinnen te krijgen

    # Filter lege zinnen en strip whitespace
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    return sentences

def save_sentences_to_file(sentences, filename):
    with open(filename, 'a', encoding='utf-8') as f:  # Gebruik 'a' om aan te hangen
        for sentence in sentences:
            f.write(sentence + '\n')  # Schrijf elke zin op een nieuwe regel

def scrape_multiple_pages(urls, filename):
    starttime = time.time()
    for url in urls:
        print(f"Scraping {url}")
        sentences = scrape_sentences(url)
        
        if sentences:
            save_sentences_to_file(sentences, filename)
            print(f"Saved {len(sentences)} sentences from {url} to '{filename}'.")
        else:
            print(f"No sentences found at {url}.")
        
        time.sleep(0.1)  # Wacht even tussen verzoeken om overbelasting te voorkomen
    endtime = time.time()
    finaltime = endtime-starttime
    print(f"Scraping complete in {finaltime} seconds.")

def main():
    urls = [
        "https://pornhub.com",
        "https://sexverhalen.com"
    ]
    
    scrape_multiple_pages(urls, 'sentences.txt')

if __name__ == "__main__":
    main()
