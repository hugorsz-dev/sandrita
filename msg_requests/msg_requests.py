

import json
import re

from data import data
from msg_requests.state import state
from msg_requests.manage_reminders import manage_reminders
from msg_requests.control_panel import control_panel
from msg_requests.man import man


path_to_admins = data.get_configuration()["msg_requests"]["path_to_admins"]
request_char=data.get_configuration()["msg_requests"]["request_char"]
content_request_char=data.get_configuration()["msg_requests"]["content_request_char"]
nicknames = data.get_configuration()["msg_requests"]["nicknames"]


"""
Returns a JSON file with the numbers that have sent requests to the bot.
    messages_response: the result of the get_messages() function
"""

def detect_requests ():
    messages_response = data.get_info_updated_messages()
    with open (path_to_admins, "r", encoding="utf-8") as file:
        admins = json.load(file)
    output = []
    if "response" in messages_response: 
        if "response" in messages_response:
            if messages_response["status"] =="success":
                for message in messages_response["response"]:
                    try:
                        if message["type"]=="chat":
                            if (
                                    any (nickname in message["content"].lower() for nickname in nicknames) 
                                    and re.search(rf'^[^{request_char}]*{request_char}[^{request_char}]+{request_char}[^{request_char}]*$', message["content"]) 
                                    and message["author"].split("@")[0] in admins
                                    and message["id"] not in data.get_msg_requests_requested_ids()
                                ):
                                    output.append({
                                            "admin_name":admins[message["author"].split("@")[0]],
                                            "phone":message["author"].split("@")[0],
                                            "id":message["id"],
                                            "content":message["content"],
                                            "request":re.findall(rf"{request_char}(.*?){request_char}", message["content"])[0].replace(" ",""),
                                            "content_request":re.findall(rf'{content_request_char}(.*?){content_request_char}',message["content"])
                                })
                    except Exception as e:
                        print ("Error collecting message:", e)
            return output
        else:
            print (messages_response)
            return False
    else:
        print ("Error: impossible to collect messages")
        return False

def request_responder ():
    requests_detected=detect_requests ()

    if requests_detected==False:
        return False
    
    for request in requests_detected:
        if data.get_modules_state()["control_panel"] and request["request"]==control_panel.get_cmd():
            control_panel.manage_input (request)
        if data.get_modules_state()["state"] and request["request"]==state.get_cmd():
            state.manage_input(request)
        if data.get_modules_state()["manage_reminders"] and request["request"]== manage_reminders.get_cmd():
            manage_reminders.manage_input(request)
        if data.get_modules_state()["man"] and request["request"]== man.get_cmd():
            man.manage_input(request)

        # ---------------------
        
        requested_ids  = data.get_msg_requests_requested_ids()
        requested_ids.append (request["id"])
        data.set_msg_requests_requested_ids (requested_ids)
           