import json
import random

from data import data
from wpp_requests import wpp_requests

path_to_reminders = data.get_configuration()["reminders"]["path_to_reminders"]
message_interval = data.get_configuration()["reminders"]["message_interval"]

"""
Fetches the "reminders.json" file
"""

def get_random_reminder():
    with open(path_to_reminders, "r", encoding="utf-8") as file:
        reminders = json.load(file)
    random_number = random.randint(0, len(reminders["messages"]) - 1)
    return reminders["messages"][random_number]

"""
Inserts a new entry into the reminders.json file
    reminder: message string to be inserted
"""

def new_reminder(reminder):
    with open(path_to_reminders, "r", encoding="utf-8") as file:
        reminders = json.load(file)
    
    if reminder in reminders["messages"] and reminder.replace(" ", "") != "":
        return False
    else:
        reminders["messages"].append(reminder)

        with open(path_to_reminders, "w", encoding="utf-8") as file:
            json.dump(reminders, file, indent=4, ensure_ascii=False)
        return True

def send_reminder_every_messages():

    # Algorithm operation:
    # reminders_sended divides the total messages by the interval, resulting in the point 
    # where the reminder message is located with respect to the total messages.
    # For example: 
    # If the message is number 28 and the interval is 30, reminders_sended will be 0.
    # If the message is number 31 and the interval is 30, reminders_sended will be 1.
    # If the message is number 63 and the interval is 30, reminders_sended will be 2.
    # If the message is number 91 and the interval is 30, reminders_sended will be 3.
    # And so on...
    # This ensures that the reminder message is sent once and only once when this condition is met.
    
    # Regarding data.get_info_total_messages() % message_interval <= 1:
    # If the remainder is between 0 and 10, this is the margin so that, if the indicated buffer (30) is exceeded 
    # in the counter (31, 32, 33, 34... 39), the reminder keeps being sent.
    
    reminders_sended = data.get_info_total_messages() // message_interval

    if data.get_info_total_messages() % message_interval <= 10 and reminders_sended == data.get_reminders_sended() + 1:
        data.set_reminders_sended(reminders_sended)
        wpp_requests.send_message(get_random_reminder())
