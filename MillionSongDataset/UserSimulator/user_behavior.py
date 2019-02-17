from enum import Enum
from spotify import SpotifyWrapper
from ResultProcessor.NymRatingFormatter import NymRatingFormatter
from json import load
from os import path
from random import random
from datetime import datetime
import time

class Devices(Enum):
    Mobile = 0
    Desktop = 1
    Desktop_1 = 2
    Mobile_1 = 3

class Days(Enum):
    Monday = 0
    Tuesday = 1
    Wendesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

Evening_Peak = (18.00, 19.00)
Morning_Peak = (9.00, 10.00)
Mobile_Worst_Morning = (3.00, 6.00)
# Approximate median of mobile spotify session length in minutes
Mobile_Session_length = 5.00

# Approximate median of desktop spotify session length in minutes
# However it is a function of the time when session started
Desktop_Session_Length = 50.00

NUM_PLAYBACKS = 684807

# Probability of listening to the full track
PROB_FULL_LISTEN = 400000/NUM_PLAYBACKS

# Probability of skipping after 5% duration of the track
PROB_SKIP = 0.8625 - PROB_FULL_LISTEN

Time_Info = {
    Devices.Desktop : {

    },
    Devices.Mobile: {
        'peak':(15.00, 18.00),
        'lowest':(3.00, 6.00)
    }
}

def calculate_session_length(day_info, device, prev_session=None):
    if device == Devices.Mobile:
        day_time =  day_info.time().hour()
        # Lowest time time for mobile userd
        if day_info.weekday() == Days.Saturday and day_time >= Mobile_Worst_Morning[0] and day_time <= Mobile_Worst_Morning[1]:
            return 0.0
        else:
            return Mobile_Session_length
    elif device == Devices.Desktop:
        return Desktop_Session_Length
    return 0.0


def load_spotify():
    config = load(open('../config.json'))
    nym_rat = NymRatingFormatter(config)
    nym_rat.load_data()
    nym_rat.parse_song_rankings()
    nym_rat.get_song_spotify_ids()
    return nym_rat.get_song_spotify_object()

def playback_decision(spotify_obj, uri):
    duration  = spotify_obj.get_duration(uri)
    rand_float = random()
    if duration:
        if rand_float >= 0 and rand_float < PROB_SKIP: 
            time.sleep(float(duration)/20)
        elif rand_float >= PROB_SKIP and rand_float < PROB_SKIP + PROB_FULL_LISTEN:
            time.sleep(float(duration)) 
    else:
        time.sleep(0.5)