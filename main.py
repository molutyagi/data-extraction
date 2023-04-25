import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the input file
input_file = pd.read_excel("input.xlsx")

# Loop through each row and extract the article text
for index, row in input_file.iterrows():
    url_id = row["URL_ID"]
    url = row["URL"]
    # Send a GET request to the URL and get the HTML content
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        continue

    html_content = response.content

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the article title and text
    try:
        article_title = soup.find('h1').text.strip()
        article_text = ''
        for p in soup.find('div', class_='td-post-content').find_all('p'):
            article_text += p.text.strip() + '\n\n'
    except AttributeError as e:
        continue

    # Save the extracted text to a file with URL_ID as its name
    with open(f"{url_id}.txt", "w", encoding="utf-8") as file:
        file.write(article_title + '\n\n' + article_text)
