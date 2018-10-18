#!/usr/bin/env python
import hashlib


def encrypt(password: str) -> str:
    """
    This function used to entry passwords in the application

    Args:
        password : str -> str string(password) to be encrypted

    Return(s):
        str encrypted string
    """
    return hashlib.sha224(bytes(password, 'utf-8')).hexdigest()
