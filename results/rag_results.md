
# RAG Implementation Results

Project: Vignesh IT Helpdesk Assistant

## Technologies
- Sentence Transformers
- all-MiniLM-L6-v2
- FAISS
- Groq LLM

## Implementation Results

| Component | Result |
|---|---|
| Document loaded | Successful |
| Chunks generated | 7 |
| Embedding dimensions | 384 |
| FAISS vectors stored | 7 |
| Top 3 retrieval | Successful |
| Answer generation | Successful |

## Test 1

Question: How do I reset my password?

Result: Correct password reset procedure retrieved
and generated from the IT Helpdesk Guide.

## Conclusion

The RAG system successfully retrieves relevant
information from the IT Helpdesk Guide using
Sentence Transformers and FAISS and generates
answers using the Groq LLM.
