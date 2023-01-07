"""Extract data from the scrapped post
"""
from textwrap import TextWrapper
from settings import LOG_PATH, WRAP_TEXT
from . import write_log

def extract_bodies(post_data: list) -> tuple:
    """Extracts the title of the post and bodies of the comments

    Args:
        post_data (list): the comments of the post

    Returns:
        tuple: the title and the list of comments
    """

    # list
    #   dict -> t3 -> Extract the title
    #       data
    #   dict -> t1 -> Extract the body
    #       data

    # empty request
    if len(post_data) == 0:
        write_log("Response is empty!", LOG_PATH)
        return

    # not enough content
    if len(post_data) != 2:
        write_log("Response doesn't have enough content!", LOG_PATH)
        return

    # wrong format -> data
    if "data" not in post_data[0]:
        write_log("Response is an invalid format: 1", LOG_PATH)
        return

    # wrong format -> children
    if "children" not in post_data[0]["data"]:
        write_log("Response is an invalid format: 2", LOG_PATH)
        return

    # wrong format -> children es empty
    if len(post_data[0]["data"]["children"]) == 0:
        write_log("Response is an invalid format: 3", LOG_PATH)
        return

    # wrong format -> kind
    if "kind" not in post_data[0]["data"]["children"][0]:
        write_log("Response is an invalid format: 4", LOG_PATH)
        return

    # wrong format -> kind is not t3 (post)
    if post_data[0]["data"]["children"][0]["kind"] != "t3":
        write_log("Response is an invalid format: 5", LOG_PATH)
        return

    # wrong format -> kind is not t3 (post)
    if "data" not in post_data[0]["data"]["children"][0]:
        write_log("Response is an invalid format: 6", LOG_PATH)
        return

    # get the title of the post
    title = post_data[0]["data"]["children"][0]["data"]["title"]

    # no data in comments
    if "data" not in post_data[1]:
        write_log("Response is an invalid format: 7", LOG_PATH)
        return

    # no data in comments
    if "children" not in post_data[1]["data"]:
        write_log("Response is an invalid format: 8", LOG_PATH)
        return

    # wrong format -> children es empty
    if len(post_data[1]["data"]["children"]) == 0:
        write_log("Response is an invalid format: 9", LOG_PATH)
        return

    # pointer to comments
    comments = post_data[1]["data"]["children"]

    # list to store the comments
    bodies = list()

    for i, child in enumerate(comments):

        # wrong format -> kind not found
        if "kind" not in child:
            write_log("Error: type of data is not comment", LOG_PATH)
            continue

        # is not comment -> kind is more (ignore)
        if child["kind"] == "more":
            continue

        # is not comment -> kind is not t1 (comment)
        if child["kind"] != "t1":
            print(i)
            write_log("Error: type of data is not comment (t1 not found)", LOG_PATH)
            continue

        if "data" not in child:
            write_log("Error: comment data is empty", LOG_PATH)
            continue

        if "body" not in child["data"]:
            write_log("Error: comment body does not exist", LOG_PATH)
            continue


        # ignore empty comments
        if child["data"]["body"] == "[removed]":
            continue
        if child["data"]["body"] == "[deleted]":
            continue

        # add the comment to the list
        bodies.append(child["data"]["body"])

    return title, bodies


def wrap_data(line: list) -> list:
    """Wraps each comment so that the lines can fit on the screen

    Args:
        line (list): a line of the script

    Returns:
        list: a list of lines
    """
    # wrap words in the text and build a new list with smaller lines
    wrapper = TextWrapper(width=WRAP_TEXT)

    return wrapper.wrap(line)


def analyze_data(comments: list) -> list:
    """Removes comments that have a size bellow average on the given post

    Args:
        comments (list): the list of comments obtained from the post response
    """

    # allocate memory
    lengths = [0 for i in comments]

    # to save the total number of characters
    total = 0

    # calculate the average characters
    comment_length = 0
    for i, comment in enumerate(comments):
        comment_length = len(comment)

        total += comment_length
        lengths[i] = comment_length

    average_size = total / len(comments)
    min_size = min(lengths)

    # removing comments bellow average
    index = 0
    while index < len(lengths):
        if lengths[index] >= average_size + min_size:
            index += 1
            continue

        lengths.pop(index)
        comments.pop(index)



def save_comments_md(data: tuple, path: str):
    """Saves the comments of the given data of a post
    on a text file on the given path

    Args:
        data (tuple): the comments data from a post (title: str, comments: list)
        path (str): the path to the savefile
    """

    with open(path, "w", encoding="utf-8") as savefile:
        savefile.write(f"# {data[0]}\n")

        for index, comment in enumerate(data[1]):
            savefile.write(f"# Story {index + 1}\n{comment}\n---\n")
