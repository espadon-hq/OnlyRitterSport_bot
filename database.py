import os
from datetime import date

import aiosqlite

from config import DB_PATH

os.makedirs("data", exist_ok=True)

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
        CREATE TABLE IF NOT EXISTS supplements_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            taken INTEGER DEFAULT 0,
            time_slot TEXT,
            date TEXT
        );
        CREATE TABLE IF NOT EXISTS weight_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            weight_kg REAL,
            date TEXT
        );
        CREATE TABLE IF NOT EXISTS training_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            duration_min INTEGER,
            notes TEXT,
            date TEXT
        );
        CREATE TABLE IF NOT EXISTS sleep_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            hours REAL,
            quality INTEGER,
            date TEXT
        );
        CREATE TABLE IF NOT EXISTS mood_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood INTEGER,
            energy INTEGER,
            time_of_day TEXT,
            date TEXT
        );
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_id TEXT,
            date TEXT
        );
        """)
        await db.commit()

# ── Supplements ──────────────────────────────────────────
async def log_supplement(user_id: int, name: str, taken: bool, time_slot: str = "manual"):
    async with aiosqlite.connect(DB_PATH) as db:
        existing = await (await db.execute(
            "SELECT id FROM supplements_log WHERE user_id=? AND name=? AND date=? AND time_slot=?",
            (user_id, name, date.today().isoformat(), time_slot)
        )).fetchone()
        if existing:
            await db.execute(
                "UPDATE supplements_log SET taken=? WHERE id=?",
                (int(taken), existing[0])
            )
        else:
            await db.execute(
                "INSERT INTO supplements_log (user_id, name, taken, time_slot, date) VALUES (?,?,?,?,?)",
                (user_id, name, int(taken), time_slot, date.today().isoformat())
            )
        await db.commit()

async def get_supplements_today(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT name, taken FROM supplements_log WHERE user_id=? AND date=?",
            (user_id, date.today().isoformat())
        ) as cursor:
            return await cursor.fetchall()