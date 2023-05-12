# -*- coding: utf-8 -*-
"""web automation utils


GetMap:  
    mymap = GetMap("愛知").map_dict
    >>> {'region': '愛知', 'lat': 35.05767555613034, 'lon': 137.11860992979004, 'accuracy': 100}


Todo:
    -set map.csv
    
"""


import csv
import os
import random
import pysnooper
import json
from pprint import pprint


class GetMap:
    """Get map from region


    Usage:
        mymap = GetMap("愛知").map_dict
        >>> {'region': '愛知', 'lat': 35.05767555613034, 'lon': 137.11860992979004, 'accuracy': 100}
    """

    def __init__(self, region):
        self.maplist = self.get_maplist()
        map_dict = [mp for mp in self.maplist if mp['region'] in region][0]
        self.map_dict = self.random_map(map_dict)

        
    @pysnooper.snoop()
    def get_maplist(self):
        """get latitude longitude by region 
        
        Args:
            region (string): 

        Returns:
            dict or list of dict: if region is None list of dict else dict
        """
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.csv"))
        with open(file_path, 'r',encoding="utf-8", newline="") as f:
            map_list = [{'region': mp[0], 'lat': mp[1], 'lon': mp[2]} for mp in csv.reader(f) if mp[0] != 'region']

        return map_list

    @pysnooper.snoop()
    def random_map(self,map_dict):
        latitude_min = float(map_dict['lat']) - 0.5
        latitude_max = float(map_dict['lat']) + 0.5
        longitude_min = float(map_dict['lon']) - 0.5
        longitude_max = float(map_dict['lon']) + 0.5
        maplist = [latitude_min, latitude_max, longitude_min, longitude_max]
        latitude = random.uniform(maplist[0], maplist[1])
        longitude = random.uniform(maplist[2], maplist[3])
        map_cord = {
            "region": map_dict['region'],
            "lat": latitude,
            "lon": longitude,
            "accuracy": 100
        }
        return map_cord


if __name__ == '__main__':

    mymap = GetMap("愛知県").map_dict
    print('a')