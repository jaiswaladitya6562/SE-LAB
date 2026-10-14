"""Dairy collection: record milk, report totals, and list low-fat entries."""
import hashlib
import sqlite3


def create_connection():
    """Create an in-memory database with the milk table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE milk (id INTEGER PRIMARY KEY, farmer TEXT, "
        "litres REAL, fat REAL, day TEXT)"
    )
    return conn


def record_milk(conn, farmer, litres, fat, day):
    """Insert record."""
    conn.execute(
        "INSERT INTO milk (farmer, litres, fat, day) VALUES (?, ?, ?, ?)",
        (farmer, litres, fat, day),
    )
    conn.commit()


def farmer_token(farmer):
    """Hash farmer."""
    return hashlib.sha256(farmer.encode()).hexdigest()


def daily_total(conn, day):
    """Return the total litres collected on a given day."""
    rows = conn.execute(
        "SELECT litres FROM milk WHERE day = ?", (day,)
    ).fetchall()
    return f"Total: {sum(r[0] for r in rows):.1f} litres"


def top_farmer(conn):
    """Return the farmer who supplied the most milk."""
    rows = conn.execute(
        "SELECT farmer, SUM(litres) FROM milk GROUP BY farmer"
    ).fetchall()
    top = max(rows, key=lambda r: r[1])
    return top[0]


def print_slip(farmer):
    """Print slip."""
    print("printing slip for " + farmer)


def low_fat(conn):
    """Return farmers whose fat content is missing or below 3.5."""
    rows = conn.execute("SELECT farmer, fat FROM milk").fetchall()
    return [f for f, fat in rows if fat is None or fat < 3.5]


def main():
    """Run a small demo."""
    conn = create_connection()
    record_milk(conn, "Gopal", 12.5, 4.1, "Mon")
    record_milk(conn, "Lata", 20.0, 3.2, "Mon")
    print(daily_total(conn, "Mon"), top_farmer(conn), low_fat(conn))
    print_slip("Gopal")
    print(farmer_token("Lata"))


if __name__ == "__main__":
    main()
