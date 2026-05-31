import os
import streamlit as st
import rag_processor

# Set page config
st.set_page_config(
    page_title="Corporate Policy Q&A - Groq Cloud RAG",
    layout="wide"
)

# Custom premium styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-title {
    text-align: center;
    margin-bottom: 30px;
}

/* Glassmorphic response block */
.response-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* Citation badges */
.citation-box {
    background: rgba(79, 172, 254, 0.15);
    border-left: 4px solid #00f2fe;
    padding: 10px 16px;
    margin-top: 10px;
    border-radius: 4px;
}

.citation-title {
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    color: #00f2fe;
    letter-spacing: 1px;
}

.citation-source {
    font-size: 14px;
    color: #e0e0e0;
    margin-top: 2px;
}


</style>
""", unsafe_allow_html=True)

# App directory configs
script_dir = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(script_dir, "documents")
os.makedirs(docs_dir, exist_ok=True)

# Initialize ChromaDB backend
collection = rag_processor.get_collection()


# App Header
st.markdown("<div class='main-title'><h1>Corporate Policy Q&A Assistant</h1><p style='color:#a0a0a0;'>Grounded AI using Groq Cloud, TinyLlama & ChromaDB Vector Store</p></div>", unsafe_allow_html=True)

# Sidebar setup for ingestion
with st.sidebar:
    st.markdown("### Ingest Documents")
    uploaded_files = st.file_uploader(
        "Upload Policy Files (PDF, TXT, DOCX)", 
        type=["pdf", "txt", "docx"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process & Embed Documents", type="primary"):
            with st.spinner("Parsing and embedding files..."):
                total_inserted = 0
                for uploaded_file in uploaded_files:
                    temp_path = os.path.join(docs_dir, uploaded_file.name)
                    # Save to disk
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Ingest
                    inserted = rag_processor.ingest_file(temp_path, uploaded_file.name, collection)
                    total_inserted += inserted
                    
                st.success(f"Processing complete! Added {total_inserted} new document chunks.")
                
    st.markdown("---")
    
    # Show active documents in DB
    st.markdown("### Currently Indexed Documents")
    all_docs = collection.get()
    unique_sources = set()
    if all_docs and "metadatas" in all_docs and all_docs["metadatas"]:
        for meta in all_docs["metadatas"]:
            if meta and "source" in meta:
                unique_sources.add(meta["source"])
                
    if unique_sources:
        for idx, source in enumerate(sorted(unique_sources)):
            st.markdown(f"**{idx+1}.** `{source}`")
    else:
        st.info("No documents currently indexed. Please upload files to begin.")
        
    st.markdown("---")
    if st.button("Reset Vector Database", help="Clear all stored documents from ChromaDB"):
        # Reset DB collection
        client = collection._client
        client.delete_collection("tinyllama_policy_scraper")
        # Re-initialize
        collection = client.get_or_create_collection(name="tinyllama_policy_scraper")
        # Clear files in documents dir
        for f in os.listdir(docs_dir):
            os.remove(os.path.join(docs_dir, f))
        st.success("Database cleared successfully!")
        st.rerun()

# Initialize session state for clean UX and state management
import datetime

def log_debug(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    try:
        with open("app_debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_citations" not in st.session_state:
    st.session_state.last_citations = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "query_to_run" not in st.session_state:
    st.session_state.query_to_run = None
if "last_error" not in st.session_state:
    st.session_state.last_error = None

log_debug(f"Script run started. processing={st.session_state.processing}, query_to_run={repr(st.session_state.query_to_run)}")

button_label = "Processing" if st.session_state.processing else "Send"
disabled_state = st.session_state.processing

# Main Panel - Q&A
st.markdown("**Ask a question about company policies:**")
with st.form(key="qa_form", clear_on_submit=False):
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input("Ask a question about company policies:", label_visibility="collapsed", disabled=disabled_state)
    with col2:
        submit_button = st.form_submit_button(
            label=button_label, 
            type="primary", 
            use_container_width=True,
            disabled=disabled_state
        )

# Stage 1: Triggered by user submission
if submit_button and query:
    log_debug(f"Stage 1 matched: submit_button={submit_button}, query={repr(query)}")
    if not unique_sources:
        st.warning("Please upload and process at least one policy document first.")
    else:
        st.session_state.processing = True
        st.session_state.query_to_run = query
        log_debug("Stage 1 calling st.rerun()")
        st.rerun()

# Stage 2: Triggered by the rerun in processing mode
if st.session_state.query_to_run:
    log_debug(f"Stage 2 matched: query_to_run={repr(st.session_state.query_to_run)}")
    with st.spinner("Searching policies and generating response..."):
        try:
            log_debug("Stage 2 calling query_rag")
            rag_response = rag_processor.query_rag(st.session_state.query_to_run, collection)
            st.session_state.last_answer = rag_response["answer"]
            st.session_state.last_citations = rag_response["citations"]
            log_debug(f"Stage 2 query_rag returned successfully: answer_len={len(rag_response['answer']) if rag_response.get('answer') else 0}")
        except Exception as e:
            log_debug(f"Stage 2 exception caught: {e}")
            st.session_state.last_error = f"Error querying RAG system: {e}"
            import traceback
            traceback.print_exc()
            st.session_state.last_answer = None
        finally:
            # Re-enable inputs and clear query queue
            st.session_state.processing = False
            st.session_state.query_to_run = None
            log_debug("Stage 2 finally block: clearing flags and calling st.rerun()")
            st.rerun()

# Display the response if it exists in session state
if st.session_state.last_answer:
    st.markdown("#### Answer:")
    st.write(st.session_state.last_answer)
    
    st.markdown("#### Sources Cited:")
    seen_citations = set()
    for citation in st.session_state.last_citations:
        cit_key = f"{citation['source']} - {citation['location']}"
        if cit_key not in seen_citations:
            seen_citations.add(cit_key)
            st.markdown(f"""
            <div class='citation-box'>
                <div class='citation-title'>SOURCE</div>
                <div class='citation-source'>{citation['source']} ({citation['location']})</div>
            </div>
            """, unsafe_allow_html=True)

# Display the error if it exists
if st.session_state.get("last_error"):
    st.error(st.session_state.last_error)
    st.session_state.last_error = None
