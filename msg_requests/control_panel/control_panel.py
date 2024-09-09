
import traceback
import json

from data import data
from wpp_requests import wpp_requests

msg_error_incomplete_request = data.get_configuration()["msg_requests"]["msg_error_incomplete_request"]
msg_error_bad_request = data.get_configuration()["msg_requests"]["msg_error_bad_request"]
msg_error_void_specification = data.get_configuration()["msg_requests"]["msg_error_void_specification"]

sub_cmd_modify = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_modify"]
sub_cmd_view = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_view"]
sub_cmd_reboot = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_reboot"]
sub_cmd_filter = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_filter"]
sub_cmd_configuraton = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_configuration"]
sub_cmd_modules = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_modules"]
sub_cmd_api = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_api"]
sub_cmd_reboot =  data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_reboot"]
sub_cmd_soft_reboot = data.get_configuration()["msg_requests"]["control_panel"]["sub_cmd_soft_reboot"]

msg_error_file_not_found = data.get_configuration()["msg_requests"]["control_panel"]["msg_error_file_not_found"]
msg_sucesfully_modified =  data.get_configuration()["msg_requests"]["control_panel"]["msg_sucesfully_modified"]
msg_sucesfully_soft_reboot =  data.get_configuration()["msg_requests"]["control_panel"]["msg_sucesfully_soft_reboot"]
about_view = data.get_configuration()["msg_requests"]["control_panel"]["about_view"]



def get_cmd ():
    return data.get_configuration()["msg_requests"]["control_panel"]["cmd"]

def format_json_for_whatsapp(data, level=0):
    result = ""

    if not isinstance (data, dict):
        return str(data)

    for key, value in data.items():
        if isinstance(value, dict):
            level += 1
            result += ("\t" * (level - 1)) + f"`{key}`\n"
            result += format_json_for_whatsapp(value, level)
            level -= 1
        else:
            result += ("\t" * level) + f"`{key}` ```{value}```\n"
    
    return result

def find_json(json, path):
    if not path:
        return None

    if len(path) == 1:
        try: 
            return json[path[0]]
        except:
            return False

    return find_json(json[path[0]], path[1:])

def modify_json(json, path, variable):
    output = {}

    for i in range(1,len(path)):
        output = find_json (json,path[:-i])
        output [path[-i]] = variable
        variable = output
    output = json 
    output [path[0]] = variable
    variable = output

    return output

def view_configuration (message_id):
    output = about_view+f" ```{sub_cmd_configuraton}```:\n"
    
    config = format_json_for_whatsapp(data.get_configuration())
    config = config.replace(data.get_configuration()["api"]["host"], "*******")
    config = config.replace(data.get_configuration()["api"]["headers"]["Authorization"], "*******")

    wpp_requests.reply_message (message_id, output+config)

def view_modules (message_id):
    output = about_view+f" ```{sub_cmd_modules}```:\n"

    for name,active in data.get_modules_state().items():

        emoji ="🔴"
        if active: emoji = "🟢"

        alias=""
        resume=""

        if name in data.get_configuration()["msg_requests"]:
            alias= "(```"+data.get_configuration()["msg_requests"][name]["cmd"]+"```)"
            if "name" in data.get_configuration()["msg_requests"][name]["manual"]:
                resume = "_"+data.get_configuration()["msg_requests"][name]["manual"]["name"]+"_"
        else:
            if "name" in data.get_configuration()[name]["manual"]:
                resume ="_"+data.get_configuration()[name]["manual"]["name"]+"_"
                
        output= output + f"\t{emoji}\t`{name}` {alias} {resume}\n"

    wpp_requests.reply_message (message_id, output)

def manage_input (request):
    
    message_id = request["id"]
    content_request = request ["content_request"]

    try:
        try:
            operation = request ["content_request"][0]
            direction = request ["content_request"][1]
        except:
            wpp_requests.reply_message(message_id, msg_error_void_specification )
            return False

        if operation == sub_cmd_view: 
            if direction == sub_cmd_modules:
                view_modules(message_id)
                return True
            if direction == sub_cmd_configuraton:
                view_configuration (message_id)
                return True
            wpp_requests.reply_message(message_id, msg_error_file_not_found)

        if operation == sub_cmd_filter:
            try:
                path = request ["content_request"][2].replace(" ", "").split(",")
            except:
                wpp_requests.reply_message(message_id, msg_error_void_specification )
                return False
           
            if direction == sub_cmd_configuraton:
                if data.get_configuration()["msg_requests"]["content_request_char"] =="_":
                    path = [field.replace("-","_") for field in path]
                
                if find_json(data.get_configuration(), path):
                    wpp_requests.reply_message(message_id,  about_view+f" ```{sub_cmd_configuraton} > {path}```:\n"+format_json_for_whatsapp(find_json(data.get_configuration(), path)))
                else:
                    wpp_requests.reply_message(message_id, msg_error_file_not_found)

                return True
        
        if operation == sub_cmd_modify: 
            try:
                path = request ["content_request"][2].replace(" ", "").split(",")
                variable =  request ["content_request"][3].replace(" ", "")

                if "," in variable: variable = variable.split(",")
                elif "{" in variable: variable = json.loads(variable)
                elif variable.lower() == "false": variable = False
                elif variable.lower()  == "true": variable = True
            except Exception as e:
                print("Error:", e)  
 
            if direction == sub_cmd_configuraton:
                if data.get_configuration()["msg_requests"]["content_request_char"] =="_":
                    path = [field.replace("-","_") for field in path]
                data.set_configuration(modify_json(data.get_configuration(), path, variable))
                wpp_requests.reply_message(message_id, msg_sucesfully_modified)
                return True

        if operation == sub_cmd_reboot:
            if direction == sub_cmd_soft_reboot:
                data.set_timer_reboot (data.get_configuration () ["boot"]["timer_reboot"]-1)
                wpp_requests.reply_message(message_id, msg_sucesfully_soft_reboot )
                return True
            wpp_requests.reply_message(message_id, msg_error_file_not_found)
  

        wpp_requests.reply_message(message_id, msg_error_bad_request)
        return False
    except Exception as e:
        print("Error:", e) 


