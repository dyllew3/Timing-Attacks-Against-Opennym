import psycopg2
from csv import reader
from random import random, randint

NYM_TABLE = "nyms"
RATING_TABLE = "ratings"
METADATA_TABLE = "nym_metadata"
COOKIES_TABLE = "session_cookies"
RULES_TABLE = "rules"
DEFENSE_TABLE = "defenses"

conn = psycopg2.connect("dbname='nym_server_dev' user='opennym' password='opennym' host='localhost'")
cur = conn.cursor()

delete_command = "DELETE FROM {}".format(COOKIES_TABLE)
cur.execute(delete_command)

# Delete all ratings in the Rating Table
delete_command = "DELETE FROM {}".format(RATING_TABLE)
cur.execute(delete_command)

# Delete all data in Nyms table
delete_command = "DELETE FROM {}".format(NYM_TABLE)
cur.execute(delete_command)

# Delete all rules in the Rating Table
delete_command = "DELETE FROM {}".format(RULES_TABLE)
cur.execute(delete_command)

delete_command = "DELETE FROM {}".format(METADATA_TABLE)
cur.execute(delete_command)

# Delete from defenses table
delete_command = "DELETE FROM {}".format(DEFENSE_TABLE)
cur.execute(delete_command)


conn.commit()

# Add nyms to the table
with open("nyms.csv") as input_file:
    csv_reader = reader(input_file)
    print("Reading in Nyms to DB")
    for row in csv_reader:
        nym = row[0]
        rating_ids = list(map(int, row[1:]))
        domain = "spotify.com"
        insert_command = "INSERT INTO {} (id, top_ratings, top_domains) VALUES(%s, %s, %s)".format(NYM_TABLE)
        cur.execute(insert_command, (nym, rating_ids, [domain]))

    conn.commit()

# Add Ratings to the table
with open("ratings.csv") as input_file:
    print("Reading in ratings to db")
    csv_reader = reader(input_file)
    next(csv_reader)
    naive_datetime = "2018-05-14T12:07:48.203697"
    for rating_id, nym, domain, item, rating, num_votes in csv_reader:
        insert_command = "INSERT INTO {} (id, domain, item, score, num_votes, nym_id, inserted_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)".format(RATING_TABLE)
        cur.execute(insert_command, (rating_id, domain, item, rating, num_votes, nym, naive_datetime, naive_datetime))

    conn.commit()

print("Adding session cookie")
insert_command = "INSERT INTO {} (domain, cookies, nym_id) VALUES(%s, %s, %s)".format(COOKIES_TABLE)
cur.execute(insert_command, ("spotify.com", "{\"sp_dc\":\"AQAvhdBi6p2xKrvCUcGAASR_cDquQ2IqzijMrueVBNvP8yP1wDbMaff-a0h3o48YLCozO5n25WGWSCwKd2Ou7jJn\",\"sp_t\":\"cf95fb8c4c8316703bd6a30ea7e9de90\",\"sp_landing\":\"http%3A%2F%2Fopen.spotify.com%2Fbrowse%2Ffeatured\",\"wp_access_token\":\"BQB-ikwylMfP3yOOjVliVX_ZrWQsLlFpNp2RH4wpPboB8d_iPto0WXXh4Xn9PXSDeZAVjz6Xceqyo5rhxtibeup31VqvhwMAOOg-1sycP048lj_buv7OdXcLqmKu5C1YyLfRmmFS69xBkFHM5_tneE_UrSqCBkLc_Q2GJ72T6qx3eFAtoZ9T2kwQPM0cL9E3GVSpBxsttRTEUegtyDVFghaURUNVWSHpSEW10w1vk8iNTsucX2iOnwS6yFl0HLrxdw6r2TzKdXo3EN8LI1qp28pLN05l4G65AYM\",\"wp_expiration\":\"1525101617000\",\"wp_expires_in\":\"3600\",\"wp_sso_token\":\"AQBuLev5qhNaY--Rs844mHjo_kw7e1iQ1wwmUZJIg92DJBBdmx2WWNP3-ZcX_nJxKXsUkH4bfR789cDoHxJ1Fokd\"}", 1))
conn.commit()

with open("rules.csv") as input_file:
    print("Reading in rules to db")
    csv_reader = reader(input_file)
    next(csv_reader)
    naive_datetime = "2018-05-14T12:07:48.203697"
    for rules_id, domain, endpoint, rule in csv_reader:
        insert_command = "INSERT INTO {} (id, domain, endpoint, rule, inserted_at, updated_at) VALUES(%s, %s, %s, %s, %s, %s)".format(RULES_TABLE)
        cur.execute(insert_command, (rules_id, domain, endpoint, rule, naive_datetime, naive_datetime))

    conn.commit()

# Add Nym version into nym metadata table
insert_command = "INSERT INTO {} (clustering_version, support_list_version) VALUES (%s, %s)".format(METADATA_TABLE)
cur.execute(insert_command, (0.1, 0.25))
conn.commit()
