from enum import Enum
from spotify import SpotifyWrapper
from ResultProcessor.NymRatingFormatter import NymRatingFormatter
from json import load
from os import path
from random import random
from datetime import datetime
import time
import numpy as np
from itertools import repeat

class MarkovUserBehavior:
    START_STATE = "appload"
    def __init__(self):
        self.states = ['fwdbtn','clickrow','trackdone','appload'] 
        self.transition_matrix = [
            [0.75, 0.05, 0.20, 0.00],
            [0.08, 0.58, 0.34, 0.00],
            [0.102, 0.055, 0.842, 0.001],
            [0.15, 0.14, 0.55, 0.16]
        ]

    def get_next_state(self, current_state):
        row = self.states.index(current_state)
        return  np.random.choice(self.states, 1, p=self.transition_matrix[row])

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


def approx_sess_len(prev_session):
    if prev_session <= 6:
        return np.random.choice([4, 0], 1, p=[0.5, 0.5])
    else:
        rise = (8 - 4)/(14.00 - 6.00)
        median_val = rise * prev_session + 1.0
        return np.random.choice([median_val, 0], 1, p=[0.5, 0.5])

def calculate_session_length(day_info, device, prev_session=None):
    if device == Devices.Mobile:
        day_time =  day_info.time().hour
        # Lowest time time for mobile users
        if day_info.weekday() == Days.Saturday and day_time >= Mobile_Worst_Morning[0] and day_time <= Mobile_Worst_Morning[1]:
            return 0.0
        elif not prev_session:
            return Mobile_Session_length
        elif prev_session:
            if prev_session <= 6:
                return np.random.choice([4, 0], 1, p=[0.5, 0.5])[0]
            else:
                return approx_sess_len(prev_session)[0]
    elif device == Devices.Desktop:
        return Desktop_Session_Length
    return 0.0


def load_spotify():
    config = load(open('config.json'))
    nym_rat = NymRatingFormatter(config)
    nym_rat.load_data()
    nym_rat.parse_song_rankings()
    return nym_rat.get_song_spotify_object()

def playback_decision(spotify_obj, uri, user_decision):
    duration  = spotify_obj.get_duration(uri)
    a = MarkovUserBehavior()
    next_dec = user_decision
    if duration:
        duration = duration/10
        next_dec = a.get_next_state(user_decision)
        if next_dec == 'fwdbtn' or next_dec == 'clickrow' :
            print("Skipping")
            time.sleep(float(duration)/20)
        elif next_dec == 'trackdone':
            print("Playing")
            print("Duration is {}".format(str(duration)))
            time.sleep(float(duration))
        return next_dec
    else:
        print("no duration found")
    return next_dec