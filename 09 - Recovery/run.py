import sys
import ctypes

def run_as_admin():
    if sys.platform == 'win32':
        script = sys.argv[0]
        params = ' '.join(sys.argv[1:])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, r"./recovery.py", params, 1)
    else:
        # For non-Windows platforms, you may need to handle running as administrator differently.
        print("Running as administrator is only supported on Windows.")

# Call the function to run the script as administrator
run_as_admin()

