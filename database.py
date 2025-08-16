import asyncpg

class DatabaseConfig:
    def __init__(self, user, password, db_name, port=5432, host='localhost'):
        self.user=user
        self.password=password
        self.db_name=db_name
        self.port=port
        self.host=host
        self.pool=None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user = self.user,
                password = self.password,
                database = self.db_name,
                port = self.port,
                host = self.host
            )
        except Exception as e:
            print('Error', e)

    async def close(self):
        await self.pool.close()

    async def create_table(self):
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                author VARCHAR(255),
                genre VARCHAR(50),
                year INT,
                copies INT                       
            );
            CREATE TABLE IF NOT EXISTS readers (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255),
                phone VARCHAR(20),
                email VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS loans (
                id SERIAL PRIMARY KEY,
                book_id INT REFERENCES books(id) ON DELETE CASCADE,
                reader_id INT REFERENCES readers(id) ON DELETE CASCADE,
                issue_date DATE,
                return_date DATE,
                returned BOOLEAN DEFAULT FALSE                
            );
    """)
        except Exception as e:
            print('Error:',e)