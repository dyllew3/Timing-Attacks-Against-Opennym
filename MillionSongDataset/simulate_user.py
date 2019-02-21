from UserSimulator.User import User
from UserSimulator.user_behavior import calculate_session_length, Devices, load_spotify
from datetime import datetime
from datetime import timedelta
import random
import time
from json import load
import pickle
import json
import csv
import requests
from DataPreprocessor.build_user_track_dict import TrainTripletParser
from DataPreprocessor.normalize_play_counts import SongRatingNormalizer
from DataPreprocessor.create_blc_input import SparseMatGenerator
from DataPreprocessor.filter_sparse_songs import SparseSongFilter
from DataPreprocessor.build_song_dict import SongDictBuilder
from DataPreprocessor.get_top_user_artists import TopUserBuilder

from ResultProcessor.process_P import PProcessor
from ResultProcessor.build_nym_ratings import NymRatingBuilder
from ResultProcessor.get_top_nym_songs import SongListBuilder
from ResultProcessor.get_unique_nym_artists import UniqueNymArtistFilter
from ResultProcessor.get_nym_artist_variance import ArtistVarianceCalculator
from ResultProcessor.NymRatingFormatter import NymRatingFormatter
from spotify import SpotifyWrapper
from os import path

REQ = "http://localhost:4000/ratings/update"
RATINGS_REQ = "http://localhost:4000/ratings/{}/spotify.com"

# pre-selected users just for convenience
# contains tuples in the form (nym, user_number)
USER_LIST = [
    (0,234384),
    (0,234384),
    (0,402687),
    (0,462404),
    (0,669980),
    (0,991089),
    (1,679065),
    (1,723268),
    (1,889236),
    (1,954125),
    (1,964856),
    (10,12383),
    (10,222379),
    (10,241854),
    (10,332593),
    (10,436898),
    (12,179532),
    (12,351979),
    (12,473021),
    (12,811920),
    (12,94387),
    (13,190513),	
    (13,272213),	
    (13,372156),	
    (13,745999),	
    (13,752718),
    (14,152776),
    (14,291748),
    (14,555065),
    (14,880214),
    (14,948598),
    (2,202368),
    (2,8028),
    (2,869250),
    (2,957121),
    (2,975702),
    (3,329210),
    (3,491540),
    (3,622692),
    (3,819217),
    (3,835998),
    (4,143096),
    (4,411888),
    (4,470913),
    (4,669115),
    (4,792160),
    (5,169059),
    (5,472503),
    (5,502502),
    (5,599726),
    (5,883355),
    (6,151851),
    (6,269475),
    (6,427642),
    (6,483795),
    (6,864712),
    (7,117436),
    (7,471509),
    (7,542147),
    (7,605562),
    (7,66213),
    (8,355770),
    (8,400013),
    (8,689580),
    (8,74987),
    (8,824276),
    (9,189979),
    (9,396445),
    (9,513441),
    (9,543235),
    (9,753614)
]
config = load(open('config.json'))



def make_rating(nym_id, domain,  item, score, num_v,):
    return {
                "nymRating" : {
                    "numVotes" : num_v,
                    "score": score
                },
                "domain": domain,
                "item": item,
                "nym_id": nym_id
            }

def manual_update(details):
    _, nym, domain, item, rating, num_votes = details
    new_rating = make_rating(nym, domain, item, rating, num_votes+1)
    headers = { "content-type": "application/json"}
    resp = requests.put(REQ, data=json.dumps({'rating' : new_rating}), headers=headers, verify=False)
    return resp



def load_user_nym_pairs():
    nym_users_dict = {}
    user_nym_pairs = []
    path_to_P_with_ids = path.join(config["nym_data"]["base"], config["nym_data"]["P_with_ids"])
    with open(path_to_P_with_ids) as input_file:
            for line in input_file:
                user_nym_pairs.append(map(int, line.split(",")))

        # Convert list to dict
    for user, nym in user_nym_pairs:
        if nym not in nym_users_dict:
            nym_users_dict[nym] = []

        nym_users_dict[nym].append(user)
    return nym_users_dict

def load_user_song_map():
    with open(path.join(config["user_data"]["base"], config["user_data"]["user_songs_map"]), 'rb') as input_pickle:
       return pickle.load(input_pickle)
    print("Done")

def havent_played_song(user,song_id):
    song = user.song_to_id_dict[song_id]
    user_songs_map = load_user_song_map()
    nym_users_dict = load_user_nym_pairs()
    result = []
    for nym, users in nym_users_dict.items():
        # print("Building ratings for nym {}".format(nym))
        # Iterate through each user in a Nym
        for user in sorted(users):
            # For each user get every song they listened to and their play counts
            found = False
            for user_song, _ in user_songs_map[user]:
                if user_song == song:
                    found = True
                    break
            if not found:
                result.append((nym, user))              
    return sorted(result, key=lambda x: x[0])



def update_data():
        # Normalize play counts
    print("Normalizing play counts")
    song_rating_normalizer = SongRatingNormalizer(config)
    song_rating_normalizer.load_user_songs_dict()
    song_rating_normalizer.normalize_data()
    song_rating_normalizer.write_data_to_disk()
    print("Done")
    del song_rating_normalizer

    # Generate sparse matrix for BLC
    print("Generating Sparse Matrix")
    sparse_mat_generator = SparseMatGenerator(config, num_users=40000)
    sparse_mat_generator.load_data()
    sparse_mat_generator.generate_sparse_mat()
    sparse_mat_generator.write_user_data()
    print("Done")
    del sparse_mat_generator

    # Filter sparse songs from matrix
    print("Filtering Sparse Songs from matrix")
    sparse_song_filter = SparseSongFilter(config)
    sparse_song_filter.parse_sparse_mat_files()
    sparse_song_filter.filter_sparse_songs()
    sparse_song_filter.write_filtered_matrix()
    print("Done")
    del sparse_song_filter

    # Build dict of song IDs to artist-song tuples
    print("Building dict of songs")
    song_dict_builder = SongDictBuilder(config)
    song_dict_builder.load_track_list()
    song_dict_builder.write_song_details_to_file()
    print("Done")
    del song_dict_builder

    # Build the top users for dataset
    print("Outputting top users")
    top_user_builder = TopUserBuilder(config)
    top_user_builder.load_data()
    top_user_builder.get_top_songs()
    top_user_builder.dump_top_users()
    del top_user_builder

def gen_db_data():
    # Map row numbers to users in raw P file
    print("Processing P")
    p_processor = PProcessor(config)
    p_processor.generate_row_user_map()
    p_processor.map_rows_to_users()
    del p_processor

    # Build ratings for nym and write out to nym_ratings directory
    print("Generating Nym Ratings")
    nym_rating_builder = NymRatingBuilder(config)
    nym_rating_builder.load_data()
    nym_rating_builder.delete_old_ratings()
    nym_rating_builder.build_ratings()
    nym_rating_builder.dump_nym_users_map()
    del nym_rating_builder

    # Get Top Nym songs based on ratings
    print("Generating Song Lists")
    song_list_builder = SongListBuilder(config)
    song_list_builder.load_data()
    song_list_builder.load_ratings()
    song_list_builder.delete_old_songs()
    song_list_builder.build_song_lists()
    del song_list_builder

    # Get artists unique to each nym
    print("Generating artists unique to each nym")
    unique_nym_artist_filter = UniqueNymArtistFilter(config)
    unique_nym_artist_filter.load_songs()
    unique_nym_artist_filter.delete_old_artists()
    unique_nym_artist_filter.build_top_nym_artists()
    unique_nym_artist_filter.filter_unique_artists()
    del unique_nym_artist_filter

    print("Calculating Artist Variances")
    artist_variance_calculator = ArtistVarianceCalculator(config)
    artist_variance_calculator.load_data()
    artist_variance_calculator.calculate_variance()
    del artist_variance_calculator

    print("Generating ratings for db")
    nym_rating_formatter = NymRatingFormatter(config)
    nym_rating_formatter.load_data()
    nym_rating_formatter.parse_song_rankings()
    nym_rating_formatter.generate_db_input()
    del nym_rating_formatter


def load_previous_ratings(nym):
    result = {}
    with open('Data/DB_Data/ratings-1.csv', 'r') as input_file:
        ratings = csv.reader(input_file, delimiter=',')
        for _,nym_r,domain, item,rating,num_v in ratings:
            if nym_r != "nym" and int(nym_r) == nym:
                result[item] = [domain,rating,num_v]
    # sort by item
    return result

def load_new_ratings(nym):
    result = {}
    with open('Data/DB_Data/ratings.csv', 'r') as input_file:
        ratings = csv.reader(input_file, delimiter=',')
        for _,nym_r,domain, item,rating,num_v in ratings:
            if  nym_r != "nym" and int(nym_r) == nym:
                result[item] = [domain,rating,num_v]
    # sort by item
    return result

# Send new ratings to the server
def update_server(nym):
    #ratings_resp = requests.get(RATINGS_REQ.format(nym), verify=False)
    #current_ratings = ratings_resp.content[:len(ratings_resp.content) - int(ratings_resp.headers["padding-len"])]
    old_ratings = load_previous_ratings(nym)
    new_ratings = load_new_ratings(nym)
    resp = None
    for k, v in new_ratings.items():
        if (not k in old_ratings) or old_ratings[k] != v:
            domain, rating, num_v = v
            print("item:{} , rating:{}, num votes:{}".format(k, rating, num_v))
            new_rating = {
                "nymRating" : {
                    "numVotes" : int(num_v),
                    "score": float(rating)
                },
                "domain": domain,
                "item": k,
                "nym_id": nym
            }
            headers = { "content-type": "application/json"}
            resp = requests.put(REQ, data=json.dumps({'rating' : new_rating}), headers=headers, verify=False)
    return resp


def listen_to_playlist(nym, user_num):
    prev_sess = None
    user = User(nym, user_num, config)
    start = datetime.now()
    sess_length = calculate_session_length(start, Devices.Mobile)
    end = timedelta(seconds=(sess_length * 60))
    spotify_obj = load_spotify()
    decision = 'appload'
    while sess_length > 0:
        while datetime.now() < start + end:
            print("Got here")
            try:
                id, nym, domain, uri, rating, num_votes = user.get_next_recommendation()
                resp = None
                decision = playback_decision(spotify_obj, uri, decision)
                if  decision == 'trackdone':
                    resp = manual_update([id, nym, domain, uri, rating, num_votes])
                if resp:
                    to_be_added = False
                    while resp.status_code != 200 and not to_be_added:
                        rating = resp.content[:len(resp.content) - int(resp.headers["padding-len"])].decode('utf8')
                        rating = load(rating)
                        if int(rating["nymRating"]["numVotes"]) == 0:
                            to_be_added = True
                        else:
                            num_votes = float(rating["nymRating"]["score"])
                            num_votes = int(rating["nymRating"]["numVotes"])
                            resp = manual_update([id, nym, domain, uri, rating, num_votes])

            except:
                continue
        prev_sess = sess_length
        sess_length = calculate_session_length(start, Devices.Mobile, prev_session=prev_sess)
        end = timedelta(seconds=(sess_length * 60))
        start = datetime.now()
    user.dump_songs()



if __name__ == "__main__":
    start = datetime.now()
    period = timedelta(hours=3)
    for _ in range(1):
        index = random.randint(0, len(USER_LIST) - 1)
        nym, user_num = USER_LIST[index]
        print("nym:{}, user:{}".format(0, user_num))
        current_hour = datetime.now().hour
        played = False
        pick_time = random.uniform(current_hour, current_hour + 1) % 24
        while datetime.now() < start + period:
            if  not played and datetime.now().minute >= (pick_time % 1) * 60:
                listen_to_playlist(nym, user_num)
                print("finished iteration")
                played = True
            if current_hour < datetime.now().hour:
                current_hour = datetime.now().hour
                played = False
                pick_time = random.uniform(current_hour, current_hour + 1) % 24