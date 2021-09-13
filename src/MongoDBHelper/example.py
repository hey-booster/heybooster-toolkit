from mongo_db_helper import MongoDBHelper

USER = ""
NAME = "test"
PW = ""
URI = ""

"""
Usage 'with'
"""
with MongoDBHelper(uri=URI, database=NAME) as db:
    result = db.find_one('user', query={'email': 'example@email.com'})
    print(result)

"""
Usage for connection manual closing 
"""
db = MongoDBHelper(uri=URI, database=NAME)
result = db.find_one('user', query={'email': 'user@email.com'})
print(result)
db.close()
