"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
from sys import argv
import getpass

from settings import LOG_PATH, APP_ID, SECRET
from utils import write_log, authenticate



def main(args):
    """main function of the code where all the others are called
    and the user interation is handeled
    """

    # username
    # url

    # not exnough args
    if len(args) == 1:
        print("Did not recieve enough arguments!")
        return

    # too many args
    elif len(args) > 3:
        print("To many arguments!")
        return

    # separate the username and url and get the pasword
    username = args[1]
    password = getpass.getpass(f"Password for username {username}: ")
    url = args[2]


    access_token = authenticate(username, password, APP_ID, SECRET)

    print(access_token)


if __name__ == "__main__":
    main(argv)


# https://www.reddit.com/r/stories/comments/101rveo/bedtime_stories_for_grownupskids/
