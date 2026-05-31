import os
import parsers
import llm
import database

def get_collection(model_name="tinyllama:latest"):
    # Returns the standardized ChromaDB collection
    return database.get_collection("tinyllama_policy_scraper")

def ingest_file(file_path, filename, collection, model_name="tinyllama:latest"):
    ext = os.path.splitext(filename)[1].lower()
    
    # 1. Parse using the Parser Layer
    if ext == ".txt":
        chunks = parsers.parse_txt_chunks(file_path, filename)
    elif ext == ".pdf":
        chunks = parsers.parse_pdf_pages(file_path, filename)
    elif ext == ".docx":
        chunks = parsers.parse_docx_paragraphs(file_path, filename)
    else:
        return 0
        
    if not chunks:
        return 0
        
    embeddings = []
    metadatas = []
    ids = []
    
    # Delete any existing chunks for this file to prevent duplicates and enable updates
    try:
        collection.delete(where={"source": filename})
    except Exception:
        pass
        
    for i, chunk in enumerate(chunks):
        chunk_id = f"{filename}_chunk_{i}"
        print(f"  Embedding chunk {i+1}/{len(chunks)} of {filename} using {model_name}...")
        # 2. Embed using the LLM Layer
        embedding = llm.get_embedding(chunk["text"], model_name)
        
        embeddings.append(embedding)
        metadatas.append(chunk["metadata"])
        ids.append(chunk_id)
        
    if ids:
        docs_to_insert = [c["text"] for c in chunks]
        # 3. Add to vector store using the Database Layer
        database.add_documents(collection, docs_to_insert, embeddings, metadatas, ids)
        return len(ids)
        
    return 0

def query_rag(query, collection, model_name="llama-3.1-8b-instant", embedding_model="tinyllama:latest"):
    # 1. Embed user query using the LLM Layer with local embedding model
    query_vector = llm.get_embedding(query, embedding_model)
    
    # 2. Retrieve similarity results using the Database Layer
    results = database.query_similarity(collection, query_vector, n_results=2)
    
    retrieved_docs = results["documents"][0]
    retrieved_metas = results["metadatas"][0]
    
    # 3. Compile context and citations
    context_parts = []
    citations = []
    for doc, meta in zip(retrieved_docs, retrieved_metas):
        context_parts.append(doc)
        citations.append({
            "source": meta["source"],
            "location": meta["location"]
        })
        
    context = "\n\n---\n\n".join(context_parts)
    
    # 4. Construct Prompt
    prompt = (
        f"You are an expert HR assistant. Answer the user question based strictly on the provided company policy contexts. "
        f"Provide a detailed, exhaustive, and comprehensive explanation of all rules, limits, timelines, and conditions relevant to the query. "
        f"Only use context information that is directly relevant to the user question; ignore any irrelevant topics in the context. "
        f"Be precise, professional, and clear. Do not use any markdown formatting such as italics (do not use * or _). Return only plain text. "
        f"If the answer cannot be verified from the context, say: "
        f"'I am sorry, but I cannot verify that from the provided policy documents.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )
    
    # 5. Query LLM Generation using the LLM Layer
    answer = llm.query_llm(prompt, model_name)
    
    return {
        "answer": answer,
        "context": context,
        "citations": citations,
        "prompt": prompt
    }
