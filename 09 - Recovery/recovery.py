import PySimpleGUI as sg
from utils import *
import sys
import datetime


# Create the GUI layout
layout = [
    [sg.Text("Start Date:"), sg.Input(key="-START-", enable_events=True, visible=False), sg.Input(key="-START-OUTPUT-", size=(10,1), readonly=True),
     sg.CalendarButton("Select Start Date", target="-START-", format='%Y-%m-%d')],
    
    [sg.Text("End Date: "), sg.Input(key="-END-", enable_events=True, visible=False), sg.Input(key="-END-OUTPUT-", size=(10,1), readonly=True),
     sg.CalendarButton("Select End Date", target="-END-", format='%Y-%m-%d')],
    
    [sg.Text("Select a function:")],
    [sg.Combo(['1-Registry changes', '2-Recent files', '3-Installed programs',
               '4-Open programs','5-Browsing history',
               '6-Connected devices', '7-Log events',"8-User's folder tree", 'All'], default_value='All', key="-FUNCTION-", enable_events=True),
        sg.Button("OK")],
    [sg.Multiline(size=(150, 25), key="-OUTPUT-", write_only=True, autoscroll=False,horizontal_scroll=True)],
    [ sg.Button("Quit"), sg.Text("Please check the console for any activity related messages.")],
]

# Create the window
window = sg.Window("Recovery (by Eduard Vendrell 2023)", layout)


# Event loop
while True:
    event, values = window.read()

    # Handle events
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    elif event == "-START-":
        window["-START-OUTPUT-"].update(values["-START-"])
    elif event == "-END-":
        window["-END-OUTPUT-"].update(values["-END-"])
    elif event == "OK":
        start_date = values["-START-"]
        end_date = values["-END-"]
        function_selection = values["-FUNCTION-"]

        output = ""

        if start_date == "" and end_date == "":
            
            from datetime import datetime, timedelta

            start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
            window["-START-OUTPUT-"].update(start_date)
            end_date =  datetime.today().strftime("%Y-%m-%d")
            window["-END-OUTPUT-"].update(end_date)

        elif end_date == "":
            end_date =  datetime.today().strftime("%Y-%m-%d")
            window["-END-OUTPUT-"].update(end_date)

        elif start_date == "":
            start_date =  datetime.today().strftime("%Y-%m-%d")
            window["-END-OUTPUT-"].update(start_date)
            
        if datetime.strptime(start_date, "%Y-%m-%d") > datetime.strptime(end_date, "%Y-%m-%d"):
            output = "Start date must be earlier or same as End date!"

        elif function_selection == "1-Registry changes" or function_selection == "All":

            result = get_registry_changes(start_date, end_date)

            output += "##########################################################\n"
            output += "# REGISTRY CHANGES                                                                #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "2-Recent files" or function_selection == "All":
            result = get_recent_files(start_date, end_date)

            output += "##########################################################\n"
            output += "# RECENT FILES                                                                          #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"


        elif function_selection == "3-Installed programs" or function_selection == "All":
            result = get_installed_programs(start_date, end_date)

            output += "##########################################################\n"
            output += "# INSTALLED PROGRAMS                                                           #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "4-Open programs" or function_selection == "All":
           
            result = get_open_programs(start_date, end_date)

            output += "##########################################################\n"
            output += "# OPEN PROGRAMS                                                                   #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "5-Browsing history" or function_selection == "All":
            
            result = get_chrome_browsing_history(start_date, end_date)

            output += "##########################################################\n"
            output += "# BROWSING HISTORY (Chrome)                                                 #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "6-Connected devices" or function_selection == "All":
            result = get_connected_devices(start_date, end_date)

            output += "##########################################################\n"
            output += "# CONNECTED DEVICES                                                             #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "7-Log events" or function_selection == "All":
            
            result = get_log_events(start_date, end_date)

            output += "##########################################################\n"
            output += "# LOG EVENTS                                                                            #\n"
            output += "##########################################################\n"
            for line in result:
                output += line + "\n"

        elif function_selection == "8-User's folder tree" or function_selection == "All":
            
            output += "##########################################################\n"
            output += "# USER'S FOLDER TREE                                                              #\n"
            output += "##########################################################\n"
            
            #output += display_directory_tree(os.path.expanduser("~"))
            
            from rptree import DirectoryTree
            tree = DirectoryTree(os.path.expanduser("~"), dir_only=True, output_file="dir_tree.txt")
            try:
                output += tree.generate()
            except:
                # obtain/print exception info
                exc_type, exc_value, exc_traceback = sys.exc_info()
                #traceback.print_tb(exc_traceback)
                output += (f"{exc_type.__name__}: {exc_value}\n")
            
        window["-OUTPUT-"].update(output)

window.close()