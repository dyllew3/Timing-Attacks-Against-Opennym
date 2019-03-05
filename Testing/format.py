import json
import csv
import datetime


# Reads in log files and splits them up a
# way which allows them to be matched with packets
def read_in_log(log_file):
    result = []
    with open(log_file, 'r') as data:
        # Read in and format the data so it can later some of it can
        # be converted to dictionary
        logs = data.read().replace('%{', '{').replace('=>', ':')
        # Get all put requests in file
        logs = logs.split("[info] PUT /ratings/update\n")
        result = [log.split('\n') for log in logs]
    # remove unnecessary details at start
    return result[1:]

# Get order of users interacting with server
def get_users_from_logs(logs):
    users = []
    for log in logs:
        payload = json.loads(log[1].replace('  Parameters: ', ''))
        ratings = payload["rating"]
        users.append(ratings['user'])
    return users

# Removes packets that do not relate to the put request
def clean_csv(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = True
        with open(output_file, 'w', newline='') as result_file:
            csv_result = csv.writer(result_file)
            prev_row = []
            for row in csv_reader:
                if header:
                    csv_result.writerow(row)
                    header = False
                if (row[6] == '' and row[5]=='2934' and prev_row[4] == "TCP"):
                    csv_result.writerow(row)
                prev_row = row
    return None

# Reads in times from the json file and returns an
# array of tuples with the frame number and the frame time
def read_in_times(packet_file):
    packet_data = json.load(open(packet_file, 'r'))
    time_frame_tuples = []
    for packet in packet_data:
        frame = packet["_source"]["layers"]["frame"]
        frame_time = frame["frame.time"].replace(' GMT Standard Time', '')
        datetime_obj = datetime.datetime.strptime(frame_time[: len(frame_time) - 3], "%b  %d, %Y %H:%M:%S.%f")
        time_frame_tuples.append((frame["frame.number"], datetime_obj))
    return time_frame_tuples


def filter_frames(frames, approved_frames):
    return list(filter(lambda x: x[0] in approved_frames, frames))

def generate_training_data(csv_file, log_file, packet_file, output_file):
    logs = read_in_log(log_file)
    users = get_users_from_logs(logs)
    time_frame_tuples = read_in_times(packet_file)
    approved_frames = []
    base_time = time_frame_tuples[0][1]
    with open(csv_file, 'r') as cleaned_csv:
        reader = csv.reader(cleaned_csv, delimiter=',')
        header = True
        count = 0
        for row in reader:
            if not header:
                approved_frames.append(row[0])
            else:
                header = False
            count += 1
    time_frame_tuples = filter_frames(time_frame_tuples, approved_frames)
    print(len(users))
    print(len(time_frame_tuples))
    result = []
    with open(output_file, 'w', newline='') as train_csv:
        training_file = csv.writer(train_csv)
        for i in range(len(users) - 1):
            seconds = (time_frame_tuples[i][1] - base_time).total_seconds()
            training_file.writerow([seconds, users[i]])
            result.append([seconds, users[i]])
    return result

#clean_csv('Packets/CSVs/1-user.csv','Packets/CSVs/1-user-clean.csv')
#(generate_training_data('Packets/CSVs/1-user-clean.csv', 'Logs/1-user.log','Packets/Json/1-user.json', 'TrainingData/training-1-user.csv'))
#
#clean_csv('Packets/CSVs/5-users.csv','Packets/CSVs/5-users-clean.csv')
#(generate_training_data('Packets/CSVs/5-users-clean.csv', 'Logs/5-users.log','Packets/Json/5-users.json', 'TrainingData/training-5-users.csv'))
#
#clean_csv('Packets/CSVs/10-users.csv','Packets/CSVs/10-users-clean.csv')
#(generate_training_data('Packets/CSVs/10-users-clean.csv', 'Logs/10-users.log','Packets/Json/10-users.json', 'TrainingData/training-10-users.csv'))

clean_csv('Packets/CSVs/50-users.csv','Packets/CSVs/50-users-clean.csv')
(generate_training_data('Packets/CSVs/50-users-clean.csv', 'Logs/50-users.log','Packets/Json/50-users.json', 'TrainingData/training-50-users.csv'))