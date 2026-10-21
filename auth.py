"""Sign-up and login."""
import hashlib

from db import get_conn


def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def sign_up(email, password, name):
    email = email.strip().lower()
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
            (email, _hash(password), name.strip()),
        )
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def login(email, password):
    """Return the user row if the email and password match, else None."""
    conn = get_conn()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email.strip(),)
    ).fetchone()
    conn.close()
    if user is None or user["password_hash"] != _hash(password):
        return None
    return dict(user)
