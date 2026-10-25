import sqlite3
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

DB = "store.db"


@tool
def search_products(category: str, max_price: int) -> str:
    """Search the store for products in a category (phone or earbuds) up to a maximum price in rupees."""
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id, name, price, rating, battery_mah FROM products WHERE category = ? AND price <= ?",
        (category, max_price),
    ).fetchall()
    conn.close()
    if not rows:
        return "No products found."
    return "\n".join(f"ID {r[0]}: {r[1]} - Rs {r[2]} - rating {r[3]} - battery {r[4]} mAh" for r in rows)


@tool
def place_order(product_id: int) -> str:
    """Place an order for a product by its ID. Only call this AFTER the user has clearly confirmed they want to buy it."""
    conn = sqlite3.connect(DB)
    product = conn.execute("SELECT name FROM products WHERE id = ?", (product_id,)).fetchone()
    if product is None:
        conn.close()
        return "Product not found."
    cur = conn.execute("INSERT INTO orders (product_id, status) VALUES (?, 'Placed')", (product_id,))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return f"Order #{order_id} placed for {product[0]}."


@tool
def track_order(order_id: int) -> str:
    """Get the current status of an order by its order number."""
    conn = sqlite3.connect(DB)
    row = conn.execute(
        "SELECT o.id, p.name, o.status FROM orders o JOIN products p ON o.product_id = p.id WHERE o.id = ?",
        (order_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return "Order not found."
    return f"Order #{row[0]} ({row[1]}): {row[2]}"


llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)

agent = create_agent(
    model=llm,
    tools=[search_products, place_order, track_order],
    system_prompt="You are ShopMind AI, a shopping assistant for an electronics store. Only recommend products returned by your tools. Never invent products or prices. Before placing an order, always ask the user to confirm.",
)

messages = []
while True:
    user = input("You: ")
    if user.lower() in ["quit", "exit"]:
        break
    messages.append({"role": "user", "content": user})
    result = agent.invoke({"messages": messages})
    messages = result["messages"]
    print("ShopMind:", messages[-1].content)