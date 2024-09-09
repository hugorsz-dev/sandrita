import json

def get_configuration ():
    with open('config.json', 'r') as file:
        return json.load(file)

def set_configuration (value):
    with open('config.json', 'w') as file:
        json.dump(value, file, indent=4, ensure_ascii=False)


"""
spam_detector
"""

def get_timer_big_spam_alert(): 
    with open('spam_detector/variables.json', 'r') as file:
        variables = json.load(file)
    return variables["timer_big_spam_alert"]

def set_timer_big_spam_alert (value):
    with open('spam_detector/variables.json', 'r') as file:
        variables = json.load(file)

    variables ["timer_big_spam_alert"] = value

    with open('spam_detector/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)

def get_big_spam_alert(): 
    with open('spam_detector/variables.json', 'r') as file:
        variables = json.load(file)
    return variables["big_spam_alert"]

def set_big_spam_alert (value):
    with open('spam_detector/variables.json', 'r') as file:
        variables = json.load(file)

    variables["big_spam_alert"] = value

    with open('spam_detector/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)

"""
wpp_boot
"""

def get_timer_reboot(): 
    with open('wpp_boot/variables.json', 'r') as file:
        variables = json.load(file)
    return variables["timer_reboot"]

def set_timer_reboot (value):
    with open('wpp_boot/variables.json', 'r') as file:
        variables = json.load(file)

    variables["timer_reboot"] = value

    with open('wpp_boot/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)


"""
info
"""
def get_info_updated_messages ():
    with open("info/variables.json", "r") as file:
        variables = json.load(file)
    return variables["updated_messages"]

def set_info_updated_messages (value):
    with open("info/variables.json", "r") as file:
        variables = json.load(file)
    
    variables["updated_messages"] = value

    with open('info/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)

def get_info_last_message_ids (): 
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["last_message_ids"]

def set_info_last_message_ids (value):
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)

    variables ["last_message_ids"] = value

    with open('info/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)

def get_info_total_messages (): 
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["total_messages"]

def set_info_total_messages (value):
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)

    variables ["total_messages"] = value

    with open('info/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)   

def set_info_total_cycles (value):
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)

    variables ["total_cycles"] = value

    with open('info/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)   

def get_info_total_cycles (): 
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["total_cycles"]

def set_info_total_reboots(value):
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)

    variables ["total_reboots"] = value

    with open('info/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False)   

def get_info_total_reboots (): 
    with open ("info/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["total_reboots"]

"""
reminders
"""

def get_reminders_sended ():
    with open ("reminders/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["sended"]

def set_reminders_sended (value):
    with open ("reminders/variables.json", "r") as file:
        variables = json.load (file)

    variables ["sended"] = value

    with open('reminders/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False) 

"""
msg_requests
"""

def get_msg_requests_requested_ids ():
    with open ("msg_requests/variables.json", "r") as file:
        variables = json.load (file)
    return variables ["requested_ids"]

def set_msg_requests_requested_ids (value): 
    with open ("msg_requests/variables.json", "r") as file:
        variables = json.load (file)

    variables ["requested_ids"] = value

    with open('msg_requests/variables.json', 'w') as file:
        json.dump(variables, file, indent=4, ensure_ascii=False) 

"""
control_panel
"""

def get_modules_state ():

    modules = {}

    for name, configuration in get_configuration().items():
        if "active" in configuration:
            if configuration["active"]:
                modules [name]= True
            else: modules[name] = False

    for name, configuration in get_configuration()["msg_requests"].items():
        if isinstance (configuration, dict):
            if "active" in configuration:
                if configuration["active"]:
                    modules [name]= True
                else: modules[name] = False
    return modules