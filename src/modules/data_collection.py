import requests
from modules.constants import FPL_URL


class FPL_Data_Collection:
    def __init__(self):
        with requests.Session() as s:
            r = s.get(url=FPL_URL)
            self.json = r.json()

    def get_full_json(self):
        """Returns the full request in a json format"""
        return self.json

    def get_player_data(self):
        """Returns the JSON data for each player"""
        return self.json["elements"]

    def get_positional_data(self):
        """Returns the JSON data relating to player position"""
        return self.json["element_types"]

    def get_team_data(self):
        """Returns the JSON data relating to the teams in the EPL"""
        return self.json["teams"]

    def get_all_data(self):
        return [self.json["elements"], self.json["element_types"], self.json["teams"]]
