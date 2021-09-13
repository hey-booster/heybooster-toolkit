### Heybooster MongoDB Helper


**Installation:**
```shell
pip3 install heybooster_toolkit
```

---

**Example:**
```python
from mongo_db_helper import MongoDBHelper


URI = "database_uri"
NAME = "database_name"

with MongoDBHelper(uri=URI, database=NAME) as db:
    result = db.find_one('user', query={'email': 'user@email.com'})
    print(result)
```

or

```python
from mongo_db_helper import MongoDBHelper


URI = "database_uri"
NAME = "database_name"

db = MongoDBHelper(uri=URI, database=NAME)
result = db.find_one('user', query={'email': 'user@email.com'})
print(result)
db.close()
```

