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
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            ssl="require",
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