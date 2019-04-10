#!/usr/bin/python3

from os import listdir, path
from pickle import load, dump
import csv

def format_artist(artist):
    final_artist_string = artist
    stop_words = ["/", " Feat", " feat ", " ft ", " Vs", " vs"]
    for stop_word in stop_words:
        if stop_word in final_artist_string:
            end = final_artist_string.index(stop_word)
            final_artist_string = final_artist_string[:end].strip()
    return final_artist_string


def get_top_artists(filepath):
    nym_top_artists = []
    with open(filepath) as input_file:
        for i in range(10):
            line = input_file.readline()
            if not line:
                break
            artist = format_artist(line.split("<SEP>")[0].strip())
            print(artist)
            nym_top_artists.append(artist)

    return nym_top_artists

class User:
    
    def __init__(self, nym, user_num,config):
        self.nym = nym
        self.is_playlist = False
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
        self.user_times = []
        self.playlist = []
        self.playlist_index = 0
        self.song_to_uri = {}
        top_artists_dir = path.join(config["nym_data"]["base"], config["nym_data"]["nym_variance_dir"])
        top_artists_file_format = config["nym_data"]["file_formats"]["top_artists"]
        dir_files = listdir(top_artists_dir)
        top_artists_file = [f for f in dir_files if "{}_top_artists.csv".format(nym) == f][0]
        print(top_artists_file)
        self.top_artists = get_top_artists(path.join(top_artists_dir, top_artists_file))

        # Load users songs map
        self.user_songs_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"])
        #self.load_user_songs()
        # Load users
        self.user_to_id_map_path = path.join(config["user_data"]["base"], config["user_data"]["user_to_id_map"])
        #self.load_users()
       
        # Load song id to their num id
        self.sids_to_ids_map_path = path.join(config["song_data"]["base"], config["song_data"]["sids_to_ids_map"])
        #self.load_song_ids()
        
        # Load song num id to their details
        self.sids_to_details_map_path = path.join(config["song_data"]["base"], config["song_data"]["sid_to_details_map"])
        #self.load_song_details()
        
        # Load song uri to songs
        self.song_to_uri_path = path.join(config["song_data"]["base"], config["song_data"]["song_to_uri_map"])
        self.load_uri_to_songs()
        
        # Load recommendations
        self.recommendations_path = path.join(config["database_data"]["base"], config["database_data"]['input_data'])
        self.load_recommendations()

        self.nym_songs_path = path.join(config["nym_data"]["base"], config["nym_data"]["nym_songs_dir"])
        self.create_playlist()


    def load_uri_to_songs(self):
        with open(self.song_to_uri_path, 'rb') as input_pickle:
            print('Loading and inverting dictionary')
            for k, v in load(input_pickle).items():
                song, artist = k.split("<SEP>")
                self.uri_to_song[v] = (artist, song)
                self.song_to_uri[song] = v
            print("Done")

    def create_playlist(self, size=100):
        with open(path.join(self.nym_songs_path, '{}.csv'.format(self.nym)),'r') as input_f:
            songs = list(csv.reader(input_f, delimiter=','))
            for x in songs:
                song, _ = x[0].split("<SEP>")
                if song in self.song_to_uri:
                    self.playlist.append(self.song_to_uri[song])
                if len(self.playlist) >= size:
                    break

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

    def load_song_tuples(self):
        with open(self.sids_to_details_map_path, 'rb') as output_pickle:
            print("Loading out song dict to pickle")
            self.song_tuple_list = load(output_pickle)
            print("Done")

    def update_user_play_count(self, song_id, amount=1):
        result = []
        song_num = self.song_to_id_dict[song_id]
        user_songs = self.user_songs_map[self.user_num]
        found = False
        for s_id, plays in user_songs:
            if s_id == song_num:
                plays += amount
                found = True
            result.append((s_id, plays))
        if not found:
            result.append((song_num, amount))
        self.user_songs_map[self.user_num] = result

    def played_song(self, song_id):
        song_num = self.song_to_id_dict[song_id]
        user_songs = self.user_songs_map[self.user_num]
        for s_id, _ in user_songs:
            if s_id == song_num:
               return True
        return False

    def find_sid(self, song_details):
        for k, v in self.sids_to_details_map.items():
            if v == song_details:
                return k
        return None

    def get_next_recommendation(self):
        self.current_recommendation += 1 
        current_recommendation = self.current_recommendation - 1
        self.current_recommendation %= len(self.recommendations)
        return self.recommendations[current_recommendation]

    def get_prev_recommendation(self):
        current_recommendation = self.current_recommendation
        self.current_recommendation -= 1 
        if self.current_recommendation < 0:
            self.current_recommendation = len(self.recommendations) - 1
        return self.recommendations[current_recommendation]

    def set_recommendation(self, index):
        self.current_recommendation = index
        return self.recommendations[index]

    def dump_songs(self):
        print("Writing new users song map to disk")
        with open(self.user_songs_map_path, 'wb') as output:
            dump(self.user_songs_map, output)
        print("Done")