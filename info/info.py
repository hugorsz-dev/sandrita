from data import data
from wpp_requests import wpp_requests

update_messages_per_cycle = data.get_configuration()["info"]["update_messages_per_cycle"]

"""
Updates the messages. Checks if the reboot counter has reached 1 to determine whether it needs 
to update 50 messages - due to the fact that reboots take several minutes to get the tool running.
"""

def update_messages ():

    if (data.get_timer_reboot() == 1):
        data.set_info_updated_messages(wpp_requests.get_messages(50))
    else:
        return data.set_info_updated_messages(wpp_requests.get_messages(10))
        

"""
Compares one array with another and returns the number of matches (len(array) - n), which is the number of 
"new inclusions."
    message_comparison: original array
    new_message_comparison: array to compare
"""
def get_number_of_new_messages(message_comparison, new_message_comparison):
    output = [message for message in message_comparison if message in new_message_comparison]
    return len(new_message_comparison) - len(output)

"""
Converts messages into message IDs.
    messages_response: a WPP API message format into an array of IDs compatible with the previous method
"""
def messages_to_array_ids(messages_response):
    output = []
    if "status" in messages_response:
        if messages_response["status"] == "success":
            for message in messages_response["response"]:
                output.append(message["id"])
    return output

def count_total_messages ():

    # Fetch the last n received messages
    messages_response = data.get_info_updated_messages()

    if (
        # If the buffer is empty, it fills with the last n messages
        messages_to_array_ids(messages_response)[:10] != data.get_info_last_message_ids()[:10]
    ):
        # Calculate the number of new messages
        number_of_new_messages = get_number_of_new_messages(
            data.get_info_last_message_ids()[:update_messages_per_cycle],
            messages_to_array_ids(messages_response)[:update_messages_per_cycle]
        )

        # Update the corresponding variables
        data.set_info_total_messages(data.get_info_total_messages() + number_of_new_messages) 
        data.set_info_last_message_ids(messages_to_array_ids(messages_response)[:update_messages_per_cycle])
