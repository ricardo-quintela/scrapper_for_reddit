"""Made by ricardoquinteladev
    Python reddit scrapper

    03/01/2022
"""
import argparse
from scraper import scrape_post
from video_generator import generate_video_file
from utils import create_log_file
from settings import LOG_PATH



def main():
    """main function of the code where all the others are called
    and the user interation is handeled
    """

    # username
    # url

    arg_parser = argparse.ArgumentParser(description="Create a video easily")
    arg_parser.add_argument(
        "-g", "--genaudio",
        help="save the recognized lines to a file",
        action="store_true",
    )

    # arguments for scrapping
    scrape_group = arg_parser.add_argument_group()
    scrape_group.add_argument(
        "-u", "--user",
        type=str,
        help="the authorized reddit username",
        metavar="",
    )
    scrape_group.add_argument(
        "-p", "--post",
        type=str,
        help="the link of the desired post",
        metavar="",
    )

    # arguments for video editing
    video_editing_group = arg_parser.add_argument_group()
    video_editing_group.add_argument(
        "-c", "--clip",
        type=str,
        help="the path to the background clip file",
        metavar="",
    )
    video_editing_group.add_argument(
        "-a", "--audio",
        type=str,
        help="the path to the audio track file",
        metavar="",
    )
    video_editing_group.add_argument(
        "-t", "--text",
        type=str,
        help="the path to the script file",
        metavar="",
    )
    video_editing_group.add_argument(
        "-n", "--name",
        type=str,
        help="the name of the video file to be generated",
        metavar="",
    )


    # arguments for chosing scrape or generate video
    group = arg_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-s", "--scrape",
        help="scrape a post from reddit and generate a script",
        action="store_true",
    )
    group.add_argument(
        "-v", "--video",
        help="generate a video from a background clip, an audio and a script",
        action="store_true",
    )


    # parse the arguments
    args = arg_parser.parse_args()


    # do scraping
    if args.scrape:
        if not (args.user and args.post):
            arg_parser.print_usage()
            print("You must provide a username and a post url to scrape")
            return

        create_log_file(LOG_PATH)
        scrape_post(args.user, args.post)

    # do editing
    elif args.video:
        if not (args.clip and args.audio and args.text):
            arg_parser.print_usage()
            print("You must provide a video clip path, an audio clip path and a script text path to generate a video")
            return

        create_log_file(LOG_PATH)

        generate_video_file(
            args.clip,
            args.audio,
            args.text,
            args.name if args.name else "video.mp4",
            args.genaudio if args.genaudio else None
        )




if __name__ == "__main__":
    main()
