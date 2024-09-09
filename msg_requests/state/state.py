import subprocess

from wpp_requests import wpp_requests
from data import data

# Dependencias de bash 
# - mpstat
# - free
# - top

def get_cmd ():
    return data.get_configuration()["msg_requests"]["state"]["cmd"]

def get_ram_usage (): 
    result = subprocess.run(["free", "-h"], capture_output=True, text=True)
    return result.stdout.split()[12]+"/"+result.stdout.split()[7]

def get_cpu_usage ():
     result = subprocess.run(["mpstat"], capture_output=True, text=True)
     return result.stdout.split()[21]

def get_services (number):
    #     PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    output = {} 
    result = subprocess.run(f"top -b -n 1 | head -n 500 | head -n {7+number} | sed '1,7d'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in result.stdout.split("\n"):
        try:
            formated_line = line.split()
            pid = formated_line[0]
            cpu = formated_line[8]
            mem = formated_line[9]
            service_name= formated_line[11]

            floated_cpu = float (cpu.replace(",","."))
            floated_mem = float (mem.replace(",","."))

            emoji_cpu =""
            emoji_mem =""

            if floated_cpu <25: emoji_cpu = "🟢"
            elif floated_cpu >=25 and floated_cpu <65: emoji_cpu = "🟡"
            else: emoji_cpu = "🔴"

            if floated_mem <25: emoji_mem = "🟢"
            elif floated_mem >=25 and floated_mem <65: emoji_mem = "🟡"
            else: emoji_mem = "🔴"
            
            output[pid] = {"name":service_name, "cpu":cpu, "mem":mem, "emoji_mem":emoji_mem, "emoji_cpu":emoji_cpu}
                
        except Exception as e:
            print ("[state.py] Warning: not taking the trace of service", e)
            #print (result.stdout)
    return output

def manage_input (request): 
    message_id = request ['id']
    total_messages = data.get_info_total_messages()
    total_cycles = data.get_info_total_cycles()
    total_reboots = data.get_info_total_reboots ()
    about_total_cycles = data.get_configuration()["msg_requests"]["state"]["about_total_cycles"]
    about_total_reboots = data.get_configuration()["msg_requests"]["state"]["about_total_reboots"]
    about_total_messages =  data.get_configuration()["msg_requests"]["state"]["about_total_messages"] 
    about_ram_usage = data.get_configuration()["msg_requests"]["state"]["about_ram_usage"]
    about_cpu_usage = data.get_configuration()["msg_requests"]["state"]["about_cpu_usage"]
    about_services = data.get_configuration()["msg_requests"]["state"]["about_services"]
    aditional_msg = data.get_configuration()["msg_requests"]["state"]["aditional_msg"]
    number_of_services_to_show = data.get_configuration()["msg_requests"]["state"]["number_of_services_to_show"] 

    state = f"""{aditional_msg}
    \t*{about_total_reboots}* ```{total_reboots}```
    \t*{about_total_cycles}* ```{total_cycles}```
    \t*{about_total_messages}* ```{total_messages}```
    \t*{about_ram_usage}*  ```{get_ram_usage ()}```
    \t*{about_cpu_usage}*  ```{get_cpu_usage ()} %```
    \t*{about_services}*"""
    
    services =get_services(number_of_services_to_show)
    for pid in services :
        state = state+f""" 
        \t`{services[pid]["name"]} ({pid})`: 
        \t\t\t{services[pid]["emoji_mem"]} _RAM_: ```{services[pid]["mem"]}``` % 
        \t\t\t{services[pid]["emoji_cpu"]} _CPU_: ```{services[pid]["cpu"]}``` %"""
    
    wpp_requests.reply_message(message_id, state)