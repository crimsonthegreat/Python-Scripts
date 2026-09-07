Log Scheme
%Y%M%D_%h%m_%H.log


Color: Cisco Blue
Red: 0
Green: 188
Blue: 235


Keyword Highlighting:

Mac:

- Navigate to /Users/username/Library/Application Support/VanDyke/SecureCRT/Config/

- If this folder doesn't exist yet, you'll have to create it

- Copy "Cisco.ini" to folder

- Navigate to VanDyke --> Config --> Keywords


Windows:

- Hit Windows button and type "Run"

- Type "%appdata%"

- Navigate to VanDyke --> Config --> Keywords

- If this folder doesn't exist yet, you'll have to create it

- Copy "Cisco.ini" to folder


Logon Script to capture hostname:

SecureCRT_Auto_Save_Session_Hostname.py

""" 
Saves the session with the hostname for better documentation.
Current configuration will save with hostname [ip address].
Change INCLUDE_IP_IN_SESSION_NAME to False to only save the session name.
Script will run everytime a session is created and rename/ remove old sessions as the hostname is changed.
"""