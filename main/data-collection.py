import requests
from bs4 import BeautifulSoup
import csv

# Currently, it only searches through 'standard' games

# To change search options:
# - Go to https://www.playdiplomacy.com/games.php?subpage=all_finished
# - Select the options
# - click 'Search Game'
# - replace the url below with the one in your browser

def url(n):
    return f'https://www.playdiplomacy.com/games.php?subpage=all_finished&game_title=&game_id=&with_usr=&with_usr_2=&type-regular=1&variant-0=1&map_variant-0=1&speed=&ambassador=&grace=&NMR_protect=&shorthanded=&fog=no&stuff_happens=no&esc=no&pc2=no&current_page={n}'


# -----

# 5748 pages
# 2-3 seconds per page
# ~5 hours


# These were useful for when it got interrupted a few times.
start_page = 1
pages = 1000

with open('diplomacy-raw.csv','a') as f:
    writer = csv.writer(f)

    for i in range(pages):
        print(f'Page {start_page + i}...')

        r = requests.get(url(start_page + i))
        soup = BeautifulSoup(r.text, 'html.parser')

        # There is one player list per game
        player_lists = soup.find_all('ul', class_='playerlist')
        titles = soup.find_all('h3')

        for n, player_list in enumerate(player_lists):
            game_id = titles[n].text.split('.')[0]
            players = player_list.find_all('li')
            
            results = []

            try:
                for player in players:
                    # The first image is the flag of the country they're playing as
                    country = player.find('img')['title']
                    result = player.find('b')
                    
                    if result == None:
                        results.append('0')
                    elif result.text == "(SOLO WIN)":
                        results.append('1')
                    elif 'DRAW' in result.text:
                        results.append(result.text[1])
                    else:
                        print('Lol')
            except:
                print('Something went wrong, skipping this game.')
            
            if int(max(results)) > 0:
                writer.writerow(
                    [start_page + i] + [game_id] + [max(results)] + results 
                )
