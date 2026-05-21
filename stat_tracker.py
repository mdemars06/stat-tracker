import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""This function retrieves the specified statistic for the given NBA player."""

base_url = "https://www.basketball-reference.com/players/"
letter_url = "https://www.basketball-reference.com/players/y/"
player_url = 'https://www.basketball-reference.com/players/y/youngtr01.html'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

#Find the wanted heading
target_heading = soup.find('a', string='Y')

#Open the wanted heading page
page_url = urljoin(base_url, letter_url)

response2 = requests.get(page_url)
soup2 = BeautifulSoup(response2.text, 'html.parser')

#scrape the actual player names
players = soup2.select('th[data-stat="player"] a')

for player in players:
    print(player.get_text(strip=True))

#open the wanted player page
response3 = requests.get(player_url)
soup3 = BeautifulSoup(response3.text, 'html.parser')
print("Trae Young")