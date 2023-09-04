# Toggle between light and dark mode automatically on Windows.

from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time
import datetime

DARK_MODE_HOUR = 17  # 5:00 PM
LIGHT_MODE_HOUR = 6  # 6:00 AM

def run_dark_theme_command():
    ps_command = """
    New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 0 -Type Dword -Force;
    New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 0 -Type Dword -Force
    """
    subprocess.run(["powershell", ps_command])

def run_light_theme_command():
    ps_command = """
    New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name SystemUsesLightTheme -Value 1 -Type Dword -Force;
    New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize -Name AppsUseLightTheme -Value 1 -Type Dword -Force
    """
    subprocess.run(["powershell", ps_command])

def check_current_time_and_set_theme():
    current_time = datetime.datetime.now().time()
    if datetime.time(LIGHT_MODE_HOUR, 0) <= current_time < datetime.time(DARK_MODE_HOUR, 0):
        run_light_theme_command()
    else:
        run_dark_theme_command()

if __name__ == '__main__':
    # Check the current time and set the initial theme accordingly
    check_current_time_and_set_theme()

    scheduler = BackgroundScheduler()

    # Run dark theme command at DARK_MODE_HOUR
    scheduler.add_job(run_dark_theme_command, 'cron', hour=DARK_MODE_HOUR)

    # Run light theme command at LIGHT_MODE_HOUR
    scheduler.add_job(run_light_theme_command, 'cron', hour=LIGHT_MODE_HOUR)

    scheduler.start()

    # Keep the script running
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
