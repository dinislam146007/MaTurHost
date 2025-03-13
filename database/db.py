import asyncpg
from config import config

async def connect() -> asyncpg.Connection:
    conn = await asyncpg.connect(
        user=config.db_user,
        password=config.db_password,
        database='matur',
        port="5432",
        host='localhost'
    )
    return conn

async def create_promotions_table():
    conn = await connect()
    try:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS promotions (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    finally:
        await conn.close()


async def create_table():
    conn = await connect()
    try:
        await conn.execute("""
CREATE TABLE hosts (
    user_id BIGINT PRIMARY KEY,
    fio TEXT,
    phone TEXT,
    ver BOOL
);
""")
    finally:
        await conn.close()
    return

async def create_table():
    conn = await connect()
    try:
        await conn.execute("""
ALTER TABLE hosts ADD COLUMN city TEXT;
""")
    finally:
        await conn.close()
    return


async def get_services(user_id: int, offset: int, limit: int):
    conn = await connect()
    return await conn.fetch(
        "SELECT city, description FROM services WHERE user_id = $1 OFFSET $2 LIMIT $3",
        user_id, offset, limit
    )

async def add_promotion(title: str, description: str):
    conn = await connect()
    try:
        await conn.execute(
            "INSERT INTO promotions (title, description) VALUES ($1, $2);",
            title, description
        )
    finally:
        await conn.close()

async def delete_promotion(promotion_id: int):
    conn = await connect()
    try:
        await conn.execute("DELETE FROM promotions WHERE id = $1;", promotion_id)
    finally:
        await conn.close()
async def get_promotions(offset: int, limit: int):
    conn = await connect()
    try:
        return await conn.fetch(
            "SELECT id, title, description FROM promotions ORDER BY created_at DESC OFFSET $1 LIMIT $2;",
            offset, limit
        )
    finally:
        await conn.close()

async def count_promotions():
    conn = await connect()
    try:
        return await conn.fetchval("SELECT COUNT(*) FROM promotions;")
    finally:
        await conn.close()


# Функция для подсчета общего количества услуг
async def count_services(user_id: int):
    conn = await connect()

    result = await conn.fetchval(
        "SELECT COUNT(*) FROM services WHERE user_id = $1",
        user_id
    )
    return result or 0


async def create_services_table():
    conn = await connect()
    try:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS services (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            city TEXT NOT NULL,
            description TEXT NOT NULL
        );
        """)
    finally:
        await conn.close()


async def create_apartament_table():
    conn = await connect()
    try:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS apartament (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            city TEXT,
            address TEXT,
            apartment TEXT,
            wifi_login TEXT,
            wifi_password TEXT
        );
        """)
    finally:
        await conn.close()

# Функция для добавления данных в таблицу
async def add_apartament(user_id, city, address, apartment, wifi_login, wifi_password):
    conn = await connect()
    try:
        await conn.execute(
            """
            INSERT INTO apartament (user_id, city, address, apartment, wifi_login, wifi_password) 
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            user_id, city, address, apartment, wifi_login, wifi_password
        )
    finally:
        await conn.close()



async def set_host(user_id, fio, phone):
    conn = await connect()
    try:
        await conn.execute(
            """
            INSERT INTO hosts (user_id, fio, phone, ver) VALUES
            ($1, $2, $3, $4)
            """,
            user_id, fio, phone, False
        )
    finally:
        await conn.close()

async def verification_host(user_id):
    conn = await connect()
    try:
        await conn.execute(
            """
            UPDATE hosts SET ver = TRUE 
            WHERE user_id = $1
            """,
            user_id
        )
    finally:
        await conn.close()

async def get_host(user_id):
    conn = await connect()
    try:
        rows  = await conn.fetch(
            """
            SELECT * FROM hosts
            WHERE user_id = $1
            """,
            user_id
        )
    except Exception:
        return None
    finally:
        await conn.close()
    return rows[0]

async def get_apartaments(user_id):
    conn = await connect()
    try:
        rows = await conn.fetch(
            """
            SELECT city, address, apartment, wifi_login, wifi_password
            FROM apartament
            WHERE user_id = $1
            """,
            user_id
        )
    finally:
        await conn.close()
    return rows

async def add_service(user_id, city, description):
    conn = await connect()
    try:
        await conn.execute(
            "INSERT INTO services (user_id, city, description) VALUES ($1, $2, $3)",
            user_id, city, description
        )
    finally:
        await conn.close()
