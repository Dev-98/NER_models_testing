import requests
from bs4 import BeautifulSoup

def extract_text_from_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            extracted_text = ' '.join(text for text in soup.stripped_strings)
            return extracted_text
        else:
            return "Failed to retrieve the web page. Status code: {}".format(response.status_code)
    except Exception as e:
        return "An error occurred: {}".format(str(e))

website_url = "https://en.wikipedia.org/wiki/Common_sunflower"
extracted_text = extract_text_from_website(website_url)
print(extracted_text)
