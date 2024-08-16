""" Module that monkey-patches the json module when it's imported so
JSONEncoder.default() automatically checks to see if the object being encoded
is an instance of an Enum type and, if so, returns its name.
"""
from enum import Enum
from json import JSONEncoder

from pymongo import MongoClient

from main.config import get_config_by_name
from main.logger.custom_logging import log
import time

_saved_default = JSONEncoder().default  # Save default method.
mongo_client = None


def json_decoder_default(self, obj):
    if isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, list) or isinstance(
            obj, dict):
        return _saved_default  # Default
    elif isinstance(obj, Enum):
        return obj.value  # Could also be obj.value
    else:
        return str(obj)  # Stringify remaining types


JSONEncoder.default = json_decoder_default  # Set new default method.


class BaseModel:

    def __init__(self):

        self.connection_string = get_config_by_name('MONGO_DATABASE_SRV')
        self.mongo_client = MongoClient(self.connection_string)
        
        self.db = self.mongo_client.get_database("sandbox_bpp")
        self.init_database()

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            column_value = getattr(self, column.name)
            d[column.name] = column_value

        return d


    def init_database(self):
        collection_names = ['search', 'select', 'init', 'confirm', 'cancel', 'status', 'support', 'track', 'update',
                            'rating', 'issue', 'issue_status', 'on_search', 'on_select', 'on_init', 'on_confirm',
                            'on_cancel', 'on_status', 'on_support', 'on_track', 'on_update', 'on_rating', 'on_issue',
                            'on_issue_status']

        ttl_in_seconds = get_config_by_name('TTL_IN_SECONDS')

        for col in collection_names:
            collection = self.db[col]
            collection.create_index("created_at", name="created_at_ttl",
                                                        expireAfterSeconds=ttl_in_seconds)
        time.sleep(1)

    def get_mongo_collection(self, collection):
        return self.db[collection]
