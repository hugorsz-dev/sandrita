import json
from data import data
from wpp_requests import wpp_requests

path_to_reminders =  data.get_configuration()["reminders"]["path_to_reminders"]

msg_error_incomplete_request = data.get_configuration()["msg_requests"]["msg_error_incomplete_request"]
msg_error_bad_request = data.get_configuration()["msg_requests"]["msg_error_bad_request"]
msg_error_void_specification = data.get_configuration()["msg_requests"]["msg_error_void_specification"]

sub_cmd_new_reminder = data.get_configuration()["msg_requests"]["manage_reminders"]["sub_cmd_new_reminder"]
sub_cmd_delete_reminder = data.get_configuration()["msg_requests"]["manage_reminders"]["sub_cmd_delete_reminder"]
msg_error_repeated_reminder = data.get_configuration()["msg_requests"]["manage_reminders"]["msg_error_repeated_reminder"]
msg_error_reminder_not_found = data.get_configuration()["msg_requests"]["manage_reminders"]["msg_error_reminder_not_found"]
msg_sucesfully_inserted = data.get_configuration()["msg_requests"]["manage_reminders"]["msg_sucesfully_inserted"]
msg_sucesfully_deleted = data.get_configuration()["msg_requests"]["manage_reminders"]["msg_sucesfully_deleted"]

def get_cmd ():
    return data.get_configuration()["msg_requests"]["manage_reminders"]["cmd"]

def new_reminder (reminder, message_id):
    
    with open (path_to_reminders, "r", encoding="utf-8") as file:
        reminders = json.load(file)

    if reminder in reminders["messages"] and reminder.replace(" ","")!="":
        wpp_requests.reply_message(message_id, msg_error_repeated_reminder)
        return False
    else:
        reminders["messages"].append(reminder)

        with open (path_to_reminders, "w", encoding="utf-8") as file:
            json.dump (reminders, file, indent=4, ensure_ascii=False)

        wpp_requests.reply_message(message_id, msg_sucesfully_inserted)

        return True

def delete_reminder (reminder, message_id):
    with open (path_to_reminders, "r", encoding="utf-8") as file:
        reminders = json.load(file)
    if reminder in reminders["messages"] and reminder.replace(" ","")!="":
        reminders["messages"] = [message for message in reminders["messages"]  if reminder not in message]
        with open (path_to_reminders, "w", encoding="utf-8") as file:
            json.dump (reminders, file, indent=4, ensure_ascii=False)

        wpp_requests.reply_message(message_id, msg_sucesfully_deleted)

        return True
    else:
        wpp_requests.reply_message(message_id, msg_error_reminder_not_found )
        return False

def manage_input (request):

    message_id = request["id"]
    content_request = request ["content_request"]

    try:
        try:
            operation = request ["content_request"][0]
            reminder = request ["content_request"][1]
        except:
            wpp_requests.reply_message(message_id, msg_error_void_specification)
            return False

        if operation == sub_cmd_new_reminder: 
            new_reminder(reminder, message_id)
            return True
        if operation == sub_cmd_delete_reminder: 
            delete_reminder(reminder, message_id)
            return True
        wpp_requests.reply_message(message_id, msg_error_bad_request )
        return False
    except Exception as e: 
        print (e)
        wpp_requests.reply_message(message_id, msg_error_incomplete_request  )    
    


