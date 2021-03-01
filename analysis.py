import csv
from pprint import pprint
import numpy as np


games = 0
totals = np.zeros(8)
by_country = np.zeros((7,8))

with open('diplomacy-raw.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader) # skips the headers

    for row in reader:
        games += 1
        totals[int(row[2])] += 1
        
        for country in range(7):
            by_country[country][int(row[3+country])] += 1

with open('diplomacy-data.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['Country','Lost','Won','2-way Draw','3-way Draw','4-way Draw', '5-way Draw','6-way Draw', '7-way Draw']
    )
    countries = ['England','France','Italy','Germany','Austria','Turkey','Russia']

    for country, row in enumerate(by_country):
        print(row)
        writer.writerow([countries[country]] + list(row))


def pc(n):
    global games
    return f'{round(n/games*100,2)}%'

print('--- RESULTS ---\n')
print(f'Total games: {games}')
print(f'Solo wins: {totals[1]} ({pc(totals[1])})')
for i in range(6):
    print(f'{i+2}-way draws: {totals[i+2]} ({pc(totals[i+2])})')


for country in range(7):
    print(f'\n- {headers[country+3]} -')
    print(f'Losses: {by_country[country][0]} ({pc(by_country[country][0])})')
    print(f'Solo wins: {by_country[country][1]} ({pc(by_country[country][1])})')
    for i in range(6):
        print(f'{i+2}-way draws: {by_country[country][i+2]} ({pc(by_country[country][i+2])})')

pprint(by_country)