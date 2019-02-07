#!/usr/bin/python3

from os import path
from pickle import load, dump
import csv


class User:
    
    def __init__(self, nym, user_num,config):
        self.nym = nym
        self.user_num = user_num
        self.current_recommendation = 0
        self.recommendations = []
        self.user_songs_dict = {}
        self.song_to_id_dict = {}
        self.user_to_id_dict = {}
        self.user_songs_map = {}
        self.song_tuple_list = {}
        self.sids_to_details_map = {}
        self.uri_to_song = {}

        # Load users songs map
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
        self.load_user_songs()
        # Load users
        self.user_to_id_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_id_map"])
        self.load_users()
       
        # Load song id to their num id
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])
        self.load_song_ids()
        
        # Load song num id to their details
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        self.load_song_details()
        
        # Load song uri to songs
        self.song_to_uri_path = path.join(config["song_data"]["base"], config["song_data"]["song_to_uri_map"])
        self.load_uri_to_songs()
        
        # Load recommendations
        self.recommendations_path = path.join(config["database_data"]["base"], config["database_data"]['input_data'])
        self.load_recommendations()


    def load_uri_to_songs(self):
        with open(self.song_to_uri_path, 'rb') as input_pickle:
            print('Loading and inverting dictionary')
            for k, v in load(input_pickle).items():
                song, artist = k.split("<SEP>")
                self.uri_to_song[v] = (artist, song)
            print("Done")

    def load_song_ids(self):
        with open(self.sids_to_ids_map_path, 'rb') as output:
            self.song_to_id_dict = load(output)
            print("Loaded dict of song ids to numbers")
    
    def load_song_details(self):
        with open(self.sids_to_details_map_path, 'rb') as input_pickle:
            self.sids_to_details_map = load(input_pickle)
            print('loaded song details')

    def load_user_songs(self):
        print("Loading user songs map")
        with open(self.user_songs_map_path, 'rb') as input_pickle:
            self.user_songs_map = load(input_pickle)
        print("Done")
    
    # Loads the dictionary of users_num to their id
    def load_users(self):
        with open(self.user_to_id_map_path, 'rb') as input_pickle:
            self.user_to_id_dict = load(input_pickle)
            print("Loaded dict of users to numbers")
        pass

    # Loads the recommendations from db file
    def load_recommendations(self):
        with open( self.recommendations_path, 'r' ) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            # Remove empty lists and only look at songs from the nym
            self.recommendations =  list(filter(lambda x: x != [] and x[1] == str(self.nym), csv_reader))
        self.current_recommendation = len(self.recommendations) - 1

    def load_song_tuples(self):
        with open(self.sids_to_details_map_path, 'rb') as output_pickle:
            print("Loading out song dict to pickle")
            self.song_tuple_list = load(output_pickle)
            print("Done")

    def update_user_play_count(self, song_id, amount=1):
        result = []
        song_num = self.song_to_id_dict[song_id]
        print(song_num)
        user_songs = self.user_songs_map[self.user_num]
        for s_id, plays in user_songs:
            if s_id == song_num:
                plays += amount
            result.append((s_id, plays))
        self.user_songs_map[self.user_num] = result

    def find_sid(self, song_details):
        for k, v in self.sids_to_details_map.items():
            if v == song_details:
                return k
        return None

    def get_next_recommendation(self):
        self.current_recommendation -= 1
        return self.recommendations[self.current_recommendation + 1]

    def dump_songs(self):
        print("Writing new users song map to disk")
        with open(self.user_songs_map_path, 'wb') as output:
            dump(self.user_songs_map, output)
        print("Done")