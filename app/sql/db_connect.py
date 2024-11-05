import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

class DBConnect:
    @classmethod
    def get_db(self):
        return pymysql.connect(
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            db=os.getenv("DB_NAME"),
            charset=os.getenv("DB_CHARSET"),
            autocommit=True,
        )