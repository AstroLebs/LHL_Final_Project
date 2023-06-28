import pickle
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import re


def scrape_fbref_scouting_reports(retry):
    if retry is None:
        retry = 0
    else:
        print(f'waiting for {retry} seconds')
        sleep(retry)
    print('start') 
    # URL for the EPL page on FBref.com
    url = 'https://fbref.com/en/comps/9/wages/Premier-League-Wages'
    response = requests.get(url, headers = {'User-agent': 'fpl_test'})
    if response.status_code == 200:
        print('Finding Players')
        soup = BeautifulSoup(re.sub("<!--|-->","", str(response.content)), "lxml")
        table = soup.find("table",{"id":"player_wages"})
        
        player_urls = [a['href'] for a in table.select('tbody tr td[data-stat="player"] a')]
        
        scouting_report = {'MF': [],'FW': [],'FB': [], 'GK': [], 'AM': [], 'CB': []}
        request_count = 0
        print('Loop Started')
        for player_url in player_urls:
            full_url = 'https://fbref.com' + player_url
            if request_count >= 25:
                
                request_count = 0
                print('Sleeping to avoid 429 status code')
                sleep(30)

            player_response = requests.get(full_url)
            if int(player_response.status_code) == 429:
                print(f"Sleeping for: {player_response.headers['Retry-After']}")
                sleep(int(player_response.headers['Retry-After']))
                player_response = requests.get(full_url)

            request_count += 1
            if player_response.status_code == 200:
                player_soup = BeautifulSoup(player_response.content, 'html.parser')
                
                # Add check against FPL Data
                for pos in ['MF','FW','FB','GK','AM','CB']:
                    scouting_table = player_soup.find('table', {'id': f'scout_summary_{pos}'})
                    if scouting_table is not None:
                        scouting_report[pos].append((player_url, [data.text for data in scouting_table.select('td')]))
                    else:
                        scouting_report[pos].append(None)

                print(f'Success: {full_url}')
            else:
                print(f"Failed to retrieve data for player: {full_url} | {player_response.status_code}")

            date = datetime.now()
            file_path = f'FBREF_SCOUT_{date.strftime('%Y%m%d').pickle'

            # Save the object to a pickle file
            with open(file_path, 'wb') as f:
                    pickle.dump(scouting_report, f)
            
        print("Scraping completed. Scouting reports saved")
    else:
        print("Failed to retrieve data from FBref.com")
        print(response.status_code)
        print(response.headers['Retry-After'])
        print(type(response.headers['Retry-After']))
        scrape_fbref_scouting_reports(int(response.headers['Retry-After']))
scrape_fbref_scouting_reports(0)
