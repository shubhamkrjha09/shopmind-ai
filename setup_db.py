import sqlite3

conn = sqlite3.connect("store.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS products")
cur.execute("DROP TABLE IF EXISTS orders")

cur.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    brand TEXT,
    price INTEGER,
    battery_mah INTEGER,
    rating REAL
)
""")

cur.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    status TEXT
)
""")

products = [
    (1, "Redmi Note 13 5G", "phone", "Xiaomi", 17999, 5000, 4.2),
    (2, "Samsung Galaxy M35 5G", "phone", "Samsung", 19999, 6000, 4.3),
    (3, "Realme 12 5G", "phone", "Realme", 16999, 5000, 4.1),
    (4, "iPhone 15", "phone", "Apple", 69999, 3349, 4.6),
    (5, "boAt Airdopes 141", "earbuds", "boAt", 1299, 0, 4.0),
    (6, "Sony WF-C700N", "earbuds", "Sony", 7990, 0, 4.4),
]
cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", products)

conn.commit()
conn.close()
print("store.db created")