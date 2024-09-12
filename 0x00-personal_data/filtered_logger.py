#!/usr/bin/env python3
"""
Filtered logger
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    res = ""

    fil = message.split(separator)
    for mas in fil:
        len = mas.find("=")
        if (len == -1):
            continue
        key = mas[:len]
        val = mas[len + 1:]
        if key in fields:
            val = redaction
        res += key + "=" + val + separator
    return res
