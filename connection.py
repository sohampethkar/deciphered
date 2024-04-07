from sqlalchemy.ext.declarative import declarative_base
import aiomysql

Base = declarative_base()
# Your MySQL connection details
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '#IITbombay71'
MYSQL_DB = 'mini_project'

async def create_mysql_pool():
    pool = await aiomysql.create_pool(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        autocommit=True
    )
    return pool

async def get_mysql_connection():
    pool = await create_mysql_pool()
    async with pool.acquire() as conn:
        yield conn
