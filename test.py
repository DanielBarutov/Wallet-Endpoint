from app.db.db import get_db
from app.db.db import engine
from sqlalchemy import text

conn = next(get_db())
result = conn.execute(text("SELECT 1"))
print(result.fetchone())