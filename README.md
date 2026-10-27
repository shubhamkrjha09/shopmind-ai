# 🛒 ShopMind AI: Agentic Shopping & Support Assistant

**Live demo:** https://shopmind-ai-agent.streamlit.app

ShopMind AI is an AI agent that handles the two biggest workloads of an online electronics store, **product discovery** and **after-sales support**, through one chat interface. It searches the catalogue, compares products, places and tracks orders, answers return-policy questions from the store's own documents, and uses computer vision to find similar products or assess damaged deliveries. Every action that changes data needs explicit customer confirmation, and refund decisions always stay with a human.

> Demo store with synthetic data. Orders and return requests reset when the app restarts.

## 💼 The business problem

Support teams in e-commerce spend a large share of their time on repetitive questions: *"Which phone fits my budget?", "Where is my order?", "Can I return this?", "My item arrived damaged."* ShopMind AI automates these conversations end to end while keeping humans in control of anything that involves money.

## ✨ Key capabilities

| Capability | How it works |
|---|---|
| **Smart product search** | Filters the catalogue by category and budget from a SQL database |
| **Side-by-side comparison** | Pulls the specs of two products and summarises the trade-offs |
| **Ordering with confirmation** | Places an order only after the customer explicitly confirms |
| **Order tracking** | Looks up live order status from the database |
| **Policy answers grounded in documents (RAG)** | Searches the store's return policy by meaning, and answers only from what it finds |
| **Visual product search** 📷 | A vision model identifies the product in a photo, then finds similar items in stock |
| **Automated damage triage** 📷 | Detects visible damage in a customer photo, checks the policy, and opens a return request for human review |

## 🏗️ Architecture

```
Customer ── Streamlit web app (chat + photo upload)
                 │
                 ▼
     LangChain agent · Qwen 3.8 (Groq) · ReAct tool-calling loop
     ├── Catalogue & orders tools ────────► SQLite
     ├── Policy search tool (RAG) ────────► ChromaDB vector index ◄─ return_policy.md
     └── Vision tools ─────► multimodal LLM → structured JSON → SQLite / policy search
```

**Stack:** Python · LangChain · Groq (Qwen 3.8, text + vision) · SQLite · ChromaDB · Streamlit · Streamlit Community Cloud

## 🧠 Engineering decisions

- **Tools instead of free-form answers.** The model can only state product facts that come from tool results, which prevents invented products and prices (hallucination control).
- **Fixed, parameterised SQL tools** instead of letting the model write SQL, so database access is predictable and safe from injection.
- **Structured JSON from the vision model** (category, brand, colour, damage), so photo analysis feeds straight into normal code.
- **RAG over the policy document** instead of putting the whole policy in every prompt: lower token cost, and answers stay tied to the source.
- **Self-provisioning deployment.** The database and vector index are built automatically on startup, so the app runs from a clean environment with no manual setup.

## 🔐 Safety & responsible AI

- **Human-in-the-loop:** orders and return requests need explicit confirmation; refunds can never be approved by the agent
- Return requests are created as **"Pending review"** for the support team
- Secrets managed through environment variables and cloud secrets, never committed to Git
- Customer uploads and generated data excluded from version control

## 📊 Evaluation

An automated test suite (`eval.py`) checks the agent's decisions, not just its wording:

| Metric | Result |
|---|---|
| Correct tool selection + guardrail tests | **11 / 11 passed** (small hand-written test set) |
| Guardrails tested | No order without confirmation · no refund approval |
| Average response time | ~11 s per question on the free inference tier |

## 🔧 Challenges I solved

- **Retired model in production code.** The originally planned model returned a 404 after the provider retired it. I queried the provider's live model list and migrated to a newer multimodal model with no loss in functionality.
- **Duplicate context bug.** After adding photo upload, every question reached the agent twice, once without the photo. I traced it to a duplicated state update and removed it.
- **Empty app after deployment.** Generated data isn't stored in Git, so the cloud instance started with no catalogue or index. I made the app build both automatically on first start.

## 🚀 Roadmap

- Streaming responses and a faster model to cut latency
- A larger evaluation set covering edge cases and adversarial prompts
- PostgreSQL for persistent orders, plus user accounts
- Analytics on common customer questions to guide the business

## 💻 Run locally

```bash
git clone https://github.com/shubhamkrjha09/shopmind-ai.git
cd shopmind-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
streamlit run app.py
```