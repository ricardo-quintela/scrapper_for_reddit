"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
from sys import argv
import getpass

from settings import APP_ID, SECRET, LOG_PATH
from utils import authenticate, make_request, save_request_data, extract_id, save_comments_md, extract_bodies, write_log, analyze_data, create_log_file



def main(args):
    """main function of the code where all the others are called
    and the user interation is handeled
    """

    # username
    # url

    # wrong args
    if len(args) != 3:
        print("Usage: scrapper {username} {post_url}")
        return

    # separate the username and url and get the pasword
    username = args[1]
    password = getpass.getpass(f"Password for username {username}: ")
    url = args[2]

    create_log_file(LOG_PATH)

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

    analyze_data(data[1])

    # save the comments to md
    save_comments_md(data, f"{post_id}.md")

    # success
    write_log(f"Data saved as {post_id}.md", LOG_PATH)


if __name__ == "__main__":
    main(argv)
