from config import get_mysql_connection

def create_category_db(category_name: str):
    """Create a MySQL category DB and setup the pages table."""
    
    # 1️⃣ Connect to MySQL server without specifying a DB
    conn = get_mysql_connection(db_name=None)
    cur = conn.cursor()

    # 2️⃣ Create database if not exists
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{category_name}`")
    conn.commit()
    cur.close()
    conn.close()

    # 3️⃣ Connect to the new category DB and run setup SQL
    conn = get_mysql_connection(db_name=category_name)
    cur = conn.cursor()

    with open("db/mysql_setup.sql") as f:
        sql = f.read()

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
