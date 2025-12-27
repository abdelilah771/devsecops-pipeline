
from app.database import engine
from sqlalchemy import inspect
import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

inspector = inspect(engine)
try:
    columns = inspector.get_columns("fix_proposals")
    print("Columns in fix_proposals table:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")
except Exception as e:
    print(f"Error inspecting table: {e}")
