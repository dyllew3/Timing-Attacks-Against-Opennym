from UserSimulator.User import User
from UserSimulator.user_behavior import calculate_session_length, Devices, load_spotify, playback_decision
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
import numpy as np
from ResultProcessor.process_P import PProcessor
from ResultProcessor.build_nym_ratings import NymRatingBuilder
from ResultProcessor.get_top_nym_songs import SongListBuilder
from ResultProcessor.get_unique_nym_artists import UniqueNymArtistFilter
from ResultProcessor.get_nym_artist_variance import ArtistVarianceCalculator
from ResultProcessor.NymRatingFormatter import NymRatingFormatter
from spotify import SpotifyWrapper
from os import path

REQ = "https://ec2-52-50-185-176.eu-west-1.compute.amazonaws.com:4400/ratings/update"
RATINGS_REQ = "http://localhost:4000/ratings/{}/spotify.com"

import threading
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






def listen_to_playlist(nym, user_num):
    prev_sess = None
    user = User(nym, user_num, config)
    start = datetime.now()
    sess_length = float(calculate_session_length(start, Devices.Mobile))
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
                    print("Updating")
                    resp = manual_update([id, nym, domain, uri, rating, int(num_votes)])
                elif decision == "clickrow":
                    user.set_recommendation(random.randint(0, len(user.recommendations)))
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

            except Exception as e:
                print(e)
        prev_sess = sess_length
        sess_length = calculate_session_length(start, Devices.Mobile, prev_session=prev_sess)
        print("Session length is {}".format(sess_length))
        end = timedelta(seconds=(int(sess_length) * 60))
        start = datetime.now()

def load_users(users_tuples):
    result = []
    for user_tuple in users_tuples:
        nym, user = user_tuple
        result.append(User(config, nym, user))
    return result


def run_for(period, nym, user):
    current_hour = datetime.now().hour
    pick_time = random.uniform(current_hour, current_hour + 1) % 24
    print("Picked time is {}".format(pick_time))
    played = False
    while datetime.now() < start + period:
        if  not played and datetime.now().minute >= (pick_time % 1) * 60:
            listen_to_playlist(nym, user)
            print("finished iteration")
            played = True
        if current_hour < datetime.now().hour:
            current_hour = datetime.now().hour
            played = False
            pick_time = random.uniform(current_hour, current_hour + 1) % 24


if __name__ == "__main__":
    start = datetime.now()
    period = timedelta(hours=3)
    num_users = int(input())
    users_tuples_indexes = np.random.choice(len(USER_LIST), num_users, replace=False)
    users_tuples = [USER_LIST[x] for x in users_tuples_indexes]
    for user in users_tuples:
        threading.Thread(target=run_for, args=(period, user[0], user[1])).start()
    