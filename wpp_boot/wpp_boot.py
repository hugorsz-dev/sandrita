import subprocess
import time

from wpp_requests import wpp_requests
from data import data

default_timer_reboot = data.get_configuration()["boot"]["timer_reboot"]
path_to_execute_previusly = data.get_configuration()["boot"]["path_to_execute_previusly"]
default_normal_time_sleep = data.get_configuration()["boot"]["time_sleep"]
default_big_spam_alert_time_sleep = data.get_configuration()["spam_detector"]["big_spam_alert_time_sleep"]

##############
# INITIALIZATION FUNCTIONS
##############

"""
Restarts all WPP Connect services
"""

def reboot_services():
    
    # Close WPP Connect
    print("Restarting WPPConnect Server - execute_previusly.sh")
    script_execution_result = subprocess.run(['bash', path_to_execute_previusly], capture_output=True, text=True)
    print("...end of the script. Waiting for API initialization.")

    # Wait until the connection starts
    while not wpp_requests.session_is_started():
        time.sleep(10)
    
    # Send a start message if necessary
    print("Sending start message via Whatsapp") 


"""
Evaluates whether WPP Connect needs to be restarted - and restarts it - within the loop
"""

def periodical_reboot():
    # Starting the service (this line will only execute once)
    if data.get_timer_reboot() == 0:
        reboot_services()
    
    # Increment counter each cycle
    data.set_timer_reboot(data.get_timer_reboot() + 1)

    # Upon reaching the limit, reset both the counter (to 1) and the cycle
    if data.get_timer_reboot() == default_timer_reboot:
        data.set_timer_reboot(1)

        # Record each reboot
        data.set_info_total_reboots(data.get_info_total_reboots() + 1)

        reboot_services()


def time_sleep():
    # Time intervals based on big_spam_alert
    if data.get_big_spam_alert():
        time.sleep(default_big_spam_alert_time_sleep)
    else:
        time.sleep(default_normal_time_sleep)
    
    # Record each cycle
    data.set_info_total_cycles(data.get_info_total_cycles() + 1)
