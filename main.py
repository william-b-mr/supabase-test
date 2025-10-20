from fastapi import FastAPI, HTTPException
import asyncpg
import os
import logging

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/test-db")
async def test_db_connection():
    try:
        pool = await asyncpg.create_pool(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            port=os.getenv("port"),
            database=os.getenv("dbname"),
            ssl="require",  # Ensures SSL
            timeout=30,
            command_timeout=60
        )
        async with pool.acquire() as conn:
            await conn.execute("SELECT 1")
        await pool.close()
        logger.info("Database connection test successful")
        return {"status": "success", "message": "Connected to database successfully"}
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Supabase Connection Test"}