"""
Error Reporting for our Compiler
"""
from setup import GLOBALS


def scanner_error(msg):
    """
    Formats the error message for the scanner
    """
    err_msg = "File: {}\nLine {} Col {}\n{}".format(
        GLOBALS["CUR_FILE"],
        GLOBALS["CUR_LINE"],
        GLOBALS["CUR_COL"],
        msg)
    raise ValueError(err_msg)
