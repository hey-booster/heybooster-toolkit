from heybooster_toolkit.helpers.database.mongodb import MongoDBHelper

NAME = "database_name"
URI = "database_uri"

"""
Usage 'with'
"""
with MongoDBHelper(uri=URI, database=NAME) as db:
    result = db.find_one('test_collection', query={'email': 'test@email.com'})
    result = db.find('test_collection', query={'email': 'test@email.com'})
    db.insert('test_collection', query={'email': 'test@email.com'})
    db.insert('test_collection', query={'email': 'test@email.com'})
    db.find_and_modify('test_collection', query={'email': 'test@email.com'}, update={"$set": 'test2@gmail.com'})

"""
Usage for connection manual closing 
"""
db = MongoDBHelper(uri=URI, database=NAME)
result = db.find_one('test_collection', query={'email': 'test@email.com'})

db.close()
print(result)
