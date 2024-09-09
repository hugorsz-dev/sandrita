from data import data
from wpp_requests import wpp_requests

msg_error_incomplete_request = data.get_configuration()["msg_requests"]["msg_error_incomplete_request"]
msg_error_bad_request = data.get_configuration()["msg_requests"]["msg_error_bad_request"]
msg_error_void_specification = data.get_configuration()["msg_requests"]["msg_error_void_specification"]

msg_error_module_not_found = data.get_configuration()["msg_requests"]["man"]["msg_error_module_not_found"]

def get_cmd ():
    return data.get_configuration()["msg_requests"]["man"]["cmd"]

def format_manual_for_whatsapp(manual):
    result = f"*{manual["name"]}*"
    result += "\n\n"
    result += f"_{manual["description"]}_"
    if "commands" in manual:
        result += "\n\n"
        result += "_____________________"
        result += "\n\n"
        for commands in manual["commands"]:
            result+=commands["cmd"]
            result += "\nv\n"
            result+=commands["cmd_description"]
            result += "\n\n"
            result += "_____________________"
            result += "\n\n"
            
            

    
    return result

def manage_input (request):
    
    message_id = request["id"]
    content_request = request ["content_request"]

    try:
        try:
            operation = request ["content_request"][0]
            operation = operation.replace ("-","_")
        except:
            wpp_requests.reply_message(message_id, msg_error_void_specification )
            return False
        
        manual = {}

            

        if operation in data.get_configuration():
            manual = data.get_configuration()[operation]["manual"]
        elif operation in data.get_configuration()["msg_requests"]: 
            manual = data.get_configuration()["msg_requests"][operation]["manual"]
        else: 
            wpp_requests.reply_message(message_id, msg_error_module_not_found  )
            return False
        
        wpp_requests.reply_message(message_id,format_manual_for_whatsapp(manual))



    except Exception as e: 
        print (e)
        wpp_requests.reply_message(message_id, msg_error_incomplete_request  )    