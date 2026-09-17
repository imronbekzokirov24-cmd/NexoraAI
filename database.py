"""
============================================================
EduMindAI Enterprise
Database System
============================================================
"""

import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self, db_name="edumindai.db"):

        self.db_name = db_name

        self._create_tables()

    # ======================================================
    # CONNECTION
    # ======================================================

    def _connect(self):

        return sqlite3.connect(
            self.db_name,
            check_same_thread=False
        )

    # ======================================================
    # CREATE TABLES
    # ======================================================

    def _create_tables(self):

        conn = self._connect()
        cursor = conn.cursor()

        # ==================================================
        # USERS
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT DEFAULT '',
                plan TEXT DEFAULT 'Free',
                questions INTEGER DEFAULT 0,
                pdfs INTEGER DEFAULT 0,
                images INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)

        # ==================================================
        # CHAT HISTORY
        # ==================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    # ======================================================
    # CREATE USER
    # ======================================================

    def create_user(
        self,
        username,
        password,
        email=""
    ):

        username = str(username).strip()
        password = str(password).strip()
        email = str(email).strip()

        if not username or not password:

            return False

        conn = self._connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password,
                    email,
                    plan,
                    questions,
                    pdfs,
                    images,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    password,
                    email,
                    "Free",
                    0,
                    0,
                    0,
                    datetime.now().isoformat()
                )
            )

            conn.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        finally:

            conn.close()

    # ======================================================
    # AUTHENTICATE USER
    # ======================================================

    def authenticate_user(
        self,
        username,
        password
    ):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (
                str(username).strip(),
                str(password).strip()
            )
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            return dict(user)

        return None

    # ======================================================
    # GET USER
    # ======================================================

    def get_user(self, user_id):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            return dict(user)

        return None

    # ======================================================
    # GET USER BY USERNAME
    # ======================================================

    def get_user_by_username(
        self,
        username
    ):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (str(username).strip(),)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            return dict(user)

        return None

    # ======================================================
    # SAVE CHAT
    # ======================================================

    def save_chat(
        self,
        user_id,
        role,
        content
    ):

        if not content:
            return False

        conn = self._connect()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO chats
                (
                    user_id,
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(user_id),
                    str(role),
                    str(content),
                    datetime.now().isoformat()
                )
            )

            conn.commit()

            return True

        except Exception:

            return False

        finally:

            conn.close()

    # ======================================================
    # LOAD CHAT
    # ======================================================

    def load_chat(
        self,
        user_id
    ):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                role,
                content,
                created_at
            FROM chats
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (str(user_id),)
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            dict(row)
            for row in rows
        ]

    # ======================================================
    # CLEAR CHAT
    # ======================================================

    def clear_chat(
        self,
        user_id
    ):

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM chats
            WHERE user_id = ?
            """,
            (str(user_id),)
        )

        conn.commit()
        conn.close()

        return True

    # ======================================================
    # INCREASE QUESTIONS
    # ======================================================

    def increase_questions(
        self,
        user_id
    ):

        return self._increase_stat(
            user_id,
            "questions"
        )

    # ======================================================
    # INCREASE PDFS
    # ======================================================

    def increase_pdfs(
        self,
        user_id
    ):

        return self._increase_stat(
            user_id,
            "pdfs"
        )

    # ======================================================
    # INCREASE IMAGES
    # ======================================================

    def increase_images(
        self,
        user_id
    ):

        return self._increase_stat(
            user_id,
            "images"
        )

    # ======================================================
    # INTERNAL STATISTICS UPDATE
    # ======================================================

    def _increase_stat(
        self,
        user_id,
        column
    ):

        allowed_columns = [
            "questions",
            "pdfs",
            "images"
        ]

        if column not in allowed_columns:

            return False

        conn = self._connect()
        cursor = conn.cursor()

        try:

            query = f"""
                UPDATE users
                SET {column} = {column} + 1
                WHERE id = ?
            """

            cursor.execute(
                query,
                (user_id,)
            )

            conn.commit()

            return True

        except Exception:

            return False

        finally:

            conn.close()

    # ======================================================
    # USER STATISTICS
    # ======================================================

    def get_statistics(
        self,
        user_id
    ):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                questions,
                pdfs,
                images
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if not row:

            return {
                "questions": 0,
                "pdfs": 0,
                "images": 0
            }

        return {
            "questions": row["questions"],
            "pdfs": row["pdfs"],
            "images": row["images"]
        }

    # ======================================================
    # UPDATE PLAN
    # ======================================================

    def update_plan(
        self,
        user_id,
        plan
    ):

        conn = self._connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET plan = ?
            WHERE id = ?
            """,
            (
                str(plan),
                user_id
            )
        )

        conn.commit()
        conn.close()

        return True

    # ======================================================
    # GET ALL USERS
    # ======================================================

    def get_all_users(self):

        conn = self._connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                plan,
                questions,
                pdfs,
                images,
                created_at
            FROM users
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            dict(row)
            for row in rows
        ]


# ==========================================================
# GLOBAL DATABASE INSTANCE
# ==========================================================

db = Database()
