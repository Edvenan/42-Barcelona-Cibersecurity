# Importing Libraries
import winreg
import wmi
import datetime
import os
import sys
import win32com.client
import psutil
from loading import ft_progress
import win32evtlog
import win32evtlogutil
import win32con
import winerror
from tree import *
from io import StringIO

####################################################
# REGISTRY CHANGES
####################################################
def get_registry_changes(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    registry_branch = winreg.HKEY_CURRENT_USER
    registry_key = r"Software"

    key = winreg.OpenKey(registry_branch, registry_key, 0, winreg.KEY_READ)
    header = []
    changes = []
    
    header.append("##########################################################")
    header.append("# REGISTRY CHANGES                                                                #")
    header.append("##########################################################")
    
    clean()
    print("Getting registry changes...")
    for i in ft_progress(range(winreg.QueryInfoKey(key)[0])):
        subkey_name = winreg.EnumKey(key, i)
        subkey_path = registry_key + "\\" + subkey_name

        subkey = winreg.OpenKey(registry_branch, subkey_path, 0, winreg.KEY_READ)
        timestamp = winreg.QueryInfoKey(subkey)[2]
        
        # Convert Windows filetime to Unix timestamp
        timestamp = (timestamp - 116444736000000000) / 10000000
                
        last_modified = datetime.datetime.fromtimestamp(timestamp)

        if start_date <= last_modified <= end_date:
            changes.append(f"{last_modified} - Change detected in subkey: {subkey_path}")

        winreg.CloseKey(subkey)

    winreg.CloseKey(key)
    print("Process completed.")
    result = header + sorted(changes, reverse = True)
    return result

####################################################
# RECENT FILES
####################################################
def get_recent_files(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    files = []
    header = []

    header.append("##########################################################")
    header.append("# RECENT FILES                                                                          #")
    header.append("##########################################################")
        
    shell = win32com.client.Dispatch("WScript.Shell")
    recent_files_directory = shell.SpecialFolders("Recent")  # Path to the Recent folder

    clean()
    print("Getting recent files...")
    for (dir_path, dir_names, recent_files) in os.walk(recent_files_directory):
        for file in ft_progress(recent_files):
            full_path = dir_path +"\\"+ file
            if file[-3:] == "lnk":
    
                creation_time = os.path.getctime(full_path)
                creation_time = creation_time = datetime.datetime.fromtimestamp(creation_time)
                modified_time = os.path.getmtime(full_path)
                modified_time = datetime.datetime.fromtimestamp(modified_time)

                # Check if the file's last modified date falls within the specified time interval
                if start_date <= modified_time <= end_date:
        
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(full_path)
                    file_path = shortcut.Targetpath

                    if os.path.isfile(file_path):
                        files.append(modified_time.strftime("%Y-%m-%d %H:%M:%S") + " - " + file_path)
 
    print("Process completed.")   
    result = header + sorted(files, reverse = True)
    return result

####################################################
# INSTALLED PROGRAMS
####################################################
def get_installed_programs(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")

    programs = []
    header = []

    header.append("##########################################################")
    header.append("# INSTALLED PROGRAMS                                                           #")
    header.append("##########################################################")

    wmi = win32com.client.GetObject("winmgmts:")
    query = f"SELECT * FROM Win32_Product WHERE InstallDate >= '{start_date_str}' AND InstallDate <= '{end_date_str}'"

    clean()
    print("Getting installed programs...")

    software_items = wmi.ExecQuery(query)

    for software in ft_progress(software_items):
        install_date = software.InstallDate
        install_date = datetime.datetime.strptime(install_date, "%Y%m%d")
        programs.append(f"{install_date.strftime('%Y-%m-%d')} - {software.Name} - {software.Version} - {software.Vendor} - {software.URLInfoAbout}")

    print("Process completed.")
    result = header + sorted(programs, reverse = True)
    return result

####################################################
# OPEN PROGRAMS
####################################################
def get_open_programs(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    programs = []
    header = []

    header.append("##########################################################")
    header.append("# OPEN PROGRAMS                                                                   #")
    header.append("##########################################################")

    clean()
    print("Getting open programs...")

    for proc in psutil.process_iter(['name', 'create_time']):
        proc_name = proc.info['name']
        create_time = datetime.datetime.fromtimestamp(proc.info['create_time'])

        if start_date <= create_time <= end_date:
            programs.append(create_time.strftime("%Y-%m-%d, %H:%M:%S") + " - " + proc_name)
    
    print("Process completed.")
    result = header + sorted(programs, reverse = True)
    return result

####################################################
# BROWSING HISTORY
####################################################
def get_browsing_history(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    from browser_history import get_history
    
    clean()
    outputs = get_history()

    # his is a list of (datetime.datetime, url) tuples
    his = outputs.histories

    browsing_history = []
    header = []

    header.append("##########################################################")
    header.append("# BROWSING HISTORY                                                                #")
    header.append("##########################################################")

    for item in ft_progress(his):
        browsing_time = item[0].replace(tzinfo=None)
        
        if start_date <= browsing_time <= end_date:    
            browsing_history.append(f"{item[0].strftime('%Y-%m-%d %H:%M:%S')} - {item[1]}")

    print("Process completed.")
    result = header + sorted(browsing_history, reverse = True)
    return result

####################################################
# CONNECTED DEVICES
####################################################
def get_connected_devices(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    
    devices = []
    header = []

    header.append("##########################################################")
    header.append("# CONNECTED DEVICES                                                             #")
    header.append("##########################################################")
    
    wmi_connection = wmi.WMI()
    #query = f"SELECT * FROM Win32_PnPEntity WHERE ConfigManagerErrorCode = 0 AND InstallDate >= {start_date_str} AND InstallDate <= {end_date_str}"
    query = f"SELECT * FROM Win32_PnPEntity WHERE ConfigManagerErrorCode = 0 AND Present = True AND Status = 'OK'"

    clean()
    print("Getting connected devices...")
    conn_devices = wmi_connection.query(query)

    for device in ft_progress(conn_devices):
        device_name = device.Name
        device_manufacturer = device.Manufacturer
        device_type = device.PNPClass
        
        device_installDate = ""
        
        if (device.InstallDate):
            # Convert Windows filetime to Unix timestamp
            device_installDate = (device_installDate - 116444736000000000) / 10000000    
            device_installDate = datetime.datetime.fromtimestamp(device_installDate)
            install_date = datetime.datetime.strptime(device_installDate, "%Y%m%d%H%M%S")
            device_installDate = install_date
        else:
            device_installDate = datetime.datetime.now().strftime("%Y-%m-%d")
        devices.append(f"{device_installDate} - {device_type} - {device_name} - {device_manufacturer}")

    print("Process completed.")
    result = header + sorted(devices, reverse = True)
    return result

####################################################
# LOG EVENTS
####################################################
def get_log_events(start_date, end_date):
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    #This dict converts the event type into a human readable form

    event_dict={win32con.EVENTLOG_AUDIT_FAILURE:'AUDIT_FAILURE',\
		  win32con.EVENTLOG_AUDIT_SUCCESS:      'AUDIT_SUCCESS',\
		  win32con.EVENTLOG_INFORMATION_TYPE:   'INFORMATION',\
		  win32con.EVENTLOG_WARNING_TYPE:       'WARNING',\
		  win32con.EVENTLOG_ERROR_TYPE:         'ERROR'}

    events = []
    header = []

    header.append("##########################################################")
    header.append("# LOG EVENTS                                                                            #")
    header.append("##########################################################")
    
    handle = win32evtlog.OpenEventLog(None, 'System')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    
    clean()
    print("Accesssing Event Logs...(This step may take about a minute)")
    
    while True:
        events_batch = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events_batch:
            break

        for event in events_batch:
            event_time =event.TimeGenerated
            if start_date <= event_time <= end_date:
                
                #data is recent enough, so print it out
                computer=str(event.ComputerName)

                cat=str(event.EventCategory)

                src=str(event.SourceName)

                record=str(event.RecordNumber)

                evt_id=str(winerror.HRESULT_CODE(event.EventID))

                evt_type=str(event_dict[event.EventType])

                msg = str(win32evtlogutil.SafeFormatMessage(event, 'system')).replace("\n", "--")

           
                events.append(f"{event_time.strftime('%Y-%m-%d %H:%M:%S')} - {computer} - {evt_type:<15} - {cat} - {record} - {evt_id} - {src} - {msg}")

    win32evtlog.CloseEventLog(handle)
    print("Process completed.")
    result = header + sorted(events, reverse = True)
    return result

####################################################
# USER'S FOLDER TREE
####################################################
def display_directory_tree(option):
    
    # user's home folder
    home = os.path.expanduser("~")
    
    header = ""

    header +="##########################################################\n"
    header +="# USER'S HOME DIRECTORY TREE                                              #\n"
    header +="##########################################################\n"
    
    clean()
    print("Collecting user's home directory tree...(This process may take up to a few minutes, depending on how large the directory tree is)")

    tree = get_fs_tree(home, include_files=option, force_absolute_ids=False)
    
    # Redirect stdout to a StringIO object
    stdout_orig = sys.stdout
    output = StringIO()
    sys.stdout = output

    # Display the tree structure
    tree.show()

    # Retrieve the contents from the StringIO object
    output = output.getvalue()

    # Reset stdout to its original value
    sys.stdout = stdout_orig
    
    print("Process completed.")
    return header+output

####################################################
# Helper function to clean screen at execution time
####################################################
def clean():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')
        