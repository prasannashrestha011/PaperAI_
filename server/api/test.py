
import asyncpg
import asyncio

async def check_connection():
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password="jLUCstm7xctPiT1o",
            database='postgres',
            host='db.cwlklruqhmtcgrtsrmkh.supabase.co',
            port=5432
        )
        print("Connected successfully!")
        await conn.close()
    except Exception as e:
        print("Connection failed:", e)

asyncio.run(check_connection())
