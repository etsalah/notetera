#!/usr/bin/env python3
"""
This module contains functions for operation related to handling and generating
id in the application
"""

import uuid

__author__ = "edem.tsalah@gmail.com"


def generate_id():
    """
    This function is used to generate ids for the various models in the
    application
    :return: str that is a uuid with the `-' replaced with empty spaces
    """
    return str(uuid.uuid4()).replace('-', '')
