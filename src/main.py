"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
from sys import argv
import getpass

from settings import APP_ID, SECRET, LOG_PATH
from utils import authenticate, make_request, save_request_data, extract_id, save_comments_md, extract_bodies, write_log



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

    # extract the comments form the response
    data = extract_bodies(response)

    if data is None:
        return

    # save the comments to md
    save_comments_md(data, f"{post_id}.md")

    # success
    write_log(f"Data saved as {post_id}.md", LOG_PATH)


if __name__ == "__main__":
    main(argv)
