from asyncpg import create_pool, Pool
from app.core.config import settings

class Database():

    async def create_pool(self):
        pool = await create_pool(dsn=str(settings.ASYNCPG_DATABASE_URI))
        if pool is None:
            raise ValueError
        
        self.pool: Pool = pool
        
db = Database()