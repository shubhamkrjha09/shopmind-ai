from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm =ChatGroq(model="qwen/qwen3.8-27b", temperature=0)

response = llm.invoke("Suggest 3 phones under 20000 rupees, one line each")
print(response.content)