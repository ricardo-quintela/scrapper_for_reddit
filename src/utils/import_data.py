"""import and clean data from a file
"""
from utils import write_log, wrap_data
from settings import LOG_PATH


def import_data(path: str):
    """Imports data from an .md script

    Args:
        path (str): the path to the script file

    Returns:
        list: a list of lines
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    except FileNotFoundError:
        write_log(f"Script file at {path} could not be found", LOG_PATH)
        return

    except IOError:
        write_log(f"An error has occured while importing the script at {path}", LOG_PATH)
        return


    filtered_lines = list()
    for line in lines:
        if "---" in line or line == "":
            continue

        filtered_lines += wrap_data(line.replace("# ", ""))

    write_log("Script imported successfully", LOG_PATH)
    return filtered_lines
