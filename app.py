import streamlit as st
import os

from agent import agent

st.title("🛒 ShopMind AI")

st.caption("AI shopping & support assistant for an electronics store")
uploaded = st.sidebar.file_uploader("📷 Upload a product photo", type=["jpg", "jpeg", "png"])
image_path = None
if uploaded:
    os.makedirs("uploads", exist_ok=True)
    image_path = os.path.join("uploads", uploaded.name)
    with open(image_path, "wb") as f:
        f.write(uploaded.getbuffer())
    st.sidebar.image(uploaded, caption="Your photo")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask about products, orders or returns...")

if question:
    content = question if image_path is None else f"{question}\n(Photo: {image_path})"
    st.session_state.messages.append({"role": "user", "content": content})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = agent.invoke({"messages": st.session_state.messages})
            answer = result["messages"][-1].content
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})