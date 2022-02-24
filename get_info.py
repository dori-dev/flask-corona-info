"""Get information in DataBase
"""
import pickle


def read_info() -> dict:
    """read info from database
    """
    with open("static/DB/info_db.dat", "rb") as info:
        return {
            "cases": pickle.load(info),
            "deaths": pickle.load(info),
            "recovered": pickle.load(info),
            "table_info": pickle.load(info),
        }


def read_old_info() -> dict:
    """read info from old database
    """
    with open("static/DB/old_info_db.dat", "rb") as info:
        return {
            "cases": pickle.load(info),
            "deaths": pickle.load(info),
            "recovered": pickle.load(info),
            "table_info": pickle.load(info),
        }
