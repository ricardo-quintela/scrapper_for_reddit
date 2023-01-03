"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
from sys import argv
import getpass

from settings import APP_ID, SECRET
from utils import authenticate, make_request, save_request_data, extract_id



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

    # extract the post id from the url
    post_id = extract_id(url)

    access_token = authenticate(username, password, APP_ID, SECRET)

    if access_token is None:
        return

    response = make_request(post_id, access_token)

    if response is None:
        return

    save_request_data(response, f"{post_id}.json")


if __name__ == "__main__":
    main(argv)


# https://www.reddit.com/r/stories/comments/101rveo/bedtime_stories_for_grownupskids/
