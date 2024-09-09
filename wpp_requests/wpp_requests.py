import requests

from data import data

host = data.get_configuration()["api"]["host"]
session = data.get_configuration()["api"]["session"]
headers = data.get_configuration()["api"]["headers"]
group_id = data.get_configuration()["group"]["id"]

"""
Checks the session: returns true if it's ready, false otherwise
"""
def session_is_started():
    url = host + session + "/status-session"
    try:
        response = requests.get(url, headers=headers)
        print(response.json()["status"])
        if response.json()["status"] == "CONNECTED":
            return True
        else:
            return False
    except:
        return False

"""
Enables or disables the ability for non-admin participants to send messages in the group
"""
def messages_admins_only(flag):
    url = host + session + "/messages-admins-only"
    payload = {
        "groupId": group_id,
        "value": flag
    }

    response = requests.post(url, json=payload, headers=headers)

"""
Returns the participants in the group
"""
def get_participants_in_group():
    url = host + session + "/group-members/" + group_id
    response = requests.get(url, headers=headers)
    return response.json()

"""
Checks if a participant is in the group
    .phone: participant's number
"""
def is_participant_in_group(phone):
    participants = get_participants_in_group()

    if "response" in participants:
        for register in participants["response"]:
            if register["id"]["user"] == phone:
                return True
    return False

"""
Removes a participant from the group
    .phone: participant's number
"""
def remove_participant(phone):
    url = host + session + "/remove-participant-group"
    payload = {
        "groupId": group_id,
        "phone": phone
    }

    response = requests.post(url, json=payload, headers=headers)

"""
Replies to a message in the group
    .message_to_reply: ID of the message to reply to
    .message: the reply message
"""
def reply_message(message_to_reply, message):
    url = host + session + "/send-reply"
    
    payload = {
        "phone": group_id,
        "isGroup": True,
        "message": message,
        "messageId": message_to_reply
    }

    response = requests.post(url, json=payload, headers=headers)

"""
Sends a message to the group
    .message: the message to send
"""
def send_message(message):
    url = host + session + "/send-message"
    
    payload = {
        "phone": group_id,
        "isGroup": True,
        "message": message
    }

    response = requests.post(url, json=payload, headers=headers)

"""
Provides a JSON with the group's messages.
    count: number of messages
"""
def get_messages(count):
    url = host + session + "/get-messages/" + group_id
    querystring = {"count": str(count)}    
    response = requests.get(url, headers=headers, params=querystring)
    
    return response.json()

"""
Returns the last message received in the response messages_response
    messages_response: result of the get_messages() function
"""
def get_last_message():
    messages_response = data.get_info_updated_messages()
    if "response" in messages_response:
        try:
            return {
                "content": messages_response["response"][-1]["content"],
                "id": messages_response["response"][-1]["id"]
            }
        except Exception as e:
            print(e)
            # If it's not a text message
            return {"content": "", "id": "NONE"}
