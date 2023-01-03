"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
from sys import argv

from settings import LOG_PATH
from utils import write_log, make_request, save_request_data


def main(args):
    """main function of the code where all the others are called
    and the user interation is handeled
    """
    # not exnough args
    if len(args) == 1:
        write_log("Did not recieve enough arguments!", LOG_PATH)
        return

    # too many args
    elif len(args) > 2:
        write_log("To many arguments!", LOG_PATH)
        return

    # make pointer to url in args
    url = args[1]

    response = make_request(url)
    save_request_data(response)


if __name__ == "__main__":
    main(argv)


# https://www.reddit.com/r/stories/comments/101rveo/bedtime_stories_for_grownupskids/
