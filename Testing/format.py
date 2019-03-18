import json
import csv
import datetime
import queue

# Reads in log files and splits them up a
# way which allows them to be matched with packets
def read_in_log(log_file):
    result = []
    with open(log_file, 'r') as data:
        # Read in and format the data so it can later some of it can
        # be converted to dictionary
        logs = data.read().replace('%{', '{').replace('=>', ':')
        # Get all put requests in file
        logs = logs.split(" [info] Sent 200 in ")
        result = [log.split('\n') for log in logs]
    # remove unnecessary details at start
    return result

# Get order of users interacting with server
def get_users_from_logs(logs):
    users = []
    ground_truth = []
    for log in logs:
        for info in log:
            if '  Parameters: ' in info:
                payload = json.loads(info.replace('  Parameters: ', ''))
                ratings = payload["rating"]
                users.append(ratings['user'])
            if ' [info] PUT /ratings/update' in info:
                start_timestamp,_ = info.split(' [info] PUT /ratings/update')
                end_timestamp = log[len(log) - 1]
                user = None
                for minfo in log:
                    if '  Parameters: ' in minfo:
                        payload = json.loads(minfo.replace('  Parameters: ', ''))
                        ratings = payload["rating"]
                        user = (ratings['user'])
                ground_truth.append((start_timestamp, end_timestamp, user))

    return users, ground_truth

def common_word(word_lists, sentence):
    for word in word_lists:
        if word in sentence:
            return word
    return None

# Removes packets that do not relate to the put request
def clean_csv(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header = True
        with open(output_file, 'w', newline='') as result_file:
            csv_result = csv.writer(result_file)
            prev_row = []
            # Keep track of which ports have opened communications
            active_ports = []
            receive_packet = queue.Queue()
            for row in csv_reader:
                if header:
                    #csv_result.writerow(row)
                    header = False
                if (row[5] == '74' or row[5] == '66') and '4400' == row[6][:4] and '[SYN, ACK]' in row[6] and row[2] == "172.31.30.80" :
                    host_port, user_port  = row[6].split("[SYN, ACK]")[0].split(" > ")
                    if '4400' in host_port:
                        active_ports.append(user_port)
                        start = row[0]
                        receive_packet.put((start, user_port))
                
                
                if (row[5]=='2934' or row[5] == '2946') and  (row[6]== '' or row[6] == 'Client > Server [UNIMPLEMENTED TYPE]') and  not receive_packet.empty():
                    start,_ = receive_packet.get()
                    end = row[0]
                    csv_result.writerow([start, end])
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
        datetime_obj = datetime.datetime.strptime(frame_time[: len(frame_time) - 7], "%b  %d, %Y %H:%M:%S.%f")
        time_frame_tuples.append((frame["frame.number"], datetime_obj))
    return time_frame_tuples


def get_time(tuples, packet_no):
    for tup in tuples:
        if tup[0] == packet_no:
            return tup[1]
    print(packet_no)
    return None

def convert_frames(frame_tuples, approved_frames):
    result = []
    for frame in approved_frames:
        start = get_time(frame_tuples, frame[0])
        end = get_time(frame_tuples, frame[1])
        result.append((start, end))
    return result


def filter_frames(frames, approved_frames):
    return list(filter(lambda x: x[0] in approved_frames, frames))

def generate_training_data(csv_file, log_file, packet_file, output_file):
    logs = read_in_log(log_file)
    users, ground_truth = get_users_from_logs(logs)
    with open('TrainingData/ground_truth.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        base_time = datetime.datetime.strptime(ground_truth[0][0], '%Y-%m-%d %H:%M:%S.%f')
        for truth in ground_truth:
            start_seconds = (datetime.datetime.strptime(truth[0], '%Y-%m-%d %H:%M:%S.%f') - base_time).total_seconds()/60
            end_seconds = (datetime.datetime.strptime(truth[1], '%Y-%m-%d %H:%M:%S.%f') - base_time ).total_seconds()/60
            writer.writerow([start_seconds, end_seconds, truth[2]])

    time_frame_tuples = read_in_times(packet_file)
    approved_frames = []
    base_time = time_frame_tuples[0][1]
    with open(csv_file, 'r') as cleaned_csv:
        reader = csv.reader(cleaned_csv, delimiter=',')
        header = True
        count = 0
        for row in reader:
            approved_frames.append(row)
            count += 1
    print(len(time_frame_tuples))
    time_frame_tuples = convert_frames(time_frame_tuples, approved_frames)
    print(len(users))
    print(len(time_frame_tuples))
    result = []
    with open(output_file, 'w', newline='') as train_csv:
        training_file = csv.writer(train_csv)
        for i in range(len(users)):
            start_seconds = (time_frame_tuples[i][0] - base_time).total_seconds()*10/60
            end_seconds = (time_frame_tuples[i][1] - base_time).total_seconds()*10/60
            training_file.writerow([start_seconds, end_seconds, users[i]])
            result.append([start_seconds, end_seconds, users[i]])
    return result

#clean_csv('Packets/CSVs/1-user.csv','Packets/CSVs/1-user-clean.csv')
#(generate_training_data('Packets/CSVs/1-user-clean.csv', 'Logs/1-user.log','Packets/Json/1-user.json', 'TrainingData/training-1-user.csv'))

#clean_csv('Packets/CSVs/2-users.csv','Packets/CSVs/2-users-clean.csv')
#(generate_training_data('Packets/CSVs/2-users-clean.csv', 'Logs/2-users.log','Packets/Jsons/2-users.json', 'TrainingData/training-2-users.csv'))

#clean_csv('Packets/CSVs/5-users.csv','Packets/CSVs/5-users-clean.csv')
#(generate_training_data('Packets/CSVs/5-users-clean.csv', 'Logs/5-users.log','Packets/Json/5-users.json', 'TrainingData/training-5-users.csv'))

#clean_csv('Packets/CSVs/5-users(1).csv','Packets/CSVs/5-users-clean(1).csv')
#(generate_training_data('Packets/CSVs/5-users-clean(1).csv', 'Logs/5-users(1).log','Packets/Json/5-users(1).json', 'TrainingData/training-5-users(1).csv'))

#clean_csv('Packets/CSVs/5-users(2).csv','Packets/CSVs/5-users-clean(2).csv')
#(generate_training_data('Packets/CSVs/5-users-clean(2).csv', 'Logs/5-users(2).log','Packets/Json/5-users(2).json', 'TrainingData/training-5-users(2).csv'))

#clean_csv('Packets/CSVs/5-users(3).csv','Packets/CSVs/5-users-clean(3).csv')
#(generate_training_data('Packets/CSVs/5-users-clean(3).csv', 'Logs/5-users(3).log','Packets/Jsons/5-users(3).json', 'TrainingData/training-5-users(3).csv'))

log_file='Logs/50-users(1).log'
logs = read_in_log(log_file)
users, ground_truth = get_users_from_logs(logs)
with open('TrainingData/ground_truth.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    base_time = datetime.datetime.strptime(ground_truth[0][0], '%Y-%m-%d %H:%M:%S.%f')
    for truth in ground_truth:
        start_seconds = (datetime.datetime.strptime(truth[0], '%Y-%m-%d %H:%M:%S.%f') - base_time).total_seconds()*10/60
        end_seconds = (datetime.datetime.strptime(truth[1], '%Y-%m-%d %H:%M:%S.%f') - base_time ).total_seconds()*10/60
        writer.writerow([start_seconds, end_seconds, truth[2]])



##
#clean_csv('Packets/CSVs/10-users.csv','Packets/CSVs/10-users-clean.csv')
#(generate_training_data('Packets/CSVs/10-users-clean.csv', 'Logs/10-users.log','Packets/Json/10-users.json', 'TrainingData/training-10-users.csv'))

#clean_csv('Packets/CSVs/50-users.csv','Packets/CSVs/50-users-clean.csv')
#(generate_training_data('Packets/CSVs/50-users-clean.csv', 'Logs/50-users.log','Packets/Json/50-users.json', 'TrainingData/training-50-users.csv'))