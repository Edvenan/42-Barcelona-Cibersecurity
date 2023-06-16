import winreg
import sqlite3
import wmi
import datetime
import os
import win32com.client
import psutil
from loading import ft_progress

def get_registry_changes(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    registry_branch = winreg.HKEY_CURRENT_USER
    registry_key = r"Software"

    key = winreg.OpenKey(registry_branch, registry_key, 0, winreg.KEY_READ)
    changes = []
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

    return sorted(changes, reverse = True)


def get_recent_files(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    files = []
        
    shell = win32com.client.Dispatch("WScript.Shell")
    recent_files_directory = shell.SpecialFolders("Recent")  # Path to the Recent folder

    clean()
    print("Getting recent files...")
    for (dir_path, dir_names, recent_files) in ft_progress(os.walk(recent_files_directory)):
        for file in recent_files:
            full_path = dir_path +"/"+ file
            if file[-3:] == "lnk":
    
                creation_time = os.path.getctime(full_path)
                creation_time = creation_time = datetime.datetime.fromtimestamp(creation_time)
                modified_time = os.path.getmtime(full_path)
                modified_time = modified_time = datetime.datetime.fromtimestamp(modified_time)

                # Check if the file's last modified date falls within the specified time interval
                if start_date <= modified_time <= end_date:
        
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(full_path)
                    file_path = shortcut.Targetpath
                    # Extract the '.lnk' extension
                    filename = file_path.rsplit('\\', 1)[-1]
                    if os.path.isfile(file_path):
                        files.append(modified_time.strftime("%Y-%m-%d %H:%M:%S") + " - " + file_path)

    return sorted(files, reverse=True)


def get_installed_programs(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")

    programs = []

    wmi = win32com.client.GetObject("winmgmts:")
    query = f"SELECT InstallDate, Name FROM Win32_Product WHERE InstallDate >= '{start_date_str}' AND InstallDate <= '{end_date_str}'"

    software_items = wmi.ExecQuery(query)

    clean()
    print("Getting installed programs...")
    for software in ft_progress(software_items):
        install_date = software.InstallDate
        install_date = datetime.datetime.strptime(install_date, "%Y%m%d")
        programs.append(install_date.strftime("%Y-%m-%d")  + " - " + software.Name)

    return sorted(programs, reverse = True)


def get_open_programs(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    programs = []

    clean()
    print("Getting oprn programs...")
    for proc in ft_progress(psutil.process_iter(['name', 'create_time'])):
        proc_name = proc.info['name']
        create_time = datetime.datetime.fromtimestamp(proc.info['create_time'])

        if start_date <= create_time <= end_date:
            programs.append(create_time.strftime("%Y-%m-%d, %H:%M:%S") + " - " + proc_name)

    return sorted(programs, reverse=True)


def get_chrome_browsing_history(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    history_path = os.path.expanduser("~") + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()

    query = "SELECT title FROM urls WHERE last_visit_time >= ? AND last_visit_time <= ?"
    params = (datetime.datetime.timestamp(start_date), datetime.datetime.timestamp(end_date))
    clean()
    print("Getting Chrome browsing history...")
    try:
        cursor.execute(query, params)

    except Exception as err:
        return ["Browser history is locked. Try closing Chrome before trying again."]

    browsing_history = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    print("Completed.")
    return browsing_history


def get_connected_devices(start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    start_date_str = start_date.strftime("%Y%m%d")
    end_date_str = end_date.strftime("%Y%m%d")
    
    devices = []

    wmi_connection = wmi.WMI()
    #query = f"SELECT * FROM Win32_PnPEntity WHERE ConfigManagerErrorCode = 0 AND InstallDate >= {start_date_str} AND InstallDate <= {end_date_str}"
    query = f"SELECT Name, InstallDate, Manufacturer, PNPClass FROM Win32_PnPEntity WHERE ConfigManagerErrorCode = 0 AND Present = True AND Status = 'OK'"
    conn_devices = wmi_connection.query(query)

    clean()
    print("Getting connected devices...")
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
        devices.append(f"{device_installDate} - {device_name} - {device_manufacturer} - {device_type}")

    return sorted(devices, reverse= True)


def convert_to_windows_timestamp(date_string):
    date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    windows_timestamp = (date_obj - datetime.datetime(1601, 1, 1)).total_seconds() * 10000000
    return int(windows_timestamp)


def get_log_events(start_date, end_date):
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date.strftime("%Y%m%d%H%M%S")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date.strftime("%Y%m%d%H%M%S")

    
    events = []

    wmi_connection = wmi.WMI()
    
    #query = f"SELECT TimeGenerated, User, Type, SourceName, Message, EventCode FROM Win32_NTLogEvent WHERE CAST(TimeGenerated AS DECIMAL) >= CAST('{start_date}' AS DECIMAL) AND CAST(TimeGenerated AS DECIMAL) <= CAST('{end_date}' AS DECIMAL)"
    query = f"SELECT * FROM Win32_NTLogEvent"    
    log_events = wmi_connection.ExecQuery(query)
    
    clean()
    print("Accesssing Event Logs...(This step may take a couple of minutes)")
    for event in ft_progress(log_events):
        if int(start_date) <= int(event.TimeGenerated.split('.')[0]) <= int(end_date):
            event_time =datetime.datetime.strptime(event.TimeGenerated[:14], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
            if (event.Message):
                events.append(f"{event_time} - {event.User} - {event.Logfile} - {event.Type} - {event.SourceName} - {(event.Message)}")
            else:
                events.append(f"{event_time} - {event.User} - {event.Logfile} - {event.Type} - {event.SourceName} - No Message")
    return sorted(events, reverse= True)

# Importing Libraries
import win32evtlog

def get_log_events2(start_date, end_date):
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    events = []

    handle = win32evtlog.OpenEventLog(None, 'System')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_records = win32evtlog.GetNumberOfEventLogRecords(handle)

    while True:
        events_batch = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events_batch:
            break

        for event in events_batch:
            event_time =event.TimeGenerated
            if start_date <= event_time <= end_date:
                events.append(f"{event.TimeGenerated} - {event.User} - {event.Type} - {event.SourceName} - {event.Message}")

    win32evtlog.CloseEventLog(handle)
    return events

# Importing Libraries
from directory_tree import display_tree

def display_directory_tree(root_dir):
    clean()
    print("Getting directory tree...")
    output = display_tree(root_dir, string_rep=True)
    return output


def display_directory_tree2(startpath):
    
    output = ""
    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output += ('{}{}/'.format(indent, os.path.basename(root)))+"\n"
        subindent = ' ' * 4 * (level + 1)
        #for f in files:
        #    print('{}{}'.format(subindent, f))
    return output


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
        