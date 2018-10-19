import sys
import os

if __name__ != '__main__':
    exit(1)  # Ought not be run as imported module

if '-h' in sys.argv or '--help' in sys.argv or 'help' in sys.argv:
    print(f"[Usage]    {sys.argv[0]} path_to_previous_day_log_file path_to_cache_directory")
    exit()  # User wanted help, thus didn't pass in valid params.

if (len(sys.argv) != 3) and (not (os.path.isfile(sys.argv[1]) and os.path.isdir(sys.argv[2]))):
    print("Exactly 2 parameters are required, use flag `-h` for specific info.")
    exit(1)

# 0:00 - 0:30 - index `0`; 0:30 - 1:00 - index `1` and so on
usage_by_time = [0 for _ in range(48)]

with open(sys.argv[1], mode='r') as provoz_log:
    # provoz.log format: (All on one line)
    # client_ip client_port local_ip local_port
    # user_name different_user_name [time]
    # "request_method request_url HTTP/protocol_version"
    # http_status size_of_reply referer_from_http_header
    for line in provoz_log:
        user_name: str = '_or_'.join(line.split(sep='[')[0].split(sep=' ')[4:])
        request_data: str = line.split(sep='"')[1]
        day, hour, minute, second = line.split(sep="[")[1].split(sep=']')[0].split(sep=' ')[0].split(sep=':')
        size_of_reply: int = int(line.split(sep='"')[2].split(' ')[1])
        time_index: int = (2 * int(hour)) + (1 if int(minute) >= 30 else 0)
        usage_by_time[time_index] += size_of_reply
work_dir: str = sys.argv[2]
with open(work_dir + ('/' if not work_dir.endswith('/') else '') + 'daily_usage_log.json', mode='w') as daily_log:
    daily_log.write('{')
    daily_log.write(f'"half_hourly_usage" : {usage_by_time}')
    daily_log.write('}')