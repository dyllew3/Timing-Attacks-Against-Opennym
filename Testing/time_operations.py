NUM_TESTS = 1
import json
import requests
import time
URL = "https://34.248.8.95"


rating_update = {
        "nymRating" : {
            "numVotes" : 27,
            "score": 5.00
        },
        "domain": "spotify.com",
        "item": "4xp6O8cMjMZiIn0TrNC3ji",
        "nym_id": 3
}

def make_requests(req, put_req=False, dat=None):
    headers = { "content-type": "application/json"}
    with requests.Session() as s:
        for i in range(NUM_TESTS):
            if not put_req:
                a = s.get(req, verify=False, headers={'Z-padding':'00000'})
            else:
                s.put(req, data=json.dumps({'rating' : rating_update}), headers=headers, verify=False)
                rating_update["nymRating"]["numVotes"] += 1
            print(i)
            time.sleep(0.2)
    return 0

def main():
    # Nyms
    #make_requests(URL + ':4400/nym')
    #make_requests(URL + ':4400/nym/0')

    # Ratings
    #make_requests(URL + ':4400/ratings/3/spotify.com')
    #make_requests(URL + ':4400/ratings/update', True, rating_update)

    # Cookies
    #make_requests(URL + ':4400/cookies/1')
    #make_requests(URL + ':4400/cookies/1/spotify.com')
    #make_requests(URL + ':4400/cookies/issued/1/spotify.com')

    # Rules
    #make_requests(URL + ':4400/rules/supported')
    #make_requests(URL + ':4400/rules/supported/version')
    #make_requests(URL + ':4400/rules/top/3')
    #make_requests(URL + ':4400/rules/spotify.com')
    #make_requests(URL + ':4400/rules/issued/spotify.com')

    # Identity
    #make_requests(URL + ':4400/identity/spotify.com')

    # Not working
    # make_requests(URL + ':4400/identity/spotify.com/timestamp')
    
    #make_requests(URL + ':4400/identity/nym/spotify.com/3')
    
    # Not working
    # make_requests(URL + ':4400/identity/nym/spotify.com/3/timestamp')
    
    # Not working
    # make_requests(URL + ':4400/identity/map/:domain/:username')

    return 0

if __name__ == "__main__":
    main()