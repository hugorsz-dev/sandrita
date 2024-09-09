# Sandrita

## Introduction

Sandrita is a Whatsapp bot programmed in Python, notable for its easy extensibility.

All operations performed by Sandrita call the `wpp_requests` module - see the current repository - a set of functions designed to make requests to the [WPP Connect Server API](https://github.com/wppconnect-team/wppconnect-server). For using this tool, it is essential to install and configure this service or develop a custom module to replace the default request system.

## Functioning

The operation of Sandrita consists of an infinite loop interrupted by a variable number of seconds between each cycle. For each of these cycles, at minimum, one `get` request is made to the API using the *request* module, to receive a set of messages which are then manipulated by the functions designated to be executed.

1. Start of the loop: `get` request that stores the received messages in memory.
2. Manipulation of the received messages according to the functions defined in the loop.
3. End of the loop, wait time until it repeats.

## Modules

## data

The `data` module controls data input and output. The input is generally stored in a configuration file named `config.json`, and the output of each module is stored in its respective file, `variables.json`.

The `get` and `set` functions can be executed anywhere in the code where this module is imported.

The purpose of this system, in addition to intercommunication between modules, is to be fully configurable from the Whatsapp chat, a goal partially achieved in some cases but incomplete, due to the following pending issues referenced in the *TODO* section of `main.py`:

- All variables should be replaced (those in the header) to directly call the `data` module.
- Therefore, the variables from `config.json` should be reassigned at the function level.

### Pending Deficiencies to be Solved

- Variables related to file locations do not refer to the `path` in `config.json`, which is not an issue as long as the files do not change location.

## wpp_requests

Using the native `requests` module, the *WPP Connect* methods are adapted so they can be used by the different modules of Sandrita. The extension of this module depends on the need, and this project does not aim to extend it to the full extent of the functions offered by the API, as long as they are not used.

## boot

Cache is often a problem. *WPP Connect* uses a Chromium instance to operate, which tends to accumulate memory that is usually freed after each restart. Thus, `wpp_boot` keeps a counter that, after reaching a specified number of cycles in `config.json`, executes the `execute_previusly.sh` file, with instructions to stop and start services.

Before initializing the system, it checks that it is indeed connected.

It is not advisable to activate this function if there is sufficient RAM memory.

## info

Its primary goal is to collect messages by calling the `get_messages()` request. To save resources, this request is executed only once during a specified interval of messages, set in `config.json`, and is stored within the specific variables set for this module, `variables.json`.

Additionally, `info` collects statistics, such as the total number of messages or the total number of restarts.

## spam_detector

The spam detector is designed to receive a set of messages every few seconds specified in `config.json`, and to analyze if the output fits the detection algorithm, which **currently only detects Whatsapp spam and not other sources** and does not have **flood prevention**. This could be a good idea for future modules.

### Meaning of Variables

- `default_big_spam_alert`: Duration of the intensive spam prevention mode (essentially, how long the message blocking lasts).
- `default_timer_big_spam_alert`: Duration of time that the intensive spam prevention mode (big_spam) lasts, during which the group will be restricted from sending messages.
- `default_timer_reboot`: Cycles in which the service takes to restart (reloading time, depends on how much the group talks).
- `default_spam_message_limit_for_alarm`: Spam messages at which the system triggers the alert.
- `default_normal_time_sleep`: Cycle duration while everything is normal.
- `default_big_spam_alert_time_sleep`: Cycle duration while in big_spam mode.
- `default_while_normal_deleting_time_sleep`: Deletion cycle duration while everything is normal.
- `default_while_big_spam_deleting_time_sleep`: Deletion cycle duration while in big_spam mode.

## reminders

Reminder system, which sends a message with a random reminder every certain interval of messages specified in `config.json`.

## msg_requests

Interpreter and handler of commands entered by the user in the chat. Within this, all modules requiring direct interaction with users are stored; users who can access the requests must be registered in the `admins.json` file.

The `config.json` file allows editing special characters with which requests are called, aliases for commands associated with modules, and even responses to these.

### control_panel

The control panel manages configuration files via Whatsapp. This aims to provide full configuration of Sandrita from messages (or at least, this is the goal, see the `data` section).

It has the following functions:

- View the configuration (or module) file, formatted for Whatsapp.
- Filter configuration file, selecting a path separated by commas to view a specific part of it.
- Modify a specific part of a configuration file.
- Perform a soft system restart without stopping the code execution.

#### Pending Deficiencies to be Solved

- All issues listed in the `data` section.
- The `admins.json` file should be modifiable, but for now, changes must be made manually.

### state

Returns in Whatsapp format information extracted from the server, as well as some data collected from the info module:

- Total restarts.
- Total cycles.
- Total messages.
- RAM usage percentage.
- CPU usage percentage.
- The most demanding server services, followed by a color tag indicating their status.

### manage_reminders

Manages reminders, allowing for their inclusion and removal.

### man

In each module of `config.json`, there is a manual section where each command and functionality is described so that users who will use it can consult it.
