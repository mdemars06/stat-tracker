import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def NBA():
    """This function retrieves the specified statistic for the given NBA player."""

    player_name = input("Enter the name of the NBA player: ")

    #Find the wanted letter
    last_initial = player_name.split()[-1][0]

    base_url = "https://www.basketball-reference.com/players/"
    letter_url = f"https://www.basketball-reference.com/players/{last_initial.lower()}/"
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find the wanted heading
    target_heading = soup.find('a', string=last_initial.upper())

    #Open the wanted heading page
    page_url = urljoin(base_url, letter_url)

    response2 = requests.get(page_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    #scrape the actual player names
    players = soup2.select('th[data-stat="player"] a')

    for player in players:
        chosen_player = player.get_text(strip=True)
        if chosen_player.lower() == player_name.lower():
            #open the wanted player page
            player_url = urljoin(base_url, player['href'])
            response3 = requests.get(player_url)
            soup3 = BeautifulSoup(response3.text, 'html.parser')
            print(player_url)
            

if __name__ == "__main__":
    NBA()
