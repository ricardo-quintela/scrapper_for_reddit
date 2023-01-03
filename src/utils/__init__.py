"""Utils for the scrapper
"""
from .log import write_log
from .request_handeler import make_request, save_request_data, authenticate
from .regular_expr import extract_id
from .extract_data import extract_bodies, save_comments_md
