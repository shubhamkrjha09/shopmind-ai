import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("return_policy")


def build_index():
    text = open("return_policy.md", encoding="utf-8").read()
    sections = ["## " + part for part in text.split("\n## ")[1:]]
    collection.upsert(
        ids=[f"section-{i}" for i in range(len(sections))],
        documents=sections,
    )
    print(f"Indexed {len(sections)} sections")


def search_policy(question, k=2):
    result = collection.query(query_texts=[question], n_results=k)
    return "\n\n".join(result["documents"][0])


if __name__ == "__main__":
    build_index()
    print(search_policy("Can I return opened earbuds?"))