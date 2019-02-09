from UserSimulator.User import User
import random
import time
from json import load
import json
import csv
import requests

REQ = "http://localhost:4000/ratings/update"
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

# Send new ratings to the server
def update_server(song_uri):
    resp = None
    with open('Data\\DB_Data\\ratings.csv', 'r') as input_file:
        ratings = csv.reader(input_file, delimiter=',')
        for rating in ratings:
            if rating[3] == song_uri:
                new_rating = {
                    "nymRating" : {
                        "numVotes" : int(rating[5]),
                        "score": int(rating[4])
                    },
                    "domain": rating[2],
                    "item": rating[3],
                    "nym_id": rating[1]
                }
                headers = { "content-type": "application/json"}
                resp = requests.put(REQ, data=json.dumps({'rating' : new_rating}), headers=headers, verify=False)
    return resp

config = load(open('config.json'))

def listen_to_playlist():
    index = random.randint(0, len(USER_LIST) - 1)
    nym, user_num = USER_LIST[index]
    user = User(nym, user_num, config)
    count = 10
    while True:
        print("running user")
        uri = user.get_next_recommendation()[3]
        song_sid = (user.find_sid(user.uri_to_song[uri]))
        user.update_user_play_count(song_sid, 200)
        user.dump_songs()
        if count <= 0:
            break
        count -= 1
        time.sleep(.50)
    pass

if __name__ == "__main__":
    listen_to_playlist()