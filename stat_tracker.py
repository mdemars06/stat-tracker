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

    #find the wanted season of statistic
    season = input("Enter season ending year (e.g., '2026'): ")

    #find specific game log for the season
    game_log_url = player_url.replace(
        ".html",
        f"/gamelog/{season}"
    ) 

    response4 = requests.get(game_log_url)
    soup4 = BeautifulSoup(response4.text, 'html.parser')

    game_log = soup4.find('table', {'id': 'player_game_log_reg'})

    #scrape the specific rows
    rows = game_log.find("tbody").find_all("tr")
    game_number = input("Enter the game number (e.g., '1' for the first game of the season): ")
    row = rows[int(game_number) - 1]

    #find the specific statistic
    stat_map = {
        "points": "pts",
        "assists": "ast",
        "rebounds": "trb",
        "steals": "stl",
        "blocks": "blk",
        "turnovers": "tov",
        "minutes": "mp",
        "fgm": "fg",
        "fga": "fga",
        "fg%": "fg_pct",
        "3pm": "fg3",
        "3pa": "fg3a",
        "3pt%": "fg3_pct",
        "ftm": "ft",
        "fta": "fta",
        "ft%": "ft_pct",
        "plus_minus": "plus_minus",
        "game_score": "game_score"
    }

    wanted_stat = input("Enter the statistic you want to retrieve (e.g., 'points', 'fg%', 'minutes'): ").lower()
    if wanted_stat in stat_map:
        stat_data = row.find('td', {'data-stat': stat_map[wanted_stat]})
        print(f"{player_name}'s Game {game_number} {wanted_stat}: {stat_data.get_text(strip=True)}")
    else:
        print("Statistic not found.")
    

if __name__ == "__main__":
    NBA()
