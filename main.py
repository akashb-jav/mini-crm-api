import os
import sqlite3
from contextlib import contextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = os.getenv("DB_PATH", "crm.db")

app = FastAPI(title="Mini CRM")


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


init_db()


class EnquiryCreate(BaseModel):
    name: str
    email: str
    message: str

class StatusUpdate(BaseModel):
    status: str




@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/enquiries", status_code=201)
def create_enquiry(enquiry: EnquiryCreate):
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO enquiries (name, email, message) VALUES (?, ?, ?)",
            (enquiry.name, enquiry.email, enquiry.message),
        )
        row = db.execute(
            "SELECT * FROM enquiries WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return dict(row)


@app.get("/enquiries")
def list_enquiries():
    with get_db() as db:
        rows = db.execute("SELECT * FROM enquiries ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]


@app.get("/enquiries/{enquiry_id}")
def get_enquiry(enquiry_id: int):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM enquiries WHERE id = ?", (enquiry_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Enquiry not found")
    return dict(row)

@app.patch("/enquiries/{enquiry_id}/status")
def update_status(enquiry_id: int, update: StatusUpdate):
    with get_db() as db:
        cur = db.execute(
            "UPDATE enquiries SET status = ? WHERE id = ?",
            (update.status, enquiry_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Enquiry not found")
        row = db.execute(
            "SELECT * FROM enquiries WHERE id = ?", (enquiry_id,)
        ).fetchone()
    return dict(row)