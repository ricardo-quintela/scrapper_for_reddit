"""Extract post id from url
"""
import re
from utils import write_log
from settings import LOG_PATH

# https://www.reddit.com/r/mildlyinfuriating/comments/101x47s/subway_folded_my_fooong_flatbread_along_the_wrong/

def extract_id(url: str) -> str:
    """Extracts the post id from the given url

    Args:
        url (str): the post url

    Returns:
        str: the post id
    """

    url_stripped = re.search(
        r"https://www.reddit.com/r/[a-zA-Z0-9_-]+/comments/[a-zA-Z0-9_-]+",
        url
    ).group()

    if url_stripped is None:
        write_log(f"Couldn't get the id of the post from the given url: {url}", LOG_PATH)
        return

    post_id = re.sub(r"https://www.reddit.com/r/[a-zA-Z0-9_-]+/comments/", "", url_stripped)


    if post_id is None:
        write_log(f"Couldn't get the id of the post from the given url: {url}", LOG_PATH)
        return

    return post_id
