"""Utils for the scraper
"""
from datetime import datetime

def write_log(string: str, path: str):
    """Write text to the logfile in the given path

    Args:
        string (str): the text to write in the logfile
        path (str): the path to the logfile
    """

    with open(path, "a", encoding="utf-8") as logfile:
        logfile.write(f"[{str(datetime.now())}]: {string}\n")

    print(f"[{str(datetime.now())}]: {string}")


def create_log_file(path: str):
    """Creates an empty log file
    or cleans it if it already exists

    Args:
        path (str): the path to the logfile
    """

    try:
        with open(path, "w", encoding="utf-8"):
            pass

    except IOError:
        print("ERROR: Log file could not be created.")
        return
