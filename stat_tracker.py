import requests
import unicodedata
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

    #Open the wanted heading page
    response2 = requests.get(letter_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    #scrape the actual player names
    players = soup2.select('th[data-stat="player"] a')
    player_url = None

    for player in players:
        chosen_player = player.get_text(strip=True)
        if chosen_player.lower() == player_name.lower():
            #open the wanted player page
            player_url = urljoin(base_url, player['href'])
            break
    if player_url is None:
        print("Player not found.")
        return

    response3 = requests.get(player_url)
    soup3 = BeautifulSoup(response3.text, 'html.parser')

    #find the wanted statistic
    stat_map = {
    "points": "pts_per_g",
    "assists": "ast_per_g",
    "rebounds": "trb_per_g",
    "fg%": "fg_pct",
    "3pt%": "fg3_pct",
    "ft%": "ft_pct"
    }

    wanted_stat = input("Enter the statistic you want to retrieve (e.g., 'points', 'assists', 'rebounds'): ").lower()
    if wanted_stat in stat_map:
        stat_data = soup3.find('td', {'data-stat': stat_map[wanted_stat]})
        print(f"{player_name}'s {wanted_stat}: {stat_data.get_text(strip=True)}")
    else:
        print("Statistic not found.")

if __name__ == "__main__":
    NBA()
