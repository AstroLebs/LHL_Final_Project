import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_fbref_scouting_reports():

    # URL for the EPL page on FBref.com
    url = 'https://fbref.com/en/comps/9/wages/Premier-League-Wages'
    
    
    response = requests.get(url)
    if response.status_code == 200:
        
        soup = BeautifulSoup(re.sub("<!--|-->","", str(response.content)), "lxml")
        table = soup.find("table",{"id":"player_wages"})
        
        player_urls = [a['href'] for a in table.select('tbody tr td[data-stat="player"] a')]
        
        scouting_reports = []
        
        for player_url in player_urls:
            full_url = 'https://fbref.com' + player_url
            
            player_response = requests.get(full_url)
            
            if player_response.status_code == 200:
                player_soup = BeautifulSoup(player_response.content, 'html.parser')
                
                scouting_table = player_soup.find('table', {'id': 'scout_summary_MF'})
                if not scouting_table:
                    continue
                scouting_data = [data.text for data in scouting_table.select('td')]
                
                scouting_reports.append(scouting_data)
            else:
                print(f"Failed to retrieve data for player: {full_url}")
        
        df = pd.DataFrame(scouting_reports)
        
        df.to_csv('epl_scouting_reports.csv', index=False)
        
        print("Scraping completed. Scouting reports saved to 'epl_scouting_reports.csv'")
    else:
        print("Failed to retrieve data from FBref.com")
        print(response.status_code)
scrape_fbref_scouting_reports()
