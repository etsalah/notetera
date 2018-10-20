#!/usr/bin/env python3
"""
This module contains functions for generating and decoding jwt tokens. As well
as code for handling the validity period for tokens in use in the application
"""
import os
from dotenv import load_dotenv
from hashlib import md5
from datetime import datetime, timedelta

import jwt
from sqlalchemy.orm.query import orm_exc

import custom_exceptions as exc
from helpers.id_helper import generate_id
# from models.token_use import TokenUse
# from models.account import Account

load_dotenv()

__author__ = "edem.tsalah@gmail.com"

_SECRET = os.getenv('SECRET', 'jwt_token_secret')
_LOGIN_VALID_TIME_SPAN = timedelta(
    minutes=float(os.getenv('TOKEN_DURATION', '60')))
ALGORITHM = os.getenv('ENCRYPT_ALGORITHM', 'HS256')
TOKEN_FIELD = "token"  # the field in the json where jwt token is expected


def get_token_checksum(token):
    return md5(bytes(token, "utf-8")).hexdigest()


def encode_token(data):
    """
    This function is responsible for encode the data that is passed to into a
    jwt token
    :param session_obj: sqlalchemy session object used to interact with the db
    :param data: data to be used to generate jwt token
    :return: string representing the generated jwt token
    """
    data.update({'exp': datetime.utcnow() + _LOGIN_VALID_TIME_SPAN})
    token = str(jwt.encode(data, _SECRET, algorithm=ALGORITHM)).lstrip(
        "b'").rstrip("'")
    del data['exp']
    # save_token(session_obj, token)
    return token


# def save_token(session_obj, token):
#     """
#     This function is responsible for saving into or updating a
#     token in the database

#     Args:
#         session_obj: sqlalchemy session object used to interact with the db
#         token: jwt token to be save or updated in the db
#     Return:
#         None
#     """
#     try:
#         token_use_obj = find_token_use(session_obj, token)
#         extend_token_validity(session_obj, token_use_obj)
#     except orm_exc.NoResultFound:
#         token_use_obj = TokenUse(
#             token=token, token_check_sum=get_token_checksum(token),
#             id=generate_id(), last_updated_at=datetime.now())
#         session_obj.add(token_use_obj)
#         session_obj.commit()


def decode_token(params, token_field=None):
    """
    This function is used to decode the jwt token into the data that was used
    to generate it

    Args:
        session_obj: sqlalchemy obj used to interact with the db
        params: json data received with request
        token_field: name of the field that token can be found in

    Return:
        resulting data from the token decode process
    """
    try:
        if not token_field:
            token = params[TOKEN_FIELD]
        else:
            token = params[token_field]

        # token_use_details = find_token_use(session_obj, token)
        # check_token_validate_period(session_obj, token_use_details)

        account_details = jwt.decode(token, _SECRET, algorithms=ALGORITHM)

        # check_login_access_revoked(
        #     session_obj, account_details, token_use_details
        # )
        # extend_token_validity(session_obj, token_use_details)

        return account_details

    except orm_exc.NoResultFound:
        raise exc.LoggedOutError()


# def check_token_validate_period(session_obj, token_use_details):
#     """
#     This function is responsible for checking that token has not been
#     invalidated because it has been used after it has expired. Using it within
#     the allowed time period extends the it's validity period like a session
#     object. It raises an exc.LoginExpiredError if the token has been been
#     invalidated

#     :param session_obj: sqlalchemy object used to interact with the db
#     :param token_use_details: details contain information about when the token
#         was used last
#     :return: None
#     """
#     interval_between_actions = (
#         datetime.now() - token_use_details.last_updated_at)

#     if interval_between_actions > _LOGIN_VALID_TIME_SPAN:
#         delete_token_use(session_obj, token_use_details)
#         raise exc.LoginExpiredError()


# def check_login_access_revoked(
#         session_obj, account_details, token_use_details):
#     """
#     This function checks if a user with a valid token which within its use
#     window has been marked as deleted. Raise exc.LoginRevokedError if the
#     user has been marked as deleted

#     :param session_obj: sqlalchemy object used to interact with the db
#     :param account_details: details of the user whose access is to be checked
#     :param token_use_details: details of the record indicating the token to
#         match the current user
#     :return: None
#     """
#     account_from_db = session_obj.query(Account).filter(
#         Account.id == account_details['id']).one()

#     if account_from_db.removed:
#         delete_token_use(session_obj, token_use_details)
#         raise exc.LoginRevokedError()


# def extend_token_validity(session_obj, token_use_details):
#     """
#     This function is used to extend the validity period for a token that was
#     just used

#     Args:
#         session_obj: sqlalchemy object that is used to interact with the db
#         token_use_details: object representing the token whose validity
#             period we want to extend
#     Returns:
#         :return: None
#     """
#     token_use_details.last_updated_at = datetime.now()
#     token_use_details.token_check_sum = get_token_checksum(
#         token_use_details.token)
#     session_obj.add(token_use_details)
#     session_obj.commit()


# def find_token_use(session_obj, token):
#     """
#     This function is used to return the record used to manage the validity
#     period of a token from the db

#     :param session_obj: sqlalchemy object used to interact with the db
#     :param token: token whose details we want to returned from the db
#     :return: object represnting token use details from the db
#     """
#     check_summed_token = get_token_checksum(token)
#     return session_obj.query(TokenUse).filter(
#         TokenUse.token_check_sum == check_summed_token).one()


# def delete_token_use(session_obj, token_use_instance):
#     """
#     This function is used to delete the record from the db that represent to
#     validity period of a token. This function is called when a token has
#     expired or if the access of a user to the application has been revoked was
#     they are are logged in to the application

#     :param session_obj: sqlalchemy object used to interact with the db
#     :param token_use_instance: object represent the token use details to be
#         deleted from the db
#     :return: None
#     """
#     session_obj.delete(token_use_instance)
#     session_obj.commit()
