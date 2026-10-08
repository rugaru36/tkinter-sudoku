import logging

def safe_str_to_int(str: str, to_log_error: bool = False):
    try:
        val = int(str)
        return val
    except ValueError:
        if to_log_error:
            logging.exception('')
        return None