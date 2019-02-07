NUM_TESTS = 1
import json
import requests
import time
URL = "http://localhost"


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
                print(a.headers)
                print(len(a.content))
            else:
                s.put(req, data=json.dumps({'rating' : rating_update}), headers=headers, verify=False)
                rating_update["nymRating"]["numVotes"] += 1
            print(i)
            time.sleep(0.2)
    return 0

def main():
    # Nyms
    #make_requests(URL + ':4000/nym')
    make_requests(URL + ':4000/nym/0')

    # Ratings
    #make_requests(URL + ':4000/ratings/3/spotify.com')
    #make_requests(URL + ':4000/ratings/update', True, rating_update)

    # Cookies
    #make_requests(URL + ':4000/cookies/1')
    #make_requests(URL + ':4000/cookies/1/spotify.com')
    #make_requests(URL + ':4000/cookies/issued/1/spotify.com')

    # Rules
    #make_requests(URL + ':4000/rules/supported')
    #make_requests(URL + ':4000/rules/supported/version')
    #make_requests(URL + ':4000/rules/top/3')
    #make_requests(URL + ':4000/rules/spotify.com')
    #make_requests(URL + ':4000/rules/issued/spotify.com')

    # Identity
    #make_requests(URL + ':4000/identity/spotify.com')

    # Not working
    # make_requests(URL + ':4000/identity/spotify.com/timestamp')
    
    #make_requests(URL + ':4000/identity/nym/spotify.com/3')
    
    # Not working
    # make_requests(URL + ':4000/identity/nym/spotify.com/3/timestamp')
    
    # Not working
    # make_requests(URL + ':4000/identity/map/:domain/:username')

    return 0

if __name__ == "__main__":
    main()