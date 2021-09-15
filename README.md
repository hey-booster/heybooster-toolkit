### Heybooster MongoDB Helper


**Installation:**
```shell
pip3 install heybooster_toolkit
```

---

**Example:**
```python
from heybooster.helpers.database.mongodb import MongoDBHelper


NAME = "database_name"
URI = "database_uri"

with MongoDBHelper(uri=URI, database=NAME) as db:
    result = db.find_one('test_collection', query={'email': 'test@email.com'})
    result = db.find('test_collection', query={'email': 'test@email.com'})
    db.insert('test_collection', query={'email': 'test@email.com'})
    db.insert('test_collection', query={'email': 'test@email.com'})
    db.find_and_modify('test_collection', query={'email': 'test@email.com'}, update={"$set": 'test2@gmail.com'})

```

or

```python
from heybooster.helpers.database.mongodb import MongoDBHelper


NAME = "database_name"
URI = "database_uri"

db = MongoDBHelper(uri=URI, database=NAME)
result = db.find_one('test_collection', query={'email': 'test@email.com'})

db.close()
print(result)
```

