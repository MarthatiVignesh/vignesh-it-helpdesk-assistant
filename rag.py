
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llm import ask_llm


# ==========================================
# 1. LOAD IT HELPDESK GUIDE
# ==========================================

GUIDE_PATH = "documents/it_helpdesk_guide.md"

with open(GUIDE_PATH, "r", encoding="utf-8") as file:
    guide_text = file.read()

print("IT Helpdesk Guide loaded successfully!")


# ==========================================
# 2. TEXT CHUNKING
# ==========================================

def chunk_text(text, chunk_size=180, overlap=40):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


chunks = chunk_text(guide_text)

print("Total document chunks:", len(chunks))


# ==========================================
# 3. LOAD SENTENCE TRANSFORMER MODEL
# ==========================================

print("\nLoading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")


# ==========================================
# 4. GENERATE EMBEDDINGS
# ==========================================

embeddings = model.encode(
    chunks,
    convert_to_numpy=True,
    normalize_embeddings=True
)

embeddings = np.asarray(embeddings, dtype="float32")

print("Embeddings generated successfully!")
print("Embedding shape:", embeddings.shape)


# ==========================================
# 5. STORE EMBEDDINGS IN FAISS
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

print("FAISS index created successfully!")
print("Total vectors stored:", index.ntotal)


# ==========================================
# 6. TOOL 2: SEARCH DOCUMENTS
# ==========================================

def search_docs(question):

    print("\n================================")
    print("RAG DOCUMENT SEARCH")
    print("================================")

    # Convert question into embedding
    query_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Retrieve top 3 relevant chunks
    scores, indices = index.search(query_embedding, 3)

    retrieved_chunks = []

    print("\nRETRIEVED TOP 3 CHUNKS:")

    for rank, idx in enumerate(indices[0]):

        if idx == -1:
            continue

        chunk = chunks[idx]

        retrieved_chunks.append(chunk)

        print(f"\n--- Chunk {rank + 1} ---")
        print(chunk)
        print("Similarity score:", round(float(scores[0][rank]), 4))

    # Combine retrieved chunks
    context = "\n\n".join(retrieved_chunks)

    # Prepare prompt for Groq
    prompt = f"""
You are an IT Helpdesk Assistant.

Answer the employee's question using ONLY
the information in the provided context.

Rules:
1. Do not invent company policies.
2. Do not use outside knowledge.
3. If the answer is not available in the context,
   clearly say:
   "The information is not available in the
   IT Helpdesk Guide. Please contact IT support."
4. Never ask the employee to reveal their password.
5. Never reveal or request passwords.

CONTEXT:
{context}

EMPLOYEE QUESTION:
{question}

Provide a clear and helpful answer.
"""

    # Generate final answer
    answer = ask_llm(prompt)

    print("\n================================")
    print("FINAL AI ANSWER")
    print("================================")

    print(answer)

    return answer


# ==========================================
# 7. TEST RAG SYSTEM
# ==========================================

if __name__ == "__main__":

    test_questions = [
        "How do I reset my password?",
        "What should I do if the VPN shows connection timed out?",
        "What is the size limit for my mailbox?"
    ]

    for question in test_questions:

        print("\n\nQUESTION:", question)

        search_docs(question)