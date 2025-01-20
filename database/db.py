import asyncpg
from config import config

async def connect():
    conn = await asyncpg.connect(
        user=config.db_user,
        password=config.db_password,
        database='matur',
        host='127.0.0.1'
    )
    return conn




