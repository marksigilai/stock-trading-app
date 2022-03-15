import network
import config
from pymongo import ReturnDocument

import sys

def find_user_account(user_id):
    #Given a user id, query the accounts database for the account info
    result = config.client.accounts.find_one(
        {'id': user_id},
    )
    return result

def get_user_stocks(user_id, stock=''):
    if stock:
        result = config.client.accounts.find_one(
            {'$and': [{'id': user_id}, {'stock': stock}]},
            projection={'stocks': True, '_id': False}
        )
    else:
        result = config.client.accounts.find_one(
            {'id': user_id},
            projection={'stocks': True, '_id': False}
        )
    return result

def add_funds(user_id, amount):
    result = config.client.accounts.find_one_and_update(
        {'id': user_id}, 
        {'$inc': {'amount': amount}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result

