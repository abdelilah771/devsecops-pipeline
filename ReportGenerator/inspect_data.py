
from app.database import engine
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM fix_proposals ORDER BY id DESC LIMIT 5"))
    for row in result:
        print(row)
