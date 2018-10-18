from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine as sql_create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_engine(conn_str, echo=False):
    """This function creates an sqlalchemy engine (connection to db)
    Args:
        conn_str(str): connection string for creating connection to db
        echo(bool): indicate whether generated sql is logged
    Returns:
        engine
    """
    return sql_create_engine(conn_str, echo=echo)


def create_db_entities(engine_instance):
    """This function create all the tables for the defined models

    Args:
        engine_instance: instance of sqlalchemy engine

    """
    Base.metadata.create_all(engine_instance)


def create_session(engine_instance):
    """This function creates the session object through which all database
    operation are going to be executed

    Args:
        engine_instance: install of sqlalchemy engine to create session with
    """
    Session = sessionmaker(bind=engine_instance)
    return Session()


def create_session_from_conn_str(conn_str: str, echo=False):
    """This function creates the session obj using the connection string that 
    is passed to it

    Args:
        conn_str: valid sqlalchemy connection string
        echo: indicates whether sql statements are printed to the console or not
    """
    return create_session(create_engine(conn_str, echo))


def model_to_dict(model_obj, field_list):
    """This function is responsible for converting an instance of any of the
    modules into a dictionary

    Args:
        model_obj: instance of a module class
        field_list(iterable): list of the fields that are defined on the class
            or the once that desired in the generated dict

    Returns:
        dict
    """
    tmp = {}

    for column in field_list:
        value = getattr(model_obj, column, None)
        if hasattr(value, 'second') and hasattr(value, 'hour') and hasattr(
                value, 'min'):
            value = value.strftime('%Y-%m-%d %H:%M:%S')

        # if value not in (None, ""):
        tmp[column] = value

    return tmp
