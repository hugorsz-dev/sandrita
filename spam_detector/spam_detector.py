import time

from data import data
from wpp_requests import wpp_requests

your_group_link = data.get_configuration()["group"]["link"]
default_spam_message_limit_for_alarm = data.get_configuration()["spam_detector"]["spam_message_limit_for_alarm"]
default_timer_big_spam_alert = data.get_configuration()["spam_detector"]["timer_big_spam_alert"]
default_big_spam_alert = data.get_configuration()["spam_detector"]["big_spam_alert"]
default_while_big_spam_deleting_time_sleep = data.get_configuration()["spam_detector"]["while_big_spam_deleting_time_sleep"]
default_while_normal_deleting_time_sleep = data.get_configuration()["spam_detector"]["while_normal_deleting_time_sleep"]

"""
Returns a JSON file with the phone numbers that have sent spam.
    messages_response: the result of the get_messages() function
"""
def detect_spam():
    messages_response = data.get_info_updated_messages()
    output = []
    if "response" in messages_response:
        if messages_response["status"] == "success":
            for message in messages_response["response"]:
                try:
                    if message["type"] == "chat":
                        if (
                            "chat.whatsapp.com" in message["content"]
                            and your_group_link not in message["content"]
                        ):
                            output.append({
                                "phone": message["author"].split("@")[0],
                                "id": message["id"]
                            })
                    if message["type"] == "image":
                        if (
                            "chat.whatsapp.com" in message["caption"]
                            and your_group_link not in message["caption"]
                        ):
                            output.append({
                                "author": message["sender"]["pushname"],
                                "phone": message["author"].split("@")[0],
                                "id": message["id"]
                            })
                except Exception as e:
                    # If it's not a text message
                    print("Error collecting message:", e)
            return output
        else:
            print(messages_response)
            return False
    else:
        print("Error: impossible to collect messages")
        return False

"""
This SPAM filter reacts to the messages flagged by the detect_spam function.
In theory, it works correctly, and the only things that may need adjustment 
are the variables controlling the timing between big_spam and normal spam alerts.
"""

def spam_filter():
    # Generate an enumerated list of phone numbers that have sent spam in the last 10 messages
    spam_detected = detect_spam()

    if spam_detected == False:
        return False
        
    # If the amount of spam exceeds 2 messages, and the spam timer exceeds its default...
    if len(spam_detected) >= default_spam_message_limit_for_alarm and data.get_timer_big_spam_alert() == default_timer_big_spam_alert: 
        data.set_big_spam_alert(default_big_spam_alert)
        data.set_timer_big_spam_alert(0)
        wpp_requests.messages_admins_only(True)
    
    # Removing participants
    for spam in spam_detected:
        # If the participant is not in the group, do not remove them
        if wpp_requests.is_participant_in_group(spam["phone"]):
            wpp_requests.remove_participant(spam["phone"])
            # print("Should remove " + spam["phone"])
        
        # Time intervals according to big_spam_alert
        if data.get_big_spam_alert() > 0: 
            time.sleep(default_while_big_spam_deleting_time_sleep)
        if data.get_big_spam_alert() == 0: 
            time.sleep(default_while_normal_deleting_time_sleep)
        
    if data.get_big_spam_alert() != 0: 
        data.set_big_spam_alert(data.get_big_spam_alert() - 1) 
    else:
        if data.get_timer_big_spam_alert() != default_timer_big_spam_alert:
            data.set_timer_big_spam_alert(data.get_timer_big_spam_alert() + 1)
    
    if data.get_big_spam_alert() == 1:
        wpp_requests.messages_admins_only(False)
