import datetime
import os
import redis
from stripe import *
from dotenv import load_dotenv


load_dotenv()

# Connect to Redis
r = redis.Redis(
    host='redis-11936.c1.us-east1-2.gce.cloud.redislabs.com',
    port=11936,
    password='MDBI6iRZeKrpTdRrhYqVaCJyY3l19FN4')


def update_prompts(key, value):
    print(f"Updating prompts with key: {key} and value: {value}")
    r.hset('prompt-data', key, value)

    # Check if the item was saved successfully
    value = r.hget('prompt-data', key)
    if value is not None:
        print(
            f"Successfully retrieved {key} with value {value.decode('utf-8')} from the database.")
    else:
        print(f"Failed to retrieve {key} from the database.")


def read_prompts(key):
    value = r.hget('prompt-data', key)
    if value is not None:
        return value.decode('utf-8')
    else:
        return None


def check_user(phone_num):
    user_info = r.hgetall(f'user:{phone_num}')
    if user_info:
        # Convert dictionary keys and values from bytes to string
        user_info = {k.decode('utf-8'): v.decode('utf-8')
                     for k, v in user_info.items()}
        return (phone_num, user_info.get('name', 'Unknown'), user_info.get('last_request', 'Unknown'))
    else:
        print("User not found")
        return None


def create_user(phone_num, name):
    '''Creates a user given a phone number and name
    initalizes last request to an empty string
    '''
    r.hset(f'user:{phone_num}', 'name', name)
    r.hset(f'user:{phone_num}', 'last_request', '')


def create_link_item(phone_num, user_message):
    '''Creates a new entry in the link-data table
    updates the user-info data for the last_request time
    '''
    timestamp = datetime.datetime.now().isoformat(' ', 'seconds')
    r.hset(f'link:{phone_num}:{timestamp}', 'link', user_message)
    r.hset(f'user:{phone_num}', 'last_request', timestamp)


def update_user_timestamp(phone_num):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    r.hset(f'user:{phone_num}', 'last_request', current_time)


def check_timestamp(phone_num):
    timestamp_str = r.hget(f'user:{phone_num}', 'last_request')
    if timestamp_str is None:
        return

    timestamp = datetime.datetime.strptime(
        timestamp_str.decode('utf-8'), "%Y-%m-%d %H:%M:%S")
    current_time = datetime.datetime.now()
    time_diff = current_time - timestamp
    print(time_diff.total_seconds())
    if time_diff.total_seconds() < 15:
        raise Exception("User cooldown activated")


def check_request_count(phone_num):
    # In Redis, you would need to keep a separate counter for each user's requests
    request_count = r.get(f'request_count:{phone_num}')
    if request_count is not None and int(request_count) > get_user_limit(phone_num):
        raise Exception("User request limit reached")
    return int(request_count) if request_count is not None else 0
