import requests
from bs4 import BeautifulSoup

url = 'https://wikidocs.net/85739'

response = requests.get(url)
# print(response)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#load_content > div.page-content.tex2jax_process')
    print(title.get_text())

else :
    print(response.status_code)

