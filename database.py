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

# ── Weight ─────────────────────────────────────────────
async def log_weight(user_id: int, weight: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO weight_log (user_id, weight_kg, date) VALUES (?,?,?)",
            (user_id, weight, date.today().isoformat())
        )
        await db.commit()

async def get_weight_history(user_id: int, days: int = 30):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT weight_kg, date FROM weight_log WHERE user_id=? AND date >= date('now',?) ORDER BY date ASC",
            (user_id, f"-{days} days")
        ) as cursor:
            return await cursor.fetchall()

# ── Training ─────────────────────────────────────────────
async def log_training(user_id: int, type_: str, duration: int, notes: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO training_log (user_id, type, duration_min, notes, date) VALUES (?,?,?,?,?)",
            (user_id, type_, duration, notes, date.today().isoformat())
        )
        await db.commit()

async def get_training_week(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT type, duration_min, notes, date FROM training_log WHERE user_id=? AND date >= date('now','-7 days') ORDER BY date DESC",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

# ── Sleep ─────────────────────────────────────────────
async def log_sleep(user_id: int, hours: float, quality: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO sleep_log (user_id, hours, quality, date) VALUES (?,?,?,?)",
            (user_id, hours, quality, date.today().isoformat())
        )
        await db.commit()

# ── Mood ─────────────────────────────────────────────
async def log_mood(user_id: int, mood: int, energy: int, time_of_day: str):
    from datetime import date
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO mood_log (user_id, mood, energy, time_of_day, date) VALUES (?,?,?,?,?)",
            (user_id, mood, energy, time_of_day, date.today().isoformat())
        )
        await db.commit()

# ── Photo ─────────────────────────────────────────────
async def log_photo(user_id: int, file_id: str, file_path: str):
    from datetime import date
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO photos (user_id, file_id, date) VALUES (?,?,?)",
            (user_id, file_id, date.today().isoformat())
        )
        await db.commit()