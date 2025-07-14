import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "")

async def test_connection():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Conexão bem-sucedida!")
        await conn.close()
    except Exception as e:
        print("❌ Erro ao conectar:", e)

asyncio.run(test_connection())
