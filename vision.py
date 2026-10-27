import base64
import json
import os
import sys

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0, max_tokens=600)

PROMPT = (
    "Look at this electronics product photo. Reply with ONLY a JSON object with these keys: "
    "category (phone, earbuds, laptop or other), brand (or null), colour, "
    "is_damaged (true or false), damage_description (short text, or null)."
)


def describe_image(image_path):
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    message = HumanMessage(content=[
        {"type": "text", "text": PROMPT},
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}},
    ])
    reply = llm.invoke([message]).content
    reply = reply.split("</think>")[-1]
    start, end = reply.find("{"), reply.rfind("}")
    return json.loads(reply[start:end + 1])


if __name__ == "__main__":
    print(describe_image(sys.argv[1]))