
import re
import time
import json
import random
from datetime import datetime

from wpp_boot import wpp_boot
from wpp_requests import wpp_requests
from spam_detector import spam_detector
from reminders import reminders
from info import info
from data import data
from msg_requests import msg_requests


while True:
    
    # TODO - In the reminders, instead of inserting the read reminders into the variable, delete them locally with a delete
    # - Administration module from which to delete members introduced as a parameter

    # - Improve the spam algorithm for repeated messages
    # - Modify the configuration so that all variables should be replaced (the ones in the header) to call data directly
    # - Introduce the `version` and `about` commands
    # - The data does not contain the path config variables
    # - Hard reset
    
    if data.get_modules_state()["boot"]: wpp_boot.periodical_reboot()

    if data.get_modules_state()["info"]: info.update_messages ()

    if data.get_modules_state()["info"]: info.count_total_messages ()

    # --------------------------

    if data.get_modules_state()["spam_detector"]: spam_detector.spam_filter ()

    if data.get_modules_state()["reminders"]:reminders.send_reminder_every_messages () 

    if data.get_modules_state()["msg_requests"]:msg_requests.request_responder ()


    # --------------------------
    
    wpp_boot.time_sleep()
 
    print ("----------"+str(datetime.now().time())+"---------")
